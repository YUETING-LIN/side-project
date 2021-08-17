from bs4 import BeautifulSoup 
from selenium import webdriver
import requests
import re
import numpy as np
import MySQLdb
import time
import random
#----------------爬蟲基礎設定-------------------------------
proxy_ips=["202.102.86.228:8080"]

url="https://www.oldsichuan.com.tw/official/location/all"
html=requests.get(url)
html.encoding='utf-8'
bs=BeautifulSoup(html.text,"html.parser")
#----------------mysql基礎設定-------------------------
conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='12345678',
        db ='webtest1',
        charset= "utf8"
        )
#-------------------------------------------------------
def data1(num,str0,str1,modificationlist):#原始資料整理
   
    i=0
    deletelist.clear()    
    for item in modificationlist:
        temp=item.encode('utf-8').decode('utf-8')
        
        firstsearch=re.search(str0,temp)
        if (firstsearch!=None) and (i+num < modificationlist.size):#先做分店的搜尋，與防止i(索引)超過shoplist的長度
            temp1=shoplist[i+num].encode('utf-8').decode('utf-8') 
            secondsearch=re.match(str1,temp1)
            if secondsearch==None: #每筆資料格式為五筆一分店，故以i+5作為判別，若為none代表資料筆數超過5筆
                deletelist.append(i+num) #紀錄非五筆一分店的資料,deletelist內的值為要刪除的索引
                i=i+1
            else:  
                i=i+1
        else:
            i=i+1    
    return deletelist
#-----------------------------------------------------
def addrcut(targetlist,num,addrINlist):#(地址的list,迴圈控制值,地址的List間隔)
    insertstr=targetlist[num+addrINlist]   
    store_str,googlestr =addrcheck(insertstr)#店家的地址與GOOGLE的地址
    
    store_str=store_str.encode('utf-8').decode('utf-8')
    googlestr=googlestr.encode('utf-8').decode('utf-8')
    addressstr=u"([\w\W\u4e00-\u9fff]{1,3}[\\u7e23\\u93ae\\u9109\\u5e02\\u5340]{1,2})"   #地址切割 
    storelist=re.split(addressstr,store_str,3)
    addresslist=re.split(addressstr,googlestr,3)
    addresslist[-1]=storelist[-1]#最後以google提供的"縣市"+店家提供的"其餘地址"
    
    return addresslist
#-----------------地址驗證系統-------------------------------
def addrcheck(addrstr):
    url="https://www.google.com.tw/maps/place/"
    
    if "：" in addrstr:#是否有檢查傳入句中是否有":"
        addrstr=re.sub("："," ",addrstr)
    if ("市" in addrstr and "區" in addrstr )or("縣" in addrstr and "鄉" in addrstr )or("縣" in addrstr and "市" in addrstr )or("縣" in addrstr and "鎮" in addrstr ):
        insertstr=addrstr.encode('utf-8').decode('utf-8')
        addressstr=u"([^0-9][\w\W\u4e00-\u9fff]{1,2}[\\u7e23\\u93ae\\u9109\\u5e02\\u5340]{1}.*)"
    elif("市" in addrstr):
        insertstr=addrstr.encode('utf-8').decode('utf-8')
        addressstr=u"([^0-9][\w\W\u4e00-\u9fff]{1,2}[\\u7e23\\u93ae\\u9109\\u5e02\\u5340]{1}.*)"
    else:
        insertstr=addrstr.encode('utf-8').decode('utf-8')
        addressstr=u"([^0-9][\w\W\u4e00-\u9fff]{1,5}[\\u7e23\\u93ae\\u9109\\u5e02\\u5340]{1}.*)"
    store_str=re.search(addressstr,insertstr).group().strip()#傳入句整理成"縣市鄉政之排列隔式"
      
    url=url+store_str
   
    #ip=random.choice(proxy_ips)#隱藏IP位置
    #resp=requests.get(url,proxies={"http":"http://"+ip})
    html=requests.get(url)
    time.sleep(2)
    html.encoding='utf-8'
    bs=BeautifulSoup(html.text,"html.parser")
   
    for tag in bs.select("meta") :
        if tag.get("property",None)=="og:title":
             insertstr=tag.get("content")#採用google地址,將值回存
             
    if insertstr =="Google Maps":  # store_str抓不到值的話用SE再跑一次     
        driver=webdriver.Chrome("chromedriver")
        driver.implicitly_wait(5)
        driver.get("https://www.google.com.tw/maps/place/")
        element=driver.find_element_by_id("searchboxinput")
        element.send_keys(store_str)
        driver.find_element_by_id("searchbox-searchbutton").click()
        time.sleep(7)
        bs=BeautifulSoup(driver.page_source,"html.parser")
        insertstr=bs.find("div",{"class":"QSFF4-text gm2-body-2"}).text
   
        insertstr=insertstr.encode('utf-8').decode('utf-8')
        addressstr=u"([^0-9][\w\W\u4e00-\u9fff]{1,2}[\\u7e23\\u93ae\\u9109\\u5e02\\u5340]{1}.*)"
        googlestr=re.search(addressstr,insertstr).group().strip()  #回存值去郵遞區號
        driver.quit()
    else:  
        insertstr=insertstr.encode('utf-8').decode('utf-8')
        addressstr=u"([\w\W\u4e00-\u9fff]{1,2}[\\u7e23\\u93ae\\u9109\\u5e02\\u5340]{1}.*)"
        googlestr=re.search(addressstr,insertstr).group().strip() 
 
    return store_str,googlestr 
#------電話檢查--------------------------
def telcheck(targetlist,num,addrINlist):
    telstr=targetlist[num+addrINlist] 
    telcheckstr="(\d{2,3}-\d{7,8}$)"#有槓
    telcheckstr2="(\d{2,3}\d{7,8}$)"#沒槓
    if re.search(telcheckstr,telstr)!=None:#有槓
        telstr=re.search(telcheckstr,telstr).group()
    else:    
        telstr=re.search(telcheckstr2,telstr).group()#沒槓
    return telstr
#-----------------------------------------------
def timetoint(opstr):#(時間轉換數字)
    timeint.clear()
    opstr=checkword(opstr)
    restr="([APM]{0,2}\s?[0-9]{2}:[0-9]{2})"  
    results=re.findall(restr,opstr)
    
    if "PM" in opstr and "AM" in opstr:#12小時
        for result in results:
            pattern=re.compile("\s")
            result=re.sub(pattern,"",result)
            temp=int(result[2:4])+12
            if result[0:2]=="PM" and temp<24:
                result=result.replace(result[2:4],str(temp))
            timeString = "1990-01-01 "+result # 時間格式為字串
            struct_time = time.strptime(timeString, "%Y-%m-%d %p%H:%M" )
            time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
            timeint.append(time_stamp)
        
        for i in range(0,len(timeint),2):  #檢查是否結束時間小於開始時間
            if i+1<len(timeint) and timeint [i]> timeint [i+1] :#i+1<len(timeint)(防止後面i+1超過陣列長度)
                result=re.sub(pattern,"",results[i+1])    
                timeString = "1990-01-02 "+result # 時間格式為字串
                struct_time = time.strptime(timeString, "%Y-%m-%d %p%I:%M") # 轉成時間元組
                time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
                timeint[i+1]=time_stamp
       
        
    elif "AM" in opstr and "AM" in opstr : 
        for result in results:
            pattern=re.compile("\s")
            result=re.sub(pattern,"",result)
            
            timeString = "1990-01-01 "+result # 時間格式為字串
            struct_time = time.strptime(timeString, "%Y-%m-%d %p%H:%M" )
            time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
            timeint.append(time_stamp)
        
        for i in range(0,len(timeint),2):  #檢查是否結束時間小於開始時間
            if i+1<len(timeint) and timeint [i]> timeint [i+1] :#i+1<len(timeint)(防止後面i+1超過陣列長度)
                result=re.sub(pattern,"",results[i+1])    
                timeString = "1990-01-02 "+result # 時間格式為字串
                struct_time = time.strptime(timeString, "%Y-%m-%d %p%H:%M") # 轉成時間元組
                time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
                timeint[i+1]=time_stamp
        
    else:
        for result in results:#24小時
            timeString = "1990-01-01 "+ result # 時間格式為字串
            struct_time = time.strptime(timeString, "%Y-%m-%d %H:%M" ) # 轉成時間元組
            time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
            timeint.append(time_stamp)
        for i in range(0,len(timeint),2):  #檢查是否結束時間小於開始時間
            if i+1<len(timeint) and timeint [i]> timeint [i+1] :#i+1<len(timeint)(防止後面i+1超過陣列長度)
                timeString = "1990-01-02 "+ results[i+1] # 時間格式為字串
                struct_time = time.strptime(timeString, "%Y-%m-%d %H:%M") # 轉成時間元組
                time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
                timeint[i+1]=time_stamp    

    return timeint
#--------------------------------------------
def openhour(opstr):#(數字轉換可用餐營業時間字串)
    temp=""
    timeint=timetoint(opstr)
    
    if timeint !=[]:
         if timeint[-1]<timeint[-2] and timeint[-1]>timeint[-3]:#最後點餐判別
            timeint[-2]=timeint[-1]
       
    else:
        finaloph="" 
        return finaloph
    
    for i in range(0,len(timeint)-1,2): #生成可用餐時間字串
        for i in range(timeint[i],timeint[i+1],1800):
           struct_time = time.localtime(i) # 轉成時間元組
           timeString = time.strftime( "%H:%M", struct_time) # 轉成字串
           temp=temp+" "+timeString
           finaloph=temp.strip().replace(" ", ",")
          
    return finaloph
#-----------------------------------------------
def checkword(opstr):#(營業時間句子判斷)
    insertstr=opstr.encode('utf-8').decode('utf-8')
    checkstr=u"(\\u5916\\u5e36.*)"#是否含有外帶
    checklist=re.split(checkstr,insertstr)
  
    if len(checklist)>1:
        for item in checklist:
            if item != re.search(checkstr,insertstr).group():
                if item!="":
                    newstr=item
    else:    
        newstr=checklist[0]

    return newstr
#-----------------------------------------------
def convert(opstr):#(星期轉換)
    newstr=checkword(opstr)
    neweeklist=[]
    insertstr=newstr.encode('utf-8').decode('utf-8')
    checkstr1=u"([\\u4e00\\u4e8c\\u4e09\\u56db\\u4e94\\u516d\\u65e5\\u9031\\u5468\\u672b\\u5929\\u661f\\u671f']{0,3}～.)"#一二三四五六日週周末天星期至
    checkstr2=u"([\\u4e00\\u4e8c\\u4e09\\u56db\\u4e94\\u516d\\u65e5\\u9031\\u5468\\u672b\\u5929\\u661f\\u671f\\u81f3']{4,5})"
    checkstr3=u"([0-9]{2}:[0-9]{2})" 
    checkpoint1=re.findall(checkstr1, insertstr)
    checkpoint2=re.findall(checkstr2, insertstr)
    checkpoint3=re.findall(checkstr3, insertstr)
    if checkpoint1 !=[] :#檢查是否有一~日
       for item in checkpoint1:
           if item in weekconvert.keys():
             neweeklist=weekconvert[item]
       
    elif checkpoint2 !=[]:
        for item in checkpoint2:
           if item in weekconvert.keys():
             neweeklist=weekconvert[item]
    
    elif checkpoint3 !=[]:#檢查是否有時間
         neweeklist=weekconvert["allweek"]
        
    else:
        neweeklist=""
      
    return neweeklist  
#--------
def finalophlist(targetlist,num):#(targetlist=有營業時間的表,num=每一筆的間隔)
    i=0 
    for item in targetlist:
        if i%num==0:#寫入店名
            insertlist.append(targetlist[i])
        if convert(item)!="":#寫入星期與時間
            
            insertlist.append(convert(item))
            insertlist.append(openhour(item))
        i=i+1  
    return   insertlist     
#------新增營業時間表---------- 
def insert_OPHlist(title,insertlist,num):#(title=店名,insertlist=有營業時間的表)
    #最終的營業時間表
    insertlist=finalophlist(insertlist,num)
    
    #資料庫的值與ophlist相比若相同進行寫入
    with conn.cursor() as cursor:#抓資料庫address表 資料
        command ="SELECT `ID`, `restName` FROM `restrauntdata` WHERE `restName`= %s"
        cursor.execute(command,(title,))
        dbdata=cursor.fetchone()
    with conn.cursor() as cursor:#抓資料庫address表 資料
        command ="SELECT `ID`, `branchName` FROM `r_restrauntaddress1` WHERE `restraunt_id`= %s"
        cursor.execute(command,(dbdata[0],))
        dbaddresslist=cursor.fetchall()
    # 新增資料庫中openhourlist1表 
      
    with conn.cursor() as cursor:
        for item in dbaddresslist:
            for index in range(len(insertlist)):  
                if item[1] == insertlist[index]:#資料庫地址表與insertlist比較店名
                    if len(insertlist[index+1])==7:#確認下一筆資料有七筆星期資料
                        for weekitem in insertlist[index+1]:
                           try:
                               command="REPLACE INTO `r_openinghours1`(`Address_ID`, `week`, `time`) VALUES (%s,%s,%s)"
                               cursor.execute(command,(item[0],weekitem,insertlist[index+2]))
                               conn.commit() 
                           except Exception as ex:
                               print(ex,item[1])
                    elif len(insertlist[index+1])+len(insertlist[index+3])==7:
                        for weekitem in insertlist[index+1]:
                           try:
                               command="REPLACE INTO `r_openinghours1`(`Address_ID`, `week`, `time`) VALUES (%s,%s,%s)"
                               cursor.execute(command,(item[0],weekitem,insertlist[index+2]))
                               conn.commit() 
                           except Exception as ex:
                               print(ex,item[1])
                        for weekitem in insertlist[index+3]:
                           try:
                               command="REPLACE INTO `r_openinghours1`(`Address_ID`, `week`, `time`) VALUES (%s,%s,%s)"
                               cursor.execute(command,(item[0],weekitem,insertlist[index+4]))
                               conn.commit() 
                           except Exception as ex:
                               print(ex,item[1]) 
                           
                    print("營業時間建立完成")                                
#-------新增分店-------
def insertaddresslist(title,shoplist,listblank,addrblank,telblank):#(title=店名,shoplist=有地址電話的表,listblank=每一分店有幾筆資料,addrblank=地址的排序,telblank=電話的排序)
    with conn.cursor() as cursor:#抓資料庫address表 資料
        command ="SELECT `ID`, `restName` FROM `restrauntdata` WHERE `restName`= %s"
        cursor.execute(command,(title,))
        dbdata=cursor.fetchone()
    
    #-------新增資料庫中r_restrauntaddress1-------
    for index in range(0,shoplist.size,listblank):#執行寫入r_restrauntaddress1`
        with conn.cursor() as cursor:
            try:
                cutaddr=addrcut(shoplist,index,addrblank)
                telstr=telcheck(shoplist,index,telblank)
                command="INSERT INTO `r_restrauntaddress1`(`branchName`, `restraunt_id`, `county`, `area`, `elseAddress`, `tel`) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(command,(shoplist[index],dbdata[0],cutaddr[1],cutaddr[3],cutaddr[4],telstr))
                conn.commit()
            except Exception as ex:
                print(ex)    
    print("分店新增完成")
#-----------屬性區-------------
addresslist=[]
telstr=""
timeint=[]
finaloph=""
newstr=""
neweeklist=[]
insertlist=[]
weekconvert={"周六周日":['SAT','SUN'],"周一至五":['MON','TUE','WED','THU','FRI'],"日～四":['SUN','MON','TUE','WED','THU'],"五～六":['FRI','SAT'],"allweek":['SUN','MON','TUE','WED','THU','FRI','SAT']}
shoplist=[]
openhourlist=[]

#爬蟲--------------------------

#創建店家資訊表
for item in bs.find_all("div",{"class":"va-set shop_info_pad hiroki-u-ss-1-1 pure-u-sm-1-1 pure-u-md-24-24 pure-u-lg-8-24"}):#OK
   shoplist.append(item.text.strip())
templist=[]
for i in shoplist:
    splitstr=i.split('\n',4)
    for item in splitstr:
        temp=item.strip()
        if temp!="":
            templist.append(temp)

shoplist=np.array(templist)#轉換np  
templist.clear()
#不規則資料整理----------------------------------
title="老四川" 
firststr=u"(^[\w\W\u4e00-\u9fff]{2,6}\\u5e97)"
deletelist=[]
elsestore=[]
for index in range(0,shoplist.size,4):
    temp=shoplist[index].encode('utf-8').decode('utf-8')
    checkitem=re.findall(firststr,temp)
    if checkitem==[]:#分店名 檢查
        for a in range(4):#一店為4筆資料
            deletelist.append(index+a)
                
for index in deletelist:
    elsestore.append(shoplist[index])
shoplist= np.delete(shoplist, deletelist)


#營業時間表 -----------------------(重新整理營業時間，每句內不包含兩個星期區間)
checkstr=u"([\\u5468{2}\\u4e00\\u4e8c\\u4e09\\u56db\\u4e94\\u516d\\u65e5\\u9031\\u5468\\u672b\\u5929\\u661f\\u671f\\u81f3']{3,4}.{15,40})"    
for index in range(0,shoplist.size,4):  
    openhourlist.append(shoplist[index])
    insertstr=shoplist[index+3].encode('utf-8').decode('utf-8')      
    pattern=re.compile("\u3000")#句內有空白刪除整理
    insertstr=re.sub(pattern,"", insertstr)
    checklist=re.split(checkstr,insertstr)

    if len(checklist) <2:#若符合checkstr判斷標準者,checklist長度必定大於2以上
        openhourlist.append(shoplist[index+3])
        openhourlist.append("")
    else:
        for item in  checklist:
            insertstr=item.encode('utf-8').decode('utf-8') 
            checkstr2=u"([\\u4e00\\u4e8c\\u4e09\\u56db\\u4e94\\u516d\\u65e5\\u9031\\u5468\\u672b\\u5929\\u661f\\u671f\\u81f3']{4,5})" 
            checklist1=re.findall(checkstr2,insertstr)
            if checklist1!=[]:
                openhourlist.append(item)

#-----執行新增---------


#店名,資料表,資料間隔,地址排序,電話排序      
#insertaddresslist(elsestore[0],aa,4,2,1)
#店名,資料表,營業時間排序
#insert_OPHlist(aa[0],aa,4) 













