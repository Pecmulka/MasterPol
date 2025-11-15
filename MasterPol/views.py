import math
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MaterialCalculatorForm
from .models import Partner, Partner_type, Region, City, Street, Partner_product, Address, Product_type, Material_type

def partner_edit(request, partner_id):
    partner = Partner.objects.select_related('type', 'address__street__city__region').get(id=partner_id)

    partner_types = Partner_type.objects.all()

    if request.method == 'POST':
        try:
            # Обновление основных данных партнера
            partner.name = request.POST.get('name')
            partner.phone = request.POST.get('phone')
            partner.email = request.POST.get('email')
            partner.CEO = request.POST.get('ceo')
            partner.INN = request.POST.get('inn')
            partner.rating = request.POST.get('rating')

            # Обновление типа компании
            type_id = request.POST.get('type')
            partner_type = Partner_type.objects.get(id=type_id)
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
            return render(request, 'partner_edit.html', {'partner': partner,
                                                         'partner_types': partner_types,
                                                         'error': str(e)})

    return render(request, 'partner_edit.html', {'partner': partner, 'partner_types': partner_types,})


def partner_add(request):
    partner_types = Partner_type.objects.all()

    if request.method == 'POST':
        try:
            # Получение данных из формы
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            ceo = request.POST.get('ceo')
            inn = request.POST.get('inn')
            rating = request.POST.get('rating')

            # Тип компании
            type_id = request.POST.get('type')
            partner_type = Partner_type.objects.get(id=type_id)

            # Создание адреса
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
                rating=rating
            )

            return redirect('partners_list')

        except Exception as e:
            return render(request, 'partner_add.html', {'partner_types': partner_types,
                                                        'error': str(e)})

    return render(request, 'partner_add.html', {'partner_types': partner_types})


def calculate_required_material(product_type_id, material_type_id, product_quantity, param1, param2):

    try:
        # Проверяем существование типов продукции и материалов
        product_type = Product_type.objects.get(id=product_type_id)
        material_type = Material_type.objects.get(id=material_type_id)

        # Расчет материала на одну единицу продукции
        material_per_unit = param1 * param2 * product_type.product_type_ratio

        # Общее количество материала без учета брака
        total_material = material_per_unit * product_quantity

        # Учет брака материала (переводим процент в долю)
        defect_rate = material_type.material_scrap_percentage / 100.0

        # Количество материала с учетом брака
        material_with_defect = total_material / (1 - defect_rate)

        # Округляем до целого в большую сторону
        return int(math.ceil(material_with_defect))

    except (Product_type.DoesNotExist, Material_type.DoesNotExist, ValueError):
        return -1

def partners_list(request):
    partners = Partner.objects.select_related('type').all()
    calculator_form = MaterialCalculatorForm()
    result = None

    if request.method == 'POST' and 'calculate' in request.POST:
        calculator_form = MaterialCalculatorForm(request.POST)
        if calculator_form.is_valid():
            product_type = calculator_form.cleaned_data['product_type']
            material_type = calculator_form.cleaned_data['material_type']
            product_quantity = calculator_form.cleaned_data['product_quantity']
            param1 = calculator_form.cleaned_data['param1']
            param2 = calculator_form.cleaned_data['param2']

            result = calculate_required_material(
                product_type.id,
                material_type.id,
                product_quantity,
                param1,
                param2
            )

    return render(request, 'partners_list.html', {'partners': partners,
                                                  'calculator_form': calculator_form,
                                                   'result': result,})


def partner_purchases(request, partner_id):
    partner = get_object_or_404(Partner, id=partner_id)
    purchases = Partner_product.objects.filter(partner=partner).select_related('product')

    return render(request, 'partner_purchases.html', {'partner': partner, 'purchases': purchases})