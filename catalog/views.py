from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Country, Mountain, Route, Stop, Org, Trip
from .serializers import CountrySerializer, MountainSerializer, RouteSerializer, StopSerializer, OrgSerializer, TripSerializer
from django.db.models.deletion import ProtectedError


class CountryList(APIView):
    def get(self, request):
        country = Country.objects.all()
        serializer = CountrySerializer(country, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({"errors": serializer.errors},status=400)
    
class CountryDetail(APIView):
    def get(self, request, id):
        try:
            country =Country.objects.get(id=id)
        except Country.DoesNotExist:
            return Response({"errors": "Країну не знайдено"}, status=404)
        serializer = CountrySerializer(country)

        return Response(serializer.data)
    
    def patch(self, request, id):
        try:
            country =Country.objects.get(id=id)
        except Country.DoesNotExist:
            return Response({"errors": "Країну не знайдено"}, status=404)
        serializer = CountrySerializer(country, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors},status=400)

    def delete(self, request, id):
        try:
            country = Country.objects.get(id=id)
        except Country.DoesNotExist:
            return Response({"errors": "Країну не знайдено"}, status=404)
        try:
            country.delete()
        except ProtectedError:
            return Response({"errors": "Неможливо видалити країну, поки до неї прив’язані гори. Спочатку видаліть або перенесіть їх."}, status = 409)
        
        return Response(status=204) 


class MountainList(APIView):
    def get(self, request):
        mountain = Mountain.objects.all()
        serializer = MountainSerializer(mountain, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = MountainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({"errors": serializer.errors},status=400)
    
class MountainDetail(APIView):
    def get(self, request, id):
        try:
            mountain =Mountain.objects.get(id=id)
        except Mountain.DoesNotExist:
            return Response({"errors": "Гору не знайдено"}, status=404)
        serializer = MountainSerializer(mountain)

        return Response(serializer.data)
    
    def patch(self, request, id):
        try:
            mountain =Mountain.objects.get(id=id)
        except Mountain.DoesNotExist:
            return Response({"errors": "Гору не знайдено"}, status=404)
        serializer = MountainSerializer(mountain, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors},status=400)

    def delete(self, request, id):
        try:
            mountain = Mountain.objects.get(id=id)
        except Mountain.DoesNotExist:
            return Response({"errors": "Гору не знайдено"}, status=404)
        try:
            mountain.delete()
        except ProtectedError:
            return Response({"errors": "Неможливо видалити гору, поки до неї прив’язані маршрути. Спочатку видаліть або перенесіть їх."}, status = 409)
        
        return Response(status=204) 
        

class RouteList(APIView):
    def get(self, request):
        route = Route.objects.all()
        serializer = RouteSerializer(route, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RouteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({"errors": serializer.errors},status=400)


class RouteDetail(APIView):
    def get(self, request, id):
        try:
            route =Route.objects.get(id=id)
        except Route.DoesNotExist:
            return Response({"errors": "Шлях не знайдено"}, status=404)
        serializer = RouteSerializer(route)

        return Response(serializer.data)
    
    def patch(self, request, id):
        try:
            route =Route.objects.get(id=id)
        except Route.DoesNotExist:
            return Response({"errors": "Шлях не знайдено"}, status=404)
        serializer = RouteSerializer(route, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors},status=400)

    def delete(self, request, id):
        try:
            route = Route.objects.get(id=id)
        except Route.DoesNotExist:
            return Response({"errors": "Шлях не знайдено"}, status=404)
        try:
            route.delete()
        except ProtectedError:
            return Response({"errors": "Неможливо видалити маршрут, поки до нього прив’язані сходження."},status=409)

        return Response(status=204)

class StopList(APIView):
    def get(self, request, route_id):
        try:
            Route.objects.get(id=route_id)
        except Route.DoesNotExist:
            return Response({"errors": "Маршрут не знайдено"}, status=404)
        stops = Stop.objects.filter(route_id=route_id).order_by("position")
        serializer = StopSerializer(stops, many=True)
        return Response(serializer.data)

    def post(self, request, route_id):
        try:
           route = Route.objects.get(id=route_id)
        except Route.DoesNotExist:
            return Response({"errors": "Маршрут не знайдено"}, status=404)
        serializer = StopSerializer(data=request.data)
        if serializer.is_valid():
            position = serializer.validated_data["position"]
            
            if Stop.objects.filter(route=route, position=position).exists():
                 return Response({"errors": "Зупинка з таким номером уже існує в цьому маршруті."},status=409)

            serializer.save(route=route)
            return Response(serializer.data, status=201)
        else:
            return Response({"errors": serializer.errors},status=400)


class StopDetail(APIView):
    def get(self, request, route_id, id):
        try:
            stop = Stop.objects.get(id=id, route_id=route_id)
        except Stop.DoesNotExist:
            return Response({"errors": "Зупинку не знайдено"}, status=404)
        serializer = StopSerializer(stop)
        return Response(serializer.data)
    
    def patch(self, request, route_id, id):
        try:
            stop = Stop.objects.get(id=id, route_id=route_id)
        except Stop.DoesNotExist:
            return Response({"errors": "Зупинку не знайдено"}, status=404)
        serializer = StopSerializer(stop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors},status=400)

    def delete(self, request, route_id, id):
        try:
            stop = Stop.objects.get(id=id, route_id=route_id)
        except Stop.DoesNotExist:
            return Response({"errors": "Зупинку не знайдено"}, status=404)
        stop.delete()
        return Response(status=204)

class OrgList(APIView):
    def get(self, request):
        org = Org.objects.all()
        serializer = OrgSerializer(org, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrgSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({"errors": serializer.errors},status=400)

class OrgDetail(APIView):
    def get(self, request, id):
        try:
            org = Org.objects.get(id=id)
        except Org.DoesNotExist:
            return Response({"errors": "Організатора не знайдено"}, status=404)
        serializer = OrgSerializer(org)
        return Response(serializer.data)

    def patch(self, request, id):
        try:
            org = Org.objects.get(id=id)
        except Org.DoesNotExist:
            return Response({"errors": "Організатора не знайдено"}, status=404)
        serializer = OrgSerializer(org, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors},status=400)

    def delete(self, request, id):
        try:
            org = Org.objects.get(id=id)
        except Org.DoesNotExist:
            return Response({"errors": "Організатора не знайдено"}, status=404)
        try:
            org.delete()
        except ProtectedError:
            return Response({"errors": "Неможливо видалити організатора, поки до нього прив’язані сходження."},status=409)

        return Response(status=204)

class TripList(APIView):
    def get(self, request):
        trip = Trip.objects.all()
        serializer = TripSerializer(trip, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if data["end_date"] < data["start_date"]:
                return Response({"errors": "Дата завершення не може бути раніше дати початку."},status=400)
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({"errors": serializer.errors},status=400)

class TripDetail(APIView):
    def get(self, request, id):
        try:
            trip = Trip.objects.get(id=id)
        except Trip.DoesNotExist:
            return Response({"errors": "Сходження не знайдено"}, status=404)
        serializer = TripSerializer(trip)
        return Response(serializer.data)

    def patch(self, request, id):
        try:
            trip = Trip.objects.get(id=id)
        except Trip.DoesNotExist:
            return Response({"errors": "Сходження не знайдено"}, status=404)
        serializer = TripSerializer(trip, data=request.data, partial=True)
        if serializer.is_valid():
            data = serializer.validated_data
            start_date = data.get("start_date", trip.start_date)
            end_date = data.get("end_date", trip.end_date)

            if end_date < start_date:
                return Response({"errors": "Дата завершення не може бути раніше дати початку."},status=400)
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)

    def delete(self, request, id):
        try:
            trip = Trip.objects.get(id=id)
        except Trip.DoesNotExist:
            return Response({"errors": "Сходження не знайдено"}, status=404)
        trip.delete()
        return Response(status=204)    
