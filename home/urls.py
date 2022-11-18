from django.contrib import admin
from django.urls import path,include
import features
from . import views
app_name='home'
urlpatterns = [
    path('',views.home,name="hom" ),
    path('logout/',views.logout ),
    path('search/',features.views.search),
    path('search/trains',features.views.getTrains),
    path('schedule/',features.views.schedule),
    path('schedule/trains',features.views.getTinfo),
    path('addR/',features.views.addR,name="addR"),
    path('addST/',features.views.addST),
    path('addT/',features.views.addT),
    path('addRT/',features.views.addRT),
    path('search/search/trains/cva/', features.views.cva),
    path('search/book1/', features.views.book1),
    path('search/book1/book/', features.views.book),
    path('cancel/',features.views.cancel),
    path('cancel/cancel/cn/',features.views.cn),
    path('pnr/',features.views.pnr,name="pnr"),
    ]