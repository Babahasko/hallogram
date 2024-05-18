from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import DetailView

from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.postgres.search import SearchVector

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, SearchForm
from .models import Profile


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


def search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Profile.objects.annotate(
                search=SearchVector('user__username', 'user__first_name', 'user__last_name'),
            ).filter(search=query)
    return render(request,
                  'account/search.html',
                  {'form': form,
                           'query': query,
                           'results': results,
                           'section': 'search'})


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'account/profile.html'
    context_object_name = 'profile'
    slug_url_kwarg = 'profile_uuid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        profile = Profile.objects.get(uuid=self.kwargs[self.slug_url_kwarg])
        return profile

