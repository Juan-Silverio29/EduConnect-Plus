from django.shortcuts import render

def foros_view(request):
    return render(request, "foros.html")
