from apps.sites.models import Odp, rekomendasi_teknologi
from apps.sites.serializer import ODPSerializer
from operator import itemgetter
from geojson import Feature, Point
from turfpy.measurement import distance


def getRecommendTechnologi(longitude, latitude):
    coordinates = [float(longitude), float(latitude)]
    start = Feature(geometry=Point(coordinates=coordinates))
    data = Odp.objects(
        teknologi='FO',
        longlat__geo_within_sphere=[coordinates, (10 / 6378.1)])
    serializer = ODPSerializer(data, many=True)
    listOdp = []
    if len(serializer.data) > 0:
        listOdp = itemgetter('id')(serializer.data)
        print(listOdp)
