"""canteen_order_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from order_management.views import *
from django.conf.urls.static import static
from django.urls import path

from django.views.static import serve
# from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="index"),    
    path('admin_login',admin_login,name="admin_login"),
    path('canteen_login',canteen_login,name="canteen_login"),
    path('student_login',student_login,name="student_login"),
    path('canteen_sign_up',canteen_sign_up,name="canteen_sign_up"),
    path('student_signup',student_signup,name="student_signup"),
    path('canteen_home',canteen_home,name="canteen_home"),
    path('canteen_update',canteen_update,name="canteen_update"),
    path('student_home',student_home,name="student_home"),
    path('student_update',student_update,name="student_update"),
    path('admin_home',admin_home,name="admin_home"),
    path('view_canteen',view_canteen,name="view_canteen"),
    path('view_students',view_students,name="view_students"),
    path('delete_candidate/<int:pid>',delete_candidate,name="delete_candidate"),
    path('pendingrequests',pendingrequests,name="pendingrequests"),
    path('approve/<int:rid>',approve,name="approve"),
    path('reject/<int:rid>',reject,name="reject"),
    path('change_pass_admin',change_pass_admin,name="change_pass_admin"),
    path('change_pass_canteen',change_pass_canteen,name="change_pass_canteen"),
    path('change_pass_student',change_pass_student,name="change_pass_student"),
    path('place_order',place_order,name="place_order"),
    path('ordering',ordering,name="ordering"),
    path('order_list_canteen',order_list_canteen,name="order_list_canteen"),
    path('delete_job/<int:rid>',delete_job,name="delete_job"),
     path('edit_orders/<int:jid>',edit_orders,name="edit_orders"),
    path('order_detail/<int:pid>',order_detail,name="order_detail"),
    path('cancel_order/<int:pid>',cancel_order,name="cancel_order"),
    # path('applied_canteens',applied_canteens,name="applied_canteens"),
    # path('reject_candidate/<int:xid>',reject_candidate,name="reject_candidate"),
    path('Logout',Logout,name="Logout"),
    path('forgot_password_canteen', forgot_password_canteen, name='forgot_password_canteen'),
    path('forgot_password_students', forgot_password_students, name='forgot_password_students'),
    # url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    # url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    
 
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
