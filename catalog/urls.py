from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    #首頁
    path('', views.index, name='index'),

    #歡迎
    path('welcome/', views.welcome, name='welcome'),

    #crm
    path('crm/', views.crm, name='crm'),

    #crm
    path('crm/rfm/', views.rfm, name='rfm'),

    path('crm/rfm/actives', views.actives, name='actives'),

    path('crm/rfm/potential', views.potential, name='potential'),

    #宣傳
    path('crm/broadcast/', views.broadcast, name='broadcast'),

    path('crm/broadcast/analysis', views.analysis, name='analysis'),

    #宣傳
    path('crm/salesanalysis/all', views.all, name='all'),

    path('crm/salesanalysis/all/day', views.day, name='day'),

    path('crm/salesanalysis/all/week', views.week, name='week'),

    path('crm/salesanalysis/all/month', views.month, name='month'),


    path('crm/salesanalysis/relevant', views.relevant, name='relevant'),
    path('crm/salesanalysis/relevant/total', views.total, name='total'),
    path('crm/salesanalysis/relevant/rday', views.rday, name='rday'),
    path('crm/salesanalysis/relevant/rweek', views.rweek, name='rweek'),
    path('crm/salesanalysis/relevant/rmonth', views.rmonth, name='rmonth'),

    path('crm/salesanalysis/', views.salespredictions, name='salespredictions'),

    #宣傳
    path('crm/salesrecord/', views.salesrecord, name='salesrecord'),

    path('crm/salesrecord/customer/1', views.customer1, name='customer1'),

    path('crm/salesrecord/customer', views.customer, name='customer'),
    #om
    path('om/', views.om, name='om'),

    #om
    path('om/inventory/', views.inventory, name='inventory'),

    #om
    path('om/orders/', views.orders, name='orders'),
    #url(r'^om/orders/$', views.orders),


    #crm首頁
    #path('', views.index, name='index'),

    path('predict/', views.predict, name='predict'),
    path('posSite/', views.posSite, name='posSite'),
]
