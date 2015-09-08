#!/usr/bin/python


import urllib
import xml.etree.ElementTree as etree
import sys, datetime as dt, time



def openUrl(url):
  try:
    uHandle=urllib.urlopen(url)
  except:
    print "Error open url: "+url
    return('neok')
  else:
    data=uHandle.read(uHandle)
    uHandle.close()
    return(data)

def getCase(uInput):
  if uInput.startswith('--'):
    if uInput.find('=')>=0:
      (key,value)=uInput.split('=')
      return({'key':key,'value':value})
    else:
      key=uInput
      value=True
      return({'key':key,'value':value})
  else:
    return(-1)

def getValuesYandex(data,uCity,uCmdList,uTime,uDateTime):
  ns,url=setUrl(uCity)
  answer=[]
  if data!='neok':
    try:
      root=etree.fromstring(data)
    except:
      return('City '+uCity+' not found ('+url+')');
    else:
      parsed_head=root.attrib
      city=parsed_head['city']
      eng_city=parsed_head['slug']
      country=parsed_head['country']
      dist=parsed_head['part']
      if uTime!='fact':
        uDate=uTime
        uTime='day'
      else:
        uDate=False
      for uTree in root.findall('site:'+uTime,ns):
        if uDate:
          if uTree.attrib['date']==uDate:
            for dPart in uTree.findall('site:day_part',ns):
              ico=dPart.find('site:image-v3',ns)
              weather=dPart.find('site:weather_type',ns)
              wind_dir=dPart.find('site:wind_direction',ns)
              wind_spd=dPart.find('site:wind_speed',ns)
              if dPart.attrib['type']==uDateTime.lower():
                for temps in dPart.find('site:temperature-data',ns):
                  if temps.tag.endswith('avg'):
                    temp=temps
        else:
          temp=uTree.find('site:temperature',ns)
          ico=uTree.find('site:image-v3',ns)
          weather=uTree.find('site:weather_type',ns)
          wind_dir=uTree.find('site:wind_direction',ns)
          wind_spd=uTree.find('site:wind_speed',ns)


    for cmd in uCmdList:
      if cmd=='temp':
        answer.append('temp:'+temp.text)
      if cmd=='type':
        answer.append('type:'+weather.text)
      if cmd=='icon':
        answer.append('icon:'+ico.text)
    answer.append('city:'+city)
    return(answer)

def setUrl(city):
  ns={'site':'http://weather.yandex.ru/forecast'}
  if city:
    url='http://export.yandex.ru/weather-ng/forecasts/'+city+'.xml'
    return(ns,url)
  else:
    url='http://export.yandex.ru/weather-ng/forecasts/28440.xml'
    return(ns,url)

city=None;
date='fact'
outAnswer=[];
cmdList=[]
out=''
today = dt.date.today()
tomorrow = dt.date.today()+dt.timedelta(+1)
dateTime='day'

args=sys.argv
selfName=args[0]
args.pop(0)
if len(args)==0:
  print 'Use '+selfName+' with args:'
  print '  --temp                  - get temperature'
  print '  --type                  - get weather'
  print '  --icon                  - get icon of weather'
  print '  --city=<city_id>        - City ID on yandex (find your city here: https://pogoda.yandex.ru/static/cities.xml)'
  print '                            default is 28440 (Ekaterinburg)'
  print '  --period=<now|tomorrow> - the forecast date period (default "now")'
  print '  --time-period=<morning|day|evening|night> - the forecast time period (default "day")'
  print ''
else:
  for case in args:
    resCase=getCase(case)
    if resCase!=-1:
      if resCase['key']=='--city':
        city=resCase['value'];
      if resCase['key']=='--tomorrow':
        date=str(tomorrow)
      if resCase['key']=='--time-period':
        date=str(tomorrow)


  ns,url=setUrl(city)
  data=openUrl(url)

  for case in args:
    resCase=getCase(case)
    if resCase!=-1:
      if resCase['key']=='--temp':
        cmdList.append('temp')
      if resCase['key']=='--type':
        cmdList.append('type')
      if resCase['key']=='--icon':
        cmdList.append('icon')
      outAnswer=getValuesYandex(data,city,cmdList,date,dateTime)
  
  for answers in outAnswer:
    out=out+answers+';'
  print out