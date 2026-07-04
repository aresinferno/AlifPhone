from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Phone, Brand, Cart, CartItem, Type, Model
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout


def new_home_page(request):
    data = Phone.objects.all()
    login_form = AuthenticationForm()
    register_form = UserCreationForm()
    return render(request, 'store/home.html', {
        'data': data,
        'login_form': login_form,
        'register_form': register_form
    })


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home_page")
    else:
        form = UserCreationForm()
    return render(request, "home.html", {"register_form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home_page")
    else:
        form = AuthenticationForm()
    return render(request, "home.html", {"login_form": form})


def logout_view(request):
    logout(request)
    return redirect("home_page")


def catalog(request):
    qs = Phone.objects.all()

    # Фильтрация по бренду
    brand_slug = request.GET.get('brand')
    part_type_slug = request.GET.get('type')
    model_slug = request.GET.get('model')
    min_price_slug = request.GET.get('min_price')
    max_price_slug = request.GET.get('max_price')

    if brand_slug:
        qs = qs.filter(brand__slug=brand_slug)
    if part_type_slug:
        qs = qs.filter(type__slug=part_type_slug)
    if model_slug:
        qs = qs.filter(model__slug=model_slug)
    if min_price_slug:
        qs = qs.filter(price__gte=min_price_slug)
    if max_price_slug:
        qs = qs.filter(price__lte=max_price_slug)

    paginator = Paginator(qs, 20)  # по 20 товаров на странице
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "store/product_list.html", {
        "products": page_obj.object_list,
        "page_obj": page_obj,
        "part_types": Type.objects.all(),
        "part_models": Model.objects.all(),
        "brands": Brand.objects.all(),
        "parts": Phone.objects.all(),

        # передаём бренды в шаблон
    })


def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Phone.objects.filter(name__icontains=query)
    return render(request, 'store/search.html', {'query': query, 'results': results})


def product_list(request):
    data = Phone.objects.all()
    return render(request, 'store/product_list.html', {'data': data})


def about_page(request):
    return render(request, 'store/about_us.html')


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Phone, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'amount': product.price})
    if not created:
        cart_item.quantity += 1
        cart_item.amount += cart_item.quantity * product.price
    else:
        pass
    cart_item.save()
    cart.update_total_amount()
    return redirect('all_product')


def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})


def delete_product(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cartitem = get_object_or_404(CartItem, id=item_id)
    if cart.user == request.user:
        cartitem.delete()
        cart.total_amount -= cartitem.amount * cartitem.quantity
        cart.save()

    return redirect('cart')

# Create your views here.
