from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .carro import Carro
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import ListView, CreateView
from django.db.models import Q
from .forms import ConctactoForm, ProductoForm, CategoriaForm, CustomUserCreationForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.urls import reverse_lazy

# Create your views here.
def index(request):
    busqueda = request.POST.get("buscador")
    product_list = Productos.objects.order_by('nombre')
    page = request.GET.get('page', 1)

    if busqueda:
        product_list = Productos.objects.filter(
            Q(nombre__icontains = busqueda) |
            Q(descripcion__icontains = busqueda)
        ).distinct()
    
    try:
        paginator = Paginator(product_list, 12)
        product_list = paginator.page(page)
    except:
        raise Http404

    data = {'entity': product_list,
            'paginator': paginator
    }
    return render(request, 'index.html', data)


# Listar productos por categoria
def productoxCategoria(request, id):
    busqueda = request.POST.get("buscador")
    lista_productos = Productos.objects.filter(categoria = id)
    
    if busqueda:
        lista_productos = Productos.objects.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        ).distinct()

    data = {'entity': lista_productos}
    return render(request, 'index.html', data)


# views productos
def detalleProducto(request, id):
    product = get_object_or_404(Productos, id=id)
    otrosProductos = Productos.objects.filter(categoria=product.categoria)
    data = {
        'producto': product,
        'productosRelacionados': otrosProductos
    }
    return render(request, 'producto/detalle.html', data)

@login_required(login_url='/login')
def addProducto(request):
    data = {
        'form' : ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Registro agregado correctamente")
            return redirect(to="/listarproductos")
        else:
            data["form"] = formulario   
    return render(request, 'producto/agregar.html', data)


@login_required(login_url='/login')
def listarProductos(request):
    busqueda = request.POST.get("buscador")
    lista_productos = Productos.objects.order_by('nombre')
    page = request.GET.get('page', 1)
    if busqueda:
        lista_productos = Productos.objects.filter(
            Q(nombre__icontains = busqueda) |
            Q(descripcion__icontains = busqueda)
        ).distinct()

    try:
        paginator = Paginator(lista_productos, 6)
        lista_productos = paginator.page(page)
    except:
        raise Http404

    data = {'entity': lista_productos,
            'title': 'LISTADO DE PRODUCTOS',
            'paginator': paginator
            }
    return render(request, 'producto/listar.html', data)


@login_required(login_url='/login')
def editarProducto(request, id):
    producto = get_object_or_404(Productos, id=id)
    data = {
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Registro modificado correctamente")
            return redirect(to="/listarproductos")
        data["form"] = formulario
    return render(request, 'producto/modificar.html', data)


@login_required(login_url='/login')
def deleteProducto(request, id):
    producto = get_object_or_404(Productos, id=id)
    producto.delete()
    messages.success(request, "Registro eliminado correctamente")
    return redirect(to="/listarproductos")

def nosotros(request):
    return render(request, 'nosotros.html')

def garantia(request):
    return render(request, 'garantia.html')

def devoluciones(request):
    return render(request, 'devoluciones.html')


# Views categorias
@login_required(login_url='/login')
def listCategorias(request):
    lista_categorias = Categorias.objects.all().order_by('nombre')
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(lista_categorias, 6)
        lista_categorias = paginator.page(page)
    except:
        raise Http404

    data = {'entity': lista_categorias,
            'title': 'LISTADO DE CATEGORIAS',
            'paginator': paginator
            }

    return render(request,'categorias.html', data)


@login_required(login_url='/login')
def addCategoria(request):
    data = {
        'form': CategoriaForm()
    }
    if request.method == 'POST':
        formulario = CategoriaForm(data=request.POST)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Registro agregado correctamente")
            return redirect(to="/categorias")
        else:
            data["form"] = formulario
    return render(request, 'categoria/agregar.html', data)


@login_required(login_url='/login')
def modificarCategoria(request, id):
    categoria = get_object_or_404(Categorias, id=id)

    data = {
        'form': CategoriaForm(instance=categoria)
    }
    if request.method == 'POST':
        formulario = CategoriaForm(data=request.POST, instance=categoria)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Registro modificado correctamente")
            return redirect(to="/categorias")
        else:
            data["form"] = formulario

    return render(request, 'categoria/modificar.html', data)


@login_required(login_url='/login')
def deleteCategoria(request, id):
    categoria = get_object_or_404(Categorias, id=id)
    categoria.delete()
    messages.success(request, "Registro eliminado correctamente")
    return redirect(to="/categorias")

def contacto(request):
    data = {
        'form': ConctactoForm()
    }

    if request.method == 'POST':
        formulario = ConctactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Gracias por su mensaje")
        else:
            data["form"] = formulario
    return render(request, 'contacto.html', data)


# def registrar(request):
#     data = {
#         'form': CustomUserCreationForm()
#     }

#     if request.method == 'POST':
#         formulario = CustomUserCreationForm(data=request.POST)
#         if formulario.is_valid():
#             formulario.save()
#             user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
#             login(request, user)
#             messages.success(request, 'Usuario registrado correctamente')
#             return redirect('/')
#         else:
#             data['form'] = formulario
    
#     return render(request, 'auth/registrar.html', data)

def registrar(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
       
        if formulario.is_valid():
            user = formulario.save(commit=False) #Tengo dudas con el user podria ser usuario
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = formulario.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            # return HttpResponse('Por favor confirma tu direccion de correo electronico para completar el registro')
            messages.success(request, ('Por favor, confirma tu email para completar el registro.'))
            return redirect('/')
        else:
            data['form'] = formulario
    
    return render(request, 'auth/registrar.html', data)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Gracias por tu confirmacion de email')
    else:
        return HttpResponse('El enlace de activacion es invalido!')

# Acciones carrito
def viewcart(request):
    return render(request, 'carrito/cart.html', {'carro': request.session['carro']})

def agregar_producto(request, producto_id):
    carro=Carro(request)
    producto=Productos.objects.get(id=producto_id)
    carro.agregar(producto=producto)
    return redirect(to="/viewcart")

def eliminar_producto(request, producto_id):
    carro=Carro(request)
    producto=Productos.objects.get(id=producto_id)
    carro.eliminar(producto=producto)
    return redirect(to="/viewcart")


def restar_producto(request, producto_id):
    carro = Carro(request)
    producto = Productos.objects.get(id=producto_id)
    carro.restar(producto=producto)
    return redirect(to="/viewcart")

def cleancart(request):
    carro=Carro(request)
    carro.limpiar_carro()
    return redirect(to="/viewcart")


def procesar_compra(request):
    messages.success(request, 'Gracias por su Compra!!')
    carro = Carro(request)
    carro.limpiar_carro()
    return redirect('/')
