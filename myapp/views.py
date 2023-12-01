from django.shortcuts import render,redirect
from .models import Contact
from .models import Signup
from django.conf import settings
from django.core.mail import send_mail
import random

# Create your views here.
def index(request):
    return render(request,'index.html')

def contact(request):
    if request.method=="POST":
        Contact.objects.create(
        name = request.POST['name'],
        email = request.POST['email'],
        mobile = request.POST['mobile'],
        remarks = request.POST['remarks']
        )
        msg="Contact Saved Successfully"
        return render(request,'contact.html',{'msg':msg})    
    else:
        return render(request,'contact.html')

def signup(request):
    if request.method=="POST":
        try:
            Signup.objects.get(email=request.POST['email'])
            msg="Email Already Registered"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                Signup.objects.create(
                    name=request.POST['name'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    password=request.POST['password'],
                )
                msg="User SIGNUP Successfully"
                return render(request,'signup.html',{'msg':msg})
            else:
                msg="Password & Confirm Password Doesnot Matched"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')

def login(request):
    if request.method=="POST":
        try:
            user=Signup.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                request.session['email']=user.email
                request.session['name']=user.name
                return render(request,'index.html')
            else:
                msg="Incorrect Password"
                return render(request,'login.html',{'msg':msg})
        except:
            msg="Email Not Registered PLEASE SIGNUP"
            return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'login.html')
    
def logout(request):
    try:
        del request.session['email']
        del request.session['name'] 
        return render(request,'login.html')
    except:
        msg="User Logged Out Successfully"
        return render(request,'login.html')

def forgot_password(request):
    if request.method=="POST":
        try:
            user= Signup.objects.get(email=request.POST['email'])
            otp=random.randint(1000,9999)
            subject = 'OTP For Forgot Password'
            message = "Hello "+user.name+",Your OTP For Forogt Password Is "+str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email,]
            send_mail( subject, message, email_from, recipient_list)
            return render(request,'otp.html',{'otp':otp,'email':user.email})
        except Exception as e:
            print(e)
            msg="Email Not Registered"
            return render(request,'forgot-password.html',{'msg':msg})
    else:
        return render(request,'forgot-password.html')
    
def verify_otp(request):
    email=request.POST['email']
    otp=int(request.POST['otp'])
    uotp=int(request.POST['uotp'])

    if otp==uotp:
        return render(request,'new-password.html',{'email':email})
    else:
        msg="Invalid OTP"
        return render(request,'otp.html',{'otp':otp,'email':email,'msg':msg})
    
def new_password(request):
    email=request.POST['email']
    np=request.POST['new_password']
    cnp=request.POST['cnew_password']

    if np==cnp:
        user=Signup.objects.get(email=email)
        user.password=np
        user.save()
        msg="Password Updated Successfully"
        return render(request,'login.html',{'msg':msg})
    else:
        msg="Password & Confirm Password Does Not Matched"
        return render(request,'new-password.html',{'email':email,'msg':msg})
    
def change_password(request):
    if request.method=="POST":
        user=Signup.objects.get(email=request.session['email'])
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                user.password=request.POST['new_password']
                user.save()
                return redirect('logout')
            else:
                msg="New Password & Confirm Password Does Not Matched"
                return render(request,'change-password.html',{'msg':msg})
        else:
            msg="Old Password Does Not Matched"
            return render(request,'change-password.html',{'msg':msg})
    else:
        return render(request,'change-password.html')
