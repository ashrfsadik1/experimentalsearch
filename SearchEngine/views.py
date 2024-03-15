from django.shortcuts import render, redirect
from SearchEngine.search import google

def homepage(request):
    return render(request,'home.html')

def secondpage(request):
    return render(request,'home.html')
def results(request):
    if request.method == "POST":
        result = request.POST.get('search')
        google_link,google_text = google(result)
        google_data = zip(google_link,google_text )
        #print(list(google_data))



        if result == '':
            return redirect('Home')
        else:
            return render(request,'results.html',{'google': google_data})