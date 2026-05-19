from django.contrib import admin
# CORRECCIÓN: Importamos 'RecetaF' con las mayúsculas correctas
from .models import Usuario, Categorias, Recetas, Favorito, RecetaF


@admin.register(Usuario)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_seller')
    list_filter = ('is_seller',)


@admin.register(Categorias)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Recetas)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'dificultad', 'owner', 'created_at')
    list_filter = ('categories',)
    search_fields = ('name',)


class CartItemInline(admin.TabularInline):
    model = RecetaF  # CORRECCIÓN: Cambiado a 'RecetaF'
    extra = 1


@admin.register(Favorito)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    inlines = [CartItemInline]


@admin.register(RecetaF)  # CORRECCIÓN: Cambiado a 'RecetaF'
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('favorito', 'recetas',)