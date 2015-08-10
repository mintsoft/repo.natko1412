# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib2
#import urllib2 as urllib2
import re
from BeautifulSoup import BeautifulSoup as bs
import itertools
import urlresolver
import json

my_addon = xbmcaddon.Addon()
alluc_username=my_addon.getSetting('alluc_username')
alluc_password=my_addon.getSetting('alluc_password')

trakt_api='684e0c03f9b8439a4ce05f957f9afab3c7a97e7890e74a25997d773b54e0f77d'
trakt_header= {
      'Content-Type': 'application/json',
      'trakt-api-version': '2',
      'trakt-api-key': '%s'%trakt_api,
      
      
    }

def read_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link.decode('utf-8')

def search_shows(query):
    request = urllib2.Request('https://api-v2launch.trakt.tv/search?query=%s&type=show'%query, headers=trakt_header)
    response_body = urllib2.urlopen(request).read().decode('utf-8')
    decoded_data=json.loads(response_body)
    results=[]
    for i in range(len(decoded_data)):
        title=decoded_data[i]['show']['title']
        year=decoded_data[i]['show']['year']
        thumb=decoded_data[i]['show']['images']['poster']['thumb']
        slug=decoded_data[i]['show']['ids']['slug']
        imdb=decoded_data[i]['show']['ids']['imdb']
        trakt=decoded_data[i]['show']['ids']['trakt']
        
        results.append([title,year,slug,imdb,trakt,thumb])
    return results


def get_popular_shows(page):

    headers = {
      'Content-Type': 'application/json',
      'trakt-api-version': '2',
      'trakt-api-key': '%s'%trakt_api,
      
      
    }
    request = urllib2.Request('https://api-v2launch.trakt.tv/shows/popular?page=%s&extended=images'%(page), headers=headers)

    response_body = urllib2.urlopen(request).read().decode('utf-8')
    decoded_data=json.loads(response_body)
    results=[]
    for i in range(len(decoded_data)):
        name=decoded_data[i]['title']
        year=decoded_data[i]['year']
        slug=decoded_data[i]['ids']['slug']
        imdb=decoded_data[i]['ids']['imdb']
        trakt=decoded_data[i]['ids']['trakt']
        thumb=decoded_data[i]['images']['poster']['thumb']
        results+=[[name,year,slug,imdb,trakt,thumb]]
    return results

def get_seasons(slug):
    request = urllib2.Request('https://api-v2launch.trakt.tv/shows/%s/seasons?extended=images'%slug, headers=trakt_header)
    response_body = urllib2.urlopen(request).read().decode('utf-8')
    decoded_data=json.loads(response_body)
    results=[]
    for i in range(len(decoded_data)):
        title='Season %s'%decoded_data[i]['number']
        number=decoded_data[i]['number']
        id=decoded_data[i]['ids']['trakt']
        thumb=decoded_data[i]['images']['poster']['thumb']
        results+=[[title,id,thumb,number]]

    return results

def get_episodes(slug,season):
    request = urllib2.Request('https://api-v2launch.trakt.tv/shows/%s/seasons/%s/?extended=images'%(slug,season), headers=trakt_header)
    response_body = urllib2.urlopen(request).read().decode('utf-8')
    decoded_data=json.loads(response_body)
    results=[]
    for i in range(len(decoded_data)):
        title=decoded_data[i]['title']
        season=decoded_data[i]['season']
        number=decoded_data[i]['number']
        id=decoded_data[i]['ids']['trakt']

        thumb=decoded_data[i]['images']['screenshot']['medium']
        results+=[[title,season,number,id,thumb]]

    return results
def get_links_putlocker(show,season,episode):

    show=show.replace(' 2014','').replace(' 2015','')
    show=show.rstrip().replace(' ','-').replace('!','').replace('?','').replace('--','')
    
    url='http://putlocker.is/watch-%s-tvshow-season-%s-episode-%s-online-free-putlocker.html'%(show,season,episode)
    print(url)
    read=read_url(url)

    soup=bs(read)
    table=soup.findAll('table',{'class':'table', 'border':'0','cellspacing':'0', 'cellpadding':'0', 'width':'100%'})[2]
    
    trs=table.findAll('tr')
    results=[]

    reg='http://www.(.+?)/'
    pat=re.compile(reg)
    for i in range(len(trs)):

        
        try:
            link=trs[i].find('td',{'width':'100%' }).find('a')['href']
            title=re.findall(pat,link)[0]
            results.append([title,link])
        except: pass
    return results
def get_links_alluc(show,season,episode,year):
    hosts=['vidzi.tv','divxstage.eu','movreel.com','videoweed.es','vodlocker.com','vk.com','grifthost.com','promptfile.com','gorillavid.in']
    url='https://www.alluc.com/api/search/stream/?user=%s&password=%s&query=%s%%20S%sE%s&count=50&from=0&getmeta=0'%(alluc_username,alluc_password,show.replace(' ','%20'),season,episode)
    print(url)
    read=read_url(url)
    decoded_data=json.loads(read)
    results=[]
    brojac=0
    for i in range (len(decoded_data['result'])):
        host=decoded_data['result'][i]['hostername']
        title='%s. %s'%(brojac+1,host)
        link=decoded_data['result'][i]['hosterurls'][0]['url']
        if host in hosts:

            results.append([title,link])
            brojac+=1
        if brojac==25:
            break
            
    return results


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)




if mode is None:  
    url = build_url({'mode': 'popular_shows', 'page':'1'})
    li = xbmcgui.ListItem('Popular shows')

    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)

    url = build_url({'mode': 'search', 'page':'1'})
    li = xbmcgui.ListItem('Search')

    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='popular_shows':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=dicti['page'][0]
    shows=get_popular_shows(page)
    for i in range(len(shows)):
        title=shows[i][0]
        year=shows[i][1]
        slug=shows[i][2]
        imdb=shows[i][3]
        trakt=shows[i][4]
        thumb=shows[i][5]

        url = build_url({'mode': 'open_show', 'foldername': '%s'%title,'year':'%s'%year, 'slug':'%s'%slug, 'imdb':'%s'%imdb, 'trakt':'%s'%trakt})
        li = xbmcgui.ListItem('%s (%s)'%(title,year), iconImage=thumb)

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)

    url = build_url({'mode': 'popular_shows', 'page':'%s'%(str(int(page)+1))})
    li = xbmcgui.ListItem('Next page >>>')

    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)


    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_show':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    title_show=dicti['foldername'][0]
    slug=dicti['slug'][0]
    imdb=dicti['imdb'][0]
    trakt=dicti['trakt'][0]
    show_year=dicti['year'][0]

    seasons=get_seasons(slug)

    for i in range(len(seasons)):
        title=seasons[i][0]
        id=seasons[i][1]
        thumb=seasons[i][2]
        number=seasons[i][3]
        url = build_url({'mode': 'open_season', 'foldername': '%s'%title,'year':'%s'%show_year, 'show_title':'%s'%title_show,'id':'%s'%number, 'slug':'%s'%slug})
        li = xbmcgui.ListItem('%s'%title, iconImage=thumb)

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)


    xbmcplugin.endOfDirectory(addon_handle)



elif mode[0]=='open_season':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    title_show=dicti['show_title'][0]
    slug=dicti['slug'][0]
    id=dicti['id'][0]
    show_year=dicti['year'][0]
    episodes=get_episodes(slug,id)
    for i in range(len(episodes)):
        title=episodes[i][0]
        season=episodes[i][1]
        number=episodes[i][2]
        id=episodes[i][3]
        thumb=episodes[i][4]
        url = build_url({'mode': 'open_episode', 'foldername': '%s'%title, 'id':'%s'%id, 'year':'%s'%show_year,'show_title':'%s'%title_show,'season':'%s'%season,'slug':'%s'%slug, 'number':'%s'%number})
        li = xbmcgui.ListItem('%sx%s %s'%(season,number,title), iconImage=thumb)

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)


    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='open_episode':
    
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    title_show=dicti['show_title'][0]
    title=dicti['foldername'][0]
    slug=dicti['slug'][0]
    season=dicti['season'][0]
    number=dicti['number'][0]
    show_year=dicti['year'][0]

    results=get_links_alluc(title_show,season,number,show_year)

    result_list=[]
    for i in range(len(results)):
        result_list+=[results[i][0]]
    dialog = xbmcgui.Dialog()
    index = dialog.select('Choose link', result_list)
    if index>-1:
        resolved=urlresolver.resolve(results[index][1])

        li = xbmcgui.ListItem('%s'%title)
        li.setInfo('video', { 'title': '%s'%title ,
                            'tvshowtitle': '%s'%title_show,
                            'episode':'%s'%number,
                            'season':'%s'%season
                                })
        xbmc.Player().play(item=resolved, listitem=li)


elif mode[0]=='search':
    keyboard = xbmc.Keyboard('', 'Search', False)
    keyboard.doModal()
    
    if keyboard.isConfirmed():
        query = keyboard.getText()
        shows=search_shows(query)


    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=dicti['page'][0]
    
    for i in range(len(shows)):
        title=shows[i][0]
        year=shows[i][1]
        slug=shows[i][2]
        imdb=shows[i][3]
        trakt=shows[i][4]
        thumb=shows[i][5]

        url = build_url({'mode': 'open_show', 'foldername': '%s'%title, 'slug':'%s'%slug, 'imdb':'%s'%imdb, 'trakt':'%s'%trakt})
        li = xbmcgui.ListItem('%s (%s)'%(title,year), iconImage=thumb)

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)

    
    
    xbmcplugin.endOfDirectory(addon_handle)
