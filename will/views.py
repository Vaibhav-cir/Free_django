from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Weapon
from .forms import WeaponForm

class HomeView(LoginRequiredMixin, ListView):
    model = Weapon
    template_name = 'home.html'
    context_object_name = 'page_obj'
    paginate_by = 6
    login_url = 'login'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Weapon.objects.filter(
                Q(weapon_name__icontains=query) |
                Q(user_name__icontains=query) |
                Q(weapon_trainer__icontains=query)
            )
        return Weapon.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['weapon_count'] = self.get_queryset().count()
        return context
    
    def render_to_response(self, context, **response_kwargs):
        # HTMX support for search
        if self.request.headers.get('HX-Request'):
            return render(self.request, 'partials/weapon_list.html', context)
        return super().render_to_response(context, **response_kwargs)

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, "Login successful!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Your account has been created. You can log in.')
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    next_page = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)

class WeaponCreateView(LoginRequiredMixin, CreateView):
    model = Weapon
    form_class = WeaponForm
    template_name = 'add_weapon.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "✅ Weapon added successfully!")
        return super().form_valid(form)

class WeaponUpdateView(LoginRequiredMixin, UpdateView):
    model = Weapon
    form_class = WeaponForm
    template_name = 'edit_weapon.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.info(self.request, f"⚔️ {self.object.weapon_name} updated successfully!")
        return super().form_valid(form)

class WeaponDeleteView(LoginRequiredMixin, DeleteView):
    model = Weapon
    template_name = 'delete_weapon.html'
    success_url = reverse_lazy('home')
    context_object_name = 'weapon'

    def delete(self, request, *args, **kwargs):
        weapon = self.get_object()
        messages.success(request, f"✅ Weapon '{weapon.weapon_name}' deleted successfully.")
        return super().delete(request, *args, **kwargs)

class AboutView(LoginRequiredMixin, TemplateView):
    template_name = 'about.html'