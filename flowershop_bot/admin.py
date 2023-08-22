from django.contrib import admin

from .models import Bouquet, Composition, Item, Order, Quiz


class CompositionInline(admin.TabularInline):
    model = Composition
    extra = 1


class BouquetAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'height', 'width', 'occasions')
    search_fields = ['name']
    inlines = [CompositionInline]


class CompositionAdmin(admin.ModelAdmin):
    list_display = ('bouquet', 'item_name', 'quantity', 'is_free')

    def item_name(self, obj):
        return obj.item.name
    item_name.short_description = 'Item Name'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_phone', 'bouquet')
    search_fields = ['customer_name', 'customer_phone']


class QuizAdmin(admin.ModelAdmin):
    list_display = ('occasion', 'price_range')
    filter_horizontal = ('bouquets',)


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Bouquet, BouquetAdmin)
admin.site.register(Composition, CompositionAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Item)