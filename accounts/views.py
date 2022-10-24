from django.shortcuts import  render, redirect, reverse
from .forms import SignupModelForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import ProfileImageModelForm


def register_view(request):
    if request.method == "POST":

        # Instantiate a new instance of blog post form
        form = SignupModelForm(request.POST or None)
        if form.is_valid():
            user_obj = form.save()

            user_profile = Profile.objects.create(user=user_obj)
            
            # Add success message
            messages.success(request, "Registration successful." )
            return redirect(reverse('login'))

        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
         # Empty form instantiation
         form = SignupModelForm()

    template_name = 'register.html'

    template_dict = {
    'form': form
    }
    return render(request, template_name, template_dict)

@login_required
def profile_view(request, **kwargs):
    """ A view to handle user profile """
    user = kwargs.get('username', None)
 
    # Get user or return error message & redirect to home page
    try:
        blog_user = User.objects.get(username=user)
    except:
        messages.error(request, 'Sorry, this user does not exist.')
        return redirect(reverse('home'))

    # Get user profile or return error message & redirect to home page
    try:
        user_profile = Profile.objects.get(user=blog_user)
    except:
        messages.error(request, 'Sorry, this profile does not exist.')
        return redirect(reverse('home'))

    template_name = 'profile.html'

    context = {
        'user_profile': user_profile,
    }

    return render(request, template_name, context)


@login_required
def profile_image_view(request, **kwargs):
    """ A view to handle uploading of profile image """
    user = kwargs.get('username', None)
    uuid = kwargs.get('profile_uuid', None)
    
    # Get user profile or return error message & redirect to home page
    try:
        user_profile = Profile.objects.get(profile_uuid=uuid)
    except:
        messages.error(request, 'Sorry, this profile does not exist.')
        return redirect(reverse('home'))

    # Check if user is profile owner
    if user_profile.user != request.user:
        messages.error(request, 'Sorry, only profile owner can upate profile image.')
        return redirect(reverse('home'))
 
    if request.method == 'POST':  
        # Instantiate a new instance of ProfileImageModelForm
        form = ProfileImageModelForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            profile_image = form.save()

            # Add success message
            messages.success(request, 'Profile image added successfully!')            
            return redirect(reverse('profile', args=[user]))
        else:
            messages.error(request, 'Failed to add profile image. \
                                    Please try again!')       
    else:
        # Empty form instantiation
        form = ProfileImageModelForm(instance=user_profile)

    template_name = 'image.html'

    context = {
        'form': form
    }

    return render(request, template_name, context)
    