from django.contrib import admin
from .models import subOtp , cseData, itData,eceData
from django.contrib.auth import get_user_model
User = get_user_model()
admin.site.register(User)
admin.site.register(subOtp)
admin.site.register(cseData)
