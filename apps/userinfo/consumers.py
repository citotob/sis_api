#websocket

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


from channels.generic.websocket import AsyncWebsocketConsumer
import json
from userinfo.models import UserInfo
import random

from channels.layers import get_channel_layer
channel_layer = get_channel_layer()
from asgiref.sync import async_to_sync
# def shout(msg):
#      channel_layer = get_channel_layer()
#      async_to_sync(channel_layer.group_send)("game", {"type": "game_message","text":msg})


import logging
from random import randint

from django.db import connection
#import mysql.connector
#from mysql.connector import Error

from django.conf import settings
import datetime
#logger

#from configparser import ConfigParser
#from ConfigParser import ConfigParser # for python3 
#data_file = 'config.ini'

#config = ConfigParser()
#config.read(data_file)

#print(config.get("mysql", "host"))


logger = logging.getLogger(__name__)
logger.setLevel(level = logging.DEBUG)

handler = logging.FileHandler("log.txt")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

#Output to console
ch = logging.StreamHandler() 
ch.setLevel(logging.DEBUG) 

logger.addHandler(handler)
logger.addHandler(ch)

from django.db import transaction 
from enum import Enum
class ChatConsumer(WebsocketConsumer):
    keyword = 'Token'
    model = None
    userinfo = None
    userImage = "None"
    updateMoneyPlayer = None
    addGameOrderr = None
    f_gameLotteryWinOrLose = None
    token=None
    
    #Calculate all winnings
    m_list_result = []
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("sis", self.channel_name)
        self.accept()

    #Solo broadcast
    def user_message(self, dict):
        isUser = self.authenticate_credentials(dict['text'])
        if isUser:
            self.send(text_data=json.dumps({"code":"mail_info"}))

    #broadcast
    def shout(self,msg):
        async_to_sync(self.channel_layer.group_send)("survey", {"type": "survey_message","text":msg})

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))
            return False

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
            return False
        self.userinfo = UserInfo.objects.get(id = token.user_id)
        self.token = token.user_id
        return True

    def disconnect(self, close_code):
        #logger.info("User id:%s-nickname:%s-connect"%(self.userinfo["Id"],self.userinfo["RealName"].encode("utf-8")))
        logger.info("=========Disconnect ws=========")
        async_to_sync(self.channel_layer.group_discard)("survey", self.channel_name)
    
    #Broadcast all users
    def survey_message(self, dict):
        self.send(text_data=json.dumps(dict))

    
    def receive(self, text_data=None, bytes_data=None):
        if text_data == "":
            self.send("ping")
            return 
        data = json.loads(text_data)
        dict = None
        with transaction.atomic():
            
            #Get user information
            if "info" == data["code"]:
                logger.info("---------info-------------")
                logger.info("")
                coin = self.userinfo["Money"].split(".")
                r_data = {"coin":coin[0],"diamond":"0","nickname":self.userinfo["RealName"],"code":self.userinfo["Id"],"imageprofile":self.userImage}
                dict = {"code":"info","result": 1,"data":r_data}
            else:
                logger.info("----------unknow------------")
            logger.info("--------------------------")
            self.send(text_data=json.dumps(dict))        

    
# Get the second element of the list
def takeSecond(elem):
    return elem[1]
 