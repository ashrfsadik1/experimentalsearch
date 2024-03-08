from django.shortcuts import render

# Create your views here.


def display_page(request):
    url = request.GET.get('url', '')
    return render(request, 'display/webviewA.html', {'url': url})
