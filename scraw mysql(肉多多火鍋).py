from bs4 import BeautifulSoup 
import requests
import re
import numpy as np
import MySQLdb
import time
#----------------爬蟲基礎設定-------------------------------
url="https://www.twrododo.com/pages/%E9%96%80%E5%BA%97%E8%B3%87%E8%A8%8A"
html=requests.get(url)
html.encoding='utf-8'
bs=BeautifulSoup(html.text,"html.parser")
data=bs.select(".ckeditor")
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
    insertstr=targetlist[num+addrINlist].encode('utf-8').decode('utf-8')   
    addressstr=u"([\w\W\u4e00-\u9fff]{1,3}[\\u7e23\\u93ae\\u9109\\u5e02\\u5340]{1,2})"   #地址切割 
    addresslist=re.split(addressstr,insertstr,2)
    return addresslist
#-----------------------------------------------
def timetoint(opstr):#(時間轉換數字)
    timeint.clear()
    opstr=checkword(opstr)
    restr="([0-9]{2}:[0-9]{2})"  
    results=re.findall(restr,opstr)
    for result in results:
        timeString = "1990-01-01 "+ result # 時間格式為字串
        struct_time = time.strptime(timeString, "%Y-%m-%d %H:%M") # 轉成時間元組
        time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
        timeint.append(time_stamp)
   
    return timeint
#--------------------------------------------
def openhour(opstr):#(數字轉換可用餐營業時間字串)
    a1=""
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
           a1=a1+" "+timeString
           finaloph=a1.strip().replace(" ", ",")
          
    return finaloph
#-----------------------------------------------
def checkword(opstr):#(營業時間句子判斷)
    insertstr=opstr.encode('utf-8').decode('utf-8')
    checkstr=u"(\\u5916\\u5e36.*)"
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
def convert(opstr):
    
    newstr=checkword(opstr)
    insertstr=newstr.encode('utf-8').decode('utf-8')
    checkstr=u"([\\u4e00\\u4e8c\\u4e09\\u56db\\u4e94\\u516d\\u65e5\\u9031\\u5468\\u672b\\u5929\\u661f\\u671f']{0,3}～.)"
    checkpoint1=re.findall(checkstr, insertstr)
    checkstr2=u"([0-9]{2}:[0-9]{2})" 
    checkpoint2=re.findall(checkstr2, insertstr)
    if checkpoint1 !=[]:#檢查是否有一~日
       for item in checkpoint1:
           if item in weekconvert.keys():
             neweeklist=weekconvert[item]
     
    elif checkpoint2 !=[]:#檢查是否有時間
         neweeklist=weekconvert["allweek"]
    else:
        neweeklist=""
    return neweeklist          


#爬蟲--------------------------
shoplist=[]
openhourlist=[]
#創建店家資訊表
for n in data[0].find_all("li"):
    shoplist.append(n.text.strip())
#營業時間表   
for tt in bs.find_all(("span")):
    if"鍋" in tt.text:
        openhourlist.append(tt.text.strip())#新增至表前切除空白
    if"內用" in tt.text: 
        openhourlist.append(tt.text.strip()) 
#轉換np-----------------------------------
shoplist.insert(144,"無意義填充值")
shoplist.insert(145,"無意義填充值")
shoplist[174]="高雄市楠梓區德民路836號1樓"

#不規則資料整理----------------------------------
shoplist=np.array(shoplist)
openhourlist.insert (89,"內用｜12:00-20:00 (外帶最後點餐19:30)") #numpyinsert函數無反應，暫時先由list新增 
openhourlist=np.array(openhourlist)
deletelist=[0,1,18]
openhourlist = np.delete(openhourlist, deletelist)
openhourlist[17]="五～六 11:00-22:00（內用最後點餐21:00、外帶最後點餐21:00）"

#word="店" \\u5e97
#ucord=word.encode('unicode_escape')

firststr=u"(^[\w\W\u4e00-\u9fff]{4,6}\\u5e97【)" #用(xxxx店【)的搜尋
secondstr =u"(^[\w\W\u4e00-\u9fff]{4,6}\\u5e97.*?】)"#用(xxxx店【XXX】)的搜尋
deletelist=[]

while True:
    shoplist = np.delete(shoplist, data1(5,firststr,secondstr,shoplist))
    if data1(5,firststr,secondstr,shoplist)==[]:
       break

title="肉多多火鍋"    
#---r_restrauntaddress1`--------------------------- 
addresslist=[]
#抓店名的ID
'''
with conn.cursor() as cursor:#抓資料庫address表 資料
    command ="SELECT `ID`, `restName` FROM `restrauntdata` WHERE `restName`= %s"
    cursor.execute(command,(title,))
    dbdata=cursor.fetchone()
'''
'''             
for index in range(0,shoplist.size,5):#執行寫入r_restrauntaddress1`
    with conn.cursor() as cursor:
        cutaddr=addrcut(shoplist,index,1)
        command="INSERT INTO `r_restrauntaddress1`(`branchName`, `restraunt_id`, `county`, `area`, `elseAddress`, `tel`) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(command,(shoplist[index],dbdata[0],cutaddr[1],cutaddr[3],cutaddr[4],shoplist[index+2]))
        conn.commit()
'''   
'''
#地址驗證系統
aa="新竹市科學園區工業東二路1號 "   
url="https://www.google.com.tw/maps/place/"
url=url+aa

html=requests.get(url)
html.encoding='utf-8'
bs=BeautifulSoup(html.text,"html.parser")
print()
data=bs.select("meta") 
print(data[6])   
'''
# r_openinghours1------------

timeint=[]
finaloph=""
newstr=""
neweeklist=[]
insertlist=[]
i=0
weekconvert={"日～四":['SUN','MON','TUE','WED','THU'],"五～六":['FRI','SAT'],"allweek":['SUN','MON','TUE','WED','THU','FRI','SAT']}

#整理原始字串
#word="外帶"
#ucord=word.encode('unicode_escape')

#最終的插入表
for item in openhourlist:
    if i%3==0:#寫入店名
        insertlist.append(openhourlist[i])
    if convert(item)!="":#寫入星期與時間
        insertlist.append(convert(item))
        insertlist.append(openhour(item))
    i=i+1  
      
'''
#資料庫的值與ophlist相比若相同進行寫入
with conn.cursor() as cursor:#抓資料庫address表 資料
    command ="SELECT `ID`, `branchName` FROM `r_restrauntaddress1` WHERE `restraunt_id`= %s"
    cursor.execute(command,('2',))
    dbaddresslist=cursor.fetchall()
    
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

'''   

    
'''#舊寫法
#deletelist=[10,16,22,28,39,45,51,57,68,74,85,96,117,118,124,129,156,162]
#shoplist = np.delete(shoplist, deletelist)

#np.insert(openhourlist,86,"內用｜12:00-20:00 (外帶最後點餐19:30)")  
"""
for n in range(0,openhourlist.size,3):
    print(openhourlist[n]) 
 
"""
  

shoplist.pop(10),shoplist.pop(15),shoplist.pop(20),shoplist.pop(25),shoplist.pop(41),shoplist.pop(35),shoplist.pop(51),shoplist.pop(61)
shoplist.pop(66),shoplist.pop(76),shoplist.pop(86),shoplist.pop(106),shoplist.pop(106)
shoplist.pop(111),shoplist.pop(115),shoplist.pop(141),shoplist.pop(148)

del openhourlist[0:2]
openhourlist[18]="五~六 11:00-22:00（內用最後點餐21:00、外帶最後點餐21:00）"
openhourlist.insert (84,"內用｜12:00-20:00 (外帶最後點餐19:30)")  
openhourlist[17]=openhourlist[17]+openhourlist[18]
openhourlist.pop(18)
'''
        












