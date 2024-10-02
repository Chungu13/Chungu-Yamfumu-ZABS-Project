from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import RegexValidator



class CustomUser(AbstractUser): 
    
    phone_validator = RegexValidator(
        regex=r'^\+260\d{9}$',
        message=("Phone number must be entered in the format: '+260XXXXXXXXX'. Up to 13 digits are allowed, and the country code +260 is required.")
    )

    phone_number = models.CharField(
        max_length=13,
        validators=[phone_validator],
        help_text=("Enter the phone number with the country code +260 (e.g., +260XXXXXXXXX)")
    )
    
    
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    
    USER_TYPES = (
    ('manufacturer', 'Manufacturer'),
    ('consumer', 'Consumer'),
    ('admin', 'Admin'),
    )
    
    
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True
    )

        
    user_type = models.CharField(max_length=50, choices=USER_TYPES, default='')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    def __str__(self):
        return self.username
    

class UserProfile(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile', limit_choices_to={'user_type': 'manufacturer'})
    company_name = models.CharField(max_length=255, default='')
    contact_person = models.CharField(max_length=255, default='')
    physical_address = models.TextField(default='')
    position = models.CharField(max_length=255, default='')
    email = models.EmailField(default='default@example.com')
    postal_address = models.TextField(default='')
    website = models.URLField(blank=True, null=True)
    
    phone_validator = RegexValidator(
        regex=r'^\+260\d{9}$',
        message=("Phone number must be entered in the format: '+260XXXXXXXXX'. Up to 13 digits are allowed, and the country code +260 is required.")
    )

    mobile = models.CharField(
        max_length=13,
        validators=[phone_validator],
        help_text=("Enter the phone number with the country code +260 (e.g., +260XXXXXXXXX)")
    )
    
    Please_specify_how_you_heard_about_ZABS = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return self.company_name 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # Excluded for now 
    
    # # Manufacturing Location if different from the one above 
    # site_name = models.CharField(max_length=255, blank=True, default='')
    # manufacturing_contact_person = models.CharField(max_length=255, blank=True, default='')
    # manufacturing_physical_address = models.TextField(blank=True, default='')
    # manufacturing_position = models.CharField(max_length=255, blank=True, default='')
    # manufacturing_mobile = models.CharField(max_length=20, blank=True, default='')
    # manufacturing_email = models.EmailField(blank=True, default='default@example.com')
    # manufacturing_postal_address = models.TextField(blank=True, default='')
    # factory_size_m2 = models.FloatField(blank=True, null=True, default=0.0)
    
    
# class EmployeeInformation(models.Model):
    
#     # Removed this from the user profile and created a new class for it 
#     # Created a link between the user_profile 
#     # one to one relationship - one user profile can only be linked to one set of employee information
#     # redefined the entire set of fields to fit the required description as per the template
    
#     user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, limit_choices_to={'user_type': 'manufacturer'})
#     total_employees = models.IntegerField(default=0)
#     no_of_shifts = models.IntegerField(default=0)
    
    
#     # Fields for Finance department shifts
#     finance_shift_1 = models.IntegerField(default=0, verbose_name="Finance Shift 1")
#     finance_shift_2 = models.IntegerField(default=0, verbose_name="Finance Shift 2")
#     finance_shift_3 = models.IntegerField(default=0, verbose_name="Finance Shift 3")
#     total_employees_finance = models.IntegerField(default=0)

#     # Fields for Administration department shifts
#     admin_shift_1 = models.IntegerField(default=0, verbose_name="Administration Shift 1")
#     admin_shift_2 = models.IntegerField(default=0, verbose_name="Administration Shift 2")
#     admin_shift_3 = models.IntegerField(default=0, verbose_name="Administration Shift 3")
#     total_employees_admin= models.IntegerField(default=0)

#     # Fields for Human Resources department shifts
#     hr_shift_1 = models.IntegerField(default=0, verbose_name="Human Resources Shift 1")
#     hr_shift_2 = models.IntegerField(default=0, verbose_name="Human Resources Shift 2")
#     hr_shift_3 = models.IntegerField(default=0, verbose_name="Human Resources Shift 3")
#     total_employees_hr = models.IntegerField(default=0)
    
    
#     marketing_sales_shift_1 = models.IntegerField(default=0, verbose_name="Marketing/Sales Shift 1")
#     marketing_sales_shift_2 = models.IntegerField(default=0, verbose_name="Marketing/Sales Shift 2")
#     marketing_sales_shift_3 = models.IntegerField(default=0, verbose_name="Marketing/Sales Shift 3")
#     total_employees_marketing_sales = models.IntegerField(default=0)
    
#     logistics_shift_1 = models.IntegerField(default=0, verbose_name="Logistics Shift 1")
#     logistics_shift_2 = models.IntegerField(default=0, verbose_name="Logistics Shift 2")
#     logistics_shift_3 = models.IntegerField(default=0, verbose_name="Logistics Shift 3")
#     total_employees_logistics = models.IntegerField(default=0)
    
#     production_shift_1 = models.IntegerField(default=0, verbose_name="Production Shift 1")
#     production_shift_2 = models.IntegerField(default=0, verbose_name="Production Shift 2")
#     production_shift_3 = models.IntegerField(default=0, verbose_name="Production Shift 3")
#     total_employees_production= models.IntegerField(default=0)
    
#     engineering_maintenance_shift_1 = models.IntegerField(default=0, verbose_name="Engineering/Maintenance Shift 1")
#     engineering_maintenance_shift_2 = models.IntegerField(default=0, verbose_name="Engineering/Maintenance Shift 2")
#     engineering_maintenance_shift_3 = models.IntegerField(default=0, verbose_name="Engineering/Maintenance Shift 3")
#     total_employees_engineering_maintenance = models.IntegerField(default=0)

#     # Subcontracted and Temporal/Unskilled
#     subcontracted_shift_1 = models.IntegerField(default=0, verbose_name="Subcontracted Shift 1")
#     subcontracted_shift_2 = models.IntegerField(default=0, verbose_name="Subcontracted Shift 2")
#     subcontracted_shift_3 = models.IntegerField(default=0, verbose_name="Subcontracted Shift 3")
#     total_employees_subcontracted = models.IntegerField(default=0)
     

#     temp_unskilled_shift_1 = models.IntegerField(default=0, verbose_name="Temporal/Unskilled Shift 1")
#     temp_unskilled_shift_2 = models.IntegerField(default=0, verbose_name="Temporal/Unskilled Shift 2")
#     temp_unskilled_shift_3 = models.IntegerField(default=0, verbose_name="Temporal/Unskilled Shift 3")
#     total_employees_temp_unskilled= models.IntegerField(default=0)

#     # Total Employees across all shifts
#     total_employees_shift_1 = models.IntegerField(default=0)
#     total_employees_shift_2 = models.IntegerField(default=0)
#     total_employees_shift_3 = models.IntegerField(default=0)

   
#     percentage_non_involved = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Percentage of employees not involved in any way in activities related to the products requiring certification")
#     significant_repetitive_tasks = models.BooleanField(default=False, help_text="Are significant number of your employees involved in the same basic repetitive tasks e.g. machine operators, sales persons, drivers etc.?")
#     task_details = models.TextField(default='', blank=True, help_text ="If yes, please give details of the tasks and the number of employees involved.")

#     def __str__(self):
#         return f"Employee Info - Total Employees: {self.total_employees}"
        

    
        # department_name = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='')
        # shift_type= models.CharField(max_length=50, choices=SHIFT_CHOICES, default='')
        # shift_start_time = models.TimeField(blank=True, null=True, default=now)
        # shift_end_time = models.TimeField(blank=True, null=True, default=now)
        # total_employees = models.IntegerField(default=0)
        # repetitive_tasks_involved = models.BooleanField(default=False, help_text='Are significant number of your employees involved in the same basic repetitive tasks (e.g., machine operators, salespersons, drivers)?')
        # details_of_tasks = models.TextField(blank=True, default='', help_text='If yes, please provide details of the tasks and the number of employees involved.')
      