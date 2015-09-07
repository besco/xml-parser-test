#!/usr/bin/python

import urllib
import xml.etree.ElementTree as etree
import sys, time

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

def getValuesYandex(data,uCity,uType,uTime):
  ns,url=setUrl(uCity)
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

      for uTree in root.findall('site:'+uTime,ns):
        temp=uTree.find('site:temperature',ns)
        ico=uTree.find('site:image-v3',ns)
        weather=uTree.find('site:weather_type',ns)
        wind_dir=uTree.find('site:wind_direction',ns)
        wind_spd=uTree.find('site:wind_speed',ns)
    if uType=='temp':
      return('temp:'+temp.text,'city:'+city)
    if uType=='type':
      return('type:'+weather.text,'city:'+city)
    if uType=='icon':
      return('icon:'+ico.text,'city:'+city)
    

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
out=''

args=sys.argv
selfName=args[0]
args.pop(0)
if len(args)==0:
  print 'Use '+selfName+' with args:'
  print '  --temp - get temperature'
  print '  --type - get weather'
  print '  --icon - get icon of weather'
  print '  --city=<city_id> City ID on yandex (find your city here: https://pogoda.yandex.ru/static/cities.xml'
  print ''
else:
  for case in args:
    resCase=getCase(case)
    if resCase!=-1:
      if resCase['key']=='--city':
        city=resCase['value'];
      if resCase['key']=='--tomorrow':
        date='tomorrow'

  ns,url=setUrl(city)
  data=openUrl(url)

  for case in args:
    resCase=getCase(case)
    if resCase!=-1:
      if resCase['key']=='--temp':
        outAnswer.append(getValuesYandex(data,city,'temp',date))
      if resCase['key']=='--type':
        outAnswer.append(getValuesYandex(data,city,'type',date))
      if resCase['key']=='--icon':
        outAnswer.append(getValuesYandex(data,city,'icon',date))
  for answers in outAnswer:
    value,city = answers
    out = out+value+';'
  out=out+city

  print out