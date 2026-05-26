from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from .forms import ProductForm
from .forms import RegisterForm
from .models import Recetas
from .models import Favorito, RecetaF, Categorias

def home(request):

    query = request.GET.get('q')
    category_id = request.GET.get('category')

    products = Recetas.objects.select_related(
        'owner'
    ).prefetch_related(
        'categories'
    ).all()

    # =========================
    # 🔎 Busqueda
    # =========================
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # =========================
    # 🏷️ Filtro categoria
    # =========================
    if category_id:
        products = products.filter(
            categories__id=category_id
        )

    # =========================
    # 📄 Paginacion
    # =========================
    paginator = Paginator(products, 6)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    categories = Categorias.objects.all()

    return render(request, 'recetas_app/home.html', {
        'page_obj': page_obj,
        'categories': categories,
        'products': products,
    })


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'recetas_app/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'recetas_app/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

# =========================
# 📊 Dashboard
# =========================
@login_required
def dashboard(request):
    if not request.user.is_seller:
        return HttpResponseForbidden("No tienes permisos")

    products = Recetas.objects.filter(owner=request.user)

    return render(request, 'recetas_app/dashboard.html', {
        'products': products
    })

# =========================
# ➕ Crear producto
# =========================
@login_required
def product_create(request):
    if not request.user.is_seller:
        return HttpResponseForbidden("Solo vendedores")

    # Importante: Añadimos request.FILES
    form = ProductForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        product = form.save(commit=False)
        product.owner = request.user
        product.save()
        form.save_m2m()
        return redirect('dashboard')

    return render(request, 'recetas_app/product_form.html', {'form': form})


# =========================
# ✏️ Editar producto
# =========================
@login_required
def product_update(request, pk):
    product = get_object_or_404(Recetas, pk=pk)

    if product.owner != request.user:
        return HttpResponseForbidden("No puedes editar este producto")

    #form = ProductForm(request.POST or None, instance=product)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if form.is_valid():
        form.save()
        return redirect('dashboard')

    return render(request, 'recetas_app/product_form.html', {'form': form})


# =========================
# 🗑️ Eliminar producto
# =========================
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Recetas, pk=pk)

    if product.owner != request.user:
        return HttpResponseForbidden("No puedes eliminar este producto")

    if request.method == 'POST':
        product.delete()
        return redirect('dashboard')

    return render(request, 'recetas_app/product_confirm_delete.html', {'product': product})


# =========================
# 🛒 Ver carrito
# =========================
@login_required
def cart_detail(request):
    cart, created = Favorito.objects.get_or_create(
        user=request.user
    )

    return render(request, 'recetas_app/cart_detail.html', {
        'cart': cart
    })


# =========================
# ➕ Agregar producto
# =========================
@login_required
def add_to_cart(request, product_id):
    cart, created = Favorito.objects.get_or_create(
            user=request.user
        )

    product = get_object_or_404(Recetas, id=product_id)

    cart_item, created = RecetaF.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')


# =========================
# ❌ Eliminar item
# =========================
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        RecetaF,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    return redirect('cart_detail')


# =========================
# 🔄 Actualizar cantidad
# =========================
@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(
        RecetaF,
        id=item_id,
        cart__user=request.user
    )

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))

        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()

    return redirect('cart_detail')