from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Platform Information",
            {
                "fields" : (
                    "role",
                    "phone_number",
                    )},
            ),

        )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ( 
         "Platform Information",
         {
             "fields" :(
                 "role",
                 "phone_number",)},
         ),
        )

    list_display = (
     "username",
     "email",
     "role",
     "is_staff",
     "is_active",
        )

    list_filter = (
        "role",
        "is_active",
        "is_staff")

    search_fields = (
        "username",
        "email",
        "phone_number",)
