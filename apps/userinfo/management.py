from django.db.models.signals import pre_migrate, post_migrate
#from userinfo.models import Pool,Debug
 


#dic = {'poolState':1,'currentPool':0,'poolsize':100,"pumprate":10,'income':0}
#dic_debug = {'debug':1,'resultid':0}
#Define receiver function
#def init_db(sender, **kwargs):
#  print("initialization:%s"%sender.name)
#  if sender.name == "userinfo":
#    Pool.objects.create(**dic)
#    Debug.objects.create()

#post_migrate.connect(init_db)