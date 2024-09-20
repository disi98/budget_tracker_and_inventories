from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_dashboard(request):
    return render(request, "dashboard/home_dashboard.html")