from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone  
from .models import StudentID, CustomUser
from django.contrib.auth.forms import AuthenticationForm
from .forms import IDSearchForm, IDForm, ClaimIDForm, LostIDForm, UserRegistrationForm

def home(request):
    if request.user.is_authenticated:
        if request.user.user_type == 1:  # Student
            return render(request, 'student_dashboard.html')
        elif request.user.user_type == 2:  # Staff
            return redirect('admin-dashboard')
        elif request.user.user_type == 3:  # Admin
            return redirect('admin-dashboard')
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-login after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Registration successful. Welcome!")
                return redirect("home")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    return render(request, "registration/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("home")
        messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")

def search_id(request):
    if request.method == 'POST':
        form = IDSearchForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data['id_number']
            student_name = form.cleaned_data['student_name']
            
            results = StudentID.objects.filter(
                id_number__icontains=id_number,
                student_name__icontains=student_name,
                status='FOUND'
            )
            return render(request, 'search_results.html', {
                'results': results,
                'search_performed': True
            })
    else:
        form = IDSearchForm()
    return render(request, 'search.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.user_type in [2, 3])  # Only staff and admin
def add_found_id(request):
    if request.method == 'POST':
        form = IDForm(request.POST, request.FILES)
        if form.is_valid():
            id_record = form.save(commit=False)
            id_record.reported_by = request.user
            id_record.status = 'FOUND'
            id_record.save()
            messages.success(request, 'ID successfully recorded in the system.')
            return redirect('admin-dashboard')
    else:
        form = IDForm()
    return render(request, 'add_id.html', {'form': form})

def claim_id(request, pk):
    id_record = get_object_or_404(StudentID, pk=pk)
    if request.method == 'POST':
        form = ClaimIDForm(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data['verification_code']
            if verification_code == id_record.verification_code:
                id_record.status = 'RETURNED'
                id_record.claimed_by = request.user if request.user.is_authenticated else None
                id_record.date_claimed = timezone.now()
                id_record.save()
                messages.success(request, 'ID successfully claimed.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid verification code.')
    else:
        form = ClaimIDForm()
    return render(request, 'claim_id.html', {'form': form, 'id_record': id_record})

@login_required
@user_passes_test(lambda u: u.user_type in [2, 3])  # Only staff and admin
def admin_dashboard(request):
    found_ids = StudentID.objects.filter(status='FOUND').order_by('-date_reported')
    returned_ids = StudentID.objects.filter(status='RETURNED').order_by('-date_claimed')
    lost_ids = StudentID.objects.filter(status='LOST')
    return render(request, 'admin_dashboard.html', {
        'found_ids': found_ids,
        'returned_ids': returned_ids,
        'lost_ids': lost_ids
    })

def report_lost_id(request):
    if request.method == "POST":
        form = LostIDForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data["id_number"]
            if StudentID.objects.filter(id_number=id_number, status="LOST").exists():
                messages.error(request, "This ID has already been reported as lost.")
                return redirect("report-lost-id")
            lost_id = form.save(commit=False)
            lost_id.status = "LOST"  
            lost_id.save()
            messages.success(request, "Lost ID reported successfully!")
            return redirect("home")  
    else:
        form = LostIDForm()
    return render(request, "report_lost_id.html", {"form": form})