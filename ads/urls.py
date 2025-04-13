from django.urls import path
from . import views

urlpatterns = [

    path('ads/', views.AdListCreateView.as_view(), name='ad-list'),
    path('ads/<int:pk>/', views.AdDetailView.as_view(), name='ad-detail'),
    path('proposals/', views.ExchangeProposalCreateView.as_view(),
         name='proposal-create'),
    path('proposals/list/', views.ExchangeProposalListView.as_view(),
         name='proposal-list'),
    path('proposals/<int:pk>/', views.ExchangeProposalUpdateView.as_view(),
         name='proposal-update'),
]
