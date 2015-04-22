from django.contrib import admin

from .models import User, Flight, FlightClass, Reservation


class FlightClassInline(admin.TabularInline):
	model = FlightClass
	extra = 3

class ReservationClassInlineReadOnly(admin.TabularInline):
	model = Reservation
	extra = 0
	readonly_fields = ['flight', 'flight_class', 'user']


class ReservationClassInline(admin.TabularInline):
	model = Reservation
	extra = 1


class UserAdmin(admin.ModelAdmin):
	fields = ['login', 'password']
	list_display = ('login', 'password')
	inlines = [ReservationClassInlineReadOnly]


class FlightAdmin(admin.ModelAdmin):
	list_display = ['departure', 'arrival', 'available_seats']
	inlines = [FlightClassInline, ReservationClassInline]



admin.site.register(User, UserAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(FlightClass)
admin.site.register(Reservation)