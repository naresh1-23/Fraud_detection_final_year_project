from .models import UserStatistics
from django.contrib import admin
from .models import CustomUser, Product, Bidding, BiddingWinner, UserStatistics
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser  # Specify the model
    list_display = ('email', 'role', 'is_active', 'is_staff', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('created_at', 'updated_at')

    # Override fieldsets to customize the fields displayed
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('role', 'is_active', 'is_staff')}),
        ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )

    # Hide the default fields that don't exist in CustomUser
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(CustomUser, CustomUserAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'starting_price', 'bidding_ending_date', 'is_sold')
    list_filter = ('is_sold', 'seller')
    search_fields = ('name', 'seller__email')
    ordering = ('bidding_ending_date',)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Product, ProductAdmin)


class BiddingAdmin(admin.ModelAdmin):
    list_display = ('bidder', 'product', 'price', 'created_at')
    list_filter = ('bidder', 'product')
    search_fields = ('bidder__email', 'product__name')
    ordering = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Bidding, BiddingAdmin)


class BiddingWinnerAdmin(admin.ModelAdmin):
    list_display = ('bidding', 'final_price', 'winning_date', 'created_at')
    list_filter = ('winning_date',)
    search_fields = ('bidding__bidder__email', 'bidding__product__name')
    ordering = ('winning_date',)
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(BiddingWinner, BiddingWinnerAdmin)


@admin.register(UserStatistics)
class UserStatisticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_item_listed', 'total_item_sold')
    search_fields = ('user__email',)
    list_filter = ('total_item_listed', 'total_item_sold')
    ordering = ('user',)

    # This method makes it easier to display the user email directly in the admin
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
