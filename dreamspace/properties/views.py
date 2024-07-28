from django.shortcuts import render, get_object_or_404
from .models import Property, PropertyType
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def home(request):
    property_types = PropertyType.objects.all()
    return render(request, 'home.html', {'property_types': property_types})


@login_required
def property_list(request):
    properties = Property.objects.all()
    return render(request, 'property_list.html', {'properties': properties})


@login_required
def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    return render(request, 'property_detail.html', {'property': property})


@login_required
def property_list_by_type(request, property_type_id):
    property_type = get_object_or_404(PropertyType, id=property_type_id)
    properties = Property.objects.filter(property_type=property_type)
    return render(request, 'property_list.html', {'properties': properties, 'property_type': property_type})


def about(request):
    return render(request, 'about.html')


@login_required
def search_results(request):
    query = request.GET.get('q')
    location = request.GET.get('location')
    property_type = request.GET.get('property_type')
    price_max = request.GET.get('price_max')

    properties = Property.objects.all()

    if query:
        properties = properties.filter(title__icontains=query)
    if location:
        properties = properties.filter(location__city__icontains=location)
    if property_type:
        properties = properties.filter(property_type__name__icontains=property_type)
    if price_max:
        properties = properties.filter(price__lte=price_max)

    context = {
        'properties': properties,
    }

    return render(request, 'search_results.html', context)





def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send an email (you need to configure email settings in settings.py)
            send_mail(
                f'Message from {name} via Contact Form',
                message,
                email,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def contact_success(request):
    return render(request, 'contact_success.html')
