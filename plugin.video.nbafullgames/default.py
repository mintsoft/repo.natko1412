from __future__ import unicode_literals
import urllib2
import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon, xbmcvfs
import re
from BeautifulSoup import BeautifulSoup as bs
import urlresolver
import datetime
import json
import os


YOUTUBE_API_KEY='AIzaSyAO7A3iaRS6RJOYUf-o9caPPK-aiMcrnEk'

def read_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link.decode('utf-8')


def get_archives():
    url='http://nbahd.com/'
    req = urllib2.Request(url=url,headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    request=urllib2.urlopen(req)
    html=request.read()
    soup=bs(html)


    tag=soup.findAll('div',{'id':'archives-2'})[0]

    arh=tag.findAll('li')
    linksout=[]
    for i in range(len(arh)):
        name=arh[i].findAll('a')[0].getText()
        link=arh[i].findAll('a')[0]['href']
        linksout.append([name,link])
    return linksout
def get_game_links_from_date(date):   # date in format yyyy/mm/dd
    basic_url='http://nbahd.com/'
    if basic_url not in date:

        dates=date.split('/')
        year=dates[0]
        month=dates[1]
        day=dates[2]

        url=basic_url + '/%s/%s/%s'%(year,month,day)
    else:
        url=date
    req = urllib2.Request(url=url,headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    request=urllib2.urlopen(req)
    html=request.read()
    soup=bs(html)

    help_list=[]
    game_links=[]
    soup=soup.find('div',{'class':'loop-content switchable-view grid-medium'})
    help_list=soup.findAll('a',{'class':'clip-link'})

    for i in range(len(help_list)):
        game_link=help_list[i]['href']
        title=help_list[i]['title']
        img=help_list[i].findAll('span')[0].findAll('img')[0]['src']
        title=title.encode('ascii','ignore').decode()
        pom=[game_link,title,img]
        game_links+=[pom]



    return game_links


def get_parts_from_game_link(game_link):
    req = urllib2.Request(url=game_link,headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    request=urllib2.urlopen(req)
    html=request.read()
    soup=bs(html)


    tag=soup.findAll('div',{'class':'entry-content rich-content'})[0]
    links=tag.findAll('a')
    part_links=[]
    for i in range(len(links)):
        link=links[i]['href']
        if 'http://nbahd.com/' in link:
            part_links+=[link]

    return part_links


def get_video_from_part_link(part_link):
    reg='file: "(.+?)"'
    pattern=re.compile(reg)



    basic_url='http://nbahd.com/'
    req = urllib2.Request(url=part_link,headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    request=urllib2.urlopen(req)
    html=request.read()
    soup=bs(html)
    try:
        tag=soup.findAll('div',{'class':'page-content rich-content'})[0]
    except:
        tag=soup.findAll('div',{'class':'entry-content rich-content'})[0]


    tag=tag.findAll('iframe')[0]
    url=tag['src']
    url=basic_url + url
    request=urllib2.urlopen(url)
    html=request.read()
    soup=bs(html)

    try:
        video_tag=re.findall(pattern,html)
        my_addon = xbmcaddon.Addon()
        HD = my_addon.getSetting('quality')
        
        if HD=='false':
            ind=1
        else:
            ind=0
        
        src=video_tag[ind]
    except:
        video_tag=soup.findAll('video')[0]
        my_addon = xbmcaddon.Addon()
        HD = my_addon.getSetting('quality')
        
        if HD=='false':
            ind=1
        else:
            ind=0
        tag=video_tag.findAll('source')[ind]
        src=tag['src']


        
        
    
    return(src)





def get_teams_list():
    site='http://nbahd.com'
    req = urllib2.Request(url=site,headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    request=urllib2.urlopen(req)
    html=request.read()
    soup=bs(html)

    tag=soup.findAll('center')[0]

    a=tag.findAll('a')
    team_links=[]
    for i in range(len(a)):
        link=a[i]['href']
        img=a[i].findAll('img')[0]['src']
        name=link.replace('http://nbahd.com/tag/','').replace('/','')
        name=name.replace('-',' ').title()
        team_links+=[[link,name,img]]
    return team_links


def get_latest_from_youtube(playlist_id,page):
    
    if page=='1':
        req_url='https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=20&playlistId=%s&key='%playlist_id+YOUTUBE_API_KEY
    else:
        req_url='https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&pageToken=%s&maxResults=20&playlistId=%s&key='%(page,playlist_id)+YOUTUBE_API_KEY
    
    read=read_url(req_url)
    decoded_data=json.loads(read)
    listout=[]
    try:
        next_page=decoded_data['nextPageToken']
    except:
        next_page='1'
    listout.append(next_page)
    for x in range(0, len(decoded_data['items'])):
        try:
            title=decoded_data['items'][x]['snippet']['title']
            video_id=decoded_data['items'][x]['snippet']['resourceId']['videoId']
            thumb=decoded_data['items'][x]['snippet']['thumbnails']['high']['url']
            desc=decoded_data['items'][x]['snippet']['description']
            listout.append([title,video_id,thumb,desc])
        except: pass #video is private
    return listout

def download(name, url):
       
            agent = None
            referer = None
            cookie = None

            my_addon = xbmcaddon.Addon()
        
            desty= my_addon.getSetting('downloads_folder')
            
            if not xbmcvfs.exists(desty):
                xbmcvfs.mkdir(desty)


            
            dest = os.path.join(desty, name + '.mp4')

            import commondownloader
            commondownloader.download(url, dest, 'NBA Full Games', referer=referer, agent=agent, cookie=cookie)
        
        
def get_playlists(page):
    channelID='UCWJ2lWNubArHWmf3FIHbfcQ'

    if page=='1':
        url='https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=%s&maxResults=10&key=%s'%(channelID,YOUTUBE_API_KEY)
    else:#
        url='https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=%s&maxResults=10&pageToken=%s&key=%s'%(channelID,page,YOUTUBE_API_KEY)
    read=read_url(url)
    decoded_data=json.loads(read)
    playlists=[]
    try:
        next_page=decoded_data['nextPageToken']
    except:
        next_page='1'
    playlists.append(next_page)
    for i in range(len(decoded_data['items'])):
        if decoded_data['items'][i]['kind']=='youtube#playlist':
            playlist_id=decoded_data['items'][i]['id']
            playlist_name=decoded_data['items'][i]['snippet']['title']
            thumb=decoded_data['items'][i]['snippet']['thumbnails']['high']['url']

            playlists.append([playlist_id,playlist_name,thumb])
    return playlists

def play_game(game_link, game_name, img):
    perc=0
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()

    progress = xbmcgui.DialogProgress()
    progress.create('Loading', 'Loading game parts to a playlist...')


    
    
    
    

    parts=get_parts_from_game_link(game_link)
    leng=len(parts)
    message ="0 out of %s"%leng
    progress.update( 0, "", message, "" )   
    perc=0
    for i in range(len(parts)):
        if leng==5:
            perc=perc+20
        if leng==4:
            perc=perc+25
        if leng==3:
            perc=perc+33
        if leng==2:
            perc=perc+50
        message = str(i+1) + " out of %s"%leng
        link=get_video_from_part_link(parts[i])
        title=game_name
        listitem = xbmcgui.ListItem(title)
        listitem.setThumbnailImage(img)
        playlist.add(link,listitem)
        progress.update( perc, "", message, "" )

        if progress.iscanceled():
            
            return

    progress.close()
    
    xbmc.Player().play(playlist)


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)


if mode is None:
    url = build_url({'mode': 'game_menu', 'foldername': 'Games'})
    li = xbmcgui.ListItem('Games', iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/nba.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    url = build_url({'mode': 'teams', 'foldername': 'Teams'})
    li = xbmcgui.ListItem('Teams', iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/nba.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    url = build_url({'mode': 'games', 'foldername': 'other', 'page':'first','date':'http://nbahd.com/category/other-sport/'})
    li = xbmcgui.ListItem('Other sports', iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/nba.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    url = build_url({'mode': 'search', 'foldername': 'Search'})
    li = xbmcgui.ListItem('Search', iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/nba.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    url = build_url({'mode': 'yt', 'foldername': 'NBA on Youtube', 'page':'1'})
    li = xbmcgui.ListItem('NBA on Youtube', iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/nba.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='game_menu':
    url = build_url({'mode': 'games', 'foldername': 'By Date', 'page':'first','date':'http://nbahd.com/'})
    li = xbmcgui.ListItem('By Date', iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/nba.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    url = build_url({'mode': 'by_month', 'foldername': 'By Month'})
    li = xbmcgui.ListItem('By Month', iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/nba.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
    
    
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='by_month':
    list_arh=get_archives()

    for i in range(len(list_arh)):
        url = build_url({'mode': 'games', 'foldername': '%s'%(list_arh[i][0]), 'page':'first', 'date': '%s'%(list_arh[i][1])})
        li = xbmcgui.ListItem('%s'%(list_arh[i][0]), iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/nba.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


    

elif mode[0] == 'dates':
    basic_url='http://nbahd.com/'
    now = datetime.datetime.now()
    okay=1
    while okay:
        year=now.strftime("%Y")
        month=now.strftime("%m")
        day=now.strftime("%d")
        if day in ('1.2.3.4.5.6.7.8.9'):
            day='0'+d
        if month in ('1.2.3.4.5.6.7.8.9'):
            month='0'+m
        url=basic_url + '%s/%s/%s'%(year,month,day)
        try:
            request=urllib2.urlopen(url)
            html=request.read()
            soup=bs(html)
        
            #tag=soup.findAll('h1',{'class':'entry-title'})[0].getText()
            if '404 Not Found' in html:
                now=now-datetime.timedelta(hours=24)
                
            okay=0

        except:
            now=now-datetime.timedelta(hours=24)

    
    for i in range(30):
        year=now.strftime("%Y")
        month=now.strftime("%m")
        day=now.strftime("%d")
        f_name='%s/%s/%s'%(year,month,day)
        url = build_url({'mode': 'games', 'foldername': '%s'%f_name, 'date' : '%s'%f_name})
        li = xbmcgui.ListItem('%s'%f_name, iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/nba.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
        now=now-datetime.timedelta(hours=24)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='games':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    date=dicti['date'][0]
    
    try:
        page=dicti['page'][0]
    except:
        page=0
    
    game_list=get_game_links_from_date(date)
    
    for i in range(len(game_list)):
        url = build_url({'mode': 'game', 'foldername': '%s'%game_list[i][1], 'link' : '%s'%game_list[i][0], 'img': '%s'%(game_list[i][2])})
        li = xbmcgui.ListItem('%s'%game_list[i][1], iconImage='%s'%game_list[i][2])

        play_uri=build_url({'mode': 'play_game', 'foldername': '%s'%game_list[i][1], 'link' : '%s'%game_list[i][0], 'img': '%s'%(game_list[i][2])})

        li.addContextMenuItems([('Play this game', 'RunPlugin(%s)'%play_uri)])

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
    if 'other-sport/' not in date:
        if 'tag' in date or page=='first' or 'page' in date:

            if 'page'not in date:
                linky=date+'page/2/'
            else:
            

                page_num=str(int(date[-2])+1)
                linky=date[:-2] + '%s/'%page_num


            
            url = build_url({'mode': 'games', 'foldername': 'Next Page >', 'date' : '%s'%linky})
            li = xbmcgui.ListItem('Next Page >', iconImage='http://www.glib.com/next.gif')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='game':
    try:
        dicti=urlparse.parse_qs(sys.argv[2][1:])
        link=dicti['link'][0]
        game=dicti['foldername'][0]
        img=dicti['img'][0]
        part_list=get_parts_from_game_link(link)
        pom=1
        if part_list==[]:
            part_list=[get_video_from_part_link(link)]
            pom=0
        for i in range(len(part_list)):

            
            if pom==1:
                url = build_url({'mode': 'play_part', 'foldername': '%s'%game, 'part_link' : '%s'%part_list[i], 'img':'%s'%img})
                li = xbmcgui.ListItem('%s: Part %s'%(game,i+1), iconImage='%s'%img)

                namee='%s-Part%s'%(game,i+1)
                down_uri = build_url({'mode': 'download', 'foldername': '%s'%(namee), 'part_link' : '%s'%part_list[i]})

                li.addContextMenuItems([ ('Download', 'RunPlugin(%s)'%down_uri)])
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)
            else:
                link=part_list[i]


                if  link!='Game not available yet':
                    li = xbmcgui.ListItem('Part %s'%(i+1), iconImage=img)
                    li.setInfo('video', { 'title': '%s - Part %s'%(game,i+1)})
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=link, listitem=li)
                else:
                    li = xbmcgui.ListItem('%s'%link, iconImage=img)
                    
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url='.', listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)   
    except:
            a=xbmcgui.Dialog().ok("NBA Full Games", "Game not available yet. Check back later.")


elif mode[0]=='play_part':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['part_link'][0]
    game=dicti['foldername'][0]
    img=dicti['img'][0]

    link=get_video_from_part_link(link)
    li = xbmcgui.ListItem('%s'%game)
    li.setInfo('video', { 'title': '%s'%game} )
    li.setThumbnailImage(img)
    xbmc.Player().play(item=link, listitem=li)

elif mode[0]=='download':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['part_link'][0]
    game=dicti['foldername'][0]
    name=game.replace(' ','_')

    link=get_video_from_part_link(link)
    download(name,link)



elif mode[0]=='teams':
    team_list=get_teams_list()
    for i in range(len(team_list)):
        link=team_list[i][0]
        name=team_list[i][1]
        img=team_list[i][2]

        url = build_url({'mode': 'games', 'foldername': '%s'%name, 'date' : '%s'%link})
        li = xbmcgui.ListItem('%s'%name, iconImage=img)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
        
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='search':
    keyboard = xbmc.Keyboard('', 'Search', False)
    keyboard.doModal()
    
    if keyboard.isConfirmed():
        query = keyboard.getText()
    

    date='http://nbahd.com/?s='+query.replace(' ','+')

    game_list=get_game_links_from_date(date)

    for i in range(len(game_list)):
        url = build_url({'mode': 'game', 'foldername': '%s'%game_list[i][1], 'link' : '%s'%game_list[i][0], 'img': '%s'%(game_list[i][2])})
        li = xbmcgui.ListItem('%s'%game_list[i][1], iconImage='%s'%game_list[i][2])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
    
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='yt':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=dicti['page'][0]


    try:
        playlist=dicti['playlist'][0]
        if playlist=='yes':
            playlista=True
    except:
        playlista=False

    
    if not playlista:

        url = build_url({'mode': 'open_playlists',  'page':'1'})
        li = xbmcgui.ListItem('[COLOR yellow]Playlists [/COLOR]',iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/nba.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)

    if playlista:
        play_id=dicti['id'][0]
    else:
        play_id='UUWJ2lWNubArHWmf3FIHbfcQ'
    game_list=get_latest_from_youtube(play_id,page)
    next_page=game_list[0]
    for i in range(1,len(game_list)):
        title=game_list[i][0].encode('utf8').decode('ascii','ignore')
        video_id=game_list[i][1]
        thumb=game_list[i][2]
        desc=game_list[i][3]
        link='plugin://plugin.video.youtube/?action=play_video&videoid='+video_id
        
        uri = build_url({'mode': 'play_yt', 'foldername': '%s'%title, 'link' : '%s'%video_id})

        li = xbmcgui.ListItem('%s'%title, iconImage=thumb)
        
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=li,isFolder=True)

    if next_page!='1':
        uri = build_url({'mode': 'yt', 'foldername': 'Next Page', 'page' : '%s'%next_page})

        li = xbmcgui.ListItem('Next Page >', iconImage='http://www.glib.com/next.gif')
        
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='play_yt':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link='plugin://plugin.video.youtube/?action=play_video&videoid='+dicti['link'][0]
    xbmc.executebuiltin('PlayMedia(%s)'%link)

elif mode[0]=='open_playlists':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    
    page=dicti['page'][0]
    
    playlists=get_playlists(page)

    next_page=playlists[0]
    for i in range (1,len(playlists)):
        id=playlists[i][0]
        name=playlists[i][1]
        thumb=playlists[i][2]


        url = build_url({'mode': 'yt', 'id': '%s'%id, 'page':'1', 'playlist':'yes'})
        li = xbmcgui.ListItem('%s'%name, iconImage='%s'%thumb)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li,isFolder=True)


    if next_page!='1':
        
        uri = build_url({'mode': 'open_playlists', 'id': '%s'%id, 'page' : '%s'%next_page ,'playlist':'yes'})
      

        li = xbmcgui.ListItem('Next Page >', iconImage='http://www.glib.com/next.gif')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='play_game':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    game_name=dicti['foldername'][0]
    game_link=dicti['link'][0]
    game_img=dicti['img'][0]
    print(game_link)
    play_game(game_link,game_name,game_img)