import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# =========================
# 👤 Usuario 
# =========================
class Usuario(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# =========================
# 🏷️ Categoría "´pais dificultad etc."
# =========================
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# =========================
# 📦 Producto "recetas"
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
    )  # 1:N

    categories = models.ManyToManyField(
        Category,
        related_name='receta'
    )  # N:M

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================
# 🛒 Favoritos "recetas guardadas"
# =========================
class Favorito(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='favoritos'
    )  # 1:N

    products = models.ManyToManyField(
        Receta,
        through='guardados',
        related_name='favoritos'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"favoritos {self.id} - {self.user}"


# =========================
# 🧾 tabla de recetas (tabla de favoritos)
# =========================
class recetaF(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    favoritos = models.ForeignKey(Favorito, on_delete=models.CASCADE)
    recetas = models.ForeignKey(Receta, on_delete=models.CASCADE)



    class Meta:
        unique_together = ('favoritos', 'recetas')

    def __str__(self):
        return f"{self.recetas} "
    