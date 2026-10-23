from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'dashboard.html')

def scan_view(request):
    return render(request, 'scan.html')

def result_view(request, prediction_id):
    return render(request, 'result.html', {'prediction_id': prediction_id})

def history_view(request):
    return render(request, 'history.html')

def analytics_view(request):
    return render(request, 'analytics.html')

def profile_view(request):
    return render(request, 'profile.html')
