from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from main.forms import CustomUserCreationForm
from main.models import Application, Category
from main.forms import ApplicationForm
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    completed_applications = Application.objects.filter(
        status='completed'
    ).order_by('-created_at')[:4]
    in_progress_count = Application.objects.filter(
        status='in_progress'
    ).count()

    return render(request, 'main/index.html', {
        'completed_applications': completed_applications,
        'in_progress_count': in_progress_count,
    })


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('home')


def profile_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Для доступа к этой странице необходимо авторизоваться.')
        return redirect('login')

    return render(request, 'main/profile.html', {'user': request.user})


def create_application_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Для создания заявки необходимо авторизоваться.')
        return redirect('login')

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('my_applications')
    else:
        form = ApplicationForm()

    return render(request, 'main/create_application.html', {'form': form})


def my_applications_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Для просмотра заявок необходимо авторизоваться.')
        return redirect('login')
    applications = Application.objects.filter(user=request.user)
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)

    return render(request, 'main/my_applications.html', {
        'applications': applications,
        'status_filter': status_filter
    })


def delete_application_view(request, application_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Для удаления заявки необходимо авторизоваться.')
        return redirect('login')

    try:
        application = Application.objects.get(id=application_id, user=request.user)
        if application.status != 'new':
            messages.error(request, 'Можно удалять только заявки со статусом "Новая"')
            return redirect('my_applications')
        application.delete()
        messages.success(request, 'Заявка успешно удалена')

    except Application.DoesNotExist:
        messages.error(request, 'Заявка не найдена')

    return redirect('my_applications')


@staff_member_required
def superadmin(request):
    if not request.user.is_staff:
        messages.error(request, 'Доступ запрещен')
        return redirect('home')
    applications = Application.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    return render(request, 'main/superadmin.html', {
        'applications': applications,
        'categories': categories,
    })


@staff_member_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            messages.success(request, f'Категория "{name}" добавлена')
    return redirect('superadmin')


@staff_member_required
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category_name = category.name
        category.delete()
        messages.success(request, f'Категория "{category_name}" удалена')
    except Category.DoesNotExist:
        messages.error(request, 'Категория не найдена')
    return redirect('superadmin')


@staff_member_required
def change_application_status(request, app_id, new_status):
    try:
        application = Application.objects.get(id=app_id)

        if application.status != 'new':
            messages.error(request, 'Нельзя изменить статус заявки, которая уже в работе или выполнена')
            return redirect('superadmin')

        if new_status == 'in_progress':
            comment = request.POST.get('comment', '').strip()
            if not comment:
                messages.error(request, 'Для принятия в работу нужен комментарий')
                return redirect('superadmin')

            application.status = 'in_progress'
            application.admin_comment = comment
            application.save()
            messages.success(request, 'Заявка принята в работу')

        elif new_status == 'completed':
            design_photo = request.FILES.get('design_photo')
            if not design_photo:
                messages.error(request, 'Для выполнения заявки нужно загрузить фото дизайна')
                return redirect('superadmin')

            application.status = 'completed'
            application.design_photo = design_photo
            application.save()
            messages.success(request, 'Заявка отмечена как выполненная')

        else:
            messages.error(request, 'Некорректный статус')

    except Application.DoesNotExist:
        messages.error(request, 'Заявка не найдена')

    return redirect('superadmin')