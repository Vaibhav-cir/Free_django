from django.shortcuts import render, redirect, get_object_or_404
from .models import Weapon
from .forms import WeaponForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from django.views.decorators.cache import never_cache

@never_cache
@login_required

def home(request):
    query = request.GET.get('q', '')
    if query:
        weapons = Weapon.objects.filter(
            Q(weapon_name__icontains=query) |
            Q(user_name__icontains=query) |
            Q(weapon_trainer__icontains=query)
        )
    else:
        weapons = Weapon.objects.all()
    weapon_count = Weapon.objects.count()

    paginator = Paginator(weapons, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request ,'home.html', {
        'page_obj': page_obj,
        'query': query,
        'weapon_count': weapon_count
    }
    )


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created, You can log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form':form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # ✅ You must pass both request and user
            messages.success(request, "Login successful!")
            return redirect("home")  # or your home page name
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def add_weapon(request):
    if request.method == "POST":
        form = WeaponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Weapon added successfully!")
            return redirect('home')
    else:
        form = WeaponForm()
    return render(request, 'add_weapon.html', {'form': form})

@login_required
def edit_weapon(request, pk):
    weapon = get_object_or_404(Weapon, pk=pk)
    if request.method == "POST":
        form = WeaponForm(request.POST, instance=weapon)
        if form.is_valid():
            form.save()
            messages.info(request, f"⚔️ {weapon.weapon_name} updated successfully!")
            return redirect('home')
    else:
        form = WeaponForm(instance=weapon)
    return render(request, 'edit_weapon.html', {'form': form, 'weapon': weapon})

@login_required
def delete_weapon(request, pk):
    weapon = get_object_or_404(Weapon, pk=pk)

    if request.method == "POST":
        weapon_name = weapon.weapon_name
        weapon.delete()
        messages.success(request, f"✅ Weapon '{weapon}' deleted successfully.")
        return redirect('home')

    # GET (or other non-POST) -> show confirmation page
    return render(request, 'delete_weapon.html', {'weapon': weapon})


@login_required
def about(request):
    return render(request, 'about.html')