from django.contrib import admin
from .models import Trains,Station,RouteStation,Route,Reservation,Payment
# Register your models here.
admin.site.register(Trains)
admin.site.register(Station)
admin.site.register(Route)
admin.site.register(RouteStation)
admin.site.register(Reservation)
admin.site.register(Payment)