from django.shortcuts import render

def index(request):
    return render(
        request,
        'pages/index.html',
    )

def page(request):
    return render(
        request,
        'pages/page.html',
    )

def post(request):
    return render(
        request,
        'pages/post.html',
    )
