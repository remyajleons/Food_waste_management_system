import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.utils import timezone

from . import models, forms

def is_volunteer(user):
    return user.groups.filter(name='VOLUNTEER').exists()

# ------------------- HOME & CLICK VIEWS -------------------
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'index.html')

def ngoclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'ngoclick.html')

def donarclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'donarclick.html')

# ------------------- SIGNUP VIEWS -------------------
def ngo_signup_view(request):
    form1 = forms.NGOUserForm()
    form2 = forms.NGOExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.NGOUserForm(request.POST)
        form2 = forms.NGOExtraForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            f2.save()
            group = Group.objects.get_or_create(name='NGO')
            group[0].user_set.add(user)
            return HttpResponseRedirect('ngologin')
    return render(request, 'ngosignup.html', context=mydict)

def donar_signup_view(request):
    form1 = forms.DonarUserForm()
    form2 = forms.DonarExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.DonarUserForm(request.POST)
        form2 = forms.DonarExtraForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            f2.save()
            group = Group.objects.get_or_create(name='DONAR')
            group[0].user_set.add(user)
            return HttpResponseRedirect('donarlogin')
    return render(request, 'donarsignup.html', context=mydict)

# ------------------- GROUP CHECKS -------------------
def is_ngo(user):
    return user.groups.filter(name='NGO').exists()

def is_donar(user):
    return user.groups.filter(name='DONAR').exists()

def is_admin(user):
    return user.is_staff

# ------------------- AFTER LOGIN REDIRECT -------------------
def afterlogin_view(request):
    if is_ngo(request.user):
        return redirect('ngo-dashboard')
    elif is_donar(request.user):
        return redirect('donar-dashboard')
    elif is_volunteer(request.user):
        return redirect('volunteer-dashboard')
    else:
        return redirect('/admin/')

# ------------------- NGO VIEWS -------------------

@login_required(login_url='ngologin')
@user_passes_test(is_ngo)
def ngo_claimed_donations_view(request):
    ngo = models.NGOExtra.objects.get(user=request.user)
    claims = models.Claim.objects.filter(ngo=ngo)
    return render(request, 'ngo_claimed_donations.html', {'claims': claims})

@login_required(login_url='ngologin')
@user_passes_test(is_ngo)
def ngo_dashboard_view(request):
    ngodata = models.NGOExtra.objects.get(user=request.user)
    notice = models.Notice.objects.all()
    mydict = {
        'address': ngodata.address,
        'mobile': ngodata.mobile,
        'date': ngodata.joindate,
        'notice': notice
    }
    return render(request, 'ngo_dashboard.html', context=mydict)

@login_required(login_url='ngologin')
@user_passes_test(is_ngo)
def ngo_donation_view(request):
    ngo = models.NGOExtra.objects.get(user=request.user)

    donations = models.Donation.objects.filter(
        status=models.DonationStatus.LISTED,
        state=ngo.state,
        food_category=ngo.accepted_category
    )

    return render(request, 'ngo_donation.html', {'donations': donations})

from .models import Volunteer
import random

@login_required(login_url='ngologin')
@user_passes_test(is_ngo)
def claim_donation_view(request, donation_id):
    donation = get_object_or_404(models.Donation, id=donation_id)
    ngo = models.NGOExtra.objects.get(user=request.user)
    if donation.status != models.DonationStatus.LISTED:
        messages.error(request, "Already Claimed!")
        return redirect('ngo-donation')

    volunteer = Volunteer.objects.filter(state=ngo.state).order_by('?').first()

    claim = models.Claim.objects.create(
        ngo=ngo,
        donation=donation,
        ngoname=request.user.first_name,
        foodName=donation.foodName,
        mobile=ngo.mobile,
        address=ngo.address
    )

    donation.status = models.DonationStatus.CLAIMED
    donation.claimed_by = ngo
    donation.assigned_volunteer = volunteer
    donation.save()

    messages.success(request, "Donation Claimed & Volunteer Assigned!")
    return redirect('ngo-donation')

@login_required(login_url='ngologin')
@user_passes_test(is_ngo)
def ngo_notice_view(request):
    form = forms.NoticeForm()
    if request.method == 'POST':
        form = forms.NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.by = request.user.first_name
            notice.save()
            return redirect('ngo-dashboard')
    return render(request, 'ngo_notice.html', {'form': form})

# ------------------- DONAR VIEWS -------------------
@login_required(login_url='donarlogin')
@user_passes_test(is_donar)
def donar_dashboard_view(request):
    donardata = models.DonarExtra.objects.get(user=request.user)
    notice = models.Notice.objects.all()
    mydict = {
        'address': donardata.address,
        'mobile': donardata.mobile,
        'company_name': donardata.company_name,
        'notice': notice
    }
    return render(request, 'donar_dashboard.html', context=mydict)

@login_required(login_url='donarlogin')
@user_passes_test(is_donar)
def donar_donation_view(request):
    if request.method == "POST":
        don = models.Donation()

        # From donor profile
        don.username = request.user.first_name
        don.companyName = request.user.donarextra.company_name
        don.number = request.user.donarextra.mobile
        don.state = request.user.donarextra.state
        don.inputState = request.user.donarextra.state

        # From form
        don.address = request.POST.get('address')
        don.foodName = request.POST.get('foodName')
        don.quantity = request.POST.get('quantity')
        don.hours = request.POST.get('hours')
        don.description = request.POST.get('description')
        don.food_category = request.POST.get('food_category')

        don.donar = request.user.donarextra

        if 'foodImage' in request.FILES:
            don.foodImage = request.FILES['foodImage']

        don.save()
        messages.success(request, "Donation Listed Successfully!!")

    return render(request, 'donar_donation.html')

@login_required(login_url='donarlogin')
@user_passes_test(is_donar)
def donor_claims_view(request):
    claims = models.Claim.objects.filter(donation__donar=request.user.donarextra)

    for c in claims:
        c.is_paid = hasattr(c, 'payment')   # <-- KEY LINE

    return render(request, 'donor_claims.html', {'claims': claims})

@login_required(login_url='donarlogin')
@user_passes_test(is_donar)
def claimed_donation_view(request):
    claims = models.Claim.objects.filter(
        donation__donar=request.user.donarextra
    )
    return render(request, 'claimed_donation.html', {'claims': claims})

@login_required(login_url='donarlogin')
@user_passes_test(is_donar)
def donar_donation_history_view(request):
    donations = models.Donation.objects.filter(donar=request.user.donarextra)
    return render(request, 'donar_donation_history.html', {'donations': donations})

@login_required(login_url='donarlogin')
@user_passes_test(is_donar)
def make_payment_view(request, claim_id):
    claim = get_object_or_404(models.Claim, id=claim_id)

    if hasattr(claim, 'payment'):
        messages.error(request, "Payment already done!")
        return redirect('donor-claims')

    if request.method == "POST":
        amount = request.POST.get('amount')
        card_number = request.POST.get('card_number')
        expiry = request.POST.get('expiry')
        cvv = request.POST.get('cvv')

        models.Payment.objects.create(
            claim=claim,
            donar=request.user.donarextra,
            amount=amount,
            transaction_id="TXN" + str(random.randint(10000, 99999)),
            status="Success"
        )

        messages.success(request, "Payment Successful!")
        return redirect('donor-claims')

    return render(request, 'payment_form.html', {'claim': claim})

# ------------------- STATIC PAGES -------------------
def aboutus_view(request):
    return render(request, 'aboutus.html')

def contactus_view(request):
    form = forms.ContactusForm()
    if request.method == 'POST':
        form = forms.ContactusForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['Email']
            name = form.cleaned_data['Name']
            message = form.cleaned_data['Message']
            send_mail(
                f"{name} || {email}",
                message,
                settings.EMAIL_HOST_USER,
                settings.EMAIL_RECEIVING_USER,
                fail_silently=False
            )
            return render(request, 'contactussuccess.html')
    return render(request, 'contactus.html', {'form': form})

@login_required
def raise_complaint_view(request):
    if is_ngo(request.user):
        base_template = 'ngobase.html'
    elif is_donar(request.user):
        base_template = 'donarbase.html'
    else:
        base_template = 'volunteerbase.html'

    if request.method == "POST":
        message = request.POST.get('message')
        models.Complaint.objects.create(
            user=request.user,
            message=message
        )
        messages.success(request, "Complaint Submitted Successfully!")
        return redirect('my-complaints')

    return render(request, 'raise_complaint.html', {'base_template': base_template})


@login_required
def my_complaints_view(request):
    complaints = models.Complaint.objects.filter(user=request.user).order_by('-created_at')

    if is_ngo(request.user):
        base_template = 'ngobase.html'
    elif is_donar(request.user):
        base_template = 'donarbase.html'
    else:
        base_template = 'volunteerbase.html'

    return render(request, 'my_complaints.html', {
        'complaints': complaints,
        'base_template': base_template
    })

@login_required
@user_passes_test(is_volunteer)
def volunteer_dashboard(request):
    volunteer = models.Volunteer.objects.get(user=request.user)
    donations = models.Donation.objects.filter(
        assigned_volunteer=volunteer,
        status__in=[
            models.DonationStatus.CLAIMED,
            models.DonationStatus.PICKED_UP
        ]
    )

    return render(request, 'volunteer_dashboard.html', {'donations': donations})


@login_required
@user_passes_test(is_volunteer)
def mark_picked_up(request, donation_id):
    donation = models.Donation.objects.get(id=donation_id)
    donation.status = models.DonationStatus.PICKED_UP
    donation.pickup_time = timezone.now()
    donation.save()
    return redirect('volunteer-dashboard')


@login_required
@user_passes_test(is_volunteer)
def mark_delivered(request, donation_id):
    donation = models.Donation.objects.get(id=donation_id)
    donation.status = models.DonationStatus.DELIVERED
    donation.delivery_time = timezone.now()
    donation.save()
    return redirect('volunteer-dashboard')

from django.contrib.auth.models import Group
from .forms import VolunteerUserForm, VolunteerForm

@login_required
@user_passes_test(is_admin)
def add_volunteer(request):
    form1 = VolunteerUserForm()
    form2 = VolunteerForm()

    if request.method == 'POST':
        form1 = VolunteerUserForm(request.POST)
        form2 = VolunteerForm(request.POST)

        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()

            volunteer = form2.save(commit=False)
            volunteer.user = user
            volunteer.save()

            group = Group.objects.get(name='VOLUNTEER')
            user.groups.add(group)

            return redirect('admin-dashboard')

    return render(request, 'add_volunteer.html', {'form1': form1, 'form2': form2})

from django.contrib.auth import authenticate, login

def volunteer_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.groups.filter(name='VOLUNTEER').exists():
            login(request, user)
            return redirect('volunteer-dashboard')
        else:
            messages.error(request, "Invalid Volunteer Credentials")

    return render(request, 'volunteer_login.html')