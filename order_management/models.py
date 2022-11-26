from distutils.command.upload import upload
from inspect import modulesbyfile
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class userdetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=15,null=True)
    gender=models.CharField(max_length=5,null=True)
    type=models.CharField(max_length=15,null=True)
    
    def _str_(self):
        return self.user.username
# student_details is similar as student_details.
class student_details(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=15,null=True)
    type=models.CharField(max_length=15,null=True)
    company=models.CharField(max_length=50,null=True)   
    status=models.CharField(max_length=20,null=True)
    
    def _str_(self):
        return self.user.username
#orders is orders    
class orders(models.Model):
    recruiter=models.ForeignKey(student_details,on_delete=models.CASCADE)
    
    description=models.CharField(max_length=250)
    
    
    def _str_(self):
        return self.description
    

class applied(models.Model):
    job=models.ForeignKey(orders,on_delete=models.CASCADE)
    candidate=models.ForeignKey(userdetails,on_delete=models.CASCADE)
    resume=models.FileField(null=True)
    applied_date=models.DateField()
    status = models.CharField(max_length=10,null=True)
     
    def _str_(self):
        return self.id