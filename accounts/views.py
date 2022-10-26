import os
from django.conf import settings

from django.shortcuts import  render, redirect, reverse
from .forms import SignupModelForm, ProfileImageModelForm, ProfileUpdateModelForm
from .models import Profile, Follow
from blogs.models import BlogPost
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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
    follower = request.user
 
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

    # Get follow objet
    user_follower = Follow.objects.filter(
            follower=follower,
            user=user
        ).first()

    if user_follower:
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    # Get posts list
    post_list = BlogPost.objects.filter(auther=blog_user).count()

    # Get followers list
    followers_list = Follow.objects.filter(user=user).count()
    
    # Get following list
    following_list = Follow.objects.filter(follower=user_profile.user).count()

    template_name = 'profile.html'

    context = {
        'user_profile': user_profile,
        'button_text': button_text,
        'posts': post_list,
        'following_list': following_list,
        'followers_list': followers_list

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

    # Get image path
    image_path = user_profile.profile_img.path
 
    if request.method == 'POST':  
        updated_image = request.FILES.get('profile_img', '')

        # Check if updated image exist or return error message & redirect to home page
        if not updated_image:
            messages.success(request, 'Please add profile image and try again.')            
            return redirect(reverse('profile', args=[user]))
        
        # Instantiate a new instance of ProfileImageModelForm
        form = ProfileImageModelForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():

            # deleting old uploaded image
            if os.path.exists(image_path):
                os.remove(image_path)
                
            # The `form.save` will update newest image & path.
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
 
 
@login_required
def profile_update_view(request, **kwargs):
    """ A view to handle profile update """
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
        messages.error(request, 'Sorry, only profile owner can upate profile.')
        return redirect(reverse('home'))

    # Get image path
    image_path = user_profile.profile_img.path
 
    if request.method == 'POST':  
        # Get image from request.FILES
        updated_image = request.FILES.get('profile_img', '')
        
        # Instantiate a new instance of ProfileImageModelForm
        form = ProfileUpdateModelForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # Delete old image only if new image is selected
            if updated_image:
                # deleting old uploaded image if new image is passed
                if os.path.exists(image_path):
                    os.remove(image_path)
                
            # The `form.save` will update newest image & path if exist or will save profile info only
            form.save()

            # Add success message
            messages.success(request, 'Profile updated successfully!')            
            return redirect(reverse('profile', args=[user]))
        else:
            messages.error(request, 'Failed to update user profile. \
                                    Please try again!')       
    else:
        # Empty form instantiation
        form = ProfileUpdateModelForm(instance=user_profile)

    template_name = 'profile_update.html'

    context = {
        'form': form,
        'user_profile': user_profile
    }

    return render(request, template_name, context)
    

@login_required
def follow_unfollow_view(request,  **kwargs):
    """ A view to handle follow/unfollow of a user """
    # Get user and follower
    follower = request.user
    user = kwargs.get('username', None)
    
    # Get follow objet
    user_follower = Follow.objects.filter(
            follower=follower,
            user=user
        ) 

    # Delete follow object if exist or create new follow object
    if len(user_follower):
        user_follower.delete()
        messages.success(request, f'{user} unfollowed successfully')
    else:
        Follow.objects.create(
            follower=follower,
            user=user
        )     
        messages.success(request, f'You are now following {user}.')

    return redirect(reverse('profile', args=[user]))
