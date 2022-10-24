from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import BlogPost, BlogComment, BlogLike

from .forms import PostModelForm, CommentModelForm

def blog_list_view(request):
    """ A view to render all blog posts """

    # Get all blog posts and order them by updated date
    blog_posts = BlogPost.objects.all().order_by('-updated')
    template_name = 'home.html'

    context = {
        'post_list': blog_posts,
    }

    return render(request, template_name, context)

def blog_detail_view(request, **kwargs):
    """ A view to render blog post detail """
   
    uuid = kwargs.get('post_uuid', None)

    if request.method == 'GET': 
        # Get a blog post by its uuid or redirect to the home page 
        try:
            blog_post = BlogPost.objects.get(post_uuid=uuid)
        except:        
            messages.error(request, 'Sorry, this post does not exist.')
            return redirect(reverse('home'))

        # Get all blog comments and order them by updated date
        blog_comments = BlogComment.objects.filter(
            comment_blog=blog_post,
        ).order_by('-updated')
   

    if request.method == 'POST':
        
        user = request.user
        
        # Get a blog post by its uuid or redirect to the home page 
        try:
            blog_post = BlogPost.objects.get(post_uuid=uuid)
        except:        
            messages.error(request, 'Sorry, this post does not exist.')

        # If condition to ensure only logged in user can add comments.
        if user.is_authenticated:
            # Instantiate a new instance of blog post form
            form = CommentModelForm(request.POST or None)
            if form.is_valid():
                comment_obj = form.save(commit=False)

                # Attach user & blog post to comment
                comment_obj.comment_auther = request.user
                comment_obj.comment_blog = blog_post

                comment_obj.save()

                # Add success message
                messages.success(request, 'Comment added successfully!')

                
                return redirect(reverse('blog_detail',  args=[blog_post.post_uuid]))

            else:
                messages.error(request, 'Failed to add comment. \
                                        Please make sure, the form is valid.')
        
        else:
            # Add an error message
            messages.error(request, 'Please login to add comment.')
            return redirect(reverse('home'))
    else:
        # Empty form instantiation
        form = CommentModelForm()
    
     
    template_name = 'detail.html'

    context = {
        'blog_post': blog_post,
        'comment_list': blog_comments,
        'form': form
        }

    return render(request, template_name, context)

@login_required
def blog_comment_edit_view(request,  **kwargs):
    """ A view to edit blog post comment if user is the owner of this blog post comment """
    # Get user and commnet_uuid from request
    user = request.user
    uuid = kwargs.get('comment_uuid', None)

    # Get a blog post comment or redirect to the home page with error message
    try:
        blog_post_comment = BlogComment.objects.get(
            comment_uuid=uuid,
            comment_auther=user
            )
    except:        
        messages.error(request, 'Only blog post comment owner can access it.')
        return redirect(reverse('home'))

    # Get blog post comment_uuid
    blog_post = blog_post_comment.comment_blog.post_uuid

    if request.method == 'POST':
        # Instantiated a form using request.post & blog post instance
        form = CommentModelForm(request.POST, instance=blog_post_comment)
        if form.is_valid():
            form.save()

            messages.success(request, 'Blog post comment updated successfully!')
            return redirect(reverse('blog_detail', args=[blog_post]))
        else:
            messages.error(request, 'Failed to update blog post comment. \
                            Please ensure the form is valid.')
    else:
        # Instantiating blog post form using the blog post
        form = CommentModelForm(instance=blog_post_comment)
        messages.info(request, f'You are editing blog post comment')

    template = 'blog_comment_edit.html'
    context = {
        'form': form,
        'blog_post': blog_post,
        'comment': blog_post_comment,
    }

    return render(request, template, context)

@login_required
def blog_detail_view(request, **kwargs):
    """ A view to render blog post detail """
   
    uuid = kwargs.get('post_uuid', None)
    user = request.user

    if request.method == 'GET': 
        # Get a blog post by its uuid or redirect to the home page 
        try:
            blog_post = BlogPost.objects.get(post_uuid=uuid)
        except:        
            messages.error(request, 'Sorry, this post does not exist.')
            return redirect(reverse('home'))

        # Get all blog comments and order them by updated date
        blog_comments = BlogComment.objects.filter(
            comment_blog=blog_post,
        ).order_by('-updated')

         # Get a blog post like or returns none 
        blog_post_like = BlogLike.objects.filter(
                like_blog=blog_post,
                like_auther=user
            ).first()

    if request.method == 'POST':  
        # Get a blog post by its uuid or redirect to the home page 
        try:
            blog_post = BlogPost.objects.get(post_uuid=uuid)
        except:        
            messages.error(request, 'Sorry, this post does not exist.')

        # If condition to ensure only logged in user can add comments.
        if user.is_authenticated:
            # Instantiate a new instance of blog post form
            form = CommentModelForm(request.POST or None)
            if form.is_valid():
                comment_obj = form.save(commit=False)

                # Attach user & blog post to comment
                comment_obj.comment_auther = request.user
                comment_obj.comment_blog = blog_post

                comment_obj.save()

                # Add success message
                messages.success(request, 'Comment added successfully!')

                
                return redirect(reverse('blog_detail',  args=[blog_post.post_uuid]))

            else:
                messages.error(request, 'Failed to add comment. \
                                        Please make sure, the form is valid.')
        
        else:
            # Add an error message
            messages.error(request, 'Please login to add comment.')
            return redirect(reverse('home'))
    else:
        # Empty form instantiation
        form = CommentModelForm()
    
     
    template_name = 'detail.html'

    context = {
        'blog_post': blog_post,
        'comment_list': blog_comments,
        'form': form,
        'like': blog_post_like
        }

    return render(request, template_name, context)

@login_required
def blog_like_view(request,  **kwargs):
    """ A view to handle like/dislike a blog post """
    # Get user and post_uuid from request
    user = request.user
    uuid = kwargs.get('post_uuid', None)

    # Get a blog post or redirect to the home page with error message
    try:
        blog_post = BlogPost.objects.get(
            post_uuid=uuid
            )
    except:        
        messages.error(request, 'This blog post does not exist.')
        return redirect(reverse('home'))

    # Get blog post likes
    blog_post_like = BlogLike.objects.filter(
        like_auther=request.user,
        like_blog=blog_post
    ).first()

    if blog_post_like is None:
        new_like = BlogLike.objects.create(
            like_auther=request.user,
            like_blog=blog_post
        )
        new_like.save()
        blog_post.num_of_likes = blog_post.num_of_likes+1
        blog_post.save()

        return redirect(reverse('blog_detail', args=[blog_post.post_uuid]))

    else:
        blog_post_like.delete()
        blog_post.num_of_likes = blog_post.num_of_likes-1
        blog_post.save()

        return redirect(reverse('blog_detail', args=[blog_post.post_uuid]))
    


@login_required
def blog_comment_delete_view(request, **kwargs):
    """ Aview to delete blog post comment from DB """
    user = request.user
    uuid = kwargs.get('comment_uuid', None)

    # Get a blog post by passing user and post_uuid or redirect to the home page
    try:
        blog_post_comment = BlogComment.objects.get(
            comment_uuid=uuid,
            comment_auther=user
            )
    except:        
        messages.error(request, 'Sorry, you aren\'t authorized to delete this blog post comment.')
        return redirect(reverse('home')) 

    # Delete blog post
    blog_post_comment.delete()
    messages.success(request, 'Blog post comment deleted successfully!')
    return redirect(reverse('home'))
    
@login_required
def blog_add_view(request):
    """ A view to add blog post """
    if request.method == 'POST':

        # Instantiate a new instance of blog post form
        form = PostModelForm(request.POST or None)
        if form.is_valid():
            blog_obj = form.save(commit=False)

            # Attach user to the blog post
            blog_obj.auther = request.user
            blog_obj.save()

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

    context = {
        'form': form
    }

    return render(request, template_name, context)
    
@login_required
def blog_add_view(request):
    """ A view to add blog post """
    if request.method == 'POST':

        # Instantiate a new instance of blog post form
        form = PostModelForm(request.POST or None)
        if form.is_valid():
            blog_obj = form.save(commit=False)

            # Attach user to the blog post
            blog_obj.auther = request.user
            blog_obj.save()

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

    context = {
        'form': form
    }

    return render(request, template_name, context)

@login_required
def blog_edit_view(request,  **kwargs):
    """ A view to edit blog post if user is the owner of this blog post """
    user = request.user
    uuid = kwargs.get('post_uuid', None)

    # Get a blog post by passing user and post_uuid or redirect to the home page
    try:
        blog_post = BlogPost.objects.get(
            post_uuid=uuid,
            auther=user)
    except:        
        messages.error(request, 'Only blog owner can access it.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        # Instantiated a form using request.post
        form = PostModelForm(request.POST, instance=blog_post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect(reverse('blog_detail', args=[blog_post.post_uuid]))
        else:
            messages.error(request, 'Failed to update blog post. \
                            Please ensure the form is valid.')
    else:
        # Instantiating blog post form using the blog post
        form = PostModelForm(instance=blog_post)
        messages.info(request, f'You are editing {blog_post.title}')

    template = 'edit.html'
    context = {
        'form': form,
        'blog_post': blog_post,
    }

    return render(request, template, context)

@login_required
def blog_delete_view(request, **kwargs):
    """ Aview to delete blog post from DB """
    user = request.user
    uuid = kwargs.get('post_uuid', None)

    # Get a blog post by passing user and post_uuid or redirect to the home page
    try:
        blog_post = BlogPost.objects.get(
            post_uuid=uuid,
            auther=user)
    except:        
        messages.error(request, 'Sorry, you aren\'t authorized to delete this blog post.')
        return redirect(reverse('home')) 

    # Delete blog post
    blog_post.delete()
    messages.success(request, 'Blog post deleted successfully!')
    return redirect(reverse('home'))
    