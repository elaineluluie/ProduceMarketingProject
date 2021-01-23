
# Create your models here.
#-*- coding: utf8 -*-

from django.db import models as M    #把Python的DB模組import近來，當然要先安裝MySQL-python
from django.db import connections
import os            #為了克服在不同系統中RUN你的網站，加入os模組(因為WINDOWS路徑用\ ，LINUX路徑用/，不然你的路徑指定會產生錯誤)



# Create your models here.



class test(M.Model):
    #objects = M.Manager()
    SID=M.IntegerField()#,primary_key=True  max_length=7
    Name=M.CharField(max_length=15)
    Height=M.FloatField(max_length=10)
    Weight=M.FloatField(max_length=10)
    class Meta:
        db_table="test"

class orders(M.Model):
    #objects = M.Manager()
    Ordernumber=M.IntegerField()#,primary_key=True  max_length=10
    date=M.DateField()
    CPhonenum=M.FloatField(max_length=10)
    #Weight=M.FloatField(max_length=10)
    class Meta:
        db_table="orders"

class material(M.Model):
    #objects = M.Manager()
    MID=M.IntegerField(max_length=10,primary_key=True)#,primary_key=True  max_length=7
    Mname=M.CharField(max_length=40)
    MPrice=M.IntegerField(max_length=255)
    Mcount=M.IntegerField(max_length=10)
    LTime=M.IntegerField(max_length=100)
    WLeft=M.IntegerField(max_length=100)
    class Meta:
        db_table="material"
