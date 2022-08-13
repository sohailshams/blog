from django.shortcuts import render

from .models import Post

def blog_list_view(request):
    """ A view to render all blog posts """

    # Get all blog posts 
    posts = Post.objects.all()

    return render(request, 'home.html', {'object_list': posts})
