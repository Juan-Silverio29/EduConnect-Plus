#dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    if request.user.is_superuser:
        return render(request, "dashboard_admin.html")
    return render(request, "dashboard_user.html")

