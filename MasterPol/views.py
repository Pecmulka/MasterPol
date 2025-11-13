from django.shortcuts import render, redirect, get_object_or_404
from .models import Partner, Partner_type, Region, City, Street, Partner_product


def partner_edit(request, partner_id):
    partner = Partner.objects.select_related('type', 'address__street__city__region').get(id=partner_id)

    if request.method == 'POST':
        partner.name = request.POST.get('name')
        partner.phone = request.POST.get('phone')
        partner.email = request.POST.get('email')
        partner.discount = request.POST.get('discount')

        type_name = request.POST.get('type')
        partner_type, created = Partner_type.objects.get_or_create(name=type_name)
        partner.type = partner_type
        partner.address.postal_code = request.POST.get('postal_code')
        partner.address.house_number = request.POST.get('house_number')
        region_name = request.POST.get('region')
        city_name = request.POST.get('city')
        street_name = request.POST.get('street')
        region, created = Region.objects.get_or_create(name=region_name)
        city, created = City.objects.get_or_create(name=city_name, region=region)
        street, created = Street.objects.get_or_create(name=street_name, city=city)

        partner.address.street = street
        partner.address.save()
        partner.save()

        return redirect('partners_list')
    return render(request, 'partner_edit.html', {'partner': partner})

def partners_list(request):
    partners = Partner.objects.select_related('type').all()
    return render(request, 'partners_list.html', {'partners': partners})


def partner_purchases(request, partner_id):
    partner = get_object_or_404(Partner, id=partner_id)
    purchases = Partner_product.objects.filter(partner=partner).select_related('product')

    return render(request, 'partner_purchases.html', {'partner': partner, 'purchases': purchases})