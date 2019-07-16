from django.shortcuts import render

def main_list(request):
    return render(request, 'blog/main.html')


def about(request):
    return render(request, 'blog/about.html')