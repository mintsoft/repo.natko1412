# -*- coding: utf-8 -*-

'''
Filmovita addon 
Autor: natko1412
Godina: 2015

Discalimer:
Izvorni kod možete mijenjati prema licenci isporucenoj sa programom

'''
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
#import urlresolver
import json
import HTMLParser
import sqlite3
import os



addonID=xbmcaddon.Addon().getAddonInfo("id")
db_dir = xbmc.translatePath("special://profile/addon_data/"+addonID)


db_dir = xbmc.translatePath("special://profile/addon_data/"+addonID)
db_path = os.path.join(db_dir, 'favourites.db')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

db=sqlite3.connect(db_path)


######################













###########################################################
#functions
category=['akcijski filmovi','animirani filmovi','avanturisticki filmovi','dokumentarni filmovi','domaci filmovi','drame',
                    'fantazije','horor filmovi','filmovi komedije','kriminalisticki filmovi','povijesni filmovi','ratni filmovi',
                    'romanticni filmovi','sf filmovi','sinkronizirani crtici','sport','sportski filmovi','trileri','westerni']



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


trakt_header= {
      'Content-Type': 'application/json',
      'trakt-api-version': '2',
      'trakt-api-key': '%s'%trakt_api,
      
      
    }


def get_episode_link(show_slug,season,number,show_year):
        slugs=['game-of-thrones','walking-dead','vampire-diaries','breaking-bad','tudors','da-vincis-demons',
            'vikings','better-call-saul','true-detective','originals','gotham','sherlock','blacklist','rome']
        slugy=['game-of-thrones','the-walking-dead','the-vampire-diaries','breaking-bad','the-tudors','da-vinci-s-demons',
            'vikings','better-call-saul','true-detective','the-originals','gotham','sherlock','the-blacklist','rome']

        for i in range(len(slugy)):
            if slugy[i]==show_slug:
                index=i
                break

        slug=slugs[index]

        if season=='6': season='sesta'
        if season=='5': season='peta'
        if season=='4': season='cetvrta'
        if season=='3': season='treca'
        if season=='2': season='druga'
        if season=='1': season='prva'

        url='http://www.serijex.com/%s-%s-sezona-epizoda-%s/'%(slug,season,number)
        print(url)
        return url
        

def cache_foldername(foldername,fake):
    
    cur = db.cursor() 
    cur.execute("drop table if exists Cache")
    init_favourites()
 
    cur.execute("begin")   
    cur.execute('INSERT INTO Cache(Folder, Folder_fake) VALUES ("%s","%s");'%(foldername,fake))
    db.commit()
    cur.close()

def return_cached(fake_name):
    cur = db.cursor()    
    cur.execute("begin")  
    
    cur.execute("SELECT Folder FROM Cache WHERE Folder_fake = ? LIMIT 1 ;",(fake_name,))

    rows = cur.fetchall()
    cur.close()
    channels=[]
    
    
    
    return rows
def get_tvshows():

    slugs=['game-of-thrones','the-walking-dead','the-vampire-diaries','breaking-bad','the-tudors','da-vinci-s-demons',
            'vikings','better-call-saul','true-detective','the-originals','gotham','sherlock','the-blacklist','rome']


    results=[]
    for slug in slugs:
        request = urllib2.Request('https://api-v2launch.trakt.tv/shows/%s?extended=images'%slug, headers=trakt_header)
        response_body = urllib2.urlopen(request).read().decode('utf-8')
        decoded_data=json.loads(response_body)

        title=decoded_data['title']
        year=decoded_data['year']
        thumb=decoded_data['images']['poster']['thumb']
        slug=decoded_data['ids']['slug']
        imdb=decoded_data['ids']['imdb']
        trakt=decoded_data['ids']['trakt']
        
        results.append([title,year,slug,imdb,trakt,thumb])
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
def init_favourites():
    
    with db:
    
        cur = db.cursor()    
        cur.execute("begin") 
        cur.execute("create table if not exists Favourites (Title TEXT, Link TEXT, Thumb TEXT, Fan Text)")
        cur.execute("create table if not exists Cache (Folder TEXT, Folder_fake TEXT)")
        
        db.commit()
        cur.close()
    return

def add_to_favourites(title,link,img,fan):
    init_favourites()
    cur = db.cursor()  
    cur.execute("begin")   
    cur.execute("INSERT INTO Favourites(Title,Link,Thumb, Fan) VALUES (?,?,?, ?);",(title,link,img,fan))
    db.commit()
    cur.close()
    return

def get_favourites():
    init_favourites()

    cur = db.cursor()
    cur.execute("begin")     
    cur.execute("SELECT Title,Link,Thumb, Fan FROM Favourites")
    
    rows = cur.fetchall()
    cur.close()
    favs=[]
    for i in range (len(rows)):
        folder=rows[i]
        favs+=[folder]
    

    
    return favs
def delete_all_favs():
   
    
    with db:
    
        cur = db.cursor()
         
    
        cur.execute("drop table if exists Favourites")
        cur.close()


    return

def remove_fav(title,link,thumb):
    #DELETE FROM COMPANY WHERE ID = 7

    

    cur = db.cursor()  
    cur.execute("begin")  
    cur.execute("DELETE FROM Favourites WHERE Title = ? AND Link = ? AND Thumb = ?",(title,link,thumb))

    db.commit()
    cur.close()
def get_host_names(urls):
    names=[]
    
    for i in range(len(urls)):
        url=urls[i]
        print(url)
        if 'www'in url:
            reg='http://www.(.+?)/'
        elif 'https' in url:
            reg='https://(.+?)/'
        else:
            reg='http://(.+?)/'
        try:
            name=re.findall(re.compile(reg),url)[0]
            names+=['%d. %s'%(i+1,name)]
        except:
            names+=[url]
    return names
    


def get_movie_info(link):
    read=read_url(link)
    reg='"http://www.imdb.com/title/(.+?)/"'
    pat=re.compile(reg)

    imdb=re.findall(pat,read)[0]

    #https://api-v2launch.trakt.tv/search?id_type=imdb&id=tt0848228
    request = urllib2.Request('https://api-v2launch.trakt.tv/search?id_type=imdb&id=%s'%imdb, headers=trakt_header)
    response_body = urllib2.urlopen(request).read().decode('utf-8')
    decoded_data=json.loads(response_body)
    results=[]
    for i in range(len(decoded_data)):
        title=decoded_data[i]['movie']['title']
        year=decoded_data[i]['movie']['year']
        thumb=decoded_data[i]['movie']['images']['poster']['thumb']
        fanart=decoded_data[i]['movie']['images']['fanart']['full']
        desc=decoded_data[i]['movie']['overview']
        
        results.append([title,year,desc,thumb,fanart])
    return results




def get_title(link):
    html=read_url(link)
    reg='class="entry-title">(.+?)</h1>'
    reg2='img src="(.+?)"'
    title=re.findall(re.compile(reg),html)[0]
    img=re.findall(re.compile(reg2),html)[0]
    print(img)
    if '(' in title and ')' in title:
        a=title.index('(')
        titel=title[:a]
        b=len(title)-1
        year=title[a+1:b]
        return[titel,year,img]
    else:
        return[title,'x',img]


def get_links(url):
    def get_string(text):
        string=text
        #numbers
        string=string.replace('\\u0030','0').replace('\\u0031','1').replace('\\u0032','2').replace('\\u0033','3').replace('\\u0034','4').replace('\\u0035','5').replace('\\u0036','6').replace('\\u0037','7').replace('\\u0038','8').replace('\\u0039','9')
        #special chars
        string=string.replace('\\u0020',' ').replace('\\u0021','!').replace('\\u0022','"').replace('\\u0023','#').replace('\\u0024','$').replace('\\u0025','%').replace('\\u0026','&')  
        string=string.replace('\\u0027',"'").replace('\\u0028','(').replace('\\u0029',')').replace('\\u002a','*').replace('\\u002b','+').replace('\\u002c',',').replace('\\u002d','-').replace('\\u002e','.').replace('\\u002f','/')    
        string=string.replace('\\u003a',':').replace('\\u003b',';').replace('\\u003c','<').replace('\\u003d','=').replace('\\u003e','>').replace('\\u003f','?').replace('\\u0040','@')  
        string=string.replace('\\u005b','[').replace('\\u005c','\\').replace('\\u005d',']').replace('\\u005e','^').replace('\\u005f','_').replace('\\u0060','`')
        string=string.replace('\\u007b','{').replace('\\u007c','|').replace('\\u007d','}').replace('\\u007e','~')
        #eng alpha
        string=string.replace('\\u0041','A').replace('\\u0042','B').replace('\\u0043','C').replace('\\u0044','D').replace('\\u0045','E').replace('\\u0046','F').replace('\\u0047','G').replace('\\u0048','H').replace('\\u0049','I').replace('\\u004a','J').replace('\\u004b','K').replace('\\u004c','L').replace('\\u004d','M').replace('\\u004e','N').replace('\\u004f','O')
        string=string.replace('\\u0050','P').replace('\\u0051','Q').replace('\\u0052','R').replace('\\u0053','S').replace('\\u0054','T').replace('\\u0055','U').replace('\\u0056','V').replace('\\u0057','W').replace('\\u0058','X').replace('\\u0059','Y').replace('\\u005a','Z')
        
        string=string.replace('\\u0061','a').replace('\\u0062','b').replace('\\u0063','c').replace('\\u0064','d').replace('\\u0065','e').replace('\\u0066','f').replace('\\u0067','g').replace('\\u0068','h').replace('\\u0069','i').replace('\\u006a','j').replace('\\u006b','k').replace('\\u006c','l').replace('\\u006d','m').replace('\\u006e','n').replace('\\u006f','o')
        string=string.replace('\\u0070','p').replace('\\u0071','q').replace('\\u0072','r').replace('\\u0073','s').replace('\\u0074','t').replace('\\u0075','u').replace('\\u0076','v').replace('\\u0077','w').replace('\\u0078','x').replace('\\u0079','y').replace('\\u007a','z')

        #hrv abc
        string=string.replace('\\u00d0','D').replace('\\u0106','C').replace('\\u0107','c').replace('\\u010c','C').replace('\\u010d','c').replace('\\u0160','S').replace('\\u0161','s').replace('\\u017d','Z').replace('\\u017e','z')
        string=string.replace('\\u000a','\n')
        return string

    def check(lista):
        lista=lista
        for i in range(len(lista)):
            if 'klipovito' in lista[i]:
                lista.pop(i)
                check(lista)
                break
            elif 'filmovita' in lista[i]:
                lista.pop(i)
                check(lista)
                break
            elif 'facebook' in lista[i]:
                lista.pop(i)
                check(lista)
                break
            elif 'twitter' in lista[i]:
                lista.pop(i)
                check(lista)
                break
            elif 'tvprofil' in lista[i]:
                lista.pop(i)
                check(lista)
                break
            elif 'narod.hr' in lista[i]:
                lista.pop(i)
                check(lista)
                break
        return lista

    def get_sites_linkovi(link):
        hosts=['streamin','played','vodlocker','neodrive','openload','filehoot','videowood','thevideo']
        read=read_url(link)
        sites=[]
        for i in range (len(hosts)):
            try:    
                reg='http://www.filmovita.com/(.+?)-%s/'%hosts[i]
                site='http://www.filmovita.com/' + re.findall(re.compile(reg),read)[0] +'-%s/'%hosts[i]
                sites+=[site]
            except: pass
        return sites

    def get_links_from_sites(sites):
        links=[]
        for i in range(len(sites)):
            html=read_url(sites[i])
            reg="id='engimadiv(.+?)'"
            enigma="engimadiv" + re.findall(re.compile(reg),html)[0] 
            soup=bs(html)
            text=soup.find('span',{'id':'%s'%enigma})['data-enigmav']
            text=get_string(text).lower()

            reg='src="(.+?)"'
            link=re.findall(re.compile(reg),text)[0]
            links+=[link]
        return links
    def get_links_str2(link):
        text=read_url(link)
        reg='href="(.+?)"'
        links=re.findall(re.compile(reg),text)
        return links


    def get_links_enigma(url):
        html=read_url(url)
        reg="id='engimadiv(.+?)'"
        enigma="engimadiv" + re.findall(re.compile(reg),html)[0] 
        soup=bs(html)
        text=soup.find('span',{'id':'%s'%enigma})['data-enigmav']
        text=get_string(text).lower()

        reg='href="(.+?)"'
        links=re.findall(re.compile(reg),text)
        return check(links)
    def get_links_verzija(url):
        print(url)
        html=read_url(url).lower()

        reg='<iframe (.+?) src="(.+?)"'
        
        listy=re.findall(re.compile(reg),html)
        items=[]
        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[1]
            items+=[item]
    
        reg="<iframe (.+?) src='(.+?)'"
        
        listy=re.findall(re.compile(reg),html)
        
        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[1]
            items+=[item]

        

        reg='href="(.+?)" (.+?)>gledaj na'
        listy=re.findall(re.compile(reg),html)

        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[0]
            print(item)
            items+=[item]
        
        return items

        
    html=read_url(url)
    
    if 'http://filmovita.com/links/' in html:
        print('With LINKS')
        reg='http://filmovita.com/links/(.+?)"'
        link='http://filmovita.com/links/' + re.findall(re.compile(reg),html)[0]
        sites=get_sites_linkovi(link)
        links=get_links_from_sites(sites)
        
        
        reg='http://filmovita.com/links/(.+?)"'
        link='http://filmovita.com/links/' + re.findall(re.compile(reg),html)[0]
            
        linko=get_links_str2(link)
        for i in range(len(linko)):
            links+=[linko[i]]
        
    elif 'enigmadiv' in html or 'enigmav' in html:
        print('with ENIGMA')
        links=get_links_enigma(url)
        
    elif 'Verzija' in html:
        print('with VERZIJA')
        links=get_links_verzija(url)
        
    elif 'youtube.com/embed/' in html:
        return ['Film je u vise djelova na youtube-u.','Posjetite filmovita.com']
    else:
        print('ELSEEE')
        reg='<iframe (.+?) src="(.+?)"'
        
        listy=re.findall(re.compile(reg),html)
        items=[]
        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[1]
            items+=[item]
        if check(items)==[]:
            reg="<iframe (.+?) src='(.+?)'"
        
        listy=re.findall(re.compile(reg),html)
        items=[]
        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[1]
            links+=[item]
    if links==[]:
        html=read_url(url).lower()

        reg='<iframe src="(.+?)"'
        
        listy=re.findall(re.compile(reg),html)
        items=[]
        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[1]
            items+=[item]
        if check(items)==[]:
            reg="<iframe (.+?) src='(.+?)'"
        
        listy=re.findall(re.compile(reg),html)
        items=[]
        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[1]
            links+=[item]
        reg='<iframe (.+?) src="(.+?)"'
        
        listy=re.findall(re.compile(reg),html)
        items=[]
        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[1]
            items+=[item]
        if check(items)==[]:
            reg="<iframe (.+?) src='(.+?)'"
        
        listy=re.findall(re.compile(reg),html)
        items=[]
        for i in range(len(listy)):
            lista=list(listy[i])
            item=lista[1]
            links+=[item]


    return check(links)
















def get_list_of_movies_genre(url,tag_categ):
    category_tags=['akcijski filmovi','animirani filmovi','avanturisticki filmovi','dokumentarni filmovi','domaci filmovi','drame',
                    'fantazije','horor filmovi','filmovi komedije','kriminalisticki filmovi','povijesni filmovi','ratni filmovi',
                    'romanticni filmovi','sf filmovi','sinkronizirani crtici','sport','sportski filmovi','trileri','westerni']
    if tag_categ in category_tags:
        pass
    else:
        return ['pogreska']


    reg='href="(.+?)"'
    pat=re.compile(reg)

    reg2='src="(.+?)"'
    pat2=re.compile(reg2)

    reg3='<iframe src="(.+?)"'
    pat3=re.compile(reg3)

    reg4='<IFRAME SRC="(.+?)"'
    pat4=re.compile(reg4)

    reg5='<script type="text/javascript" src="(.+?)"'
    pat5=re.compile(reg5)

    reg6='http://www.imdb.com/title/(.+?)/'
    imdb=re.compile(reg6)
    url=url

    req = urllib2.Request(url=url,headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    request = urllib2.urlopen(req)
    html=request.read()

    soup=bs(html)

    imena=[]
    links=[]
    linkks=[]
    te=soup.find("img",{"alt":"%s"%tag_categ})
    tag=te.findNext("ul", {"class":"lcp_catlist"})
    tags=tag.findAll('a')
    linkovi=''
    for i in range(len(tags)):
        pp=tags[i]
        ime=pp.getText()

        pp=unicode(str(tags[i]),'utf-8')
        imena+=[ime]
        
        linkovi+=pp
        linkovi+='\n'
    linkovi=linkovi.encode('utf-8')
    links=re.findall(pat,linkovi)
    for i in range(len(imena)):
        linkks+=[[links[i],imena[i]]]
    return linkks

def get_latest(page):
    if page=='1':
        site='http://www.filmovita.com'
    else:
        site='http://www.filmovita.com/page/%s/'%page


    reg='href="(.+?)"'
    pat=re.compile(reg)

    req = urllib2.Request(url=site,headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    request = urllib2.urlopen(req)
    html=request.read()
    soup=bs(html)
    linksout=[]
    tags=soup.findAll('article')
    for i in range(len(tags)):
        names=tags[i].find('h1',{'class':'entry-title'})
        h = HTMLParser.HTMLParser()
        ime=h.unescape(names.getText())
        link=re.findall(pat,str(names))[0]
        img=tags[i].find('img')['src']
        ps=len(tags[i].findAll('p'))-2
        
        linksout+=[[link,ime,img]]

    return linksout

def get_category(site,page):
    if page=='1':
        pass
    else:
        site=site+'%s/'%page


    reg='href="(.+?)"'
    pat=re.compile(reg)

    req = urllib2.Request(url=site,headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    request = urllib2.urlopen(req)
    html=request.read()
    soup=bs(html)
    linksout=[]
    tags=soup.findAll('article')
    for i in range(len(tags)):
        names=tags[i].find('h1',{'class':'entry-title'})
        h = HTMLParser.HTMLParser()
        ime=h.unescape(names.getText())
        link=re.findall(pat,str(names))[0]
        img=tags[i].find('img')['src']
        ps=len(tags[i].findAll('p'))-2
        
        linksout+=[[link,ime,img]]

    return linksout



def get_list_of_all_movies():
    site='http://www.filmovita.com/lista-svih-filmova/'
    category_tags=['akcijski filmovi','animirani filmovi','avanturisticki filmovi','dokumentarni filmovi','domaci filmovi','drame',
                    'fantazije','horor filmovi','filmovi komedije','kriminalisticki filmovi','povijesni filmovi','ratni filmovi',
                    'romanticni filmovi','sf filmovi','sinkronizirani crtici','sport','sportski filmovi','trileri','westerni']
    lista=[]
    for i in range(len(category_tags)):
        pom_lista=[]
        pom_lista=get_list_of_movies_genre(site,category_tags[i])
        for j in range(len(pom_lista)):
            lista+=[pom_lista[j]]
    return lista
def search_movies(query):
    indexi=[]
    lista=[]
    html=read_url('http://www.filmovita.com/lista-svih-filmova/')
    reg='a href="(.+?)" title="(.+?)"'
    lista=re.findall(re.compile(reg),html)
    
    
    for i in range(len(lista)):
        ime=lista[i][1]
        link=lista[i][0]
        index=[link,ime]
        if query.lower() in ime.lower() and index not in indexi:

            indexi+=[index]
       

    return indexi
#==============================================================================================================================0


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:
    url = build_url({'mode': 'latest', 'foldername': 'Zadnje dodano', 'page':'1'})
    li = xbmcgui.ListItem('Zadnje dodano', iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/zadnje.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    url = build_url({'mode': 'cats', 'foldername': 'Kategorije'})
    li = xbmcgui.ListItem('Kategorije', iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/kategorije.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    url = build_url({'mode': 'list_favourites', 'foldername': 'Favoriti'})
    li = xbmcgui.ListItem('Favoriti', iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/favoriti-filmovita.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    url = build_url({'mode': 'search', 'foldername': 'Pretraga'})
    li = xbmcgui.ListItem('Pretraga', iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/pretraga.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    url = build_url({'mode': 'shows', 'foldername': 'Serije'})
    li = xbmcgui.ListItem('Serije', iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/filmovita-serije.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='search':

    keyboard = xbmc.Keyboard('', 'Pretraga', False)
    keyboard.doModal()
    
    if keyboard.isConfirmed():
        query = keyboard.getText()
    
    lista=search_movies(query)
    for i in range(len(lista)):
        h = HTMLParser.HTMLParser()
        ime=h.unescape(lista[i][1])
        link=lista[i][0]
        titles=get_title(link)    
        thumb=titles[2]
            
        
        


        url = build_url({'mode': 'open_movie', 'foldername': 'movie','link':'%s'%link , 'thumb':'%s'%thumb })
        li = xbmcgui.ListItem('%s'%ime, iconImage='%s'%thumb)

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
    
elif mode[0]=='latest':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    page=dicti['page'][0]
    lista=get_latest(page)
    
    for i in range(len(lista)):
        ime=lista[i][1]
        link=lista[i][0]
        img=lista[i][2]
        #fake=ime.decode('ascii','replace')
        #cache_foldername(ime,fake)


        url = build_url({'mode': 'open_movie', 'foldername': 'movie','link':'%s'%link , 'thumb':'%s'%img })
        li = xbmcgui.ListItem('%s'%ime, iconImage=img)

        fav_uri = build_url({'mode': 'add_fav', 'title':'banana', 'thumb':'%s'%img, 'link':'%s'%link})

        li.addContextMenuItems([ ('Dodaj u Filmovita favorite', 'RunPlugin(%s)'%fav_uri)])

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)

    url = build_url({'mode': 'latest', 'foldername': 'Zadnje dodano', 'page':'%s'%(str(int(page)+1))})
    li = xbmcgui.ListItem('Sljedeća stranica >>', iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/zadnje.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)



elif mode[0]=='cats':
    category_tags=[['Akcije','http://www.filmovita.com/category/akcije/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/akcija.jpg'],
    ['Animirani','http://www.filmovita.com/category/animirani/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/animirani.jpg'],
    ['Avanture','http://www.filmovita.com/category/avanture/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/avanture.jpg'],
    ['Dokumentarci','http://www.filmovita.com/category/dokumentarci/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/doku.jpg'],
    ['Domaci filmovi','http://www.filmovita.com/category/domacifilmovi/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/domaci.jpg'],
                    ['Drame','http://www.filmovita.com/category/drame/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/drama.jpg'],
                    ['Fantasy','http://www.filmovita.com/category/fantazije/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/fantasy.jpg'],
                    ['Horori','http://www.filmovita.com/category/horori/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/horori.jpg'],
                    ['Komedije','http://www.filmovita.com/category/komedije/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/komedije.jpg'],
                    ['Kriminalisticki','http://www.filmovita.com/category/kriminalisticki/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/krimi.jpg'],
                    ['Povijesni','http://www.filmovita.com/category/povijesni/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/povijesni.jpg'],
                    ['Ratni','http://www.filmovita.com/category/ratni/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/ratni.jpg'],
                    ['Romanticni','http://www.filmovita.com/category/romanticni/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/romanticni.jpg'],
                    ['SF filmovi','http://www.filmovita.com/category/sfovi/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/sf.jpg'],
                    ['Sinkronizirani crtani','http://www.filmovita.com/category/sinkroniziranicrtici/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/animirani.jpg'],
                    ['Sport','http://www.filmovita.com/category/sport/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/sport.jpg'],
                    ['Sportski filmovi','http://www.filmovita.com/category/sportski/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/sport.jpg'],
                    ['Trileri','http://www.filmovita.com/category/trileri/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/triler.jpg'],
                    ['Westerni','http://www.filmovita.com/category/westerni/','https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/western.jpg']]

    for i in range(len(category_tags)):
        url = build_url({'mode': 'open_category', 'foldername': '%s'%category_tags[i][0], 'link':'%s'%category_tags[i][1],'page':'1'})
        li = xbmcgui.ListItem('%s'%category_tags[i][0], iconImage=category_tags[i][2])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_category':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    page=dicti['page'][0]

    lista=get_category(link,page)
    
    for i in range(len(lista)):
        ime=lista[i][1]
        link=lista[i][0]
        img=lista[i][2]
        


        url = build_url({'mode': 'open_movie', 'foldername': 'movie','link':'%s'%link , 'thumb':'%s'%img })
        li = xbmcgui.ListItem('%s'%ime, iconImage=img)

        fav_uri = build_url({'mode': 'add_fav', 'title':'banana', 'thumb':'%s'%img, 'link':'%s'%link})

        li.addContextMenuItems([ ('Dodaj u Filmovita favorite', 'RunPlugin(%s)'%fav_uri)])

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)

    url = build_url({'mode': 'latest', 'open_category': 'Zadnje dodano','link':'%s'%link, 'page':'%s'%(str(int(page)+1))})
    li = xbmcgui.ListItem('Sljedeća stranica >>', iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/zadnje.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_movie':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    try:
        info=get_movie_info(link)

        title=info[0][0]
        year=info[0][1]
        desc=info[0][2]
        thumb=info[0][3]
        fanart=info[0][4]
    except:
        title=get_title(link)[0]
        year=get_title(link)[1]
        desc=get_title(link)[2]
        thumb=''
        fanart=''

    links=get_links(link)
    hosts=get_host_names(links)
    dialog = xbmcgui.Dialog()
    index = dialog.select('Odaberite link:', hosts)

    prob=['Film je u vise djelova na youtube-u.','Posjetite filmovita.com']
    if index>-1 and links!=prob:
        try:
            link=links[index]
            import urlresolver
            resolved=urlresolver.resolve(link)

            li = xbmcgui.ListItem('%s'%title)
            li.setInfo('video', { 'title': '%s'%title ,
                                'year': '%s'%year,
                                'plotoutline' : '%s'%desc,
                                'plot':'%s'%desc,
                                'tagline':'%s'%desc
                                    })
            li.setThumbnailImage(thumb)
            li.setLabel(desc)
            li.setProperty('IsPlayable', 'true')

            xbmc.Player().play(item=resolved, listitem=li)
        except:
            a=xbmcgui.Dialog().ok("Filmovita", "Nije moguće reproducirati odabrani link.","Molim Vas, odaberite drugi.")
    else:
        pass
    
elif mode[0]=='list_favourites':
    lista=get_favourites()
    for i in range(len(lista)):
        ime=lista[i][0]
        link=lista[i][1]
        img=lista[i][2]
        fan=lista[i][3]
        


        url = build_url({'mode': 'open_movie', 'foldername': 'movie','link':'%s'%link , 'thumb':'%s'%img })
        li = xbmcgui.ListItem('%s'%ime, iconImage=img)

        rem_uri = build_url({'mode': 'rem_fav', 'title':'%s'%ime, 'thumb':'%s'%img, 'link':'%s'%link})
        rem_all = build_url({'mode': 'rem_all', 'title':'%s'%ime, 'thumb':'%s'%img, 'link':'%s'%link})

        li.addContextMenuItems([ ('Ukloni iz favorita', 'RunPlugin(%s)'%rem_uri),
                                ('Ukloni sve favorite', 'RunPlugin(%s)'%rem_all) ])
        li.setProperty("Fanart_Image", fan)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='add_fav':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    info=get_movie_info(link)

    title=info[0][0]
    year=info[0][1]
    desc=info[0][2]
    img=info[0][3]
    fanart=info[0][4]

    add_to_favourites(title,link,img,fanart)

elif mode[0]=='rem_fav':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    title=dicti['title'][0]
    img=dicti['thumb'][0]

    remove_fav(title,link,img)
    xbmc.executebuiltin("Container.Refresh")
elif mode[0]=='rem_all':
    delete_all_favs()
    xbmc.executebuiltin("Container.Refresh")





elif mode[0]=='shows':
    shows=get_tvshows()
    for i in range(len(shows)):
        title=shows[i][0]
        year=shows[i][1]
        slug=shows[i][2]
        imdb=shows[i][3]
        trakt=shows[i][4]
        thumb=shows[i][5]

        url = build_url({'mode': 'open_show', 'foldername': '%s'%title, 'slug':'%s'%slug, 'imdb':'%s'%imdb, 'trakt':'%s'%trakt, 'year':'%s'%year})
        li = xbmcgui.ListItem('%s (%s)'%(title,year), iconImage=thumb)

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
        if title!='Season 0':
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
        url = build_url({'mode': 'open_episode','foldername':'%s'%title, 'thumb':'%s'%thumb, 'id':'%s'%id,'slug':'%s'%slug, 'year':'%s'%show_year,'show_title':'%s'%title_show,'season':'%s'%season, 'number':'%s'%number})
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
    thumb=dicti['thumb'][0]
    link=get_episode_link(slug,season,number,show_year)
    links=get_links(link)
    hosts=get_host_names(links)
    dialog = xbmcgui.Dialog()
    index = dialog.select('Odaberite link:', hosts)

    prob=['Film je u vise djelova na youtube-u.','Posjetite filmovita.com']
    if index>-1 and links!=prob:
        
            link=links[index]
            import urlresolver
            resolved=urlresolver.resolve(link)

            li = xbmcgui.ListItem('%s'%title)
            li.setInfo('video', {'tvshowtitle':'%s'%title_show,
                                'title':'%s'%title,
                                'season':'%s'%season,
                                'episode':'%s'%number
                                
                                    })
            li.setThumbnailImage(thumb)
            
            li.setProperty('IsPlayable', 'true')

            xbmc.Player().play(item=resolved, listitem=li)
    else:
        pass