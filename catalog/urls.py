from django.urls import path
from .views import CountryList, CountryDetail, MountainDetail, MountainList, RouteList, RouteDetail, StopList, StopDetail, OrgList, OrgDetail, TripList, TripDetail

urlpatterns = [
    path("countries", CountryList.as_view()),
    path("countries/<int:id>", CountryDetail.as_view()),
    path("mountains", MountainList.as_view()),
    path("mountains/<int:id>", MountainDetail.as_view()),
    path("routes", RouteList.as_view()),
    path("routes/<int:id>", RouteDetail.as_view()),
    path("routes/<int:route_id>/stops", StopList.as_view()),
    path("routes/<int:route_id>/stops/<int:id>", StopDetail.as_view()),
    path("organizers", OrgList.as_view()),
    path("organizers/<int:id>", OrgDetail.as_view()),
    path("trips", TripList.as_view()),
    path("trips/<int:id>", TripDetail.as_view()),
]