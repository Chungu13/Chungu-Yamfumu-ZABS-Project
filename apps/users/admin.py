from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import CustomUser, UserProfile
from zabs_project.admin_site import admin_site


class CustomUserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'phone_number', 'location', 'date_of_birth', 'gender', 'user_type')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('gender', 'date_of_birth')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'location', 'gender', 'date_of_birth', 'profile_picture')}),
        ('Role', {'fields': ('user_type',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2')
        }),
    )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'company_name', 'contact_person', 'position', 'mobile', 'email')
    search_fields = ('manufacturer__username', 'company_name', 'contact_person', 'email')
    ordering = ('manufacturer__username',)

    fieldsets = (
        (None, {'fields': ('manufacturer',)}),
        ('Company Details', {'fields': ('company_name', 'physical_address',  'postal_address', 'contact_person', 'position', 'mobile', 'email',  'website')}),
        # ('Manufacturing Location', {'fields': ('site_name', 'manufacturing_contact_person', 'manufacturing_physical_address', 'manufacturing_position', 'manufacturing_mobile', 'manufacturing_email', 'manufacturing_postal_address', 'factory_size_m2')}),
        ('How Did You Hear About ZABS', {'fields': ( 'Please_specify_how_you_heard_about_ZABS',)}),
    )


# Registering the models with their admin classes
admin_site.register(CustomUser, CustomUserAdmin)
admin_site.register(UserProfile, UserProfileAdmin)









# Excluded for now 

# class EmployeeInformationAdmin(admin.ModelAdmin):
#    list_display = ('user_profile','total_employees', 'no_of_shifts', 'percentage_non_involved', 'significant_repetitive_tasks')
#    list_filter = ('no_of_shifts', 'significant_repetitive_tasks')
#    search_fields = ('total_employees',)
   
   
   
#    fieldsets = (
#         (None, {'fields': ('user_profile',)}),
#         ('General Information', {'fields': ('total_employees', 'no_of_shifts', 'percentage_non_involved', 'significant_repetitive_tasks', 'task_details')}),
#         ('Finance Department', {'fields': ('finance_shift_1', 'finance_shift_2', 'finance_shift_3','total_employees_finance'),}),
#         ('Administration Department', {'fields': ('admin_shift_1', 'admin_shift_2', 'admin_shift_3', 'total_employees_admin'),}),
#         ('Human Resources Department', {'fields': ('hr_shift_1', 'hr_shift_2', 'hr_shift_3', 'total_employees_hr'),}),
#         ('Marketing/Sales Department', {'fields': ('marketing_sales_shift_1', 'marketing_sales_shift_2', 'marketing_sales_shift_3', 'total_employees_marketing_sales')}),
#         ('Logistics Department', {'fields': ('logistics_shift_1', 'logistics_shift_2', 'logistics_shift_3', 'total_employees_logistics')}),
#         ('Production Department', {'fields': ('production_shift_1', 'production_shift_2', 'production_shift_3', 'total_employees_production')}),
#         ('Engineering/Maintenance Department', {'fields': ('engineering_maintenance_shift_1', 'engineering_maintenance_shift_2', 'engineering_maintenance_shift_3', 'total_employees_engineering_maintenance')}),
    
#         # Add similar sections for other departments...
#         ('Subcontracted Employees', {'fields': ('subcontracted_shift_1', 'subcontracted_shift_2', 'subcontracted_shift_3', 'total_employees_subcontracted'),}),
#         ('Temporal/Unskilled Employees', {'fields': ('temp_unskilled_shift_1', 'temp_unskilled_shift_2', 'temp_unskilled_shift_3', 'total_employees_temp_unskilled'),}),
#         ('Shift Totals', {'fields': ('total_employees_shift_1', 'total_employees_shift_2', 'total_employees_shift_3'),}),
#     )

# admin_site.register(EmployeeInformation, EmployeeInformationAdmin)
    
   

    




