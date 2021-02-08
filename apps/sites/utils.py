from apps.sites.models import Odp, rekomendasi_teknologi, ListOdp
from apps.odps.serializer import ODPSerializer
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
        for x in serializer.data:
            end = Feature(geometry=Point(x["longlat"]["coordinates"]))
            id = itemgetter('id')(x)
            distances = "%.2f km" % distance(start, end, units="km")
            odp = ListOdp(
                odp=id,
                jarak=distances
            )
            listOdp.append(odp)
        listOdp.sort(key=itemgetter('jarak'))
        tech = rekomendasi_teknologi(
            teknologi='FO',
            list_odp=listOdp
        )
    else:
        tech = rekomendasi_teknologi(
            teknologi='VSAT',
            list_odp=[]
        )
    tech.save()
    return tech.id
