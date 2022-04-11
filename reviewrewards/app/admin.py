from django.contrib import admin
from .models import Review,Business,RegUser,EmailAccounts,RateRequest,RealReview
# Register your models here.
admin.site.register(Business)
admin.site.register(Review)
admin.site.register(RegUser)
admin.site.register(EmailAccounts)
admin.site.register(RateRequest)
admin.site.register(RealReview)