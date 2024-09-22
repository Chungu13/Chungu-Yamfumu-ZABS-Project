# your_app/admin_site.py
from django.contrib.admin import AdminSite

#This is the default class Django uses to create the admin interface.

class MyAdminSite(AdminSite):  
    
    #  MyAdminSite(AdminSite): Creates a custom admin dashboard by extending Django’s default AdminSite.
    
        
    site_header = 'My Admin'
    
    #Sets the top text of the admin dashboard to "My Admin" instead of "Django Administration".
    
    
    site_title = 'My Admin Portal'
    
    #Changes the browser tab title to "My Admin Portal".
    
    index_title = 'Welcome to My Admin Portal'

admin_site = MyAdminSite(name='myadmin')

#Sets the main page title of the admin interface to "Welcome to My Admin Portal".
