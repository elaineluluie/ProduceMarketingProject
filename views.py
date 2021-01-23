from django.shortcuts import render
from catalog.models import orders
from catalog.models import material
from django.template.loader import get_template
from pymysql import cursors, connect
import time
import datetime
import math
import statistics

#from catalog.ConnectSQL import SQLconnect

# Create your views here.
from django.http import HttpResponse


'''def index(request):
    results=test.objects.all()
    return render(request,"Page1.html",{"test":results})
'''
def index(request):
    #results=orders.objects.all()
    return render(request,"index.html")

def welcome(request):
    #results=orders.objects.all()
    return render(request,"welcome.html")

def crm(request):
    #results=orders.objects.all()
    return render(request,"crm.html")

def rfm(request):
    sqlQ1="select c.cPhonenum id,c.cName 名字,max(o.date) R,count(distinct o.date) F,sum(o.Price) M, case when DATEDIFF(CURRENT_DATE(),max(o.date))<7 and count(distinct o.date)>=4 and sum(o.Price)>400 then 111 when DATEDIFF(CURRENT_DATE(),max(o.date))<7 and count(distinct o.date)>=4 and sum(o.Price)<=400 then 112 when DATEDIFF(CURRENT_DATE(),max(o.date))<7 and count(distinct o.date)<4 and sum(o.Price)<=400 then 122 when DATEDIFF(CURRENT_DATE(),max(o.date))<7 and count(distinct o.date)<4 and sum(o.Price)>400 then 121 when DATEDIFF(CURRENT_DATE(),max(o.date))>=7 and count(distinct o.date)>=4 and sum(o.Price)>400 then 211 when DATEDIFF(CURRENT_DATE(),max(o.date))>=10 and count(distinct o.date)<4 and sum(o.Price)>400 then 221 when DATEDIFF(CURRENT_DATE(),max(o.date))>=7 and count(distinct o.date)>=7 and sum(o.Price)<=400 then 212 else 222 end as 顧客分群 from Customer as c inner join Orders as o on c.cPhonenum=o.cPhonenum group by c.cPhonenum order by 顧客分群,R desc, F desc, M DESC"
    conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)
    cur=conn.cursor()
    cur.execute(sqlQ1)
    results=cur.fetchall()
    return render(request,"crm.rfm.html",{"rfm":results})

def broadcast(request):
    #results=orders.objects.all()
    return render(request,"crm.broadcast.html")

def salespredictions(request):
    #results=orders.objects.all()
    conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)
    sql="select count(distinct t1.cPhonenum) 第一周, count(distinct t2.cPhonenum) 第二周,count(distinct t3.cPhonenum) 第三周,count(distinct t4.cPhonenum) 第四周,count(distinct t5.cPhonenum) 第五周 from(select  cPhonenum from Orders where date>='2020-11-30' and date<'2020-12-07')t1 left join(select cPhonenum from Orders where date>='2020-12-07' and date<'2020-12-14')t2 on t1.cPhonenum=t2.cPhonenum left join(select cPhonenum from Orders where date>='2020-12-14' and date<'2020-12-21')t3 on t1.cPhonenum=t2.cPhonenum and t2.cPhonenum=t3.cPhonenum left join(select cPhonenum from Orders where date>='2020-12-21' and date<'2020-12-28')t4 on t2.cPhonenum=t1.cPhonenum and t2.CPhonenum=t3.CPhonenum and t3.CPhonenum=t4.CPhonenum left join(select cPhonenum from Orders where date>='2020-12-28' and date<'2021-01-04')t5 on t2.cPhonenum=t1.cPhonenum and t2.CPhonenum=t3.CPhonenum and t3.CPhonenum=t4.CPhonenum and t4.cPhonenum=t5.cPhonenum"
    cur=conn.cursor()
    cur.execute(sql)
    results=cur.fetchall()
    week1=results[0]['第一周']
    week2=results[0]['第二周']
    week3=results[0]['第三周']
    week4=results[0]['第四周']
    week5=results[0]['第五周']
    original=results[0]['第一周']
    rr0=1
    rr1=round((week2/week1),3)
    rr2=round((week3/week2),3)
    rr3=round((week4/week3),3)
    rr4=round((week5/week4),3)
    sr0="null"
    sr1=round(rr1,3)
    sr2=round((sr1*rr2),3)
    sr3=round((sr2*rr3),3)
    sr4=round((sr3*rr4),3)

    week1=round((sr1*original),3)
    week2=round((sr2*original),3)
    week3=round((sr3*original),3)
    week4=round((sr4*original),3)

    lt0="null"
    lt1=week1
    lt2=round((week2*2),3)
    lt3=round((week3*3),3)
    lt4=round((week4*4),3)
    alt=round(((lt1+lt2+lt3+lt4)/original),3)

    return render(request,"crm.salesanalysis.html",locals())

def salesrecord(request):
    conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)
    sql = "SELECT c.CPhonenum id, c.Cname 名字, o.date 購買日期,o.buyItem 購買品項, o.price 金額, o.Ordernumber 購物編號 FROM customer as c inner join orders as o on c.CPhonenum=o.CPhonenum ORDER BY 購買日期 DESC,購物編號 DESC, id;"
    cur=conn.cursor()
    cur.execute(sql)
    results=cur.fetchall()
    return render(request,"crm.salesrecord.html",{"record":results})

def om(request):
    #results=orders.objects.all()
    return render(request,"om.html")

def inventory(request):
    #results=material.objects.all()
    todayDate=datetime.datetime.now()
    i=0
    cornCheeseSum=0
    bananaSum=0
    blackSum=0
    greenSum=0
    cornArr=[]
    bananaArr=[]
    blackArr=[]
    greenArr=[]
    #corncheese
    while i < 30:
        conn = connect(
            host='localhost',
            port=3307,
            user='test08',
            password='xup6ji3hj/ ',
            database='test',
            charset='utf8',
            cursorclass=cursors.DictCursor)
        delta = datetime.timedelta(days=i)
        buyDate=todayDate-delta
        buyDate2=str(buyDate.strftime("%Y/%m/%d"))
        sqlQ1 = "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='CornCheese'"
        sqlQ2 = "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='Banana'"
        sqlQ3= "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='Black'"
        sqlQ4 = "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='Green'"
        cur=conn.cursor()
        cornCheeseSum+=cur.execute(sqlQ1)
        bananaSum+=cur.execute(sqlQ2)
        blackSum+=cur.execute(sqlQ3)
        greenSum+=cur.execute(sqlQ4)
        cornArr.append(cur.execute(sqlQ1))
        bananaArr.append(cur.execute(sqlQ1))
        blackArr.append(cur.execute(sqlQ1))
        greenArr.append(cur.execute(sqlQ1))

        i+=1
        conn.close
            #print("-------------")
            #print(buyDate)
            #print("corncheese",cornCheeseSum)
            #print("banana",bananaSum)
            #print("black",blackSum)
            #print("green",greenSum)
    averageCornCheese=cornCheeseSum/30
    averageBanana=bananaSum/30
    averageBlack=blackSum/30
    averageGreen=greenSum/30
            #print(averageCornCheese)
            #print(averageBanana)
            #print(averageBlack)
            #print(averageGreen)
    #rop=LTime*demand*the count which material could made
    ropCorn=math.ceil(averageCornCheese*1*10)
    ropCheese=math.ceil(averageCornCheese*1*10)
    ropBanana=math.ceil(averageBanana*1*3)
    ropBlack=math.ceil(averageBlack*3*30)
    ropGreen=math.ceil(averageGreen*3*30)
            #print(ropCorn)
            #print(ropCheese)
            #print(ropBanana)
            #print(ropBlack)
            #print(ropGreen)
    #results=cur.fetchall()
    conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)
    sqlQ = "SELECT * FROM material"
    cur=conn.cursor()
    cur.execute(sqlQ)
    rQuery=cur.fetchall()
    results=rQuery
    conn.close
    cornWLeft=rQuery[0]['Mcount']*10
    cheeseWLeft=rQuery[1]['Mcount']*10
    bananaWLeft=rQuery[2]['Mcount']*3
    blackWLeft=rQuery[3]['Mcount']*30
    greenWLeft=rQuery[4]['Mcount']*30
    #determine whether the material should be ordered
    #corn
    if cornWLeft>ropCorn:
        cornOrder=False
    else:
        cornOrder=True
    #cheese
    if cheeseWLeft>ropCheese:
        cheeseOrder=False
    else:
        cheeseOrder=True
    #banana
    if bananaWLeft>ropBanana:
        bananaOrder=False
    else:
        bananaOrder=True
    #black
    if blackWLeft>ropBlack:
        blackOrder=False
    else:
        blackOrder=True
    #green
    if greenWLeft>ropGreen:
        greenOrder=False
    else:
        greenOrder=True
    results[0].update({'orderOrNot':cornOrder})
    results[1].update({'orderOrNot':cheeseOrder})
    results[2].update({'orderOrNot':bananaOrder})
    results[3].update({'orderOrNot':blackOrder})
    results[4].update({'orderOrNot':greenOrder})
    results[0].update({'WLeft':cornWLeft})
    results[1].update({'WLeft':cheeseWLeft})
    results[2].update({'WLeft':bananaWLeft})
    results[3].update({'WLeft':blackWLeft})
    results[4].update({'WLeft':greenWLeft})
    cheeseArr=cornArr
    results[0].update({'deviation':math.ceil(statistics.stdev(cornArr)*3)})
    results[1].update({'deviation':math.ceil(statistics.stdev(cheeseArr)*3)})
    results[2].update({'deviation':math.ceil(statistics.stdev(bananaArr)*3)})
    results[3].update({'deviation':math.ceil(statistics.stdev(blackArr)*3)})
    results[4].update({'deviation':math.ceil(statistics.stdev(greenArr)*3)})
    return render(request,"om.inventory.html",{"material":results})

def orders(request):
    # 格式化成2016-03-20 11:45:39形式
    todayDate=datetime.datetime.now()
    i=0
    cornCheeseSum=0
    bananaSum=0
    blackSum=0
    greenSum=0
    cornArr=[]
    bananaArr=[]
    blackArr=[]
    greenArr=[]
    #corncheese
    while i < 30:
        conn = connect(
            host='localhost',
            port=3307,
            user='test08',
            password='xup6ji3hj/ ',
            database='test',
            charset='utf8',
            cursorclass=cursors.DictCursor)
        delta = datetime.timedelta(days=i)
        buyDate=todayDate-delta
        buyDate2=str(buyDate.strftime("%Y/%m/%d"))
        sqlQ1 = "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='CornCheese'"
        sqlQ2 = "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='Banana'"
        sqlQ3= "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='Black'"
        sqlQ4 = "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='Green'"
        cur=conn.cursor()
        cornCheeseSum+=cur.execute(sqlQ1)
        bananaSum+=cur.execute(sqlQ2)
        blackSum+=cur.execute(sqlQ3)
        greenSum+=cur.execute(sqlQ4)
        cornArr.append(cur.execute(sqlQ1))
        bananaArr.append(cur.execute(sqlQ2))
        blackArr.append(cur.execute(sqlQ3))
        greenArr.append(cur.execute(sqlQ4))
        i+=1
        conn.close
            #print("-------------")
            #print(buyDate)
            #print("corncheese",cornCheeseSum)
            #print("banana",bananaSum)
            #print("black",blackSum)
            #print("green",greenSum)
    averageCornCheese=cornCheeseSum/30
    averageBanana=bananaSum/30
    averageBlack=blackSum/30
    averageGreen=greenSum/30
            #print(averageCornCheese)
            #print(averageBanana)
            #print(averageBlack)
            #print(averageGreen)
    #rop=LTime*demand*the count which material could made
    ropCorn=math.ceil(averageCornCheese*1*10)
    ropCheese=math.ceil(averageCornCheese*1*10)
    ropBanana=math.ceil(averageBanana*1*3)
    ropBlack=math.ceil(averageBlack*3*30)
    ropGreen=math.ceil(averageGreen*3*30)
            #print(ropCorn)
            #print(ropCheese)
            #print(ropBanana)
            #print(ropBlack)
            #print(ropGreen)
    #results=cur.fetchall()
    conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)
    sqlQ = "SELECT Mcount FROM material"
    cur=conn.cursor()
    cur.execute(sqlQ)
    rQuery=cur.fetchall()
    cornWLeft=rQuery[0]['Mcount']*10
    cheeseWLeft=rQuery[1]['Mcount']*10
    bananaWLeft=rQuery[2]['Mcount']*3
    blackWLeft=rQuery[3]['Mcount']*30
    greenWLeft=rQuery[4]['Mcount']*30
    #determine whether the material should be ordered
    #corn
    if cornWLeft>ropCorn:
        cornOrder=False
    else:
        cornOrder=True
    #cheese
    if cheeseWLeft>ropCheese:
        cheeseOrder=False
    else:
        cheeseOrder=True
    #banana
    if bananaWLeft>ropBanana:
        bananaOrder=False
    else:
        bananaOrder=True
    #black
    if blackWLeft>ropBlack:
        blackOrder=False
    else:
        blackOrder=True
    #green
    if greenWLeft>ropGreen:
        greenOrder=False
    else:
        greenOrder=True
    results=[{'cornOrder':cornOrder,'cheeseOrder':cheeseOrder,'bananaOrder':bananaOrder,'blackOrder':blackOrder,'greenOrder':greenOrder}]
    #r=cur.execute("SELECT connS FROM material").fetchall()
    #if request.method == "POST" :
    cur.execute("SELECT connS FROM material")
    r=cur.fetchall()
    cornC=r[0]['connS']
    cheeseC=r[1]['connS']
    bananaC=r[2]['connS']
    blackC=r[3]['connS']
    greenC=r[4]['connS']
    #if request.method ==
    '''if(r[0]['connS']==0 or r[1]['connS']==0 or r[2]['connS']==0 or r[3]['connS']==0 or [4]['connS']==0):
        if cornOrder == True:
            if request.method=="post":
                cur.execute("UPDATE `material` SET `connS`=1 WHERE Mname= 'corn'")
        if cornOrder == True:
            if request.method=="post":
                cur.execute("UPDATE `material` SET `connS`=1 WHERE Mname= 'cheese'")
        if cornOrder == True:
            if request.method=="post":
                cur.execute("UPDATE `material` SET `connS`=1 WHERE Mname= 'banana'")
        if cornOrder == True:
            if request.method=="post":
                cur.execute("UPDATE `material` SET `connS`=1 WHERE Mname= 'blackTea'")
        if cornOrder == True:
            if request.method=="post":
                cur.execute("UPDATE `material` SET `connS`=1 WHERE Mname= 'greenTea'")
    else:
        if r[0]['connS']==1:
            cur.execute("UPDATE `material` SET `connS`=0 WHERE Mname= 'corn'")
            cur.execute("UPDATE `material` SET `Mcount`=3 WHERE Mname= 'corn'")
        if r[0]['connS']==1:
            cur.execute("UPDATE `material` SET `connS`=0 WHERE Mname= 'cheese'")
            cur.execute("UPDATE `material` SET `Mcount`=3 WHERE Mname= 'cheese'")
        if r[0]['connS']==1:
            cur.execute("UPDATE `material` SET `connS`=0 WHERE Mname= 'banana'")
            cur.execute("UPDATE `material` SET `Mcount`=3 WHERE Mname= 'banana'")
        if r[0]['connS']==1:
            cur.execute("UPDATE `material` SET `connS`=0 WHERE Mname= 'blackTea'")
            cur.execute("UPDATE `material` SET `Mcount`=3 WHERE Mname= 'blackTea'")
        if r[0]['connS']==1:
            cur.execute("UPDATE `material` SET `connS`=0 WHERE Mname= 'greenTea'")
            cur.execute("UPDATE `material` SET `Mcount`=3 WHERE Mname= 'greenTea'")'''
    cur.execute("SELECT * FROM supplier")
    r=cur.fetchall()
    a=r[0]['SName']
    b=r[0]['SPhone']
    c=r[1]['SName']
    d=r[1]['SPhone']
    e=r[2]['SName']
    f=r[2]['SPhone']
    g=r[3]['SName']
    h=r[3]['SPhone']
    i=r[4]['SName']
    j=r[4]['SPhone']
    cheeseArr=cornArr
    deviationCorn=math.ceil(statistics.stdev(cornArr)*3)
    deviationCheese=math.ceil(statistics.stdev(cheeseArr)*3)
    deviationBanana=math.ceil(statistics.stdev(bananaArr)*3)
    deviationBlack=math.ceil(statistics.stdev(blackArr)*3)
    deviationGreen=math.ceil(statistics.stdev(greenArr)*3)
    conn.close
    return render(request,"om.order.html",locals())

def all(request):
    #results=orders.objects.all()
    return render(request,"crm.salesanalysis.all.html")

def day(request):
    #results=orders.objects.all()
    conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)
    sql = "select o.date 日,count(Ordernumber) as 每日銷量, sum(o.Price) as 每日銷售額 from orders as o where year(o.date)=2020 or year(o.date)=2021 group BY o.date order by year(o.date) desc,month(o.date) desc,week(o.date) desc"
    cur=conn.cursor()
    cur.execute(sql)
    results=cur.fetchall()
    return render(request,"crm.salesanalysis.all.day.html",{"day":results})

def week(request):
    #results=orders.objects.all()
    conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)
    sql = "select year(o.date) 年, month(o.date) 月, week(o.date) 周,count(Ordernumber) as 每周銷量, sum(o.Price) as 每周銷售額 from orders as o where year(o.date)=2020 or year(o.date)=2021 group BY year(o.date) ,week(o.date) order by year(o.date) desc,month(o.date) desc,week(o.date) desc"
    cur=conn.cursor()
    cur.execute(sql)
    results=cur.fetchall()
    return render(request,"crm.salesanalysis.all.week.html",{"week":results})

def month(request):
    #results=orders.objects.all()
    conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)
    sql = "select year(o.date) 年, month(o.date) 月,count(Ordernumber) as 每月銷量, sum(o.Price) as 每月銷售額 from orders as o where year(o.date)=2020 or year(o.date)=2021 group BY year(o.date),month(o.date) order by year(o.date) desc,month(o.date) desc"
    cur=conn.cursor()
    cur.execute(sql)
    results=cur.fetchall()
    return render(request,"crm.salesanalysis.all.month.html",{"month":results})


def relevant(request):
    #results=orders.objects.all()
    return render(request,"crm.salesanalysis.relevant.html")

def total(request):
    #results=orders.objects.all()
    conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)
    sql = "select distinct buyItem pd, count(buyItem) bpd from orders group by pd order by bpd desc limit 4"
    cur=conn.cursor()
    cur.execute(sql)
    results=cur.fetchall()
    return render(request,"crm.salesanalysis.relevant.total.html",{"total":results})

def rday(request):
    #results=orders.objects.all()
    todayDate=datetime.datetime.now()
    i=0
    #corncheese
    results=[]
    conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)
    while i < 30:
        dictR={}
        delta = datetime.timedelta(days=i)
        buyDate=todayDate-delta
        buyDate2=str(buyDate.strftime("%Y/%m/%d"))
        cornCheeseSum=0
        bananaSum=0
        blackSum=0
        greenSum=0
        sqlQ1 = "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='CornCheese'"
        sqlQ2 = "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='Banana'"
        sqlQ3= "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='Black'"
        sqlQ4 = "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='Green'"
        cur=conn.cursor()
        cornCheeseSum+=cur.execute(sqlQ1)
        bananaSum+=cur.execute(sqlQ2)
        blackSum+=cur.execute(sqlQ3)
        greenSum+=cur.execute(sqlQ4)
        dictR={'date':buyDate2,'B':bananaSum,'C':cornCheeseSum,'BL':blackSum,'GR':greenSum}
        results.append(dictR)
        i+=1
    conn.close
    return render(request,"crm.salesanalysis.relevant.rday.html",{"rData":results})

def rweek(request):
    #results=orders.objects.all()
    todayDate=datetime.datetime.now()
    i=0
    #corncheese
    results=[]
    conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)
    while i < 5:
        j=0
        cornCheeseSum=0
        bananaSum=0
        blackSum=0
        greenSum=0
        while j<7:
            dictR={}
            delta = datetime.timedelta(days=4*i+j)
            buyDate=todayDate-delta
            buyDate2=str(buyDate.strftime("%Y/%m/%d"))
            sqlQ1 = "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='CornCheese'"
            sqlQ2 = "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='Banana'"
            sqlQ3= "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='Black'"
            sqlQ4 = "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='Green'"
            cur=conn.cursor()
            cornCheeseSum+=cur.execute(sqlQ1)
            bananaSum+=cur.execute(sqlQ2)
            blackSum+=cur.execute(sqlQ3)
            greenSum+=cur.execute(sqlQ4)
            j+=1
        dictR={'date':buyDate2,'B':bananaSum,'C':cornCheeseSum,'BL':blackSum,'GR':greenSum}
        results.append(dictR)
        i+=1
    conn.close
    return render(request,"crm.salesanalysis.relevant.rweek.html",{"rData":results})

def rmonth(request):
    #results=orders.objects.all()
    todayDate=datetime.datetime.now()
    i=0
    #corncheese
    results=[]
    conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)
    while i < 12:
        j=0
        cornCheeseSum=0
        bananaSum=0
        blackSum=0
        greenSum=0
        days=0
        if i == 1 or i == 3 or i == 5 or i == 7 or i == 8 or i == 10 or i == 12:
            days=31
        elif i ==2:
            days=28
        else:
            days=30
        while j<days:
            dictR={}
            delta = datetime.timedelta(days=days*i+j)
            buyDate=todayDate-delta
            buyDate2=str(buyDate.strftime("%Y/%m/%d"))
            sqlQ1 = "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='CornCheese'"
            sqlQ2 = "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='Banana'"
            sqlQ3= "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='Black'"
            sqlQ4 = "SELECT * FROM orders WHERE date='"+buyDate2+"' AND buyItem='Green'"
            cur=conn.cursor()
            cornCheeseSum+=cur.execute(sqlQ1)
            bananaSum+=cur.execute(sqlQ2)
            blackSum+=cur.execute(sqlQ3)
            greenSum+=cur.execute(sqlQ4)
            j+=1
        dictR={'date':buyDate2,'B':bananaSum,'C':cornCheeseSum,'BL':blackSum,'GR':greenSum}
        results.append(dictR)
        i+=1
    conn.close
    return render(request,"crm.salesanalysis.relevant.rmonth.html",{"rData":results})

def actives(request):
    sqlQ1="select c.cPhonenum id,c.cName 名字,max(o.date) R,count(distinct o.date) F,sum(o.Price) M, case when DATEDIFF(CURRENT_DATE(),max(o.date))<7 and count(distinct o.date)>=4 and sum(o.Price)>400 then 111 when DATEDIFF(CURRENT_DATE(),max(o.date))<7 and count(distinct o.date)>=4 and sum(o.Price)<=400 then 112 when DATEDIFF(CURRENT_DATE(),max(o.date))<7 and count(distinct o.date)<4 and sum(o.Price)<=400 then 122 when DATEDIFF(CURRENT_DATE(),max(o.date))<7 and count(distinct o.date)<4 and sum(o.Price)>400 then 121 when DATEDIFF(CURRENT_DATE(),max(o.date))>=7 and count(distinct o.date)>=4 and sum(o.Price)>400 then 211 when DATEDIFF(CURRENT_DATE(),max(o.date))>=10 and count(distinct o.date)<4 and sum(o.Price)>400 then 221 when DATEDIFF(CURRENT_DATE(),max(o.date))>=7 and count(distinct o.date)>=7 and sum(o.Price)<=400 then 212 else 222 end as 顧客分群 from Customer as c inner join Orders as o on c.cPhonenum=o.cPhonenum group by c.cPhonenum order by 顧客分群, R desc, F desc, M DESC"
    conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)
    cur=conn.cursor()
    cur.execute(sqlQ1)
    results01=cur.fetchall()
    #results=orders.objects.all()
    results=[]
    for getdata in results01:
        if getdata['顧客分群']==111 or getdata['顧客分群']==112:
            results.append(getdata)
    return render(request,"crm.rfm.actives.html",{"rfm":results})

def potential(request):
    sqlQ1="select c.cPhonenum id,c.cName 名字,max(o.date) R,count(distinct o.date) F,sum(o.Price) M, case when DATEDIFF(CURRENT_DATE(),max(o.date))<7 and count(distinct o.date)>=4 and sum(o.Price)>400 then 111 when DATEDIFF(CURRENT_DATE(),max(o.date))<7 and count(distinct o.date)>=4 and sum(o.Price)<=400 then 112 when DATEDIFF(CURRENT_DATE(),max(o.date))<7 and count(distinct o.date)<4 and sum(o.Price)<=400 then 122 when DATEDIFF(CURRENT_DATE(),max(o.date))<7 and count(distinct o.date)<4 and sum(o.Price)>400 then 121 when DATEDIFF(CURRENT_DATE(),max(o.date))>=7 and count(distinct o.date)>=4 and sum(o.Price)>400 then 211 when DATEDIFF(CURRENT_DATE(),max(o.date))>=10 and count(distinct o.date)<4 and sum(o.Price)>400 then 221 when DATEDIFF(CURRENT_DATE(),max(o.date))>=7 and count(distinct o.date)>=7 and sum(o.Price)<=400 then 212 else 222 end as 顧客分群 from Customer as c inner join Orders as o on c.cPhonenum=o.cPhonenum group by c.cPhonenum order by 顧客分群, R desc, F desc, M DESC"
    conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)
    cur=conn.cursor()
    length=cur.execute(sqlQ1)
    cur.execute(sqlQ1)
    results01=cur.fetchall()
    #results=orders.objects.all()
    results=[]
    for getdata in results01:
        if getdata['顧客分群']==121 or getdata['顧客分群']==212:
            results.append(getdata)

    return render(request,"crm.rfm.potential.html",{"rfm":results})

def customer1(request):
    #esults=orders.objects.all()
    conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)
    sql = "SELECT c.CPhonenum id, c.Cname 名字, o.date 購買日期,o.buyItem 購買品項, o.price 金額, o.Ordernumber 購物編號 FROM customer as c inner join orders as o on c.CPhonenum=o.CPhonenum where c.cPhonenum=0911111111 ORDER BY 購買日期 DESC,購物編號 DESC"
    cur=conn.cursor()
    cur.execute(sql)
    results=cur.fetchall()
    return render(request,"crm.salesrecord.customer.1.html",{"customer1":results})

def customer(request):
    #esults=orders.objects.all()
    '''conn = connect(
        host='localhost',
        port=3307,
        user='test08',
        password='xup6ji3hj/ ',
        database='test',
        charset='utf8',
        cursorclass=cursors.DictCursor)
    cur=conn.cursor()
    command="select * from orders where CPhonenum=%d order by date DESC"
    cursor.execute(command,(search_ppl))
    results=cursor.fetchall()'''
    return render(request,"crm.salesrecord.customer.html")

def analysis(request):
    #results=orders.objects.all()
    return render(request,"crm.broadcast.analysis.html")

'''def predict(request):
    results=orders.objects.all()
    return render(request,"predict.html",{"orders":results})'''
#預測
def predict(request):
    results=orders.objects.all()
    return render(request,"predict.html",{"orders":results})

#POS
def posSite(request):
    return render(request,"posSite.html")

#predict
#def ROPCalculate():
