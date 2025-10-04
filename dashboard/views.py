from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    user = request.user

    if user.is_superuser or user.is_staff:
        return render(request, "dashboard_admin.html")

    if hasattr(user, "is_teacher") and user.is_teacher:
        cursos = [
            {"nombre": "Matemáticas I", "grupo": "1A", "alumnos": 30},
            {"nombre": "Historia", "grupo": "2B", "alumnos": 25},
        ]
        return render(request, "dashboard_profesor.html", {"cursos": cursos})

    return render(request, "dashboard_user.html")
@login_required
def dashboard_profesor(request):
    return render(request, "dashboard_profesor.html")

def dashboard_user(request):
    return render(request, "dashboard_user.html")
