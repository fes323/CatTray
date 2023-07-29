from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def main_page(request):
    context = {
    }

    return render(request, template_name='main_page.html', context=context)