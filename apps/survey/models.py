from django.db import models
import random
from django.conf import settings
from mongoengine import *
from mongoengine import signals
from django.contrib.auth.hashers import make_password, check_password
import datetime
from bson import ObjectId
from datetime import timedelta ,datetime
from userinfo.models import UserInfo, Surveyor, JenisSurvey

# Create your models here.
#class JenisSurvey(Document):
#    #user = ReferenceField(UserInfo)
#    #user = StringField(required=True)
#    jenis = StringField(required=True)

#    def serialize(self):
#        return {
#            'id': str(self.id),
#            'user': self.user.serialize(),
#            'jenis': str(self.jenis),
#        }


#class Surveyor(Document):
#    user = ReferenceField(UserInfo)
#    #user = StringField(required=True)
#    name = StringField(required=True)
#    jenissurvey = ReferenceField(JenisSurvey)

#    meta = {
#        'indexes': [
#            {'fields': ('name', 'jenissurvey'), 'unique': True}
#        ]
#    }

#    def serialize(self):
#        return {
#            #'id': str(self.id),
#            'user': self.user.serialize(),
#            'jenissurvey': self.jenissurvey.serialize(),
#            'name': str(self.name),
#        }


class provinsi(Document):
    #user = ReferenceField(UserInfo)
    name = StringField(required=True)
    tanggal_pembuatan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    tanggal_perubahan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    prefix = StringField(required=True)
    meta = {
        'strict': False,
    }

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'tanggal_pembuatan': str(self.tanggal_pembuatan),
            'tanggal_perubahan': str(self.tanggal_perubahan),
        }


class kabupaten(Document):
    name = StringField(required=True)
    provinsi = ReferenceField(provinsi)
    tanggal_pembuatan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    tanggal_perubahan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))

    meta = {
        'strict': False,
    }

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            # 'provinsi': str(self.provinsi.serialize()),
            'tanggal_pembuatan': str(self.tanggal_pembuatan),
            'tanggal_perubahan': str(self.tanggal_perubahan),
        }


class kota(Document):
    name = StringField(required=True)
    provinsi = ReferenceField(provinsi)
    tanggal_pembuatan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    tanggal_perubahan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))

    meta = {
        'strict': False,
    }

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            # 'provinsi': str(self.provinsi.serialize()),
            'tanggal_pembuatan': str(self.tanggal_pembuatan),
            'tanggal_perubahan': str(self.tanggal_perubahan),
        }


class kecamatan(Document):
    name = StringField(required=True)
    kabupaten = ReferenceField(kabupaten)
    kota = ReferenceField(kota)
    tanggal_pembuatan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    tanggal_perubahan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))

    meta = {
        'strict': False,
    }

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            # 'kabupaten': self.kabupaten.serialize(),
            # 'kota': self.kabupaten.serialize(),
            'tanggal_pembuatan': str(self.tanggal_pembuatan),
            'tanggal_perubahan': str(self.tanggal_perubahan),
        }


class desa(Document):
    name = StringField(required=True)
    kecamatan = ReferenceField(kecamatan)
    tanggal_pembuatan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    tanggal_perubahan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))

    meta = {
        'strict': False,
    }

    def serialize(self):
        return {
            'id': str(self.id),
            'name': str(self.name),
            # 'kecamatan': str(self.kecamatan.serialize()),
            'tanggal_pembuatan': str(self.tanggal_pembuatan),
            'tanggal_perubahan': str(self.tanggal_perubahan),
        }


class LokasiSurvey(Document):
    jenis = StringField(required=True)
    provinsi = ReferenceField(provinsi)
    kabupaten = ReferenceField(kabupaten)
    kota = ReferenceField(kota)
    kecamatan = ReferenceField(kecamatan)
    desa = ReferenceField(desa)
    latitude = StringField(required=True)
    longitude = StringField(required=True)
    status = ListField(required=True)

    def serialize(self):
        try:
            return {
                'id': str(self.id),
                'jenis': str(self.jenis),
                'provinsi': self.provinsi.serialize(),
                'kabupaten': self.kabupaten.serialize(),
                'kecamatan': self.kecamatan.serialize(),
                'desa': self.desa.serialize(),
                'latitude': str(self.latitude),
                'longitude': str(self.longitude),
                'status': self.status,
            }
        except:
            return {
                'id': str(self.id),
                'jenis': str(self.jenis),
                'provinsi': self.provinsi.serialize(),
                'kota': self.kota.serialize(),
                'kecamatan': self.kecamatan.serialize(),
                'desa': self.desa.serialize(),
                'latitude': str(self.latitude),
                'longitude': str(self.longitude),
                'status': self.status,
            }


"""
class LokasiSurvey(Document):
    jenis = StringField(required=True)
    provinsi = StringField(provinsi)
    kabupaten = StringField(kabupaten)
    kota = StringField(kota)
    kecamatan = StringField(kecamatan)
    desa = StringField(desa)
    latitude = StringField(required=True)
    longitude = StringField(required=True)
    status = ListField(required=True)

    #def serialize(self):
    #    try:
    #        return {
    #            'id': str(self.id),
    #            'jenis': str(self.jenis),
    #            'provinsi': self.provinsi.serialize(),
    #            'kabupaten': self.kabupaten.serialize(),
    #            'kecamatan': self.kecamatan.serialize(),
    #            'desa': self.desa.serialize(),
    #            'latitude': str(self.latitude),
    #            'longitude': str(self.longitude),
    #            'status': self.status,
    #        }
    #    except:
            return {
                'id': self.id,
                'jenis': str(self.jenis),
                'provinsi': self.provinsi.serialize(),
                'kota': self.kota.serialize(),
                'kecamatan': self.kecamatan.serialize(),
                'desa': self.desa.serialize(),
                'latitude': str(self.latitude),
                'longitude': str(self.longitude),
                'status': self.status,
            }
"""
class DocumentPenugasan(Document):
    name = StringField()
    path = StringField()
    create_date = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))
    update_date = DateTimeField(
        default=datetime.utcnow() + timedelta(hours=7))

    def serialize(self):
        return {
            "name": self.name,
            "path": self.path,
            "create_date": self.create_date,
            "update_date": self.update_date,
        }

class Penugasan(Document):
    user = ReferenceField(UserInfo)
    kode = StringField(required=True,unique=True)
    jenissurvey = ReferenceField(JenisSurvey)
    surveyor = ReferenceField(Surveyor)
    lokasisurvey = ReferenceField(LokasiSurvey)
    assignfrom = ReferenceField(UserInfo)
    assignto = ReferenceField(Surveyor)
    #assigndate = DateTimeField(
    #    default=(datetime.utcnow() + timedelta(hours=7)))
    #assigntodate = DateTimeField(
    #    default=(datetime.utcnow() + timedelta(hours=7)))

    assignfrom1 = ReferenceField(UserInfo)
    assignto1 = ReferenceField(UserInfo)
    #assign1 = DateTimeField(
    #    default=(datetime.utcnow() + timedelta(hours=7)))
    #assignto1date = DateTimeField(
    #    default=(datetime.utcnow() + timedelta(hours=7)))

    tanggal_penugasan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))

    target = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))

    finish = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    # status = StringField(required=True,choices=[
    #                     'created', 'assigned','verified', 'issued','declined', 'finished'], default='created')
    status = ListField(required=True)
    nospk = StringField(required=True)
    spk = ReferenceField(DocumentPenugasan)

    meta = {
        'indexes': [
            {'fields': ('jenissurvey', 'lokasisurvey', 'nospk'), 'unique': True}
            
        ]
    }

    def serialize(self):
        try:
            sr_assignfrom = self.assignfrom.serialize()
        except:
            sr_assignfrom = str(self.assignfrom)
        try:
            sr_assignto = self.assignto.serialize()
        except:
            sr_assignto = str(self.assignto)
        try:
            sr_assignfrom1 = self.assignfrom1.serialize()
        except:
            sr_assignfrom1 = str(self.assignfrom1)
        try:
            sr_assignto1 = self.assignto1.serialize()
        except:
            sr_assignto1 = str(self.assignto1)
        try:
            spk_ = self.spk.serialize()
        except:
            spk_ = 'null'
        return {
            'id': str(self.id),
            'user': self.user.serialize(),
            'kode': str(self.kode),
            'jenissurvey': self.jenissurvey.serialize(),
            'surveyor': self.surveyor.serialize(),
            'jenissurvey': self.jenissurvey.serialize(),
            'lokasisurvey': self.lokasisurvey.serialize(),
            'tanggal_penugasan': str(self.tanggal_penugasan),
            'assignfrom': sr_assignfrom,
            'assignto': sr_assignto,
            #'assigndate': str(self.assigndate),
            'assignfrom1': sr_assignfrom1,
            'assignto1': sr_assignto1, 
            #'assign1': str(self.assign1),
            'target': str(self.target),
            'finish': str(self.finish),
            'nospk': str(self.nospk),
            "spk": spk_,
            'status': self.status,
        } 
    
    def serializeAssign(self):
        return {
            #'id': self.id.serialize(),
            'kode': str(self.kode),
        }
    

class patternFoto(EmbeddedDocument):
    def instan(self, nama, url):
        self.nama = nama
        self.url = url
        return self

    nama = StringField(required=True,default='-')
    url = StringField(required=True,default='-')

class ModaTransportasi(EmbeddedDocument):
    darat = StringField(required=True,default='-')
    laut = StringField(required=True,default='-')
    udara = StringField(required=True,default='-')
    durasiPerjalanan = StringField(required=True,default='-')
    namaKotaKecamatan = StringField(required=True,default='-')


class FotoAI(EmbeddedDocument):
    def instan(self, aksesJalan, plang, markingPerangkat, kwhMeter, gambarDenah, lanskapBangunan
               ):
        self.aksesJalan = aksesJalan
        self.plang = plang
        self.markingPerangkat = markingPerangkat
        self.kwhMeter = kwhMeter
        self.gambarDenah = gambarDenah
        self.lanskapBangunan = lanskapBangunan
        return self

    aksesJalan = EmbeddedDocumentField(patternFoto)
    plang = EmbeddedDocumentField(patternFoto)
    markingPerangkat = EmbeddedDocumentField(patternFoto)
    kwhMeter = EmbeddedDocumentField(patternFoto)
    gambarDenah = EmbeddedDocumentField(patternFoto)
    lanskapBangunan = EmbeddedDocumentField(patternFoto)

class LainyaTemplate(EmbeddedDocument):
    def instan(self, nama, qty):
        self.nama = nama
        self.qty = qty
        return self
    nama=StringField(required=True,default='-')
    qty = StringField(required=True, default='0')

class Device(EmbeddedDocument):
    pc = StringField(required=True, default='0')
    tablet = StringField(required=True, default='0')
    smartPhone = StringField(required=True, default='0')
    laptop = StringField(required=True, default='0')
    lainnya1 = EmbeddedDocumentField(LainyaTemplate,required=False)
    lainnya2 = EmbeddedDocumentField(LainyaTemplate,required=False)


class Pic(EmbeddedDocument):
    namaPic = StringField(required=True,default='-')
    phonePic =StringField(required=True,default='-')

class Power(EmbeddedDocument):
    idPelangganPLN= StringField(required=True,default='-')
    sumber_listrik = StringField(required=True,default='-')
    kapasitas_listrik= StringField(required=True,default='-')
    jamOperasionalListrik= StringField(required=True,default='-')
    jamOperasionalLokal= StringField(required=True,default='-')
    sumber_cadangan = StringField(required=True,default='-')

class Relokasi(EmbeddedDocument):
    provinsi = StringField(required=True,default='-')
    kab_kota = StringField(required=True,default='-')
    kecamatan = StringField(required=True,default='-')
    desa = StringField(required=True,default='-')
    alasan = StringField(required=True,default='-')
    kodelama = StringField(required=True,default='-')

class Network(EmbeddedDocument):
    tipe = StringField(required=True,default='-')
    download = StringField(required=True,default='0')
    upload = StringField(required=True,default='0')
    
class hasilSurvey(Document):
    user = ReferenceField(UserInfo)
    kodeHasilSurvey = StringField(required=True)
    nomorSurvey = StringField(required=True)
    pic = EmbeddedDocumentField(Pic)
    tanggalPelaksanaan = DateTimeField()

    namaLokasi = StringField(required=True)
    alamatLokasi = StringField(required=True)

    modaTransportasi = EmbeddedDocumentField(ModaTransportasi)

    elevation = StringField(required=True)
    tipeBisnis = StringField(required=True)

    power = EmbeddedDocumentField(Power)
    # jenisPeninjauan = StringField(required=True)
    # solusiTeknologi = StringField(required=True)
    # catatan = StringField(required=True)
    # # sisiInternalTeknisi = StringField(required=True)
    # # sisiPelanggan = StringField(required=True)
    # resume = StringField(required=True)

    longitude = StringField(required=True, default='-')
    latitude = StringField(required=True, default='-')

    status = ListField(required=True)

    listFoto = EmbeddedDocumentField(FotoAI)
    device = EmbeddedDocumentField(Device)
    note = StringField(required=True)

    tanggal_pembuatan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    tanggal_pembaruan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))

    issue = ListField(required=False)
    relokasi = EmbeddedDocumentField(Relokasi)
    kategori = StringField(required=True, default='-')
    network = EmbeddedDocumentField(Network)


        
class Section1(EmbeddedDocument):
    tipeKawasan = StringField(required=True)
    alamatLokasi = StringField(required=True)
    modaTransportasi = EmbeddedDocumentField(ModaTransportasi)
    tipeAntena = StringField(required=True)

class Section2(EmbeddedDocument):
    
    latitude = StringField(required=True)
    longitude = StringField(required=True)
    ketinggianAsl = StringField(required=True)


class Section3(EmbeddedDocument):
    posisiTower = StringField(required=True)
    jarakPemukiman = StringField(required=False)
    kepemilikanLahan = StringField(required=True)
    statusKondisiLahan = StringField(required=True)
    kondisiSosial = StringField(required=True)
    keamanan = StringField(required=True)
    ukuranLahan = StringField(required=True)


class Section4(EmbeddedDocument):
    coverageRadius = StringField(required=True)
    levelSinyal = StringField(required=True)
    dbm = StringField(required=True)
    callSite = StringField(required=True)
    smsSite = StringField(required=True)
    namaOperator = StringField(required=True)


class Section5(EmbeddedDocument):
    topografiUmum = StringField(required=True)
    klasifikasiLahan = StringField(required=True)
    objekPenghalang = StringField(required=True)
    rekondisiLahan = StringField(required=True)
    tipeTanah = StringField(required=True)
    jarakSungaiLaut = StringField(required=True)


class Section6(EmbeddedDocument):
    sumberListrik = StringField(required=True)
    phaseListrik = StringField(required=True)
    dayaListrik = StringField(required=True)
    jamOperasionalListrik = StringField(required=True)
    jarakSumberListrik = StringField(required=True)
    generatorBackup = StringField(required=True)
    merk = StringField(required=False)
    kapasitas = StringField(required=False)
    kapasitasBbm = StringField(required=False)
    pasokanBbm = StringField(required=True)
    jenisBbm = StringField(required=True)
    harga = StringField(required=True)
    listrikIdeal = StringField(required=True)

class Section7(EmbeddedDocument):
    suratTanah = StringField(required=True)
    izinDiperlukan = StringField(required=True)


class Section8(EmbeddedDocument):
    populasi = StringField(required=True)
    kepadatanPenduduk = StringField(required=True)
    sebaranPenduduk = StringField(required=True)
    desaTerdekat = StringField(required=True)
    namaDesa = StringField(required=False)
    jarakDesaTerdekat = StringField(required=True)
    mataPencaharian = StringField(required=True)
    penggunaHp = StringField(required=True)
    tipeHp = StringField(required=True)
    providerSimCard = StringField(required=True)
    wargaBimtek = StringField(required=True)
    aksesInternet = StringField(required=True)
    rumahDenganGenset = StringField(required=True)
    

class Section9(EmbeddedDocument):
    def instan(self,fotoLahan):
        self.fotoLahan = fotoLahan
    fotoLahan = EmbeddedDocumentField(patternFoto)


class Section10(EmbeddedDocument):
    fotoDetailLahan = EmbeddedDocumentField(patternFoto)
    fotoDetailMarking = EmbeddedDocumentField(patternFoto)
    fotoDetailSisiUtara = EmbeddedDocumentField(patternFoto)
    fotoDetailSisiTimur = EmbeddedDocumentField(patternFoto)
    fotoDetailSisiBarat = EmbeddedDocumentField(patternFoto)
    fotoDetailSisiSelatan = EmbeddedDocumentField(patternFoto)


class Section11(EmbeddedDocument):
    def instan(self,coverage0N,coverage0Ndesc,coverage45N,coverage45Ndesc,
    coverage90N,coverage90Ndesc,coverage135N,coverage135Ndesc,
    coverage180N,coverage180Ndesc,coverage225N,coverage225Ndesc,
    coverage270N,coverage270Ndesc,coverage315N,coverage315Ndesc):
        self.coverage0N = coverage0N
        self.coverage0Ndesc = coverage0Ndesc
        self.coverage45N = coverage45N
        self.coverage45Ndesc = coverage45Ndesc
        self.coverage90N = coverage90N
        self.coverage90Ndesc = coverage90Ndesc
        self.coverage135N = coverage135N
        self.coverage135Ndesc = coverage135Ndesc
        self.coverage180N = coverage180N
        self.coverage180Ndesc = coverage180Ndesc
        self.coverage225N = coverage225N
        self.coverage225Ndesc = coverage225Ndesc
        self.coverage270N = coverage270N
        self.coverage270Ndesc = coverage270Ndesc
        self.coverage315N = coverage315N
        self.coverage315Ndesc = coverage315Ndesc
    
    coverage0N = StringField(required=True)
    coverage0Ndesc = StringField(required=True)
    coverage45N = StringField(required=True)
    coverage45Ndesc = StringField(required=True)
    coverage90N = StringField(required=True)
    coverage90Ndesc = StringField(required=True)
    coverage135N = StringField(required=True)
    coverage135Ndesc = StringField(required=True)
    coverage180N = StringField(required=True)
    coverage180Ndesc = StringField(required=True)
    coverage225N = StringField(required=True)
    coverage225Ndesc = StringField(required=True)
    coverage270N = StringField(required=True)
    coverage270Ndesc = StringField(required=True)
    coverage315N = StringField(required=True)
    coverage315Ndesc = StringField(required=True)


class Section12(EmbeddedDocument):
    def instan(self,fotoGnetTrack0N2Km,fotoGnetTrack45N2Km,
    fotoGnetTrack90N2Km,fotoGnetTrack135N2Km,fotoGnetTrack180N2Km,
    fotoGnetTrack225N2Km,fotoGnetTrack270N2Km,fotoGnetTrack315N2Km
    ):
        self.fotoGnetTrack0N2Km = fotoGnetTrack0N2Km
        self.fotoGnetTrack45N2Km = fotoGnetTrack45N2Km
        self.fotoGnetTrack90N2Km = fotoGnetTrack90N2Km
        self.fotoGnetTrack135N2Km = fotoGnetTrack135N2Km
        self.fotoGnetTrack180N2Km = fotoGnetTrack180N2Km
        self.fotoGnetTrack225N2Km = fotoGnetTrack225N2Km
        self.fotoGnetTrack270N2Km = fotoGnetTrack270N2Km
        self.fotoGnetTrack315N2Km = fotoGnetTrack315N2Km
    
    fotoGnetTrack0N2Km = EmbeddedDocumentField(patternFoto)
    fotoGnetTrack45N2Km = EmbeddedDocumentField(patternFoto)
    fotoGnetTrack90N2Km = EmbeddedDocumentField(patternFoto)
    fotoGnetTrack135N2Km = EmbeddedDocumentField(patternFoto)
    fotoGnetTrack180N2Km = EmbeddedDocumentField(patternFoto)
    fotoGnetTrack225N2Km = EmbeddedDocumentField(patternFoto)
    fotoGnetTrack270N2Km = EmbeddedDocumentField(patternFoto)
    fotoGnetTrack315N2Km = EmbeddedDocumentField(patternFoto)


class Section13(EmbeddedDocument):
    def instan(self,fotoGnetTrack0N5Km,fotoGnetTrack45N5Km,
    fotoGnetTrack90N5Km,fotoGnetTrack135N5Km,fotoGnetTrack180N5Km,
    fotoGnetTrack225N5Km,fotoGnetTrack270N5Km,fotoGnetTrack315N5Km
    ):
        self.fotoGnetTrack0N5Km = fotoGnetTrack0N5Km
        self.fotoGnetTrack45N5Km = fotoGnetTrack45N5Km
        self.fotoGnetTrack90N5Km = fotoGnetTrack90N5Km
        self.fotoGnetTrack135N5Km = fotoGnetTrack135N5Km
        self.fotoGnetTrack180N5Km = fotoGnetTrack180N5Km
        self.fotoGnetTrack225N5Km = fotoGnetTrack225N5Km
        self.fotoGnetTrack270N5Km = fotoGnetTrack270N5Km
        self.fotoGnetTrack315N5Km = fotoGnetTrack315N5Km
    
    fotoGnetTrack0N5Km = EmbeddedDocumentField(patternFoto)
    fotoGnetTrack45N5Km = EmbeddedDocumentField(patternFoto)
    fotoGnetTrack90N5Km = EmbeddedDocumentField(patternFoto)
    fotoGnetTrack135N5Km = EmbeddedDocumentField(patternFoto)
    fotoGnetTrack180N5Km = EmbeddedDocumentField(patternFoto)
    fotoGnetTrack225N5Km = EmbeddedDocumentField(patternFoto)
    fotoGnetTrack270N5Km = EmbeddedDocumentField(patternFoto)
    fotoGnetTrack315N5Km = EmbeddedDocumentField(patternFoto)
    

class Section14(EmbeddedDocument):
    latitudeMapping = StringField(required=True)
    longitudeMapping = StringField(required=True)
    elevasiMapping = StringField(required=True)
    latitudeAlt1 = StringField(required=False)
    longitudeAlt1 = StringField(required=False)
    elevasiAlt1 = StringField(required=False)
    latitudeAlt2 = StringField(required=False)
    longitudeAlt2 = StringField(required=False)
    elevasiAlt2 = StringField(required=False)


class Section15(EmbeddedDocument):
    def instan(self,topografiSektor0N,landscapeSektor0N,demografiSektor0N,
    topografiSektor45N,landscapeSektor45N,demografiSektor45N,
    topografiSektor90N,landscapeSektor90N,demografiSektor90N,
    topografiSektor135N,landscapeSektor135N,demografiSektor135N,
    topografiSektor180N,landscapeSektor180N,demografiSektor180N,
    topografiSektor225N,landscapeSektor225N,demografiSektor225N,
    topografiSektor270N,landscapeSektor270N,demografiSektor270N,
    topografiSektor315N,landscapeSektor315N,demografiSektor315N):
        self.topografiSektor0N = topografiSektor0N
        self.landscapeSektor0N = landscapeSektor0N
        self.demografiSektor0N = demografiSektor0N
        self.topografiSektor45N = topografiSektor45N
        self.landscapeSektor45N = landscapeSektor45N
        self.demografiSektor45N = demografiSektor45N
        self.topografiSektor90N = topografiSektor90N
        self.landscapeSektor90N = landscapeSektor90N
        self.demografiSektor90N = demografiSektor90N
        self.topografiSektor135N = topografiSektor135N
        self.landscapeSektor135N = landscapeSektor135N
        self.demografiSektor135N = demografiSektor135N
        self.topografiSektor180N = topografiSektor180N
        self.landscapeSektor180N = landscapeSektor180N
        self.demografiSektor180N = demografiSektor180N
        self.topografiSektor225N = topografiSektor225N
        self.landscapeSektor225N = landscapeSektor225N
        self.demografiSektor225N = demografiSektor225N
        self.topografiSektor270N = topografiSektor270N
        self.landscapeSektor270N = landscapeSektor270N
        self.demografiSektor270N = demografiSektor270N
        self.topografiSektor315N = topografiSektor315N
        self.landscapeSektor315N = landscapeSektor315N
        self.demografiSektor315N = demografiSektor315N
    topografiSektor0N = StringField(required=True)
    landscapeSektor0N = StringField(required=True)
    demografiSektor0N = StringField(required=True)
    topografiSektor45N = StringField(required=True)
    landscapeSektor45N = StringField(required=True)
    demografiSektor45N = StringField(required=True)
    topografiSektor90N = StringField(required=True)
    landscapeSektor90N = StringField(required=True)
    demografiSektor90N = StringField(required=True)
    topografiSektor135N = StringField(required=True)
    landscapeSektor135N = StringField(required=True)
    demografiSektor135N = StringField(required=True)
    topografiSektor180N = StringField(required=True)
    landscapeSektor180N = StringField(required=True)
    demografiSektor180N = StringField(required=True)
    topografiSektor225N = StringField(required=True)
    landscapeSektor225N = StringField(required=True)
    demografiSektor225N = StringField(required=True)
    topografiSektor270N = StringField(required=True)
    landscapeSektor270N = StringField(required=True)
    demografiSektor270N = StringField(required=True)
    topografiSektor315N = StringField(required=True)
    landscapeSektor315N = StringField(required=True)
    demografiSektor315N = StringField(required=True)



class Section16(EmbeddedDocument):
    def instan(self,fotoSektor0N,fotoSektor45N,fotoSektor90N,
    fotoSektor135N,fotoSektor180N,fotoSektor225N,
    fotoSektor270N,fotoSektor315N,tempatFotoSektor):
        self.fotoSektor0N = fotoSektor0N
        self.fotoSektor45N = fotoSektor45N
        self.fotoSektor90N = fotoSektor90N
        self.fotoSektor135N = fotoSektor135N
        self.fotoSektor180N = fotoSektor180N
        self.fotoSektor225N = fotoSektor225N
        self.fotoSektor270N = fotoSektor270N
        self.fotoSektor315N = fotoSektor315N
        self.tempatFotoSektor = tempatFotoSektor
    fotoSektor0N = EmbeddedDocumentField(patternFoto)
    fotoSektor45N = EmbeddedDocumentField(patternFoto)
    fotoSektor90N = EmbeddedDocumentField(patternFoto)
    fotoSektor135N = EmbeddedDocumentField(patternFoto)
    fotoSektor180N = EmbeddedDocumentField(patternFoto)
    fotoSektor225N = EmbeddedDocumentField(patternFoto)
    fotoSektor270N = EmbeddedDocumentField(patternFoto)
    fotoSektor315N = EmbeddedDocumentField(patternFoto)
    tempatFotoSektor = StringField(required=True)


class Section17(EmbeddedDocument):
    def instan(self,fotoPenggunaPotensial1,fotoPenggunaPotensial2,fotoPenggunaPotensial3,
    fotoPenggunaPotensial4,fotoPenggunaPotensial5):
        self.fotoPenggunaPotensial1 = fotoPenggunaPotensial1
        self.fotoPenggunaPotensial2 = fotoPenggunaPotensial2
        self.fotoPenggunaPotensial3 = fotoPenggunaPotensial3
        self.fotoPenggunaPotensial4 = fotoPenggunaPotensial4
        self.fotoPenggunaPotensial5 = fotoPenggunaPotensial5
    
    fotoPenggunaPotensial1 = EmbeddedDocumentField(patternFoto)
    fotoPenggunaPotensial2 = EmbeddedDocumentField(patternFoto)
    fotoPenggunaPotensial3 = EmbeddedDocumentField(patternFoto)
    fotoPenggunaPotensial4 = EmbeddedDocumentField(patternFoto)
    fotoPenggunaPotensial5 = EmbeddedDocumentField(patternFoto)


class Section18(EmbeddedDocument):
    def instan(self,fotoAksesSite1,fotoAksesSite2,fotoAksesSite3,
    fotoAksesSite4,fotoAksesSite5):
        self.fotoAksesSite1 = fotoAksesSite1
        self.fotoAksesSite2 = fotoAksesSite2
        self.fotoAksesSite3 = fotoAksesSite3
        self.fotoAksesSite4 = fotoAksesSite4
        self.fotoAksesSite5 = fotoAksesSite5
    fotoAksesSite1 = EmbeddedDocumentField(patternFoto)
    fotoAksesSite2 = EmbeddedDocumentField(patternFoto)
    fotoAksesSite3 = EmbeddedDocumentField(patternFoto)
    fotoAksesSite4 = EmbeddedDocumentField(patternFoto)
    fotoAksesSite5 = EmbeddedDocumentField(patternFoto)





class hasilSurveyBts(Document):
    user = ReferenceField(UserInfo)
    kodeHasilSurvey = StringField(required=True)
    nomorSurvey = StringField(required=True)

    section1 = EmbeddedDocumentField(Section1)    
    section2 = EmbeddedDocumentField(Section2) 
    section3 = EmbeddedDocumentField(Section3)    
    section4 = EmbeddedDocumentField(Section4)    
    section5 = EmbeddedDocumentField(Section5)    
    section6 = EmbeddedDocumentField(Section6)    
    section7 = EmbeddedDocumentField(Section7)    
    section8 = EmbeddedDocumentField(Section8)    
    section9 = EmbeddedDocumentField(Section9)    
    section10 = EmbeddedDocumentField(Section10)    

    section11 = EmbeddedDocumentField(Section11)    
    section12 = EmbeddedDocumentField(Section12)    
    section13 = EmbeddedDocumentField(Section13)    
    section14 = EmbeddedDocumentField(Section14)    
    section15 = EmbeddedDocumentField(Section15)    
    section16 = EmbeddedDocumentField(Section16)    
    section17 = EmbeddedDocumentField(Section17)    
    section18 = EmbeddedDocumentField(Section18)    
    

    comment = StringField(required=True)


class hasilSurveybts(Document):
    user = ReferenceField(UserInfo)
    kodeHasilSurvey = StringField(required=True)
    nomorSurvey = StringField(required=True)
    pic = EmbeddedDocumentField(Pic)
    tanggalPelaksanaan = DateTimeField()
    namaLokasi = StringField(required=True)
    longitude = StringField(required=True)
    latitude = StringField(required=True)
    note = StringField(required=True)
    status = ListField(required=True)
    fotoKandidatLahan = EmbeddedDocumentField(patternFoto)
    fotoMarkingGps = EmbeddedDocumentField(patternFoto)
    fotoUtaraTitik = EmbeddedDocumentField(patternFoto)
    fotoTimurTitik = EmbeddedDocumentField(patternFoto)
    fotoSelatanTitik = EmbeddedDocumentField(patternFoto)
    fotoBaratTitik = EmbeddedDocumentField(patternFoto)
    
    tanggal_pembuatan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    tanggal_pembaruan = DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))

    issue = ListField(required=False)
    relokasi = EmbeddedDocumentField(Relokasi)
    kategori = StringField(required=True, default='-')
    network = EmbeddedDocumentField(Network)

class issueHasilSurvey(Document):
    HasilSurvey = ReferenceField(hasilSurvey)
    deskripsiIssueIdPelanggan = StringField(required=False)
    deskripsiIssueSumberListrik = StringField(required=False)
    deskripsiIssueKapasitasListrik = StringField(required=False)
    deskripsiIssueSumberListrikCadangan = StringField(required=False)
    deskripsiIssuePc = StringField(required=False)
    deskripsiIssueLaptop = StringField(required=False)
    deskripsiIssueUps = StringField(required=False)
    deskripsiIssueModem = StringField(required=False)
    deskripsiIssueLainnya = StringField(required=False)
    deskripsiIssueLainnya = StringField(required=False)

    def serialize(self):
        return {
            'id': str(self.id),
            'kodeHasilSurvey': self.kodeHasilSurvey,
            'idPelangganPLN': self.idPelangganPLN,
            'sumber_listrik': self.sumber_listrik,
            'kapasitas_listrik': self.kapasitas_listrik,
            'sumber_cadangan': self.sumber_cadangan,
            'pc': self.pc,
            'laptop': self.laptop,
            'ups': self.ups,
            'modem': self.modem,
            'pendukung': self.pendukung,
            'foto': self.foto,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'status': self.status,
            'tanggal_pembuatan': self.tanggal_pembuatan,
            'tanggal_pembaruan': self.tanggal_pembaruan,
        }
