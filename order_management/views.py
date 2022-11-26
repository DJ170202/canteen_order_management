from urllib import response
from django.conf import settings
from django.shortcuts import render,redirect
from django.http import Http404, HttpResponse
from canteen_order_management.settings import BASE_DIR
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
from django.core.mail import send_mail
import string,random

# Create your views here.
def index(request):
    return render(request,'index.html')

def admin_login(request):
    error=""
    if request.method=='POST':
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        user=authenticate(username=uname,password=pwd)
        
        try:
            if user.is_staff:
                login(request,user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    # else:
    #     error = "yes"
    dic = {'error':error}
    return render(request,'admin_login.html',dic)

def canteen_login(request):
    error=""
    if request.method=='POST':
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        user=authenticate(username=uname,password=pwd)
        
        try:
            user1 = userdetails.objects.get(user=user)
            if user1.type == "candidate":
                login(request,user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    #    error = "yes"
    dic = {'error':error}
    return render(request,'canteen_login.html',dic)

def canteen_sign_up(request):
    error=""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        # d = request.POST['dob']
        g = request.POST['gender']
        mob = request.POST['mobile']
        e = request.POST['email']
        p = request.POST['pwd']
        try:
        #    uname=f+str(mob[-2:])
           user= User.objects.create_user(first_name=f,last_name=l,username=e,password=p,email=e)
           userdetails.objects.create(user=user,mobile=mob,gender=g,type="candidate")
           error="no"
        except:
            error="yes"
    dic = {'error': error}
    return render(request,'canteen_sign_up.html',dic)


def student_login(request):
    error=""
    if request.method=='POST':
        uname = request.POST['uname']
        pwd = request.POST['pwd']
        user=authenticate(username=uname,password=pwd)
        
        try:
            user1 = student_details.objects.get(user=user)
            if user1.type == "recruiter" and user1.status!="pending":
                login(request,user)
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    # else:
    #     error = "yes"
    dic = {'error':error}
    return render(request,'student_login.html',dic)


def student_signup(request):
    error=""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        mob = request.POST['mobile']
        e = request.POST['email']
        # c = request.POST['company']
        p = request.POST['pwd']
        try:
        #    uname=f+str(mob[-2:])
           user= User.objects.create_user(first_name=f,last_name=l,username=e,password=p,email=e)
           student_details.objects.create(user=user,mobile=mob,type="recruiter",status="pending")
           error="no"
        except:
            error="yes"
    dic = {'error': error}
    return render(request,'student_signup.html',dic)


def Logout(request):
    logout(request)
    return redirect('index')


def canteen_update(request):
    if not request.user.is_authenticated:
        return redirect('canteen_login')
    
    user1 = request.user
    candidate = userdetails.objects.get(user=user1)
    
    error=""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        mob = request.POST['mobile']
        g = request.POST['gender']

        candidate.user.first_name=f
        candidate.user.last_name=l
        candidate.mobile=mob
        candidate.gender=g
        try:
            candidate.save()
            candidate.user.save()
            error="no"
        except:
            error="yes"
    d = {'candidate':candidate,'error': error}
    return render(request,'canteen_update.html',d)


def canteen_home(request):
    if not request.user.is_authenticated:
        return redirect('canteen_login')
    return render(request,'canteen_home.html')

def student_home(request):
    if not request.user.is_authenticated:
        return redirect('student_login')
    return render(request,'student_home.html')


def student_update(request):
    if not request.user.is_authenticated:
        return redirect('student_login')
    
    user1 = request.user
    recruiter = student_details.objects.get(user=user1)
    
    error=""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        mob = request.POST['mobile']

        recruiter.user.first_name=f
        recruiter.user.last_name=l
        recruiter.mobile=mob
        try:
            recruiter.save()
            recruiter.user.save()
            error="no"
        except:
            error="yes"
    d = {'recruiter':recruiter,'error': error}
    return render(request,'student_update.html',d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    # rcount= student_details.objects.all().count()
    # ccount= userdetails.objects.all().count()
    # d = {'rcount':rcount, 'ccount':ccount}
    return render(request,'admin_home.html')

def view_canteen(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = userdetails.objects.all()
    dic = {'data': data}
    return render(request,'view_canteen.html',dic)


def delete_candidate(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    candidate = User.objects.get(id=pid)
    candidate.delete()
    return redirect('view_canteen')

# def reject_candidate(request,xid):
#     if not request.user.is_authenticated:
#         return redirect('student_login')
#     candidate = applied.objects.get(id=xid)
#     candidate.status='Rejected'
#     candidate.save()
#     return redirect('applied_canteens')

def pendingrequests(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = student_details.objects.filter(status='pending')
    dic = {'data': data}
    return render(request,'pendingrequests.html',dic)

def approve(request,rid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = student_details.objects.get(id=rid)
    data.status = "approved"
    data.save()
    return redirect('pendingrequests')

def reject(request,rid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = User.objects.get(id=rid)
    data.delete()
    return redirect('pendingrequests')

def view_students(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = student_details.objects.all()
    dic = {'data': data}
    return render(request,'view_students.html',dic)


def change_pass_admin(request):
    error=""
    if request.method=='POST':
        c = request.POST['pwd']
        p = request.POST['cnpwd']
        try:
            user= User.objects.get(id=request.user.id)
            if user.check_password(c):
                user.set_password(p)
                user.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    dic = {'error': error}
    return render(request,'change_pass_admin.html',dic)


def change_pass_canteen(request):
    error=""
    if request.method=='POST':
        c = request.POST['pwd']
        p = request.POST['cnpwd']
        try:
            user= User.objects.get(id=request.user.id)
            if user.check_password(c):
                user.set_password(p)
                user.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    dic = {'error': error}
    return render(request,'change_pass_canteen.html',dic)



def change_pass_student(request):
    error=""
    if request.method=='POST':
        c = request.POST['pwd']
        p = request.POST['cnpwd']
        try:
            user= User.objects.get(id=request.user.id)
            if user.check_password(c):
                user.set_password(p)
                user.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    dic = {'error': error}
    return render(request,'change_pass_student.html',dic)



def place_order(request):
    if not request.user.is_authenticated:
        return redirect('student_login')
    error=""
    if request.method=='POST':
        
        des = request.POST['description']
        
        
        user1=request.user
        recruiter1=student_details.objects.get(user=user1)
        try:
           orders.objects.create(recruiter=recruiter1,description=des)
           error="no"
        except:
            error="yes"
    dic = {'error': error}
    return render(request,'place_order.html',dic)



def ordering(request):
    if not request.user.is_authenticated:
        return redirect('student_login')
    user1=request.user
    recruiter1=student_details.objects.get(user=user1)
    data = orders.objects.filter(recruiter=recruiter1)

    dic = {'data':data}
    return render(request,'ordering.html',dic)


def order_list_canteen(request):
    if not request.user.is_authenticated:
        return redirect('canteen_login')
    
    user1=request.user
    candidate1=userdetails.objects.get(user=user1)
    job = orders.objects.all()
    data=applied.objects.filter(candidate=candidate1)
    
    li1 = set()
    li2 = set()
    for i in data:
        if i.status == 'Applied':
            li1.add(i.job.id)
        elif i.status == 'Rejected':
            li2.add(i.job.id)
        
    dic = {'job':job,'li1':li1,'li2':li2}
    return render(request,'order_list_canteen.html',dic)




def delete_job(request,rid):
    if not request.user.is_authenticated:
        return redirect('student_login')
    data = orders.objects.get(id=rid)
    data.delete()
    return redirect('ordering')


def edit_orders(request,jid):
    if not request.user.is_authenticated:
        return redirect('student_login')
    error=""
    job=orders.objects.get(id=jid)
    if request.method=='POST':
        t = request.POST['title']
        loc = request.POST['location']
        s = request.POST['salary']
        e = request.POST['end_date']
        exp = request.POST['experience']
        skill = request.POST['skills']
        des = request.POST['description']
        
        job.title=t
        job.location=loc
        job.salary=s
        job.experience=exp
        job.skills=skill
        job.description=des
        
        try:
            job.save()
            error="no"
        except:
            error="yes"
        
        if e:
            job.end_date=e
            job.save()
        
    dic = {'error': error,'job':job}
    return render(request,'edit_orders.html',dic)

def order_detail(request,pid):
    if not request.user.is_authenticated:
        return redirect('canteen_login')
    data = orders.objects.get(id=pid)
    d = {'job':data}
    return render(request,'order_detail.html',context = d)



def cancel_order(request,pid):
    if not request.user.is_authenticated:
        return redirect('canteen_login')
    
    error="ok"
    user1 = request.user
    candidate = userdetails.objects.get(user=user1)
    job = orders.objects.get(id=pid)
    
    #date1 = date.today()
    # if job.end_date < date1:
    #     error="close"
    # else:
    #     if request.method == 'POST':
    #         r = request.FILES['resume']
    #         applied.objects.create(resume=r,applied_date=date1,candidate=candidate,job=job,status='Applied')
    #         error="ok"
    d = {'error':error,'candidate':candidate}
    return render(request,'cancel_order.html',d)


# def applied_canteens(request):
#     if not request.user.is_authenticated:
#         return redirect('student_login')
    
#     data = applied.objects.filter(status='Applied')
#     dic = {'data':data}
#     return render(request,'applied_canteens.html',dic)


def forgot_password_canteen(request):
    error,p="",""
    if request.method=='POST':
        e = request.POST['email']
        li = set()
        data = User.objects.all()
        for i in data:
            li.add(i.username)
        
        if e in li:
            u = User.objects.get(username=e)
            p= ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) 
            u.set_password(p)
            print(p)
            print(u.username)
            u.save()
            
            subject = 'OTP for login'
            message = f'''Hi {u.username} ,

Your one-time password is  {p}.

Best wishes,
Job-portal team'''
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e]
            print(recipient_list)
            send_mail( subject, message, email_from, recipient_list)
            error="no" 
        else:
            error="yes"
     
    dic = {'error': error}
    return render(request,'forgot_password_canteen.html',dic)


def forgot_password_students(request):
    error,p="",""
    if request.method=='POST':
        e = request.POST['email']
        li = set()
        data = User.objects.all()
        for i in data:
            li.add(i.username)
        
        if e in li:
            u = User.objects.get(username=e)
            p= ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) 
            u.set_password(p)
            print(p)
            print(u.username)
            u.save()
            
            subject = 'OTP for login'
            message = f'''Hi {u.username} ,

Your one-time password is  {p}.

Best wishes,
Job-portal team'''
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e]
            print(recipient_list)
            send_mail( subject, message, email_from, recipient_list)
            error="no" 
        else:
            error="yes"
     
    dic = {'error': error}
    return render(request,'forgot_password_students.html',dic)
    