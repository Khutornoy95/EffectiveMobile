from rest_framework import serializers
from .models import Ad, ExchangeProposal
from django.utils.translation import gettext_lazy as _


class AdSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    image_url = serializers.URLField(
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text=_('Необязательное поле')
    )

    class Meta:
        model = Ad
        fields = [
            'id', 'user', 'title', 'description',
            'image_url', 'category', 'condition', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']
        extra_kwargs = {
            'title': {'error_messages': {'blank': _('Заголовок не может быть '
                                                    'пустым')}},
            'description': {'error_messages': {'blank': _('Описание не может '
                                                          'быть пустым')}},
            'category': {'error_messages': {'blank': _('Укажите категорию')}},
            'condition': {'error_messages': {'blank': _('Укажите состояние')}},
        }


class ExchangeProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = ['id', 'ad_sender', 'ad_receiver', 'comment', 'status',
                  'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'ad_sender': {
                'error_messages': {
                    'does_not_exist': _('Объявление отправителя не найдено')
                }
            },
            'ad_receiver': {
                'error_messages': {
                    'does_not_exist': _('Объявление получателя не найдено')
                }
            },
            'comment': {
                'error_messages': {
                    'blank': _('Комментарий не может быть пустым')
                }
            }
        }

    def validate(self, data):
        if 'ad_sender' in data and 'ad_receiver' in data:
            if data['ad_sender'] == data['ad_receiver']:
                raise serializers.ValidationError(
                    {'non_field_errors': [_('Нельзя предлагать обмен на то же '
                                            'объявление')]}
                )
        return data
