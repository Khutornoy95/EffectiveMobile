from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal


class BaseTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password123'
        )

        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Лучшая книга по Python',
            description='Python для чайников',
            category='books',
            condition='new'
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Велосипед',
            description='Горный велосипед. 24 скорости. Не бит, не крашен.',
            category='sport',
            condition='used'
        )

        self.client1 = APIClient()
        self.client1.force_authenticate(user=self.user1)

        self.client2 = APIClient()
        self.client2.force_authenticate(user=self.user2)


class AdTests(BaseTestCase):
    def test_create_ad(self):
        # Создание объявления
        url = reverse('ad-list')
        data = {
            'title': 'Новая книга',
            'description': 'Описание',
            'category': 'books',
            'condition': 'new'
        }
        response = self.client1.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ad.objects.count(), 3)
        self.assertEqual(Ad.objects.latest('id').user, self.user1)

    def test_edit_own_ad(self):
        # Редактирование объявления
        url = reverse('ad-detail', args=[self.ad1.id])
        data = {'title': 'Обновленное название'}
        response = self.client1.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.title, 'Обновленное название')

    def test_edit_other_user_ad(self):
        # Редактирование чужого объявления
        url = reverse('ad-detail', args=[self.ad2.id])
        data = {'title': 'Попытка изменить'}
        response = self.client1.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_ad(self):
        # Удаление объявления
        url = reverse('ad-detail', args=[self.ad1.id])
        response = self.client1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ad.objects.count(), 1)

    def test_search_ads(self):
        # Поиск
        url = reverse('ad-list')
        response = self.client1.get(url, {'search': 'книга'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.ad1.id)

    def test_filter_ads(self):
        # Фильтр
        url = reverse('ad-list')
        response = self.client1.get(url, {'category': 'books'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class ExchangeProposalTests(BaseTestCase):
    # Создание предложения
    def test_create_proposal(self):
        url = reverse('proposal-create')
        data = {
            'ad_sender': self.ad1.id,
            'ad_receiver': self.ad2.id,
            'comment': 'Предлагаю обмен'
        }
        response = self.client1.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExchangeProposal.objects.count(), 1)
        self.assertEqual(
            ExchangeProposal.objects.first().status,
            'pending'
        )

    def test_cant_create_proposal_with_own_ad_as_receiver(self):
        # Предложение обмена на своё объявление
        url = reverse('proposal-create')
        data = {
            'ad_sender': self.ad1.id,
            'ad_receiver': self.ad1.id,
            'comment': 'Попытка самообмена'
        }
        response = self.client1.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_proposal_status(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Тест',
            status='pending'
        )
        url = reverse('proposal-update', args=[proposal.id])
        data = {'status': 'accepted'}

        # Только получатель может менять статус
        response = self.client2.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Отправитель не может менять статус
        response = self.client1.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_proposal_lists(self):
        proposal1 = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Тест 1',
            status='pending'
        )
        proposal2 = ExchangeProposal.objects.create(
            ad_sender=self.ad2,
            ad_receiver=self.ad1,
            comment='Тест 2',
            status='pending'
        )

        user3 = User.objects.create_user(username='user3', password='pass')
        ad3 = Ad.objects.create(user=user3, title='Чужое', description='ррр',
                                category='other', condition='new')
        ExchangeProposal.objects.create(
            ad_sender=ad3,
            ad_receiver=self.ad2,
            comment='Чужое предложение',
            status='pending'
        )

        url = reverse('proposal-list')

        # Проверка отправленных предложений user1
        response = self.client1.get(url, {'ad_sender': self.ad1.id})
        results = response.data[
            'results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], proposal1.id)

        # Проверка полученных предложений user1
        response = self.client1.get(url, {'ad_receiver': self.ad1.id})
        results = response.data[
            'results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], proposal2.id)
