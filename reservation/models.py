from django.db import models

class User(models.Model):
	login = models.CharField(max_length=200)
	password = models.CharField(max_length=200)

	def __str__(self):
		return self.login


class Flight(models.Model):
	departure = models.CharField(max_length=200)
	arrival = models.CharField(max_length=200)
	date = models.DateTimeField('date decollage')

	def total_available_seats(self):
		classes_for_this_flight = [x for x in self.flightclass_set.all()
				if len(x.reservation_set.all()) < x.seats_amount]
		return sum([c.seats_amount - c.reservation_set.count()
				for c in classes_for_this_flight])

	def available_seats(self):
		classes_for_this_flight = [x for x in self.flightclass_set.all()
				if len(x.reservation_set.all()) < x.seats_amount]
		return [c.text + ': ' + repr(c.seats_amount - c.reservation_set.count())
				for c in classes_for_this_flight]

	def available_classes(self):
		return [x for x in self.flightclass_set.all()
				 if len(x.reservation_set.all()) < x.seats_amount]

	def classes(self):
		return self.flightclass_set.all()

	def __str__(self):
		return self.departure + ' vers ' + self.arrival + ' le '\
				+ repr(self.date.year) + '-' + repr(self.date.month) + '-' + repr(self.date.day)


class FlightClass(models.Model):
	text = models.CharField(max_length=200)
	seats_amount = models.IntegerField()
	price = models.IntegerField()
	flight = models.ForeignKey(Flight)

	def have_seats_available(self):
		return (self.reservation_set.count() < self.seats_amount)

	def available_seats(self):
		return self.seats_amount - self.reservation_set.count()

	def __str__(self):
		return self.text


class Reservation(models.Model):
	flight = models.ForeignKey(Flight)
	flight_class = models.ForeignKey(FlightClass)
	user = models.ForeignKey(User)


	def price(self):
		return self.flight_class.price

	def flight_id(self):
		return self.flight.pk

	def flight_class_if(self):
		return self.flight_class.pk

	def __str__(self):
		return 'de ' + self.user.login + ' pour le vol  '\
			+ self.flight.__str__() + ' dans la classe '\
			+ self.flight_class.__str__()

