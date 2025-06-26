from django.contrib import admin

from .models import Item, OrderItem, Order, Payment, Coupon, Refund, BillingAddress, Category, Slide, ShoeSize, ProductRating


# Register your models here.

# ShoeSize admin configuration
class ShoeSizeAdmin(admin.ModelAdmin):
    list_display = ['size_number', 'size_text']
    search_fields = ['size_number', 'size_text']

# ProductRating admin configuration


class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__title', 'user__username', 'comment']


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ref_code',
                    'ordered',
                    'status',
                    'billing_address_display',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'ref_code',
        'coupon'
    ]
    list_filter = ['user',
                   'ordered',
                   'status',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    readonly_fields= [
        'ref_code',
        'start_date',
        'ordered_date',
        'shipping_address_display',
        'billing_address_display',
        'payment',
        'coupon',
        'refund_requested',
        'refund_granted',
        'being_delivered',
        'received',
        'ordered',
        'billing_address',
        'shipping_address'
    ]
    actions = [make_refund_accepted]

    def shipping_address_display(self, obj):
        if obj.shipping_address:
            return f"{obj.shipping_address.street_address}, {obj.shipping_address.city}, {obj.shipping_address.country}"
        return "-"

    def billing_address_display(self, obj):
        if obj.billing_address:
            return f"{obj.billing_address.street_address}, {obj.billing_address.city}, {obj.billing_address.country}"
        return "-"

    shipping_address_display.short_description = "Shipping Address"
    billing_address_display.short_description = "Billing Address"


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


def copy_items(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()


copy_items.short_description = 'Copy Items'


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
    ]
    list_filter = ['title', 'category']
    search_fields = ['title', 'category']
    prepopulated_fields = {"slug": ("title",)}
    actions = [copy_items]


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'is_active'
    ]
    list_filter = ['title', 'is_active']
    search_fields = ['title', 'is_active']
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Slide)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(BillingAddress, AddressAdmin)
admin.site.register(ShoeSize, ShoeSizeAdmin)
admin.site.register(ProductRating, ProductRatingAdmin)
