from django.shortcuts import  render, redirect, reverse
from .forms import SignupModelForm
from django.contrib import messages

def register_view(request):
    if request.method == "POST":

        # Instantiate a new instance of blog post form
        form = SignupModelForm(request.POST or None)
        if form.is_valid():
            user_obj = form.save()
            
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
