import uuid  # <-- CORREGIDO: Cambiado 'MODES import uuid' por 'import uuid'
from django.db import models
from django.contrib.auth.models import AbstractUser

# =========================
# Usuario 
# =========================
class Usuario(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# =========================
# Categoría
# =========================
class Categorias(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# =========================
# Recetas
# =========================
class Recetas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    description = models.TextField()
    dificultad = models.TextField()
    ingredientes = models.TextField()
    image = models.ImageField(upload_to='upload/', blank=True, null=True)

    owner = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='receta'
    )

    categories = models.ManyToManyField(
        Categorias,
        related_name='receta'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================
# Recetas Guardadas
# =========================
class Favorito(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='favoritos'
    )

    # CORRECCIÓN: Apunta exactamente a 'RecetaF'
    products = models.ManyToManyField(
        Recetas,
        through='recetas_app.RecetaF', 
        related_name='favoritos'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lista de {self.user.username}"


# =========================
# Tabla Intermedia
# =========================
# CORRECCIÓN: Cambiado 'recetasf' a 'RecetaF' para que coincida con el through
class RecetaF(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    favorito = models.ForeignKey(Favorito, on_delete=models.CASCADE)
    recetas = models.ForeignKey(Recetas, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('favorito', 'recetas',)

    def __str__(self):
        return f"{self.recetas}"