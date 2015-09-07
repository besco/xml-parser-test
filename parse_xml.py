#!/usr/bin/python

import urllib
from xml.dom import minidom
import xml.dom
import xml.etree.ElementTree as etree
import sys


def openUrl(url):
  try:
    uHandle=urllib.urlopen(url)
  except:
    print "Error open url: "+url
  else:
    data=uHandle.read(uHandle)
    return('neok')
  finally:
    uHandle.close()
    return(data)


url='http://export.yandex.ru/weather-ng/forecasts/28440.xml'
root=''
ns={'site':'http://weather.yandex.ru/forecast'}
data=openUrl(url)

if data!='neok':
  root=etree.fromstring(data)
  parsed_head=root.attrib
  city=parsed_head['city']
  country=parsed_head['country']
  dist=parsed_head['part']

  for fact in root.findall('site:fact',ns):
    temp=fact.find('site:temperature',ns)
    ico=fact.find('site:image-v3',ns)
    weather=fact.find('site:weather_type',ns)
    wind_dir=fact.find('site:wind_direction',ns)
    wind_spd=fact.find('site:wind_speed',ns)

for case in sys.argv:
  if case=='v':
    print weather.text
  if case=='i':
    print ico.text
  if case=='a':
    print temp.text
  if case=='c':
    print city
  if case=='d':
    print dist
