from django.shortcuts import render, redirect, reverse
from django.contrib import messages

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


    template_name = 'detail.html'

    template_dict = {
        'post_title': post_title,
        'post_auther': post_auther,
        'post_body': post_body
        }

    return render(request, template_name, template_dict)

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
