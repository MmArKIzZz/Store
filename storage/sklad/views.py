from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group

from sklad.forms import RegistrationForm, YourForm
from sklad.models import Products_in_storage


from django.shortcuts import render, redirect
from django.contrib import messages




@login_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('storage')
        else:
            error_message = 'Неверные имя пользователя или пароль'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

@login_required
def storage_view(request):
    products = Products_in_storage.objects.all()
    context = {'products': products, 'user': request.user}  # Добавлено 'user' в контекст
    return render(request, 'storage.html', context)

@login_required
@user_passes_test(lambda user: user.is_superuser or user.groups.filter(name='View All Orders').exists())
def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        product = Products_in_storage(name=name, amount=amount)
        product.save()
    return redirect('storage')

@login_required
@user_passes_test(lambda user: user.is_superuser or 'View All Orders' in user.groups.values_list('name', flat=True))
def update_product(request, product_id):
    if request.method == 'POST':
        product = Products_in_storage.objects.get(id=product_id)
        product.name = request.POST['name']
        product.amount = request.POST['amount']
        product.save()
    return redirect('storage')

@login_required
@user_passes_test(lambda user: user.is_superuser or 'View All Orders' in user.groups.values_list('name', flat=True))
def delete_product(request, product_id):
    if request.method == 'POST':
        product = Products_in_storage.objects.get(id=product_id)
        product.delete()
    return redirect('storage')

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Обработка успешной регистрации
            return render(request, 'success.html')
    else:
        form = RegistrationForm()
    return render(request, 'registration_form.html', {'form': form})

from django.contrib.auth.models import User
from django.shortcuts import render

@login_required
def user_list(request):
    users = User.objects.all()
    groups = Group.objects.all()
    context = {
        'users': users,
        'groups': groups,
    }
    return render(request, 'user_list.html', context)



@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    groups = Group.objects.all()

    if request.method == 'POST':
        # Обработка отправки формы
        user.username = request.POST['username']
        user.set_password(request.POST['password'])

        # Проверяем наличие поля email в запросе
        if 'email' in request.POST:
            user.email = request.POST['email']

        user.save()
        user.groups.set(request.POST.getlist('groups'))
        return redirect('user_list')

    context = {'user': user, 'groups': groups}
    return render(request, 'user_edit.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_list')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST.get('email', '')  # Делаем поле email необязательным
        group_ids = request.POST.getlist('groups')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.groups.set(group_ids)

        return redirect('user_list')

    groups = Group.objects.all()
    context = {'groups': groups}
    return render(request, 'user_create.html', context)

