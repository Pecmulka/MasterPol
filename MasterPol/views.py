from django.shortcuts import render
from .models import Partner

def partners_list(request):
    partners = Partner.objects.select_related('type').all()
    return render(request, 'partners_list.html', {'partners': partners})