from django.shortcuts import render,redirect,get_object_or_404
from django. contrib.auth  import authenticate,login,logout,update_session_auth_hash
from .models import customuser,Task,Category
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test,login_required
import random
from django.core.mail import send_mail
from django.conf import settings
from .utils import send_otp_email

def is_admin_user(user):
    return user.is_authenticated and user.is_admin

# -----------------   Home Page -----------------------------------------------------------------------------------

def home(request):
    return render(request,'home.html')

# ---------------- View Respective Page -------------------------------------------------

def adminclick(request):
    return render(request,'adminclick.html')
   
def userclick(request):
    return render(request,'userclick.html')

# -------------------- SIGNup Page ---------------------------------------------------

def userignup(request):
    if request.method == 'POST':
        u = request.POST['u']
        f = request.POST['f']
        e = request.POST['e']
        p = request.POST['p']
        n = request.POST['n']
        if customuser.objects.filter(username=u).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'usersignup.html')
        user = customuser.objects.create_user(
            username=u,
            first_name=f,
            email=e,
            password=p,
            phone=n,
        )
        user.is_user = True
        user.is_staff = False
        user.save()
        return render(request, 'usersignup.html', {
            'signup_success': True
        })

    return render(request, 'usersignup.html')


def adminsignup(request):
    if request.method == 'POST':
        u = request.POST['u']
        f = request.POST['f']
        e = request.POST['e']
        p = request.POST['p']
        n = request.POST['n']
        if customuser.objects.filter(username=u).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'adminsignup.html') 
        user = customuser.objects.create_user(
            username=u,
            first_name=f,
            email=e,
            password=p,
            phone=n
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return redirect('adminlogin')
    return render(request, 'adminsignup.html')

# ---------------------------- Login Page --------------------------------------------------

def admin_login(request):
    show_modal = False

    if request.method == 'POST':
        username = request.POST.get('u')
        password = request.POST.get('p')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_admin:
            login(request, user)
            show_modal = True
        else:
            messages.error(request, "Invalid admin credentials")

    return render(request, 'adminlogin.html', {
        'show_modal': show_modal
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('u')
        password = request.POST.get('p')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_user:
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()
            request.session['otp_user_id'] = user.id
            send_otp_email(user.email, otp)   
            messages.success(request, "OTP sent to your email")
            return redirect('verify_otp')
        else:
            messages.error(request, "Invalid user credentials")
    return render(request, 'userlogin.html')

# --------------------------------- OTP Page ------------------------------------------

def verify_otp(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        messages.error(request, "Session expired. Login again.")
        return redirect('userlogin')
    user = customuser.objects.get(id=user_id)
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        if entered_otp == user.otp:
            user.is_verified = True
            user.otp = None
            user.save()
            login(request, user)
            request.session.pop('otp_user_id', None)
            return redirect('userdashboard')
        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'verify_otp.html')

#  ------------------------------ LOGOUT ---------------------------------------

def user_logout(request):
    logout(request)
    return redirect('userlogin')  

def admin_logout(request):
    logout(request)
    return redirect('adminlogin')  

# -------------------------- to view Dashbord -------------------------------

@user_passes_test(is_admin_user)
@login_required(login_url='adminlogin')
def admindashboard(request):
    return render(request, 'admindashboard.html')

@login_required(login_url='studentlogin')
def userdashboard(request):
    return render(request,'user_dashboard.html')

# -------------------------------- Task Managing -----------------------

@login_required(login_url='userlogin')
def add_task(request):
    categories = Category.objects.filter(user__is_admin=True)
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id) if category_id else None
        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            category=category
        )
        return render(request, 'add_task.html', {
            'categories': categories,
            'task_success': True
        })
    return render(request, 'add_task.html', {
        'categories': categories
    })

@login_required(login_url='userlogin')
def running_tasks(request):
    tasks = Task.objects.filter(
        user=request.user,
        status='running'
    )
    return render(request, 'running_tasks.html', {'tasks': tasks})

@login_required(login_url='userlogin')
def complete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.status = 'completed'
    task.save()
    return redirect('completed_tasks')

@login_required(login_url='userlogin')
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    categories = Category.objects.all()
    if request.method == "POST":
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.priority = request.POST.get('priority')
        task.status = request.POST.get('status')
        task.due_date = request.POST.get('due_date')
        category_id = request.POST.get('category')
        task.category = Category.objects.get(id=category_id) if category_id else None
        task.save()
        return redirect('running_tasks')
    return render(request, 'edit_task.html', {
        'task': task,
        'categories': categories
    })


@login_required(login_url='userlogin')
def completed_tasks(request):
    tasks = Task.objects.filter(user=request.user, status='completed')
    return render(request, 'completed_tasks.html', {'tasks': tasks})


@login_required(login_url='userlogin')
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('completed_tasks')

# -------------------------------- Add Category -----------------------------------
@user_passes_test(is_admin_user)
@login_required(login_url='adminlogin')
def add_category(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            Category.objects.create(
                name=name,
                user=request.user
            )
            messages.success(request, "Category added successfully!")
            return redirect('add_category')
    return render(request, 'add_category.html')


@login_required(login_url='userlogin')
def profile(request):
    return render(request, 'profile.html')

# -------------------- Change Password ----------------------
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        user = request.user
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect("change_password")
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect("change_password")
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        return render(request, "change_password.html", {"password_updated": True})
    return render(request, "change_password.html")


@login_required(login_url='adminlogin')
def admin_tasks_users(request):
    users = customuser.objects.filter(is_user=True)
    return render(request, 'admin_tasks_users.html', {'users': users })


@login_required(login_url='adminlogin')
def admin_user_tasks(request, user_id):
    user = get_object_or_404(customuser, id=user_id)
    tasks = Task.objects.filter(user=user).order_by('-updated_at') 
    return render(request, 'admin_user_task_detail.html', {
        'user': user,
        'tasks': tasks
    })

