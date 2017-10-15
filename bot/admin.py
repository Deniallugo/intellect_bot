from django.contrib import admin

from bot.models import Address, BotMessage, MessageButton, Company, \
    TelegramFile, TelegramUser, Question, Order, OrderType

admin.site.register(Question)
admin.site.register(Order)
admin.site.register(OrderType)


class AdresAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Address, AdresAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ['text', 'type']


admin.site.register(BotMessage, MessageAdmin)


class MessageButtonAdmin(admin.ModelAdmin):
    list_display = ['text', 'message_type']
    list_display_links = ['text']

    def message_type(self, obj):
        return obj.message.type

    message_type.admin_order_field = 'message__type'


admin.site.register(MessageButton, MessageButtonAdmin)


class AddressInline(admin.StackedInline):
    model = Address


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'uid']
    inlines = [AddressInline]

    def uid(self, obj):
        return obj.uid


admin.site.register(Company, CompanyAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']


admin.site.register(TelegramUser, UserAdmin)


class TelegramFileAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'file', 'file_type']


admin.site.register(TelegramFile, TelegramFileAdmin)


#
# class UsersCompanyAdmin(admin.ModelAdmin):
#     list_display = ['company', 'user_name', 'authorized']
#
#     def user_name(self, obj):
#         return obj.user.first_name + " " + obj.user.last_name
#
#     def company_name(self, obj):
#         return obj.company.name
#
#
# admin.site.register(UserCompany, UsersCompanyAdmin)
