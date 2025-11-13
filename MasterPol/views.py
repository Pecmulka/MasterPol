from django.shortcuts import render, redirect, get_object_or_404
from .models import Partner, Partner_type, Region, City, Street, Partner_product, Address


def partner_edit(request, partner_id):
    partner = Partner.objects.select_related('type', 'address__street__city__region').get(id=partner_id)

    if request.method == 'POST':
        try:
            # Обновление основных данных партнера
            partner.name = request.POST.get('name')
            partner.phone = request.POST.get('phone')
            partner.email = request.POST.get('email')
            partner.discount = request.POST.get('discount')
            partner.CEO = request.POST.get('ceo')
            partner.INN = request.POST.get('inn')
            partner.rating = request.POST.get('rating')

            # Обновление типа компании
            type_name = request.POST.get('type')
            if partner.type.name != type_name:
                partner_type = Partner_type.objects.filter(name=type_name).first()
                if not partner_type:
                    partner_type = Partner_type.objects.create(name=type_name)
                partner.type = partner_type

            # Обновление адреса
            postal_code = request.POST.get('postal_code')
            house_number = request.POST.get('house_number')
            region_name = request.POST.get('region')
            city_name = request.POST.get('city')
            street_name = request.POST.get('street')

            # Проверяем, изменился ли адрес
            current_address = partner.address
            current_region = current_address.street.city.region.name
            current_city = current_address.street.city.name
            current_street = current_address.street.name

            if (current_region != region_name or current_city != city_name or
                    current_street != street_name or
                    current_address.house_number != int(house_number) or
                    current_address.postal_code != int(postal_code)):

                # Поиск региона
                region = Region.objects.filter(name=region_name).first()
                if not region:
                    region = Region.objects.create(name=region_name)

                # Поиск города
                city = City.objects.filter(name=city_name, region=region).first()
                if not city:
                    city = City.objects.create(name=city_name, region=region)

                # Поиск улицы
                street = Street.objects.filter(name=street_name, city=city).first()
                if not street:
                    street = Street.objects.create(name=street_name, city=city)

                # Поиск адреса
                address = Address.objects.filter(
                    postal_code=postal_code,
                    street=street,
                    house_number=house_number
                ).first()

                if not address:
                    address = Address.objects.create(
                        postal_code=postal_code,
                        street=street,
                        house_number=house_number
                    )

                partner.address = address

            partner.save()
            return redirect('partners_list')

        except Exception as e:
            context = {
                'partner': partner,
                'error': str(e)
            }
            return render(request, 'partner_edit.html', context)

    return render(request, 'partner_edit.html', {'partner': partner})


def partner_add(request):
    if request.method == 'POST':
        try:
            # Получение данных из формы
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            discount = request.POST.get('discount')
            ceo = request.POST.get('ceo')
            inn = request.POST.get('inn')
            rating = request.POST.get('rating')

            # Поиск или создание типа компании
            type_name = request.POST.get('type')
            partner_type = Partner_type.objects.filter(name=type_name).first()
            if not partner_type:
                partner_type = Partner_type.objects.create(name=type_name)

            # Поиск или создание адреса
            postal_code = request.POST.get('postal_code')
            house_number = request.POST.get('house_number')
            region_name = request.POST.get('region')
            city_name = request.POST.get('city')
            street_name = request.POST.get('street')

            # Поиск региона
            region = Region.objects.filter(name=region_name).first()
            if not region:
                region = Region.objects.create(name=region_name)

            # Поиск города
            city = City.objects.filter(name=city_name, region=region).first()
            if not city:
                city = City.objects.create(name=city_name, region=region)

            # Поиск улицы
            street = Street.objects.filter(name=street_name, city=city).first()
            if not street:
                street = Street.objects.create(name=street_name, city=city)

            # Проверка существования адреса
            address = Address.objects.filter(
                postal_code=postal_code,
                street=street,
                house_number=house_number
            ).first()

            if not address:
                address = Address.objects.create(
                    postal_code=postal_code,
                    street=street,
                    house_number=house_number
                )

            # Создание партнера
            partner = Partner.objects.create(
                name=name,
                type=partner_type,
                CEO=ceo,
                email=email,
                phone=phone,
                address=address,
                INN=inn,
                rating=rating,
                discount=discount
            )

            return redirect('partners_list')

        except Exception as e:
            return render(request, 'partner_add.html', {'error': str(e)})

    return render(request, 'partner_add.html')

def partners_list(request):
    partners = Partner.objects.select_related('type').all()
    return render(request, 'partners_list.html', {'partners': partners})


def partner_purchases(request, partner_id):
    partner = get_object_or_404(Partner, id=partner_id)
    purchases = Partner_product.objects.filter(partner=partner).select_related('product')

    return render(request, 'partner_purchases.html', {'partner': partner, 'purchases': purchases})