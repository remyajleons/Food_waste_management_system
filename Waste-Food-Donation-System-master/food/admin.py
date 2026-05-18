from django.contrib import admin
from .models import Donation, Claim, NGOExtra, DonarExtra, Notice
from .models import Payment, Complaint
# Register your models here. (by sumit.luv)
class NGOExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(NGOExtra, NGOExtraAdmin)

class DonarExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(DonarExtra, DonarExtraAdmin)

class DonationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Donation, DonationAdmin)

class NoticeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notice, NoticeAdmin)

class ClaimAdmin(admin.ModelAdmin):
    pass
admin.site.register(Claim, ClaimAdmin)

class PaymentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Payment, PaymentAdmin)

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_message', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'message')
    list_editable = ('status',)
    readonly_fields = ('user', 'message', 'created_at')
    fields = ('user', 'message', 'reply', 'status', 'created_at')

    def short_message(self, obj):
        return obj.message[:40]
    short_message.short_description = "Message"

admin.site.register(Complaint, ComplaintAdmin)

from .models import Volunteer

admin.site.register(Volunteer)