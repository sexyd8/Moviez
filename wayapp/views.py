import uuid
import requests
import json


from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth import logout, authenticate, login 
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash 
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages 
from django.contrib.auth.decorators import login_required 


from . forms import *
from . models import *

# Create your views here.
def index(request):
    foreign = Product.objects.filter(foreign=True)[:8]
    local = Product.objects.filter(local=True)
    latest = Product.objects.filter(latest=True)
    

    context = { 
        'foreign':foreign,
        'local':local,
        'latest':latest,
    }


    return  render(request, 'index.html', context,)



def categories(request):
    categories=Category.objects.all()

    context = {
        'categories':categories
    }
    return render(request, 'category.html', context)



def diamond(request):
    diamond=Product.objects.filter(diamond=True)
    user= Profile.objects.get(user__username=request.user.username)
    upgrade = Member.objects.exclude(title='Wood')
    downgrade = Member.objects.exclude(title='Diamond')

    context = {
         'diamond':diamond,
        'user':user ,
        'upgrade':upgrade,
        'downgrade':downgrade
    }

    return render(request, 'diamond.html', context)

def gold(request):
    gold=Product.objects.filter(gold=True)
    user= Profile.objects.get(user__username=request.user.username)
    upgrade = Member.objects.exclude(title='Wood')
    downgrade = Member.objects.exclude(title='Diamond')

    context = {
        'gold':gold,
        'user':user ,
        'upgrade':upgrade,
        'downgrade':downgrade
    }

    return render(request, 'gold.html', context)


def wood(request):
    wood=Product.objects.filter(wood=True)
    user= Profile.objects.get(user__username=request.user.username)
    upgrade = Member.objects.exclude(title='Wood')
    downgrade = Member.objects.exclude(title='Diamond')

    context = {
        'wood':wood,
         'user':user ,
        'upgrade':upgrade,
        # 'downgrade':downgrade
    }

    return render(request, 'wood.html', context)



def products(request):
    product=Product.objects.all().order_by('-id')

    context={
        'product':product
    }
    return render(request, 'products.html', context)




def details(request,id):
    details=Product.objects.get(pk=id)

    context={
        'details':details

    }
    return render(request, 'details.html',context)



def signupform(request):
    reg = SignupForm()
    if request.method == 'POST':
        reg = SignupForm(request.POST)
        if reg.is_valid():
            newreg = reg.save() 
            new = Profile(user=newreg)
            new.first_name = newreg.first_name
            new.last_name = newreg.last_name
            new.save()
            login(request,newreg)
            messages.success(request, 'Successfully!')
            return redirect('index')
        else:
            messages.warning(request, reg.errors)
            return redirect('signupform')
            
    context ={
        'reg': reg
    }
    return render(request, 'signup.html', context)




def loginform(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            if Profile.objects.filter(user__username=request.user.username, title='Diamond'):
                messages.success(request, 'You can now watch movies of your choice!')
                return redirect('diamond')
            elif  Profile.objects.filter(user__username=request.user.username, title='Gold'):
                    messages.success(request, 'You can now watch movies of your choice!')
                    return redirect('gold')
            elif  Profile.objects.filter(user__username=request.user.username, title='Wood'):
                    messages.success(request, 'You can now watch movies of your choice!')
                    return redirect('wood')
            else:
                    messages.success(request, 'You do not have an active membership plan, please subscribe.')
                    return redirect('index')

        else:
            messages.info(request, 'Username/password incorrect')
            return redirect('loginform')

    return render(request, 'loginform.html')


@login_required(login_url='loginform')
def dashboard(request):
    user = User.objects.get(username= request.user.username)
    if user:
        login(request, user)
        if Profile.objects.filter(user__username=request.user.username, title='Diamond'):
            return redirect('diamond')
        elif  Profile.objects.filter(user__username=request.user.username, title='Gold'):
            return redirect('gold')
        elif  Profile.objects.filter(user__username=request.user.username, title='Wood'):
            return redirect('wood')
        else:
            messages.info(request, 'Subscribe to watch')
            return redirect('renew')
    else:
        messages.warning(request, 'You have to login to view the Dashboard')
        return redirect('loginform')



def logoutfunc(request): 
    logout(request)
    return redirect('loginform')


@login_required(login_url='loginform')
def  profile(request):
    user= Profile.objects.get(user__username=request.user.username)
    upgrade = Member.objects.exclude(title='Wood')
    downgrade = Member.objects.exclude(title='Diamond')

    context={
        'user':user ,
        'upgrade':upgrade,
        'downgrade':downgrade
    }
    return render(request, 'profile.html', context)

@login_required(login_url='loginform')
def  history(request):
    user= Profile.objects.get(user__username=request.user.username)
    pay= Payment.objects.filter(user__username=request.user.username)
    upgrade = Member.objects.exclude(title='Wood')
    downgrade = Member.objects.exclude(title='Diamond')


    context={
        'user':user,
        'pay':pay,
        'upgrade':upgrade,
        'downgrade':downgrade
    }
    return render(request, 'history.html', context)


@login_required(login_url='loginform')
def profileupdate(request):
    user= Profile.objects.get(user__username=request.user.username)
    form = ProfileForm(instance = request.user.profile)
    if request.method=='POST':
        form = ProfileForm(request.POST,  instance=request.user.profile)
        if form.is_valid:
            form.save()
            messages.success(request, 'Profile update successful')
            return redirect('dashboard')
         
    context = {
        'form': form,
        'user':user 
    }

    return render(request, 'profileupdate.html', context)

@login_required(login_url='loginform')
def password(request):
    update = PasswordChangeForm(request.user)
    if request.method=='POST':
        update=PasswordChangeForm(request.user, request.POST)
        if update.is_valid():
            user=update.save()
            update_session_auth_hash(request,user)
            messages.success(request, 'Password Update Successful')
            return redirect('index')
        else:
            messages.error(request, update.errors)
            return redirect('password')

    context={
        'update':update
    }
    return render(request, 'password.html', context)


@login_required(login_url='loginform')
def membership(request, id):
    newmem = Member.objects.get(pk=id)
    form = MemberForm()
    if request.method == 'POST':
        phone = request.POST['phone']
        email = request.POST['username']
        title = request.POST['title']
        dfee = request.POST['dfee']
        form = MemberForm(request.POST)
        if form.is_valid(): 
            user = form.save(commit=False) 
            user.email = email
            user.save()
            new = Profile(user=user)
            new.first_name = user.first_name
            new.last_name = user.last_name
            new.email = email
            new.phone = phone
            new.title = title
            new.dfee = dfee
            new.save()
            login(request,user)
            messages.success(request, 'You are one step away from completing your membership. confirm Phone number')
            return redirect('confirmation')
        else:
            messages.warning(request, form.errors)
            return redirect('index')
            
    context ={
        'form': form,
        'newmem':newmem,
    }
    return render(request, 'member.html', context)


@login_required(login_url='loginform')
def confirmation(request):
    user=User.objects.get(username=request.user.username)
    

    context={
        'user':user ,
    }
    return render(request, 'confirmation.html', context)



@login_required(login_url='loginform')
def memberfee(request):
    if request.method=='POST':
        api_key='sk_test_0e8a6068679eadbbbd2a7ff3a68f60bcf767faba'
        curl= 'https://api.paystack.co/transaction/initialize'
        # cburl='http://54.172.142.223/dashboard/'
        cburl='http://localhost:8000/dashboard/'
        user= User.objects.get(username=request.user.username)
        total= float(user.profile.dfee) *100
        pay_code= str(uuid.uuid4())
                     

       #collect data that you will send to paystack
        headers={'Authorization': f'Bearer {api_key}'}
        data={'reference':pay_code,'email':user.email,'amount':int(total),'callback_url':cburl,'order_number':user.id}

        #make a call to paystack
        try:
            r=requests.post(curl, headers=headers, json=data)
        except Exception:
            messages.error(request, 'Network busy, try again')
        else:
            transback= json.loads(r.text)
            print('RESULT', transback)
            rd_url= transback['data']['authorization_url']

            pay = Payment()
            pay.user= user
            pay.first_name = user.first_name
            pay.last_name = user.last_name
            pay.pay_code = pay_code  
            pay.phone = user.profile.phone
            pay.title = user.profile.title
            pay.amount = total/100
            pay.paid = True
            pay.save()

            paid = Membership()
            paid.user=user.username
            paid.memeber_no=user.id
            paid.first_name=user.first_name
            paid.last_name=user.last_name
            paid.fee=total /100
            paid.pay_code=pay_code 
            paid.membership=user.profile.title
            paid.phone=user.profile.phone 
            paid.save()

            return redirect(rd_url)
    return redirect('confirmation')


@login_required(login_url='loginform')
def upgrade(request, id):
    single = Member.objects.get(pk=id)
    user=User.objects.get(username=request.user.username)
    user= Profile.objects.get(user__username=request.user.username)
    upgradeform = ProfileForm(instance = request.user.profile)
    if request.method=='POST':
        upgradeform = ProfileForm(request.POST,  instance=request.user.profile)
        if upgradeform.is_valid:
            upgradeform.save() 
            return redirect('confirmupgrade')
            # login(request, user)
           
    context={
        'user':user,
        'single':single,
        'upgradeform':upgradeform
    }
    return render(request, 'upgrade.html', context)



@login_required(login_url='loginform')
def packageupgrade(request):
    user= Profile.objects.get(user__username=request.user.username)
    upgradeform = ProfileForm(instance = request.user.profile)
    if request.method=='POST':
        title = request.POST['title']
        dfee = request.POST['dfee']
        upgradeform = ProfileForm(request.POST,  instance=request.user.profile)
        if upgradeform.is_valid:
            upgradeform.save()
            messages.success(request, 'Package upgrade successful')
            return redirect('confirmupgrade')
         
    context = {
        'upgradeform': upgradeform,
        'user':user,
        'title':title, 
        'dfee':dfee
    }

    return render(request, 'upgrade.html', context)

@login_required(login_url='loginform')
def confirmupgrade(request):
    user=User.objects.get(username=request.user.username)
    

    context={
        'user':user ,
    }
    return render(request, 'confirmupgrade.html', context)


@login_required(login_url='loginform')
def memberupgrade(request):
    if request.method=='POST':
        api_key='sk_test_0e8a6068679eadbbbd2a7ff3a68f60bcf767faba'
        curl= 'https://api.paystack.co/transaction/initialize'
        cburl='http://localhost:8000/dashboard/'
        # cburl='http://54.172.142.223/dashboard/'
        user= User.objects.get(username=request.user.username)
        total= float(user.profile.dfee) *100
        pay_code= str(uuid.uuid4())
             

       #collect data that you will send to paystack
        headers={'Authorization': f'Bearer {api_key}'}
        data={'reference':pay_code,'email':user.email,'amount':int(total),'callback_url':cburl,'order_number':user.id}

        #make a call to paystack
        try:
            r=requests.post(curl, headers=headers, json=data)
        except Exception:
            messages.error(request, 'Network busy, try again')
        else:
            transback= json.loads(r.text)
            rd_url= transback['data']['authorization_url']

            pay = Payment()
            pay.user= user
            pay.first_name = user.first_name
            pay.last_name = user.last_name
            pay.pay_code = pay_code  
            pay.phone = user.profile.phone
            pay.title = user.profile.title
            pay.amount = total/100
            pay.paid = True
            pay.save()

            paid = Membership()
            paid.user=user.username
            paid.memeber_no=user.id
            paid.first_name=user.first_name
            paid.last_name=user.last_name
            paid.fee=total /100
            paid.pay_code=pay_code 
            paid.membership=user.profile.title
            paid.phone=user.profile.phone 
            paid.save()

            messages.success(request, 'Your membership has been upgraded ')
        return redirect(rd_url)
    return redirect('profile')



@login_required(login_url='loginform')
def downgrade(request, id):
    single = Member.objects.get(pk=id)
    user=User.objects.get(username=request.user.username)
    user= Profile.objects.get(user__username=request.user.username)
    downgradeform = ProfileForm(instance = request.user.profile)
    if request.method=='POST':
        downgradeform = ProfileForm(request.POST,  instance=request.user.profile)
        if downgradeform.is_valid:
            downgradeform.save() 
            return redirect('confirmdowngrade')
            
           
    context={
        'user':user,
        'single':single,
        'downgradeform':downgradeform
    }
    return render(request, 'downgrade.html', context)


@login_required(login_url='loginform')
def packagedowngrade(request):
    user= Profile.objects.get(user__username=request.user.username)
    downgradeform = ProfileForm(instance = request.user.profile)
    if request.method=='POST':
        downgradeform = ProfileForm(request.POST,  instance=request.user.profile)
        if downgradeform.is_valid:
            downgradeform.save()
            messages.success(request, 'Package upgrade successful')
            return redirect('confirmdowngrade')
         
    context = {
        'downgradeform': downgradeform,
        'user':user,
    }

    return render(request, 'downgrade.html', context)

@login_required(login_url='loginform')
def confirmdowngrade(request):
    user=User.objects.get(username=request.user.username)
    

    context={
        'user':user ,
    }
    return render(request, 'confirmdowngrade.html', context)


@login_required(login_url='loginform')
def memberdowngrade(request):
    if request.method=='POST':
        api_key='sk_test_0e8a6068679eadbbbd2a7ff3a68f60bcf767faba'
        curl= 'https://api.paystack.co/transaction/initialize'
        cburl='http://localhost:8000/dashboard/'
        # cburl='http://54.172.142.223/dashboard/'
        user= User.objects.get(username=request.user.username)
        total= float(user.profile.dfee)*100
        pay_code= str(uuid.uuid4())
             

       #collect data that you will send to paystack
        headers={'Authorization': f'Bearer {api_key}'}
        data={'reference':pay_code,'email':user.email,'amount':int(total),'callback_url':cburl,'order_number':user.id}

        #make a call to paystack
        try:
            r=requests.post(curl, headers=headers, json=data)
        except Exception:
            messages.error(request, 'Network busy, try again')
        else:
            transback= json.loads(r.text)
            rd_url= transback['data']['authorization_url']

            pay = Payment()
            pay.user= user
            pay.first_name = user.first_name
            pay.last_name = user.last_name
            pay.pay_code = pay_code  
            pay.phone = user.profile.phone
            pay.title = user.profile.title
            pay.amount = total/100
            pay.paid = True
            pay.save()

            paid = Membership()
            paid.user=user.username
            paid.memeber_no=user.id
            paid.first_name=user.first_name
            paid.last_name=user.last_name
            paid.fee=total /100
            paid.pay_code=pay_code 
            paid.membership=user.profile.title
            paid.phone=user.profile.phone 
            paid.save()
            
            messages.success(request, 'Your membership has been upgraded ')
        return redirect(rd_url)
    return redirect('profile')


@login_required(login_url='loginform')
def deletemember(request):
    deletemember = Deletemember.objects.all().first()
    user=User.objects.get(username=request.user.username)
    user= Profile.objects.get(user__username=request.user.username)
    deletedform = ProfileForm(instance = request.user.profile)
    if request.method=='POST':
        deletedform = ProfileForm(request.POST, instance=request.user.profile)
        if deletedform.is_valid:
            deletedform.save() 
            return redirect('dashboard')
            
           
    context={
        'user':user,
        'deletedform':deletedform,
        'deletemember':deletemember
    }
    return render(request, 'deletemember.html', context)


@login_required(login_url='loginform')
def renewmember(request, id):
    single = Member.objects.get(pk=id)
    user=User.objects.get(username=request.user.username)
    user= Profile.objects.get(user__username=request.user.username)
    renewalform = ProfileForm(instance = request.user.profile)
    if request.method=='POST':
        renewalform = ProfileForm(request.POST,  instance=request.user.profile)
        if renewalform.is_valid:
            renewalform.save() 
            return redirect('confirmrenewal')
            
           
    context={
        'user':user,
        'single':single,
        'renewalform':renewalform
    }
    return render(request, 'renewmember.html', context)


@login_required(login_url='loginform')
def memberrenewal(request):
    user= Profile.objects.get(user__username=request.user.username)
    renewalform = ProfileForm(instance = request.user.profile)
    if request.method=='POST':
        renewalform = ProfileForm(request.POST,  instance=request.user.profile)
        if renewalform.is_valid:
            renewalform.save()
            messages.success(request, 'Package upgrade successful')
            return redirect('confirmrenewal')
         
    context = {
        'renewalform': renewalform,
        'user':user,
    }

    return render(request, 'renewmember.html', context)

@login_required(login_url='loginform')
def confirmrenewal(request):
    user=User.objects.get(username=request.user.username)
    

    context={
        'user':user ,
    }
    return render(request, 'confirmrenewal.html', context)


@login_required(login_url='loginform')
def payrenewal(request):
    if request.method=='POST':
        api_key='sk_test_0e8a6068679eadbbbd2a7ff3a68f60bcf767faba'
        curl= 'https://api.paystack.co/transaction/initialize'
        cburl='http://localhost:8000/dashboard/'
        # cburl='http://54.172.142.223/dashboard/'
        user= User.objects.get(username=request.user.username)
        total= float(user.profile.dfee)*100
        pay_code= str(uuid.uuid4())
             

       #collect data that you will send to paystack
        headers={'Authorization': f'Bearer {api_key}'}
        data={'reference':pay_code,'email':user.email,'amount':int(total),'callback_url':cburl,'order_number':user.id}

        #make a call to paystack
        try:
            r=requests.post(curl, headers=headers, json=data)
        except Exception:
            messages.error(request, 'Network busy, try again')
        else:
            transback= json.loads(r.text)
            rd_url= transback['data']['authorization_url']

            pay = Payment()
            pay.user= user
            pay.first_name = user.first_name
            pay.last_name = user.last_name
            pay.pay_code = pay_code  
            pay.phone = user.profile.phone
            pay.title = user.profile.title
            pay.amount = total/100
            pay.paid = True
            pay.save()

            paid = Membership()
            paid.user=user.username
            paid.memeber_no=user.id
            paid.first_name=user.first_name
            paid.last_name=user.last_name
            paid.fee=total /100
            paid.pay_code=pay_code 
            paid.membership=user.profile.title
            paid.phone=user.profile.phone 
            paid.save()
            
            messages.success(request, 'Your membership has been renewed!')
        return redirect(rd_url)
    return redirect('profile')


@login_required(login_url='loginform')            
def renew(request):
    foreign = Product.objects.filter(foreign=True)
    local = Product.objects.filter(local=True)
    latest = Product.objects.filter(latest=True)
    

    context = { 
        'foreign':foreign,
        'local':local,
        'latest':latest,
    }

    return render(request, 'renew.html',context)