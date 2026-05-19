import uuid
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
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# =========================
# recetas
# =========================
class Receta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    description = models.TextField()
    dificultad = models.TextField()
    ingredientes = models.TextField()

    owner = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='receta'
    )

    categories = models.ManyToManyField(
        Category,
        related_name='receta'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================
# recetas guardadas
# =========================
class Favorito(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='favoritos'
    )

    products = models.ManyToManyField(
        Receta,
        through='recetaF', 
        related_name='favoritos'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lista de {self.user.username}"


# =========================
#Tabla intermedia (recetaF)
# =========================
class recetaF(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # CORRECCIÓN: Se añade la relación que faltaba hacia Favorito
    favorito = models.ForeignKey(Favorito, on_delete=models.CASCADE)
    recetas = models.ForeignKey(Receta, on_delete=models.CASCADE)

    class Meta:
        # CORRECCIÓN: Se añade la coma al final y ambos campos para que sea una tupla válida
        unique_together = ('favorito', 'recetas',)

    def __str__(self):
        return f"{self.recetas}"