import xbmcgui
import xbmcplugin
import os
import xbmcaddon
import urllib2
import re
import urllib
import calendar
import datetime
import xbmc
import urlparse
from random import randint




base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'pictures')


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:
	url = build_url({'mode': 'todays', 'foldername': "Today's comic"})
	li = xbmcgui.ListItem("Today's comic" ,iconImage='http://vignette2.wikia.nocookie.net/garfield/images/3/3f/Garfield_by_is6ca.jpg/revision/latest?cb=20130109232246')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
    
                                listitem=li, isFolder=True)

	url = build_url({'mode': 'last_week', 'foldername': "Last 30 days"})
	li = xbmcgui.ListItem("Last 30 days" ,iconImage='http://vignette2.wikia.nocookie.net/garfield/images/3/3f/Garfield_by_is6ca.jpg/revision/latest?cb=20130109232246')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

	url = build_url({'mode': 'random', 'foldername': "Random comic"})
	li = xbmcgui.ListItem("Random comic" ,iconImage='http://vignette2.wikia.nocookie.net/garfield/images/3/3f/Garfield_by_is6ca.jpg/revision/latest?cb=20130109232246')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

	url = build_url({'mode': 'enter', 'foldername': "Enter date"})
	li = xbmcgui.ListItem("Enter date" ,iconImage='http://vignette2.wikia.nocookie.net/garfield/images/3/3f/Garfield_by_is6ca.jpg/revision/latest?cb=20130109232246')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
	xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='todays':
	now = datetime.datetime.now()
	year=now.strftime("%Y")
	month=now.strftime("%m")
	day=now.strftime("%d")

	
		
	pom=year+'-'+month+'-'+day
	url='http://garfield.com/uploads/strips/'+pom+'.jpg'
	print(url)
	try:
		req=urllib2.urlopen(url)
		html=req.read()
	
	except:
		now=datetime.datetime.now() - datetime.timedelta(hours=24)
		
	year=now.strftime("%Y")
	month=now.strftime("%m")
	day=now.strftime("%d")

	
		
	
	pom=year+'-'+month+'-'+day
	url='http://garfield.com/uploads/strips/'+pom+'.jpg'
	print(url)
	xbmc.executebuiltin("ShowPicture(%s)"%url)
elif mode[0]=='last_week':
	now = datetime.datetime.now()
	year=now.strftime("%Y")
	month=now.strftime("%m")
	day=now.strftime("%d")


	try:
		req=urllib2.urlopen(url)
		html=req.read()
	
	except:
		now=datetime.datetime.now() - datetime.timedelta(hours=24)



	for i in range(30):
		year=now.strftime("%Y")
		month=now.strftime("%m")
		day=now.strftime("%d")
		pom=year+'-'+month+'-'+day
		uroo='http://garfield.com/uploads/strips/'+pom+'.jpg'
		url = build_url({'mode': 'view', 'foldername': "%s"%pom , 'link': '%s'%uroo})
		li = xbmcgui.ListItem("%s"%pom ,iconImage='http://vignette2.wikia.nocookie.net/garfield/images/3/3f/Garfield_by_is6ca.jpg/revision/latest?cb=20130109232246')
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
		now=now-datetime.timedelta(hours=24)
	xbmcplugin.endOfDirectory(addon_handle)
		


elif mode[0]=='view':
	dicti=urlparse.parse_qs(sys.argv[2][1:])
	link=dicti['link'][0]
	print(link)
	xbmc.executebuiltin("ShowPicture(%s)"%link)





elif mode[0]=='random':
	def trY():
		def rand():
			yy=randint(1978,2015)
			mm=randint(1,12)
		 	dd=randint(1,31)
		 	y=str(yy)
		 	m=str(mm)
		 	d=str(dd)
		 	if d in ('1.2.3.4.5.6.7.8.9'):
		 		d='0'+d
		 	if m in ('1.2.3.4.5.6.7.8.9'):
		 		m='0'+m
		 	random= '%s-%s-%s'%(y,m,d)
		 	return random
		try:
			url='http://garfield.com/uploads/strips/'+rand()+'.jpg'
			req=urllib2.urlopen(url)
			print(url)
			xbmc.executebuiltin("ShowPicture(%s)"%url)

		except:
			trY()
	trY()

                                     	
elif mode[0]=='enter':
	keyboard = xbmc.Keyboard('yyyy-mm-dd', 'Enter date(yyyy-mm-dd)', False)
	keyboard.doModal()
	if keyboard.isConfirmed():
		date = keyboard.getText()

	url='http://garfield.com/uploads/strips/'+date+'.jpg'
	try:
		req=urllib2.urlopen(url)
		print(url)
		xbmc.executebuiltin("ShowPicture(%s)"%url)
	except:
		xbmc.executebuiltin('Notification("Wrong input format","You entered the wrong date format or something else went wrong. Please try again!")')