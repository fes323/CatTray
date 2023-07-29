from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def login_template(request):
    context = {
    }

    return render(request, template_name='login.html', context=context)