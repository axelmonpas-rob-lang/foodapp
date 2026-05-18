from django.contrib import admin
from .models import Usuario, Category, Receta, Favorito, recetaF


@admin.register(Usuario)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_seller')
    list_filter = ('is_seller',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Receta)
class ProductAdmin(admin.ModelAdmin):
    # CORRECCIÓN: Solo campos reales de Receta (eliminados price y stock)
    list_display = ('name', 'dificultad', 'owner', 'created_at')
    list_filter = ('categories',)
    search_fields = ('name',)


class CartItemInline(admin.TabularInline):
    model = recetaF
    extra = 1


@admin.register(Favorito)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    inlines = [CartItemInline]


@admin.register(recetaF)
class CartItemAdmin(admin.ModelAdmin):
    # CORRECCIÓN: Usando los nombres exactos de los campos en recetaF
    list_display = ('favoritos', 'recetas')