from __future__ import unicode_literals
import urllib2
import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import re
import json

from BeautifulSoup import BeautifulSoup as bs

def read_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link.decode('utf8')




def resolve_link(url):
	print(url)
	html=read_url(url)
	soup=bs(html)

	tag=soup.findAll('script',{'type':"text/javascript"})
	for i in range(len(tag)):
		
		if '//config.playwire.com' in str(tag[i]):
			tag=tag[i]
			break
		
	

	help_link=tag['data-config']
	if 'http' not in help_link:
		help_link='http:'+help_link
	print(help_link)
	html=read_url(help_link)
	data=json.loads(html)
	#print(data)
	try:
		link=data['content']['media']['f4m']
	except:
		reg='"src":"http://(.+?).f4m"'
		pat=re.compile(reg)
		pom=re.findall(pat,html)[0]
		link='http://'+pom+'.f4m'
		
	print(link)

	html=read_url(link)
	soup=bs(html)
	try:
		base=soup.findAll('baseURL')[0].getText()+'/'
	except:
		base=soup.findAll('baseurl')[0].getText()+'/'
	suffix=soup.find('media')['url']
	link=base+suffix
	return link

def get_matches(site,page):
	url=site

	if page!=1:
		suffix='/page/'+str(page)
	else:
		suffix=''
	link=url+suffix
	html=read_url(link)
	soup=bs(html)
	tag=soup.find('div',{'id':'cat-blog-wrapper'})
	matches=tag.findAll('li')
	linksout=[]
	for i in range(len(matches)):
		
		thumb=matches[i].find('a').find('img')['src'].encode('utf8').decode('utf8')
		if thumb=='http://cdn.footballtarget.com/wp-content/uploads/2013/04/footballtargetvideo133.jpg':
			thumb='http://upload.wikimedia.org/wikipedia/en/thumb/e/ec/Soccer_ball.svg/480px-Soccer_ball.svg.png'
		title=matches[i].find('a')['title'].encode('utf8').decode('utf8')
		link=matches[i].find('a')['href'].encode('utf8').decode('utf8')
		linksout+=[[link,title,thumb]]
		
	return linksout

def get_parts(url):
	html=read_url(url)
	reg="of \d"
	pattern=re.compile(reg)
	parts=re.findall(pattern,html)[0]
	parts=int(parts.replace('of ',''))
	if parts==2:
		linksout=[None]*2
		linksout[0]=[url,'First Half']
		linksout[1]=[url+'2/','Second Half']
	elif parts==3:
		linksout=[None]*3
		linksout[0]=[url,'First Half']
		linksout[1]=[url+'2/','Second Half']
		linksout[2]=[url+'3/','Extra time']

	
	return linksout




base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'videos')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:
    url = build_url({'mode': 'list_games', 'foldername': 'Games','site':'http://www.footballtarget.com/full-match-replay-video/','page': '1'})
    li = xbmcgui.ListItem('Games', iconImage='http://upload.wikimedia.org/wikipedia/en/thumb/e/ec/Soccer_ball.svg/480px-Soccer_ball.svg.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    url = build_url({'mode': 'highs', 'foldername': 'Highlights','site':'http://www.footballtarget.com/latest/','page':'1'})
    li = xbmcgui.ListItem('Highlights', iconImage='http://upload.wikimedia.org/wikipedia/en/thumb/e/ec/Soccer_ball.svg/480px-Soccer_ball.svg.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    

    
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='list_games':
	dicti=urlparse.parse_qs(sys.argv[2][1:])
	site=dicti['site'][0]
	page=int(dicti['page'][0])
	match_list=get_matches(site,page)
	
	print(match_list)
	for i in range(20):
		try:
			link=str(match_list[i][0])
			thumb=str(match_list[i][2])
			name=match_list[i][1].encode('utf8').decode('ascii','ignore')
			if 'Full Match' in name:
				url = build_url({'mode': 'game', 'foldername': '%s'%name, 'link':'%s'%link, 'thumb':'%s'%thumb})
			else:
				url = build_url({'mode': 'play', 'foldername': '%s'%name, 'link':'%s'%link, 'thumb':'%s'%thumb})
			li = xbmcgui.ListItem(name, iconImage='%s'%thumb)
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
	                                listitem=li,isFolder=True)
		except:
			pass
	        
	url = build_url({'mode': 'list_games', 'foldername': 'Games','site':'http://www.footballtarget.com/full-match-replay-video/','page': '%s'%str(page+1)})
	li = xbmcgui.ListItem('Next Page >>', iconImage='http://upload.wikimedia.org/wikipedia/en/thumb/e/ec/Soccer_ball.svg/480px-Soccer_ball.svg.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
	xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='highs':
	dicti=urlparse.parse_qs(sys.argv[2][1:])
	site=dicti['site'][0]
	page=int(dicti['page'][0])
	match_list=get_matches(site,page)
	
	print(match_list)
	for i in range(20):
		try:
			link=str(match_list[i][0])
			thumb=str(match_list[i][2])
			name=match_list[i][1].encode('utf8').decode('ascii','ignore')
			url = build_url({'mode': 'play', 'foldername': '%s'%name, 'link':'%s'%link, 'thumb':'%s'%thumb})
			li = xbmcgui.ListItem(name, iconImage='%s'%thumb)
			
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
	                                listitem=li)
		except:
			pass
	        

	url = build_url({'mode': 'highs', 'foldername': 'Games','site':'http://www.footballtarget.com/latest/','page': '%s'%str(page+1)})
	li = xbmcgui.ListItem('Next Page >>', iconImage='http://upload.wikimedia.org/wikipedia/en/thumb/e/ec/Soccer_ball.svg/480px-Soccer_ball.svg.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
	
	xbmcplugin.endOfDirectory(addon_handle)



elif mode[0]=='play':
	dicti=urlparse.parse_qs(sys.argv[2][1:])
	link=dicti['link'][0]
	name=(dicti['foldername'][0])
	thumb=(dicti['thumb'][0])
	link=resolve_link(link)
	li = xbmcgui.ListItem('%s'%name,iconImage='%s'%thumb)
	li.setInfo('video', { 'title': '%s'%name })
	xbmc.Player().play(item=link, listitem=li)





elif mode[0]=='game':
	dicti=urlparse.parse_qs(sys.argv[2][1:])
	link=dicti['link'][0]
	name=(dicti['foldername'][0])
	name=name[12:]
	parts=get_parts(link)
	link1=parts[0][0]
	link2=parts[1][0]
	url1=resolve_link(link1)
	url2=resolve_link(link2)
	
	li = xbmcgui.ListItem('First Half (%s)'%name, iconImage='http://upload.wikimedia.org/wikipedia/en/thumb/e/ec/Soccer_ball.svg/480px-Soccer_ball.svg.png')
	li.setInfo('video', { 'title': 'First Half (%s)'%name })
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url1,
                                listitem=li)
	
	li = xbmcgui.ListItem('Second Half (%s)'%name, iconImage='http://upload.wikimedia.org/wikipedia/en/thumb/e/ec/Soccer_ball.svg/480px-Soccer_ball.svg.png')
	li.setInfo('video', { 'title': 'Second Half (%s)'%name})
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url2,
                                listitem=li)
	try:
		link3=parts[1][0]
		url3=resolve_link(link3)
		if link3!=link2 and link3!=link1:
			li = xbmcgui.ListItem('Extra time (%s)'%name, iconImage='http://upload.wikimedia.org/wikipedia/en/thumb/e/ec/Soccer_ball.svg/480px-Soccer_ball.svg.png')
			li.setInfo('video', { 'title': 'Extra time (%s)'%name})
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url3,
	                                listitem=li)
	except:
		pass

	xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='liga':

	url = build_url({'mode': 'list_games', 'foldername': 'Premier league','site':'http://www.soccerhighlightstoday.com/search/label/Barclays%%20Premier%%20League'})
	li = xbmcgui.ListItem('Premier League', iconImage='http://www.sitioco.com/futbolcolombiano/wp-content/uploads/2011/04/Premier-League.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
	url = build_url({'mode': 'list_games', 'foldername': 'Serie A','site':'http://www.footballtarget.com/seriea/'})
	li = xbmcgui.ListItem('Serie A', iconImage='http://www.logoeps.com/wp-content/uploads/2012/12/serie-a-vector-logo.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
	url = build_url({'mode': 'list_games', 'foldername': 'Bundesliga','site':'http://www.footballtarget.com/bundesliga/'})
	li = xbmcgui.ListItem('Bundesliga', iconImage='http://upload.wikimedia.org/wikipedia/hr/9/92/Njema%C4%8Dka-Bundesliga-logo.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
	url = build_url({'mode': 'list_games', 'foldername': 'Liga BBVA','site':'http://www.footballtarget.com/liga-bbva/'})
	li = xbmcgui.ListItem('Liga BBVA', iconImage='http://www.tipforwin.com/wp-content/uploads/2014/05/spain_primera_division.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
	url = build_url({'mode': 'list_games', 'foldername': 'Ligue 1','site':'http://www.footballtarget.com/france/'})
	li = xbmcgui.ListItem('Ligue 1', iconImage='http://upload.wikimedia.org/wikipedia/en/thumb/9/9b/Logo_de_la_Ligue_1_(2008).svg/364px-Logo_de_la_Ligue_1_(2008).svg.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
	url = build_url({'mode': 'list_games', 'foldername': 'Champions League','site':'http://www.footballtarget.com/champions-league/'})
	li = xbmcgui.ListItem('Champions League', iconImage='http://upload.wikimedia.org/wikipedia/en/thumb/b/bf/UEFA_Champions_League_logo_2.svg/200px-UEFA_Champions_League_logo_2.svg.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
	url = build_url({'mode': 'list_games', 'foldername': 'Europa League','site':'http://www.footballtarget.com/uefaleague/'})
	li = xbmcgui.ListItem('Europa League', iconImage='http://3.bp.blogspot.com/-L8SR1hSS7V8/VCrrWR2-yyI/AAAAAAAAAO8/L9fOWfcAVog/s1600/3532gsx.jpg')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
	xbmcplugin.endOfDirectory(addon_handle)
