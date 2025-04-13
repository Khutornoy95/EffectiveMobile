from django.contrib import admin
from .models import Ad, ExchangeProposal


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'condition')
    search_fields = ('title', 'description')
    list_filter = ('category', 'condition')


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad_sender', 'ad_receiver', 'status', 'comment')
    list_filter = ('status',)
    search_fields = ('comment',)