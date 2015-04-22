from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.models import User
from reservation.models import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken import views
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class ReservationSerializer(serializers.HyperlinkedModelSerializer):
	flight_id = serializers.IntegerField()
	flight_class_id = serializers.IntegerField()
	price = serializers.IntegerField()

	class Meta:
		model = Reservation
		fields = ('pk', 'flight_id', 'flight_class_id', 'price')


class FlightClassSerializer(serializers.Serializer):
	pk = serializers.IntegerField()
	text = serializers.StringRelatedField()
	available_seats = serializers.IntegerField()
	price = serializers.IntegerField()

	class Meta:
		model = FlightClass
		fields = ('pk', 'text', 'available_seats', 'price')


class FlightSerializer(serializers.Serializer):
	pk = serializers.IntegerField()
	departure = serializers.CharField(max_length=200)
	arrival = serializers.CharField(max_length=200)

	total_available_seats = serializers.IntegerField()
	classes = FlightClassSerializer(many=True)

	class Meta:
		model = Flight
		fields = ('departure', 'arrival', 'total_available_seats', 'classes')


class FlightSerializerList(serializers.Serializer):
	pk = serializers.IntegerField()
	departure = serializers.CharField(max_length=200)
	arrival = serializers.CharField(max_length=200)

	total_available_seats = serializers.IntegerField()

	class Meta:
		model = Flight
		fields = ('departure', 'arrival', 'total_available_seats')


class FlightViewSet(viewsets.ModelViewSet):
	queryset = Flight.objects.all()
	serializer_class = FlightSerializer

	def retrieve(self, request, pk=None):
		queryset = Flight.objects.all()
		flight = get_object_or_404(queryset, pk=pk)
		serializer = FlightSerializer(flight)
		return Response(serializer.data)

	def list(self, request):
		queryset = Flight.objects.all()
		serializer = FlightSerializerList(queryset, many=True)
		return Response(serializer.data)


class ReservationViewSet(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer

	def get_queryset(self):
		print("lol")
		if self.request.user.is_authenticated():
			username = self.request.user.username
		user = User.objects.get(login=username)
		print('lol')
		return Reservation.objects.all().filter(user=user)	


class AvailableFlightsViewSet(viewsets.ModelViewSet):
	serializer_class = FlightSerializerList
	queryset = Flight.objects.all()

	def get_queryset(self):
		queryset = [f for f in Flight.objects.all() if len(f.available_seats()) > 0]
		return queryset

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def deleteReservationViewSet(request, id):
	try:
		reservation = Reservation.objects.get(pk=id)
		iden = reservation.pk
		reservation.delete()
		return HttpResponse('{\n   \'status\' : \'OK\''
						+ ',\n   \'message\' : \'réservation ' + reservation.__str__() + '\''
						+ ',\n   \'id\' : \'' + repr(iden) + '\''
						+ '\n}')
	except:
		return HttpResponse('{\n   \'status\' : \'Fail\''
						+ ',\n   \'message\' : \'la réservation n existe pas\''
						+ ',\n   \'id\' : \'\''
						+ '\n}')

def createReservation(flight_id, flight_class_id, user):
	fail = False
	identifier = 0

	if not fail:
		try:
			wanted_flight = Flight.objects.get(pk=flight_id)
		except:
			status = 'Fail'
			fail = True
			message = 'Ce vol n existe pas'

	if not fail:
		try:
			flight_class = FlightClass.objects.get(pk=flight_class_id)
		except:
			status = 'Fail'
			fail = True
			message = 'Cette classe n est pas disponible sur ce vol'

	if not fail:
		if not flight_class.have_seats_available():
			fail = True
			status = 'Fail'
			message = 'Il n y a plus de place dans cette classe'

	if not fail:
		try:
			reservation = Reservation(flight=wanted_flight, flight_class=flight_class, user=user)
			reservation.save()
			identifier = reservation.pk
			status = 'OK'
			message = 'Réservation effectuée :' + reservation.__str__()
		except:
			message = 'Erreur lors de la création de la reservation'
			status = 'Fail'

	return HttpResponse('{\n   \'status\' : \'' + status + '\''
						+ ',\n   \'message\' : \'' + message + '\''
						+ ',\n   \'id\' : \'' + repr(identifier) + '\''
						+ '\n}')

@api_view(['POST', 'PUT'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def makeReservationView(request):
	serializer_class = ReservationSerializer	
	permission_classes = (IsAuthenticated,)

	status = 'Fail'
	identifier = ''
	message = ''
	fail = False
	flight_id = 0
	flight_class_text = ""
	user = None

	if request.method != 'POST':
		return HttpResponse("POST only")

	if request.user.is_authenticated():
		username = request.user.username
		user = User.objects.get(login=username)
	else:
		message = 'vous n êtes pas identifié'
		status = 'Fail'
		fail = True

	try:
		flight_id = request.POST["flight_id"]
		flight_class_text = request.POST["flight_class"]
	except:
		status = 'Fail'
		message = 'données entrées incorrectes'
		fail = True

	if not fail:
		return createReservation(flight_id, flight_class_text, user)
	else:
		return HttpResponse('{\n   \'status\' : \'Fail\''
						+ ',\n   \'message\' : \'Données entrées incorrectes\''
						+ ',\n   \'id\' : \'\''
						+ '\n}')


router = routers.DefaultRouter()
router.register(r'flights', FlightViewSet, 'p')
router.register(r'available_flights', AvailableFlightsViewSet, 'p')
router.register(r'reservations', ReservationViewSet, 'p')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/?', views.obtain_auth_token),
    url(r'^reservation/(?P<id>[0-9]+)/cancel/?', deleteReservationViewSet),
    url(r'^reservation/create/?', makeReservationView),
]
