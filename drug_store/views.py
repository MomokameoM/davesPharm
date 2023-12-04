from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import (
    Product,
    Provideer,
    Client,
    RemessionNote,
    Bill,
    Employee,
    SaleDetails,
)

from .forms import ProvideerForm, RemessionNoteForm, ProductForm

# Create your views here.

"""
Funcion para registrar usuarios
"""


def signup(request):
    # Si la peticion es de tipo GET se retorna el formulario de creacion de usuario
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"]
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Username already exists."},
                )
        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "Passwords did not match."},
        )


@login_required
def get_products_generics(request):
    products = Product.objects.filter(generic=True)
    return render(request, "tasks.html", {"products": products})


"""@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False
    ).order_by("-datecompleted")
    return render(request, "tasks.html", {"tasks": tasks})"""


@login_required
def create_product(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": ProductForm})
    else:
        try:
            form = Product(request.POST)
            new_product = form.save(commit=False)
            new_product.user = request.user
            new_product.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "create_task.html",
                {"form": ProductForm, "error": "Error creating product"},
            )


def home(request):
    return render(request, "home.html")


@login_required
def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Username or password is incorrect.",
                },
            )

        login(request, user)
        return redirect("tasks")


@login_required
def remision_note_detail(request, remission_note_id):
    if request.method == "GET":
        remission_note = get_object_or_404(
            RemessionNote, pk=remission_note_id, user=request.user
        )
        form = RemessionNoteForm(instance=remission_note)
        return render(
            request,
            "task_detail.html",
            {"remission_note": remission_note, "form": form},
        )
    else:
        try:
            remission_note = get_object_or_404(
                RemessionNote,
                pk=remission_note_id,
            )
            form = RemessionNoteForm(request.POST, instance=remission_note)
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "task_detail.html",
                {"task": remission_note, "form": form, "error": "Error updating task."},
            )


@login_required
def delete_task(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        product.delete()
        return redirect("tasks")
