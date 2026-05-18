from django.db import models
from django.contrib.auth.models import User

FOOD_CATEGORIES = [
    ('Veg', 'Veg'),
    ('Non-Veg', 'Non-Veg'),
    ('Packed', 'Packed'),
    ('Raw', 'Raw'),
]

# ---------------- NGO & Donor Models ----------------
class NGOExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    joindate = models.DateField(auto_now_add=True)
    mobile = models.CharField(max_length=40)
    share_contact = models.BooleanField(default=True)

    accepted_category = models.CharField(max_length=20, choices=FOOD_CATEGORIES, default='Veg')
    state = models.CharField(max_length=50, default='Kerala')

    photo = models.ImageField(upload_to='profiles/', default='profiles/default.png')

    @property
    def get_name(self):
        return self.user.first_name

class DonarExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=191)
    address = models.TextField()
    mobile = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    share_contact = models.BooleanField(default=True)

    food_category = models.CharField(max_length=20, choices=FOOD_CATEGORIES, default='Veg')
    state = models.CharField(max_length=50, default='Kerala')

    photo = models.ImageField(upload_to='profiles/', default='profiles/default.png')

    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


# ---------------- Donation Models ----------------
class DonationStatus(models.TextChoices):
    LISTED = 'Listed'
    CLAIMED = 'Claimed'
    PICKED_UP = 'Picked Up'
    DELIVERED = 'Delivered'

class Donation(models.Model):
    donar = models.ForeignKey(DonarExtra, on_delete=models.CASCADE)
    username = models.CharField(max_length=191)
    companyName = models.CharField(max_length=191)
    number = models.CharField(max_length=50)
    address = models.TextField(max_length=500)
    foodName = models.CharField(max_length=191)
    
    foodImage = models.ImageField(upload_to='donations/', null=True, blank=True)
    inputState = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50)
    hours = models.CharField(max_length=50)
    description = models.TextField(max_length=500, null=True)
    status = models.CharField(max_length=20, choices=DonationStatus.choices, default=DonationStatus.LISTED)
    claimed_by = models.ForeignKey('NGOExtra', null=True, blank=True, on_delete=models.SET_NULL)
    pickup_time = models.DateTimeField(null=True, blank=True)
    delivery_time = models.DateTimeField(null=True, blank=True)
    donationdate = models.DateField(auto_now_add=True)
    food_category = models.CharField(max_length=20, choices=FOOD_CATEGORIES, default='Veg')
    state = models.CharField(max_length=50, default='Kerala')
    assigned_volunteer = models.ForeignKey('Volunteer', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.foodName} by {self.username}"


# ---------------- Claim / Payment Models ----------------
class Claim(models.Model):
    ngo = models.ForeignKey(NGOExtra, on_delete=models.CASCADE)
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE)
    ngoname = models.CharField(max_length=191)
    foodName = models.CharField(max_length=191)
    mobile = models.CharField(max_length=40)
    address = models.TextField()

    def __str__(self):
        return f"{self.foodName} claimed by {self.ngoname}"

class Payment(models.Model):
    claim = models.OneToOneField(Claim, on_delete=models.CASCADE)
    donar = models.ForeignKey(DonarExtra, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default="Pending")
    transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return f"Payment {self.transaction_id} for {self.claim.foodName}"


# ---------------- Notice & Complaint Models ----------------
class Notice(models.Model):
    date = models.DateField(auto_now=True)
    by = models.CharField(max_length=20, null=True, default='food')
    message = models.CharField(max_length=500)

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=[('Pending','Pending'), ('Resolved','Resolved')],
        default='Pending'
    )

    reply = models.TextField(blank=True, null=True)  # ⭐ NEW FIELD

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Complaint by {self.user.username} - {self.status}"
    
class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=40)
    address = models.TextField()
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.user.first_name