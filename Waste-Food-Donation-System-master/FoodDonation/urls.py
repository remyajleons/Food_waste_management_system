"""FoodDonation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from unicodedata import name
from django.contrib import admin
from django.urls import path
from food import views
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Zero Food Admin"
admin.site.site_title = "Zero Food Admin Portal"
admin.site.index_title = "Welcome to Zero Food Researcher Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),

    path('ngoclick', views.ngoclick_view,name='ngoclick'),
    path('donarclick', views.donarclick_view,name='donarclick'),

    path('ngosignup', views.ngo_signup_view,name='ngosignup'),
    path('donarsignup', views.donar_signup_view,name='donarsignup'),
    path('ngologin', LoginView.as_view(template_name='ngologin.html')),
    path('donarlogin', LoginView.as_view(template_name='donarlogin.html')),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='index.html'),name='logout'),

    path('ngo-dashboard', views.ngo_dashboard_view,name='ngo-dashboard'),
    path('ngo-donation', views.ngo_donation_view,name='ngo-donation'),
    path('ngo-notice', views.ngo_notice_view,name='ngo-notice'),
    path('claim-donation/<int:donation_id>/', views.claim_donation_view, name='claim-donation'),
    path('ngo-claimed-donations', views.ngo_claimed_donations_view, name='ngo-claimed-donations'),
    
    path('donar-dashboard', views.donar_dashboard_view,name='donar-dashboard'),
    path('donar-donation', views.donar_donation_view,name='donar-donation'),
    path('claimed-donation', views.claimed_donation_view,name='claimed-donation'),
    path('donar-donation-history', views.donar_donation_history_view,name='donar-donation-history'),

    path('aboutus', views.aboutus_view,name='aboutus'),
    path('contactus', views.contactus_view,name='contactus'),
    
    path('donor-claims/', views.donor_claims_view, name='donor-claims'),
    path('make-payment/<int:claim_id>/', views.make_payment_view, name='make-payment'),
    path('raise-complaint/', views.raise_complaint_view, name='raise-complaint'),
    path('my-complaints/', views.my_complaints_view, name='my-complaints'),
    
    
    path('volunteer-dashboard', views.volunteer_dashboard, name='volunteer-dashboard'),
    path('picked/<int:donation_id>/', views.mark_picked_up, name='mark-picked'),
    path('delivered/<int:donation_id>/', views.mark_delivered, name='mark-delivered'),
    path('add-volunteer/', views.add_volunteer, name='add-volunteer'),
    path('volunteerlogin/', views.volunteer_login_view, name='volunteerlogin'),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
