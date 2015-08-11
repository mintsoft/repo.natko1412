import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib2
import sqlite3
import re
import os
import json
from BeautifulSoup import BeautifulSoup as bs
from pftvso import *
try:
    from addon.common.addon import Addon
    from addon.common.net import Net
except:
    print 'Failed to import script.module.addon.common'
    xbmcgui.Dialog().ok("PFTVso Import Failure", "Failed to import addon.common", "A component needed by PFTVso is missing on your system", "Please visit www.tvaddons.ag for support")

try:
    from metahandler import metahandlers
except:
    print 'Failed to import script.module.metahandler'
    xbmcgui.Dialog().ok("PFTV Import Failure", "Failed to import Metahandlers", "A component needed by PFTV is missing on your system", "Please visit www.xbmchub.com for support")

addonID=xbmcaddon.Addon().getAddonInfo("id")
db_dir = xbmc.translatePath("special://profile/addon_data/"+addonID)
db_path = os.path.join(db_dir, 'favourites.db')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

db=sqlite3.connect(db_path)



addon = Addon('plugin.video.pftvso', sys.argv)
AddonPath = addon.get_path()
IconPath = AddonPath + "/icons/simple/"

def icon_path(filename):
    return IconPath + filename

def get_links(url):
    my_addon = xbmcaddon.Addon()
    black = unicode(my_addon.getSetting('source_blacklist'))
    blacklist=black.split(',')

    linksout=[]
    html=read_url(url)
    
    soup=bs(html)
    
    rows=soup.findAll('tr')
    a=2
    if 'movie' in url:
        a=3
    
    for i in range(a,len(rows)):
        row=rows[i]
        link=row.find('td').find('a')['href']
        h = HTMLParser.HTMLParser()
        dm=row.find('td').getText()
        domain=h.unescape(dm).strip()
        age=row.findAll('td')[2].getText().strip()
        if 'movie' in url and domain not in blacklist:   
            linksout+=[[domain,link]]
        elif domain not in blacklist:
            linksout+=[[domain,link,age]]

    return linksout
def add_favourite_show(name, link, thumb):
    with db:

        cur = db.cursor()    
        cur.execute("begin") 
        cur.execute("create table if not exists Favourite_shows (Link TEXT,Title TEXT, Thumb TEXT )")    
        db.commit()

        cur.execute("INSERT INTO Favourite_shows(Link,Title, Thumb) VALUES (?,?, ?);",(link,name,thumb))

        db.commit()
        cur.close()
    return
def add_favourite_movie(title,year,link,thumb):

    with db:

        cur = db.cursor()    
        cur.execute("begin") 
        cur.execute("create table if not exists Favourite_movies (Title TEXT, Year TEXT, Thumb TEXT, Link TEXT)")    
        db.commit()

        cur.execute("INSERT INTO Favourite_movies(Title,Year, Thumb,Link) VALUES (?,?,?,?);",(title, year, thumb,link))

        db.commit()
        cur.close()
    return

def get_favourite_shows():
    with db:

        cur = db.cursor()
        cur.execute("begin")   
        cur.execute("create table if not exists Favourite_shows (Title TEXT, Link TEXT, Thumb TEXT)")    
        db.commit()  
        cur.execute("SELECT Title,Link,Thumb FROM Favourite_shows")
        rows = cur.fetchall()
        cur.close()
        favs=[]
        for i in range (len(rows)):
            folder=rows[i]
            favs+=[folder]
    

    
    return favs
def get_favourite_movies():
    with db:

        cur = db.cursor()
        cur.execute("begin")    
        cur.execute("create table if not exists Favourite_movies (Title TEXT, Year TEXT, Thumb TEXT, Link TEXT)")    
        db.commit() 
        cur.execute("SELECT Title,Year,Thumb,Link FROM Favourite_movies")
        rows = cur.fetchall()
        cur.close()
        favs=[]
        for i in range (len(rows)):
            folder=rows[i]
            favs+=[folder]
    

    
    return favs


def delete_all_movie_favs():
   
    
    with db:
    
        cur = db.cursor()
         
    
        cur.execute("drop table if exists Favourite_movies")
        cur.close()


    return

def delete_all_tv_favs():
   
    
    with db:
    
        cur = db.cursor()
         
    
        cur.execute("drop table if exists Favourite_shows")
        cur.close()


    return

def remove_movie_fav(title,year,thumb,link):

    

    cur = db.cursor()  
    cur.execute("begin")  
    cur.execute("DELETE FROM Favourite_movies WHERE Title = ? AND Year= ? AND Thumb = ? AND Link = ?",(title,year,thumb,link))

    db.commit()
    cur.close()

def remove_tv_fav(title,link):

    

    cur = db.cursor()  
    cur.execute("begin")  
    cur.execute("DELETE FROM Favourite_shows WHERE Title = ? AND Link = ?",(title,link))

    db.commit()
    cur.close()

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:
    url = build_url({'mode': 'movies', 'foldername': 'movies'})
    li = xbmcgui.ListItem('Movies', iconImage=icon_path('Movies.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'tv', 'foldername': 'shows'})
    li = xbmcgui.ListItem('TV Shows', iconImage=icon_path('TV_Shows.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'favs', 'foldername': 'favs'})
    li = xbmcgui.ListItem('Favourites', iconImage=icon_path('Favourites.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'search', 'foldername': 'search'})
    li = xbmcgui.ListItem('Search All', iconImage=icon_path('Search.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'settings'})
    li = xbmcgui.ListItem('Settings', iconImage=icon_path('Settings.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='settings':
    xbmc.executebuiltin("Addon.OpenSettings(%s)"%addonID)


elif mode[0]=='favs':
    url = build_url({'mode': 'fav_movies', 'foldername': 'favs'})
    li = xbmcgui.ListItem('Movie Favourites', iconImage=icon_path('Movies.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'fav_tv', 'foldername': 'favs'})
    li = xbmcgui.ListItem('TV Favourites', iconImage=icon_path('Tv_Shows.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

   


    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='fav_tv':
    shows=get_favourite_shows()

    for i in range(len(shows)):
        url = build_url({'mode': 'open_show', 'link': '%s'%(shows[i][1])})
        title=shows[i][0]
        link=shows[i][1]
        thumb=shows[i][2]
        li = xbmcgui.ListItem('%s'%shows[i][0], iconImage=thumb)

        try:
            del_uri = build_url({'mode': 'del_show_fav', 'title':title,  'link':link})

        except:
            del_uri = build_url({'mode': 'del_show_fav', 'title':title.encode('ascii','ignore'),'link':link})

        del_all = build_url({'mode': 'del_tv_all'})

        li.addContextMenuItems([('Remove from PFTV favourites','RunPlugin(%s)'%del_uri),
                                ('Remove all PFTV TV favourites','RunPlugin(%s)'%del_all)])
        
        
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='del_show_fav':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    title=dicti['title'][0]
    link=dicti['link'][0] 
    remove_tv_fav(title,link) 
    xbmc.executebuiltin("Container.Refresh")

elif mode[0]=='del_tv_all':
    delete_all_tv_favs()
    xbmc.executebuiltin("Container.Refresh")
elif mode[0]=='fav_movies':
    movies=get_favourite_movies()
    for i in range(len(movies)):
        title=movies[i][0]
        year=movies[i][1]
        thumb=movies[i][2]
        link=movies[i][3]
        

        my_addon = xbmcaddon.Addon()
        meta_setting = my_addon.getSetting('movie_metadata')
        meta=None
        if meta_setting!='false':
            metaget=metahandlers.MetaData()             
            meta = metaget.get_meta('movie', unicode(title), year=unicode(year))
        if meta==None:
            meta={}
            meta['title']=title
            meta['year']=year
            meta['cover_url']=thumb
            meta['backdrop_url']=None

        url = build_url({'mode': 'open_movie', 'foldername': 'movies', 'link':'%s'%link, 'meta':json.dumps(meta)})
        li = xbmcgui.ListItem('%s (%s)'%(title,year), iconImage='%s'%meta['cover_url'])
        try:
            del_uri = build_url({'mode': 'del_movie_fav', 'title':title, 'thumb':thumb , 'link':link, 'year':year})

        except:
            del_uri = build_url({'mode': 'del_movie_fav', 'title':title.encode('ascii','ignore'), 'thumb':thumb , 'link':link, 'year':year})

        del_all = build_url({'mode': 'del_movie_all'})

        li.addContextMenuItems([('Movie Information', 'XBMC.Action(Info)'),
                                ('Remove from PFTV favourites','RunPlugin(%s)'%del_uri),
                                ('Remove all PFTV Movie favourites','RunPlugin(%s)'%del_all)])
        
        li.setInfo('video', meta)
        li.setProperty("Fanart_Image", meta['backdrop_url'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='del_movie_fav':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    title=dicti['title'][0]
    year=dicti['year'][0]
    thumb=dicti['thumb'][0]
    link=dicti['link'][0] 
    remove_movie_fav(title,year,thumb,link) 
    xbmc.executebuiltin("Container.Refresh")

elif mode[0]=='del_movie_all':
    delete_all_movie_favs()
    xbmc.executebuiltin("Container.Refresh")



elif mode[0]=='movies':
    url = build_url({'mode': 'fav_movies', 'foldername': 'favs'})
    li = xbmcgui.ListItem('Favourites', iconImage=icon_path('Favourites.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'latest_movies', 'foldername': 'movies', 'page':'1'})
    li = xbmcgui.ListItem('Latest Added', iconImage=icon_path('Latest_Added.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'movies_genre', 'foldername': 'movies'})
    li = xbmcgui.ListItem('Genre', iconImage=icon_path('Genre.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'movies_year', 'foldername': 'movies'})
    li = xbmcgui.ListItem('Year', iconImage=icon_path('Year.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'search_movies', 'foldername': 'search'})
    li = xbmcgui.ListItem('Search', iconImage=icon_path('Search.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)


    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='tv':
    url = build_url({'mode': 'fav_tv', 'foldername': 'favs'})
    li = xbmcgui.ListItem('Favourites', iconImage=icon_path('Favourites.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'latest_tv', 'foldername': 'shows'})
    li = xbmcgui.ListItem('Lastest Added', iconImage=icon_path('Last_24_Hours.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'last7_tv', 'foldername': 'shows'})
    li = xbmcgui.ListItem('Last Week', iconImage=icon_path('Last_7_Days.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'az_shows', 'foldername': 'shows'})
    li = xbmcgui.ListItem('A-Z', iconImage=icon_path('AZ.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'all_tv', 'foldername': 'shows'})
    li = xbmcgui.ListItem('All', iconImage=icon_path('All_Shows.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'search_tv', 'foldername': 'search'})
    li = xbmcgui.ListItem('Search', iconImage=icon_path('Search.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)


    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='latest_movies':

    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=dicti['page'][0]
    movies=get_latest_movies(page)
    for i in range(len(movies)):
        title=movies[i][0]
        year=movies[i][1]
        thumb=movies[i][2]
        link=movies[i][3]
        

        my_addon = xbmcaddon.Addon()
        meta_setting = my_addon.getSetting('movie_metadata')
        meta=None
        if meta_setting!='false':
            metaget=metahandlers.MetaData()             
            meta = metaget.get_meta('movie', unicode(title), year=unicode(year))
        if meta==None:
            meta={}
            meta['title']=title
            meta['year']=year
            meta['cover_url']=thumb
            meta['backdrop_url']=None

        url = build_url({'mode': 'open_movie', 'foldername': 'movies', 'link':'%s'%link, 'meta':json.dumps(meta)})
        li = xbmcgui.ListItem('%s (%s)'%(title,year), iconImage='%s'%meta['cover_url'])

        li.setInfo('video', meta)
        try:
            fav_uri = build_url({'mode': 'add_movie_fav', 'title':title, 'thumb':thumb , 'link':link, 'year':year})
        except:
            fav_uri = build_url({'mode': 'add_movie_fav', 'title':title.encode('ascii','ignore'), 'thumb':thumb , 'link':link, 'year':year})


        li.addContextMenuItems([('Movie Information', 'XBMC.Action(Info)'),
                                ('Add to PFTV favourites','RunPlugin(%s)'%fav_uri)])
        li.setProperty("Fanart_Image", meta['backdrop_url'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'latest_movies', 'page': str((int(page)+1))})
    li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='add_movie_fav':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    title=dicti['title'][0]
    year=dicti['year'][0]
    thumb=dicti['thumb'][0]
    link=dicti['link'][0] 
    add_favourite_movie(title,year,link,thumb)    
elif mode[0]=='movies_genre':
    genres=['Action','Adventure','Animation','Biography','Comedy','Crime','Documentary','Drama','Family','Fantasy','History','Horror','Musical','Mystery','Romance','Sci-Fi','Sport','Thriller','War','Western']

    for i in range(len(genres)):
        url = build_url({'mode': 'open_genre', 'slug': '%s'%(genres[i].lower()), 'page':'1'})
        li = xbmcgui.ListItem('%s'%genres[i], iconImage=icon_path('Genre.png'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)




elif mode[0]=='open_genre':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    genre=dicti['slug'][0]
    page=dicti['page'][0]
    movies=get_movies_genre(genre,page)

    for i in range(len(movies)):
        title=movies[i][0]
        year=movies[i][1]
        thumb=movies[i][2]
        link=movies[i][3]
        

        my_addon = xbmcaddon.Addon()
        meta_setting = my_addon.getSetting('movie_metadata')
        meta=None
        if meta_setting!='false':
            metaget=metahandlers.MetaData()             
            meta = metaget.get_meta('movie', unicode(title), year=unicode(year))
        if meta==None:
            meta={}
            meta['title']=title
            meta['year']=year
            meta['cover_url']=thumb
            meta['backdrop_url']=None

        url = build_url({'mode': 'open_movie', 'foldername': 'movies', 'link':'%s'%link, 'meta':json.dumps(meta)})
        li = xbmcgui.ListItem('%s (%s)'%(title,year), iconImage='%s'%meta['cover_url'])

        li.setInfo('video', meta)
        try:
            fav_uri = build_url({'mode': 'add_movie_fav', 'title':title, 'thumb':thumb , 'link':link, 'year':year})
        except:
            fav_uri = build_url({'mode': 'add_movie_fav', 'title':title.encode('ascii','ignore'), 'thumb':thumb , 'link':link, 'year':year})


        li.addContextMenuItems([('Movie Information', 'XBMC.Action(Info)'),
                                ('Add to PFTV favourites','RunPlugin(%s)'%fav_uri)])
        li.setProperty("Fanart_Image", meta['backdrop_url'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'open_genre','slug': genre, 'page': str((int(page)+1))})
    li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)



elif mode[0]=='movies_year':
    years=['2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000']

    for i in range(len(years)):
        url = build_url({'mode': 'open_year', 'year': '%s'%(years[i]), 'page':'1'})
        li = xbmcgui.ListItem('%s'%years[i], iconImage=icon_path('Year.png'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'search_year' })
    li = xbmcgui.ListItem('Enter a Year', iconImage=icon_path('Search.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)


    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_year':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    year=dicti['year'][0]
    page=dicti['page'][0]
    movies=get_movies_year(year,page)
    for i in range(len(movies)):
        title=movies[i][0]
        year=movies[i][1]
        thumb=movies[i][2]
        link=movies[i][3]
        

        my_addon = xbmcaddon.Addon()
        meta_setting = my_addon.getSetting('movie_metadata')
        meta=None
        if meta_setting!='false':
            metaget=metahandlers.MetaData()             
            meta = metaget.get_meta('movie', unicode(title), year=unicode(year))
        if meta==None:
            meta={}
            meta['title']=title
            meta['year']=year
            meta['cover_url']=thumb
            meta['backdrop_url']=None

        url = build_url({'mode': 'open_movie', 'foldername': 'movies', 'link':'%s'%link, 'meta':json.dumps(meta)})
        li = xbmcgui.ListItem('%s (%s)'%(title,year), iconImage='%s'%meta['cover_url'])

        li.setInfo('video', meta)
        try:
            fav_uri = build_url({'mode': 'add_movie_fav', 'title':title, 'thumb':thumb , 'link':link, 'year':year})
        except:
            fav_uri = build_url({'mode': 'add_movie_fav', 'title':title.encode('ascii','ignore'), 'thumb':thumb , 'link':link, 'year':year})


        li.addContextMenuItems([('Movie Information', 'XBMC.Action(Info)'),
                                ('Add to PFTV favourites','RunPlugin(%s)'%fav_uri)])
        li.setProperty("Fanart_Image", meta['backdrop_url'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'open_year','year': year, 'page': str((int(page)+1))})
    li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='search_year':
    keyboard = xbmc.Keyboard('', 'Enter a year', False)
    keyboard.doModal()
    
    if keyboard.isConfirmed():
        year = keyboard.getText()
        page='1'

        movies=get_movies_year(year,page)
    for i in range(len(movies)):
        title=movies[i][0]
        year=movies[i][1]
        thumb=movies[i][2]
        link=movies[i][3]
        

        my_addon = xbmcaddon.Addon()
        meta_setting = my_addon.getSetting('movie_metadata')
        meta=None
        if meta_setting!='false':
            metaget=metahandlers.MetaData()             
            meta = metaget.get_meta('movie', unicode(title), year=unicode(year))
        if meta==None:
            meta={}
            meta['title']=title
            meta['year']=year
            meta['cover_url']=thumb
            meta['backdrop_url']=None

        url = build_url({'mode': 'open_movie', 'foldername': 'movies', 'link':'%s'%link, 'meta':json.dumps(meta)})
        li = xbmcgui.ListItem('%s (%s)'%(title,year), iconImage='%s'%meta['cover_url'])

        li.setInfo('video', meta)
        try:
            fav_uri = build_url({'mode': 'add_movie_fav', 'title':title, 'thumb':thumb , 'link':link, 'year':year})
        except:
            fav_uri = build_url({'mode': 'add_movie_fav', 'title':title.encode('ascii','ignore'), 'thumb':thumb , 'link':link, 'year':year})


        li.addContextMenuItems([('Movie Information', 'XBMC.Action(Info)'),
                                ('Add to PFTV favourites','RunPlugin(%s)'%fav_uri)])
        li.setProperty("Fanart_Image", meta['backdrop_url'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'open_year','year': year, 'page': str((int(page)+1))})
    li = xbmcgui.ListItem('Next Page >>', iconImage=icon_path('Next.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)




elif mode[0]=='latest_tv':
    eps=get_last_eps()
    

    for i in range(len(eps)):


        my_addon = xbmcaddon.Addon()
        action = my_addon.getSetting('episodes_action')
        if action=='0':
            try:
                my_addon = xbmcaddon.Addon()
                meta_setting = my_addon.getSetting('tv_metadata')
                meta=None
                if meta_setting!='false':
                    metaget=metahandlers.MetaData()             
                    meta=metaget.get_episode_meta(eps[i][0], '', eps[i][1], eps[i][2])
                if meta==None:
                    meta={}
                    title='%s'%(eps[i][0])
                    meta['title']=title
                    meta['year']=''
                    meta['poster']=icon_path('TV_Shows.png')
                    meta['backdrop_url']=None



                url = build_url({'mode': 'open_ep', 'link': '%s'%(eps[i][3]), 'show':'%s'%eps[i][0] , 'season':'%s'%eps[i][1] , 'ep':'%s'%eps[i][2], 'meta':json.dumps(meta)})
                li = xbmcgui.ListItem('%s: %sx%s'%(eps[i][0],eps[i][1],eps[i][2]), iconImage=meta['poster'])

                li.setInfo('video', meta)
                li.addContextMenuItems([(('Episode Information', 'XBMC.Action(Info)'))])
                li.setProperty("Fanart_Image", meta['backdrop_url'])
        
                
            except:
                sh=eps[i][0].encode('ascii','ignore')
                
                my_addon = xbmcaddon.Addon()
                meta_setting = my_addon.getSetting('tv_metadata')
                meta=None
                if meta_setting!='false':
                    metaget=metahandlers.MetaData()             
                    meta=metaget.get_episode_meta(sh, '', eps[i][1], eps[i][2])
                if meta==None:
                    meta={}
                    title='%s'%(eps[i][0])
                    meta['title']=title
                    meta['year']=''
                    meta['poster']=icon_path('TV_Shows.png')
                    meta['backdrop_url']=None



                url = build_url({'mode': 'open_ep', 'link': '%s'%(eps[i][3]), 'show':'%s'%sh , 'season':'%s'%eps[i][1] , 'ep':'%s'%eps[i][2], 'meta':json.dumps(meta)})
                li = xbmcgui.ListItem('%s: %sx%s'%(eps[i][0],eps[i][1],eps[i][2]), iconImage=meta['poster'])

                li.setInfo('video', meta)
                li.addContextMenuItems([(('Episode Information', 'XBMC.Action(Info)'))])
                li.setProperty("Fanart_Image", meta['backdrop_url'])

        else:
                try:
                    my_addon = xbmcaddon.Addon()
                    meta_setting = my_addon.getSetting('tv_metadata')
                    meta=None
                    if meta_setting!='false':
                        metaget=metahandlers.MetaData()             
                        meta=metaget.get_episode_meta(eps[i][0], '', eps[i][1], eps[i][2])
                    if meta==None:
                        meta={}
                        title='%s'%(eps[i][0])
                        meta['title']=title
                        meta['year']=''
                        meta['poster']=icon_path('TV_Shows.png')
                        meta['backdrop_url']=None

                    play_url = build_url({'mode': 'open_ep_dialog', 'link': '%s'%(eps[i][3]), 'show':'%s'%eps[i][0] , 'season':'%s'%eps[i][1] , 'ep':'%s'%eps[i][2], 'meta':json.dumps(meta)})
                except:
                    sh=eps[i][0].encode('ascii','ignore')
                    my_addon = xbmcaddon.Addon()
                    meta_setting = my_addon.getSetting('tv_metadata')
                    meta=None
                    if meta_setting!='false':
                        metaget=metahandlers.MetaData()             
                        meta=metaget.get_episode_meta(sh, '', eps[i][1], eps[i][2])
                    if meta==None:
                        meta={}
                        title='%s'%(eps[i][0])
                        meta['tvshowtitle']=title
                        meta['year']=''
                        meta['poster']=icon_path('TV_Shows.png')
                        meta['backdrop_url']=None
                    play_url = build_url({'mode': 'open_ep_dialog', 'link': '%s'%(eps[i][3]), 'show':'%s'%sh , 'season':'%s'%eps[i][1] , 'ep':'%s'%eps[i][2], 'meta':json.dumps(meta)})

                url = build_url({'mode': 'more_tv','link':'%s'%eps[i][3]})

                li = xbmcgui.ListItem('%s: %sx%s'%(eps[i][0],eps[i][1],eps[i][2]), iconImage=meta['poster'])

                li.setInfo('video', meta)
                li.addContextMenuItems([(('Episode Information', 'XBMC.Action(Info)')),
                                        ('Open episode', 'RunPlugin(%s)'%play_url)])
                li.setProperty("Fanart_Image", meta['backdrop_url'])


        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='open_ep_dialog':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    sh=dicti['show'][0]
    s=dicti['season'][0]
    e=dicti['ep'][0]
    meta=json.loads(dicti['meta'][0])


    links=get_links(link)
    hosts=[]
    for i in range(len(links)):
        hosts+=[links[i][0]+' ('+links[i][2]+')']


    dialog = xbmcgui.Dialog()
    index = dialog.select('Choose a link', hosts)
    if index>-1:
        if meta['title']==sh:
            meta['tvshowtitle']=sh
            meta['title']='%s: %sx%s'%(sh,s,e)
            meta['season']=s
            meta['episode']=e
        link=get_link(links[index][1])
        import urlresolver
        resolved=urlresolver.resolve(link)

        li = xbmcgui.ListItem('%s: %sx%s'%(sh,s,e))
        li.setInfo('video', meta)
        
        
        li.setProperty('IsPlayable', 'true')

        xbmc.Player().play(item=resolved, listitem=li)



elif mode[0]=='more_tv':
    
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=dicti['link'][0]
    
    show=get_show_from_ep(page)
    

    episodes=get_episodes(show)


    for ep in reversed(episodes):

        my_addon = xbmcaddon.Addon()
        meta_setting = my_addon.getSetting('tv_metadata')
        meta=None
        if meta_setting!='false':
            metaget=metahandlers.MetaData()             
            meta=metaget.get_episode_meta(ep[0], '', ep[1], ep[2])
        if meta==None:
            meta={}
            title='%s'%(ep[0])
            meta['title']=title
            meta['year']=''
            meta['poster']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None



        url = build_url({'mode': 'open_ep', 'link': '%s'%(ep[3]), 'show':'%s'%ep[0] , 'season':'%s'%ep[1] , 'ep':'%s'%ep[2], 'meta':json.dumps(meta)})
        li = xbmcgui.ListItem('%sx%s. %s'%(ep[1],ep[2], meta['title']), iconImage=meta['poster'])

        li.setInfo('video', meta)
        li.addContextMenuItems([(('Episode Information', 'XBMC.Action(Info)'))])
        li.setProperty("Fanart_Image", meta['backdrop_url'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='last7_tv':
    days=get_last_days()

    for i in range(len(days)):
        url = build_url({'mode': 'open_days', 'ind': '%s'%(days[i][1])})
        li = xbmcgui.ListItem('%s'%days[i][0], iconImage=icon_path('Upcoming.png'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='open_days':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=dicti['ind'][0]

    eps=get_day_eps(int(page))
    

    for i in range(len(eps)):


        my_addon = xbmcaddon.Addon()
        action = my_addon.getSetting('episodes_action')
        if action=='0':
            try:
                my_addon = xbmcaddon.Addon()
                meta_setting = my_addon.getSetting('tv_metadata')
                meta=None
                if meta_setting!='false':
                    metaget=metahandlers.MetaData()             
                    meta=metaget.get_episode_meta(eps[i][0], '', eps[i][1], eps[i][2])
                if meta==None:
                    meta={}
                    title='%s'%(eps[i][0])
                    meta['title']=title
                    meta['year']=''
                    meta['poster']=icon_path('TV_Shows.png')
                    meta['backdrop_url']=None



                url = build_url({'mode': 'open_ep', 'link': '%s'%(eps[i][3]), 'show':'%s'%eps[i][0] , 'season':'%s'%eps[i][1] , 'ep':'%s'%eps[i][2], 'meta':json.dumps(meta)})
                li = xbmcgui.ListItem('%s: %sx%s'%(eps[i][0],eps[i][1],eps[i][2]), iconImage=meta['poster'])

                li.setInfo('video', meta)
                li.addContextMenuItems([(('Episode Information', 'XBMC.Action(Info)'))])
                li.setProperty("Fanart_Image", meta['backdrop_url'])
        
                
            except:
                sh=eps[i][0].encode('ascii','ignore')
                
                my_addon = xbmcaddon.Addon()
                meta_setting = my_addon.getSetting('tv_metadata')
                meta=None
                if meta_setting!='false':
                    metaget=metahandlers.MetaData()             
                    meta=metaget.get_episode_meta(sh, '', eps[i][1], eps[i][2])
                if meta==None:
                    meta={}
                    title='%s'%(eps[i][0])
                    meta['title']=title
                    meta['year']=''
                    meta['poster']=icon_path('TV_Shows.png')
                    meta['backdrop_url']=None



                url = build_url({'mode': 'open_ep', 'link': '%s'%(eps[i][3]), 'show':'%s'%sh , 'season':'%s'%eps[i][1] , 'ep':'%s'%eps[i][2], 'meta':json.dumps(meta)})
                li = xbmcgui.ListItem('%s: %sx%s'%(eps[i][0],eps[i][1],eps[i][2]), iconImage=meta['poster'])

                li.setInfo('video', meta)
                li.addContextMenuItems([(('Episode Information', 'XBMC.Action(Info)'))])
                li.setProperty("Fanart_Image", meta['backdrop_url'])

        else:
                try:
                    my_addon = xbmcaddon.Addon()
                    meta_setting = my_addon.getSetting('tv_metadata')
                    meta=None
                    if meta_setting!='false':
                        metaget=metahandlers.MetaData()             
                        meta=metaget.get_episode_meta(eps[i][0], '', eps[i][1], eps[i][2])
                    if meta==None:
                        meta={}
                        title='%s'%(eps[i][0])
                        meta['title']=title
                        meta['year']=''
                        meta['poster']=icon_path('TV_Shows.png')
                        meta['backdrop_url']=None

                    play_url = build_url({'mode': 'open_ep_dialog', 'link': '%s'%(eps[i][3]), 'show':'%s'%eps[i][0] , 'season':'%s'%eps[i][1] , 'ep':'%s'%eps[i][2], 'meta':json.dumps(meta)})
                except:
                    sh=eps[i][0].encode('ascii','ignore')
                    my_addon = xbmcaddon.Addon()
                    meta_setting = my_addon.getSetting('tv_metadata')
                    meta=None
                    if meta_setting!='false':
                        metaget=metahandlers.MetaData()             
                        meta=metaget.get_episode_meta(sh, '', eps[i][1], eps[i][2])
                    if meta==None:
                        meta={}
                        title='%s'%(eps[i][0])
                        meta['title']=title
                        meta['year']=''
                        meta['poster']=icon_path('TV_Shows.png')
                        meta['backdrop_url']=None
                    play_url = build_url({'mode': 'open_ep_dialog', 'link': '%s'%(eps[i][3]), 'show':'%s'%sh , 'season':'%s'%eps[i][1] , 'ep':'%s'%eps[i][2], 'meta':json.dumps(meta)})

                url = build_url({'mode': 'more_tv','link':'%s'%eps[i][3]})

                li = xbmcgui.ListItem('%s: %sx%s'%(eps[i][0],eps[i][1],eps[i][2]), iconImage=meta['poster'])

                li.setInfo('video', meta)
                li.addContextMenuItems([(('Episode Information', 'XBMC.Action(Info)')),
                                        ('Open episode', 'RunPlugin(%s)'%play_url)])
                li.setProperty("Fanart_Image", meta['backdrop_url'])


        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='az_shows':
    abc=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' , '1', '2', '3', '5', '9']

    for i in range(len(abc)):
        if abc[i] not in '12359':
            url = build_url({'mode': 'open_letter', 'letter':'%s'%abc[i]})
            li = xbmcgui.ListItem('%s'%abc[i], iconImage=icon_path('%s.png'%abc[i]))
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
        else:
            url = build_url({'mode': 'open_letter', 'letter':'%s'%abc[i]})
            li = xbmcgui.ListItem('%s'%abc[i], iconImage=icon_path('0.png'))
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_letter':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    letter=dicti['letter'][0]

    shows=get_shows_by_letter(letter)

    for i in range(len(shows)):
        url = build_url({'mode': 'open_show', 'link': '%s'%(shows[i][1])})
        li = xbmcgui.ListItem('%s'%shows[i][0], iconImage=icon_path('TV_Shows.png'))
        try:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': shows[i][0],'link': shows[i][1]})
        except:
            fav_uri = build_url({'mode': 'add_tv_fav', 'show': ((shows[i][0]).encode('ascii','ignore')),'link':shows[i][1] })

        li.addContextMenuItems([ ('Add to PFTV favourites', 'RunPlugin(%s)'%fav_uri)])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='all_tv':
    shows=get_all_shows()
    

    for i in range(len(shows)):
        url = build_url({'mode': 'open_show', 'link': '%s'%(shows[i][1])})
        li = xbmcgui.ListItem('%s'%shows[i][0], iconImage=icon_path('TV_Shows.png'))

        fav_uri = build_url({'mode': 'add_tv_fav', 'show': shows[i][0],'link': shows[i][1]})

        li.addContextMenuItems([ ('Add to PFTV favourites', 'RunPlugin(%s)'%fav_uri)])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='add_tv_fav':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    name=dicti['show'][0]
    link=dicti['link'][0]
    thumb=get_show_img(link)

    add_favourite_show(name,link,thumb)


elif mode[0]=='open_show':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]

    seasons=get_seasons(link)

    for season in seasons:
        url = build_url({'mode': 'open_season', 'link': '%s'%(season[1])})
        li = xbmcgui.ListItem('%s'%season[0], iconImage=icon_path('TV_Shows.png'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_season':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]

    episodes=get_episodes(link)
    for ep in episodes:

        my_addon = xbmcaddon.Addon()
        meta_setting = my_addon.getSetting('tv_metadata')
        meta=None
        if meta_setting!='false':
            metaget=metahandlers.MetaData()             
            meta=metaget.get_episode_meta(ep[0], '', ep[1], ep[2])
        if meta==None:
            meta={}
            title='%s'%(ep[0])
            meta['title']=title
            meta['year']=''
            meta['poster']=icon_path('TV_Shows.png')
            meta['backdrop_url']=None



        url = build_url({'mode': 'open_ep', 'link': '%s'%(ep[3]), 'show':'%s'%ep[0] , 'season':'%s'%ep[1] , 'ep':'%s'%ep[2], 'meta':json.dumps(meta)})
        li = xbmcgui.ListItem('%sx%s. %s'%(ep[1],ep[2], meta['title']), iconImage=meta['poster'])

        li.setInfo('video', meta)
        li.addContextMenuItems([(('Episode Information', 'XBMC.Action(Info)'))])
        li.setProperty("Fanart_Image", meta['backdrop_url'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_ep':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    sh=dicti['show'][0]
    s=dicti['season'][0]
    e=dicti['ep'][0]
    meta=dicti['meta'][0]
    links=get_links(link)
    my_addon = xbmcaddon.Addon()

    setting = my_addon.getSetting('host_select')
    if setting=='0':

        for link in links:

            url = build_url({'mode': 'open_link', 'link': '%s'%(link[1]), 'show':'%s'%sh , 'season':'%s'%s , 'ep':'%s'%e , 'meta':meta })
            if link[2]!='today':
                li = xbmcgui.ListItem('%s (%s ago)'%(link[0],link[2]), iconImage=icon_path('TV_Shows.png'))
            else:
                li = xbmcgui.ListItem('%s (%s)'%(link[0],link[2]), iconImage=icon_path('TV_Shows.png'))

            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
        xbmcplugin.endOfDirectory(addon_handle)


    else:
        hosts=[]
        for i in range(len(links)):
            hosts+=[links[i][0]+' ('+links[i][2]+')']


        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose a link', hosts)
        if index>-1:
            link=get_link(links[index][1])
            import urlresolver
            resolved=urlresolver.resolve(link)

            li = xbmcgui.ListItem('%s: %sx%s'%(sh,s,e))
            li.setInfo('video', json.loads(meta))
            
            
            li.setProperty('IsPlayable', 'true')

            xbmc.Player().play(item=resolved, listitem=li)


elif mode[0]=='open_link':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    sh=dicti['show'][0]
    s=dicti['season'][0]
    e=dicti['ep'][0]
    meta=json.loads(dicti['meta'][0])


    link=get_link(link)
    import urlresolver
    resolved=urlresolver.resolve(link)

    if meta['title']==sh:
        meta['tvshowtitle']=sh
        meta['title']='%s: %sx%s'%(sh,s,e)
        meta['season']=s
        meta['episode']=e
                               


    li = xbmcgui.ListItem(meta['title'])
    li.setInfo('video',meta)
    
    
    li.setProperty('IsPlayable', 'true')
    li.setThumbnailImage(meta['poster'])


    xbmc.Player().play(item=resolved, listitem=li)



elif mode[0]=='open_movie':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    meta =dicti['meta'][0]
    links=get_links(link)
    my_addon = xbmcaddon.Addon()
    setting = my_addon.getSetting('host_select')
    if setting=='0':
        for link in links:

            url = build_url({'mode': 'open_movie_link', 'link': '%s'%(link[1]), 'meta':meta  })
            li = xbmcgui.ListItem('%s'%(link[0]), iconImage=icon_path('TV_Shows.png'))

            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
        xbmcplugin.endOfDirectory(addon_handle)
    else:
        hosts=[]
        for i in range(len(links)):
            hosts+=[links[i][0]]


        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose a link', hosts)
        if index>-1:
            link=get_link(links[index][1])
            import urlresolver
            resolved=urlresolver.resolve(link)
            meta=json.loads(meta)
            li = xbmcgui.ListItem(meta['title'])
            li.setInfo('video', meta)
            
            li.setThumbnailImage(meta['cover_url'])

            li.setProperty('IsPlayable', 'true')

            xbmc.Player().play(item=resolved, listitem=li)



elif mode[0]=='open_movie_link':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    meta =dicti['meta'][0]
    meta=json.loads(meta)
    link=get_link(link)
    import urlresolver
    resolved=urlresolver.resolve(link)
    
    li = xbmcgui.ListItem('%s'%meta['title'])
    li.setInfo('video', meta)
    li.setThumbnailImage(meta['cover_url'])
    
    
    li.setProperty('IsPlayable', 'true')

    xbmc.Player().play(item=resolved, listitem=li)

elif mode[0]=='search':
    url = build_url({'mode': 'search_movies', 'foldername': 'search'})
    li = xbmcgui.ListItem('Search Movies', iconImage=icon_path('Search.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'search_tv', 'foldername': 'search'})
    li = xbmcgui.ListItem('Search TV Shows', iconImage=icon_path('Search.png'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)


    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='search_movies':
    keyboard = xbmc.Keyboard('', 'Search movies', False)
    keyboard.doModal()
    
    if keyboard.isConfirmed():
        query = keyboard.getText()
        movies=search(query,'movie')

        for i in range(len(movies)):
            title=movies[i][0]
            year=movies[i][1]
            thumb=movies[i][2]
            link=movies[i][3]
            

            my_addon = xbmcaddon.Addon()
            meta_setting = my_addon.getSetting('movie_metadata')
            meta=None
            if meta_setting!='false':
                metaget=metahandlers.MetaData()             
                meta = metaget.get_meta('movie', unicode(title), year=unicode(year))
            if meta==None:
                meta={}
                meta['title']=title
                meta['year']=year
                meta['cover_url']=thumb
                meta['backdrop_url']=None

            url = build_url({'mode': 'open_movie', 'foldername': 'movies', 'link':'%s'%link, 'meta':json.dumps(meta)})
            li = xbmcgui.ListItem('%s (%s)'%(title,year), iconImage='%s'%meta['cover_url'])

            li.setInfo('video', meta)
            try:
                fav_uri = build_url({'mode': 'add_movie_fav', 'title':title, 'thumb':thumb , 'link':link, 'year':year})
            except:
                fav_uri = build_url({'mode': 'add_movie_fav', 'title':title.encode('ascii','ignore'), 'thumb':thumb , 'link':link, 'year':year})


            li.addContextMenuItems([('Movie Information', 'XBMC.Action(Info)'),
                                ('Add to PFTV favourites','RunPlugin(%s)'%fav_uri)])
            li.setProperty("Fanart_Image", meta['backdrop_url'])
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    
        xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='search_tv':
    keyboard = xbmc.Keyboard('', 'Search TV Episodes', False)
    keyboard.doModal()
    
    if keyboard.isConfirmed():
        query = keyboard.getText()
        episodes=search(query,'tv')

        for ep in episodes:

            my_addon = xbmcaddon.Addon()
            meta_setting = my_addon.getSetting('tv_metadata')
            meta=None
            if meta_setting!='false':
                metaget=metahandlers.MetaData()             
                meta=metaget.get_episode_meta(ep[0], '', ep[1], ep[2])
            if meta==None:
                meta={}
                title='%s'%(ep[0])
                meta['title']=title
                meta['year']=''
                meta['poster']=icon_path('TV_Shows.png')
                meta['backdrop_url']=None



            url = build_url({'mode': 'open_ep', 'link': '%s'%(ep[3]), 'show':'%s'%ep[0] , 'season':'%s'%ep[1] , 'ep':'%s'%ep[2], 'meta':json.dumps(meta)})
            li = xbmcgui.ListItem('%sx%s. %s'%(ep[1],ep[2], meta['title']), iconImage=meta['poster'])

            li.setInfo('video', meta)
            li.addContextMenuItems([(('Episode Information', 'XBMC.Action(Info)'))])
            li.setProperty("Fanart_Image", meta['backdrop_url'])
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
        xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='erase_all':
    ret = xbmcgui.Dialog().yesno('Remove all favourites', 'Are you sure you want to reset your favourites?' ) 
    
    if ret:       

        delete_all_movie_favs()
        delete_all_tv_favs()
        xbmcgui.Dialog().ok("ProjectFreeTV.so", "Successfully erased favourites database!")




