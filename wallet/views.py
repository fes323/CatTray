from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def wallet(request):
    context = {
    }

    return render(request, template_name='wallet.html', context=context)