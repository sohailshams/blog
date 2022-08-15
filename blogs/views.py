from django.shortcuts import render

from .models import Post

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