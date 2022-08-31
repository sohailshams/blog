from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Post

from .forms import PostModelForm

def blog_list_view(request):
    """ A view to render all blog posts """

    # Get all blog posts and order them by updated date
    posts = Post.objects.all().order_by('-updated')
   
    template_name = 'home.html'

    template_dict = {
        'post_list': posts,
    }

    return render(request, template_name, template_dict)

def blog_detail_view(request, post_pk):
    """ A view to render blog post detail """

    # Get a blog post by its id 
    post = Post.objects.filter(id=post_pk)
   
    post_title = post[0].title
    post_auther = post[0].auther
    post_body = post[0].body
    post_id = post[0].id


    template_name = 'detail.html'

    template_dict = {
        'post_title': post_title,
        'post_auther': post_auther,
        'post_body': post_body,
        'post_id': post_id
        }

    return render(request, template_name, template_dict)

@login_required
def blog_add_view(request):
    """ A view to add blog post """
    if request.method == 'POST':

        # Instantiate a new instance of blog post form
        form = PostModelForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)

            # Attach user to the blog post
            obj.auther = request.user
            obj.save()

            # Add success message
            messages.success(request, 'Blog added successfully!')
            return redirect(reverse('home'))

        else:
            messages.error(request, 'Failed to add blog post. \
                                    Please make sure, the form is valid.')
    else:
        # Empty form instantiation
        form = PostModelForm()

    template_name = 'form.html'

    template_dict = {
        'form': form
    }

    return render(request, template_name, template_dict)

@login_required
def blog_edit_view(request, post_pk):
    """ A view to edit blog post if user is the owner of this blog post """
    # Check if user is the owner of blog post
    post_users = Post.objects.filter(auther=request.user)
    print(post_users)
    if not post_users.count():
        messages.error(
            request, 'Sorry, you aren\'t authorized to edit this blog post.'
        )
        return redirect(reverse('home'))
    post_user = post_users[0]

    # Check if user is blog owner or return error
    if post_user.role != 'owner':
        messages.error(request, 'Only blog owner can access it.')
        return redirect(reverse('home'))

    # Get blog post or return error 
    try:
        post = Post.objects.get(auther=request.user, id=post_pk)
    except:
        messages.error(request, 'Blog post can not be found!')
        return redirect(reverse('home'))

    if request.method == 'POST':
        # Instantiated a form using request.post and post_pk
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect(reverse('blog_detail', args=[post.id]))
        else:
            messages.error(request, 'Failed to update blog post. \
                            Please ensure the form is valid.')
    else:
        # Instantiating blog post form using the blog post
        form = PostModelForm(instance=post)
        messages.info(request, f'You are editing {post.title}')

    template = 'edit.html'
    context = {
        'form': form,
        'post': post,
    }

    return render(request, template, context)

@login_required
def blog_delete_view(request, post_pk):
    """ Aview to delete blog post from DB """
    # Check if user is the owner of blog post
    post_users = Post.objects.filter(auther=request.user)
    if not post_users.count():
        messages.error(
            request, 'Sorry, you aren\'t authorized to delete this blog post.'
        )
        return redirect(reverse('home'))
    post_user = post_users[0]

    # Check if user is blog owner or return error
    if post_user.role != 'owner':
        messages.error(request, 'Only blog owner can access it.')
        return redirect(reverse('home'))

     # Get blog post or return error 
    try:
        post = Post.objects.get(auther=request.user, id=post_pk)
    except:
        messages.error(request, 'Blog post can not be found!')
        return redirect(reverse('home'))

    # Delete blog post
    post.delete()
    messages.success(request, 'Blog post deleted successfully!')
    return redirect(reverse('home'))
    