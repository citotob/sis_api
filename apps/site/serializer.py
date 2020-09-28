#from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from survey.models import Penugasan,hasilSurvey,hasilSurveyBts,hasilSurveybts

class PenugasanSerializer(DocumentSerializer):
    class Meta:
        model = Penugasan
        fields = '__all__'
        depth = 2

class hasilSurveySerializer(DocumentSerializer):
    class Meta:
        model = hasilSurvey
        #fields = '__all__'
        
        fields = [
            'id',
            'user',
            'kodeHasilSurvey',
            'nomorSurvey',
            'pic',
            'tanggalPelaksanaan',
            'namaLokasi',
            'alamatLokasi',
            'modaTransportasi',
            'elevation',
            'tipeBisnis',
            'power',
            'longitude',
            'latitude',
            'status',
            'listFoto',
            'device',
            'note',
            'tanggal_pembuatan',
            'tanggal_pembaruan',
            'issue',
            'relokasi',
            'kategori',
            'network'
        ]
        read_only_fields = fields
        depth = 2

#def hasilSurveySerializer(kodeHasilSurvey: hasilSurvey) -> Dict[str, Any]:
#    return {
#        'id': hasilSurvey.id,
#        'last_login': user.last_login.isoformat() if user.last_login is not None else None,
#        'is_superuser': user.is_superuser,
#        'username': user.username,
#        'first_name': user.first_name,
#        'last_name': user.last_name,
#        'email': user.email,
#        'is_staff': user.is_staff,
#        'is_active': user.is_active,
#        'date_joined': user.date_joined.isoformat(),
#    }

class hasilSurveyBtsSerializer(DocumentSerializer):
    class Meta:
        model = hasilSurveyBts
        fields = '__all__'
        depth = 2

class btsSerializer(DocumentSerializer):
    class Meta:
        model = hasilSurveybts
        fields = '__all__'
        depth = 2



#class BookingSerializer(serializers.ModelSerializer):
#    booking_demands = BookingDemandSerializer(source='bookingdemand_set', many=True)

#    class Meta:
#        model = Booking
#        fields = '__all__'
