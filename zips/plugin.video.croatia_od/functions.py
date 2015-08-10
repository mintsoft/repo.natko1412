# -*- coding: utf-8 -*-
import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib2
#import urllib.request as urllib2
import re
from BeautifulSoup import BeautifulSoup as bs
import itertools
import xbmcvfs
import os
import xbmc

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)


def read_url(url):

        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link.decode('utf-8')


def resolve_rtl_link(link):
    end_url='?domain=www.rtl.hr&xml=1'
    link=link+end_url
    try:
        resp = urllib2.urlopen(link)
        contents = resp.read()
    except urllib2.HTTPError, error:
        contents = error.read()
    html=contents
    soup=bs(html)
    
    sp=bs(html)
    vid=sp.findAll('video')[0]
    link=vid.getText()
    return link


def get_new(site,category):
    
    
    base_url=''
    #base_url='http://www.rtl.hr'
    url=site
    
    try:
        resp = urllib2.urlopen(url)
        contents = resp.read()
    except urllib2.HTTPError, error:
        contents = error.read()
    html=contents.replace('č','c').replace('ć','c').replace('š','s').replace('Č','C').replace('Ć','C').replace('ž','z').replace('Ž','Z').replace('đ','d').replace('Đ','D').replace('Š','S')
    soup=bs(html)

    if site=='http://www.rtl.hr/rtl-sada/gastro/tri-dva-jedan-kuhaj/':
        
        tags=soup.findAll('div',{'class':'items_inner'})[0]
            

        linksout=[]
        
        aas=tags.findAll('a')
        
        for i in range((len(aas))):
            link=base_url + aas[i]['href'] 
            
            if 'rtl-sada' not in link:
                pass
            else:
                title=aas[i]['title']
                
                img=(aas[i].findAll('span')[0]).findAll('img')[0]['src']
                
                link=resolve_rtl_link(link)
                
                linksout.append([link,title,img])
        return linksout


    else:
        pass

    try:
        try:
            tags_sez=soup.findAll('h1',{'class':'h3 pl_xs h_outside'})
            sez=tags_sez[0].getText().lower().title()
        except:
            sez='x'

        if 'SEZONA' in sez or 'Sezona' in sez  or 'sezona' in sez:
            
            tags=soup.findAll('ul',{'class':'clearfix listing grid_archive'})
            linksout=[]
            
            for category in range(len(tags_sez)):
                
                tag=tags[category]
                aas=tag.findAll('a')
                sez=tags_sez[category].getText().lower().title()
                for i in range((len(aas))):
                    link=base_url + aas[i]['href'] 
                    
                    if 'rtl-sada' not in link:
                        pass
                    else:
                        tit=aas[i]['title']
                        title=aas[i].findAll('span',{'class':'title'})[0].getText()#.strip('\n').strip(' ').replace('                                                 ','')
                        title='%s: '%(sez)+title
                        img=(aas[i].findAll('span')[0]).findAll('img')[0]['src']
                        
                        link=resolve_rtl_link(link)
                        linksout.append([link,title,img])

            if linksout!=[]:
                return linksout
            else:
                tags=soup.findAll('ul',{'class':'clearfix listing grid_archive'})[0]
        

                linksout=[]
                
                aas=tags.findAll('a')
                
                for i in range((len(aas))):
                    link=base_url + aas[i]['href'] 
                    
                    if 'rtl-sada' not in link:
                        pass
                    else:
                        title=aas[i]['title']
                        
                        img=(aas[i].findAll('span')[0]).findAll('img')[0]['src']
                        
                        link=resolve_rtl_link(link)
                        
                        linksout.append([link,title,img])
                    if linksout!=[]:
                        return linksout
                    else:
                        tags=soup.findAll('div',{'class':'container clearfix mb_s'})

                        tag=tags[category]
                        
                        aas=tag.findAll('a')
                        if (category >= 1):# and (site=='http://www.rtl.hr/rtl-sada/'):
                            aas.pop(0)
                        linksout=[]
                        for i in range((len(aas))):
                            link=base_url + aas[i]['href'] 
                            
                            if 'rtl-sada' not in link:
                                pass
                            else:
                                tit=aas[i]['title']
                                title=aas[i].findAll('span',{'class':'subtitle'})[0].getText().strip('\n').strip(' ').replace('                                                 ','')
                                title=tit+': '+title
                                img=(aas[i].findAll('span')[0]).findAll('img')[0]['src']
                                
                                link=resolve_rtl_link(link)
                                linksout.append([link,title,img])

                        return linksout




        
        else:
            tags=soup.findAll('ul',{'class':'clearfix listing grid_archive'})[0]
            

            linksout=[]
            
            aas=tags.findAll('a')
            
            for i in range((len(aas))):
                link=base_url + aas[i]['href'] 
                
                if 'rtl-sada' not in link:
                    pass
                else:
                    title=aas[i]['title']
                    
                    img=(aas[i].findAll('span')[0]).findAll('img')[0]['src']
                    
                    link=resolve_rtl_link(link)
                    
                    linksout.append([link,title,img])
            return linksout

    except:

        

        tags=soup.findAll('div',{'class':'container clearfix mb_s'})

        tag=tags[category]
        
        aas=tag.findAll('a')
        if (category >= 1):# and (site=='http://www.rtl.hr/rtl-sada/'):
            aas.pop(0)
        linksout=[]
        for i in range((len(aas))):
            link=base_url + aas[i]['href'] 
            
            if 'rtl-sada' not in link:
                pass
            else:
                tit=aas[i]['title']
                try:
                    title=aas[i].findAll('span',{'class':'subtitle'})[0].getText().strip('\n').strip(' ').replace('                                                 ','')
                except:
                    title=''
                if title!='':
                    title=tit+': '+title
                else:
                    title=tit
                

                img=(aas[i].findAll('span')[0]).findAll('img')[0]['src']
                
                link=resolve_rtl_link(link)
                linksout.append([link,title,img])

        return linksout


def get_shows_rtl(site):
    html=read_url(site)
    soup=bs(html)
    shows=[]
    tag=soup.find('div',{'class':'list_holder'})
    #first_name=tag.find('div',{'class':'first-in-row'}).find('a')['title']
    #first_link=tag.find('div',{'class':'first-in-row'}).find('a')['href']
    #shows+=[[first_name,first_link]]

    items=tag.findAll('li')
    for item in items:
        try: lex=item['class']
        except: lex=''

        if lex=='extra_dd':
            pass
        else:
            name=item.find('a')['title']
            link=item.find('a')['href']

            shows+=[[name,link]]


    return shows


def hrt_get_shows_letter(letter):#=====>  vraca listu tipa likovi[index]=[link_emisije[index],ime_emisije[index]]
        br=0
        linksout = []
        html=read_url('http://www.hrt.hr/enz/dnevnik/')
        soup = bs(html)
        tag = soup.find("div", {"class":"all_shows"})
        letters=tag.find('ul',{'data-letter':'%s'%letter})
        emisija=[None]*len(letters)
        emisije=[None]*200
        name=[None]*200
        
        emisije_tags=letters.findAll('li')
        
        for j in range(len(emisije_tags)):
            css=emisije_tags[j].findAll('a')
            for a in css:
                    link=a['href']
                    br+=1
                    link='http:'+link
                    emisije[br]=link
                    name[br]=emisije_tags[j].getText()
               
                
        emisije = [x for x in emisije if x != None]
        name = [x for x in name if x != None]
        linkovi=[None]*len(emisije)
        for g in range(len(emisije)):
            linkovi[g]=[emisije[g],name[g]]
        
        return linkovi


def get_episodes_hrt(link,broj_rez): #======> vraca listu tipa linkovi[0]=[link_epizode[0],ime_epizode[0]]

        reg='value="(.+?)"'
        pattern=re.compile(reg)
        reg2='">(.+?)<option value='
        pattern2=re.compile(reg2)
        

        
        request = urllib2.urlopen(link)
        html = request.read()
        soup = bs(html)

        tag = soup.find("table", {"class":"show_info"})
        eps=tag.findAll('select')
        gg=eps[0]
            
        stri=str(gg)
        
        br=0
        br1=0
        values=[None]*(int(broj_rez)+1)
        names=[None]*(int(broj_rez)+1)
        for m in itertools.islice(re.finditer(pattern, stri), (int(broj_rez)+1)):
            values[br]=m.group(1)
            br+=1
        for v in itertools.islice(re.finditer(pattern2, stri), (int(broj_rez)+1)):
            names[br1]=v.group(1)
            br1+=1
        
        values = [x for x in values if x is not None]
        values.pop()
        names = [x for x in names if x is not None]
        
        
        

        
        epizoda=[None]*len(values)
        linkovi=[None]*len(values)
        
        for f in range(len(values)):
            epizoda[f]=link+values[f]
            linkovi[f]=[epizoda[f],names[f]]
        
        if len(values)==0:
            return '123445'
        return linkovi

       # except:
        #    return ('No episodes available')

def get_show_name(url):
    html=read_url(url)
    soup=bs(html)
    return soup.find('td',{'class':'show_name'}).getText()

def get_episode_link(link):                #====> vraca .mp4 link
        request = urllib2.urlopen(link)
        html = request.read()
        soup = bs(html)

        tag = soup.find("div", {"class":"video"})
        tag=tag.find("video")
        try:
            linka=tag['data-url']
        except:
            linka=tag['src']

        return linka

def get_shows_mreza(tagy):
    url='http://mreza.tv/video/'
    shows=[]
    request=urllib.urlopen(url)
    html=request.read()
    soup=bs(html)

    tag=soup.find("div", {"id":"wrapper-glavni"})
    tag=tag.find("section",{"class":"%s"%tagy})
   
    pom=tag.findAll("h5")
    for i in range(len(pom)):
        pomy=pom[i].findAll("a")[0]
        ime=pomy.get("title")
        link=pomy.get("href")
        shows+=[[link,ime]]
    return shows

def get_episodes_mreza(url):
    
    reg1='"title":"(.+?)"'
    pat1=re.compile(reg1)

    reg2='"file":"(.+?)"'
    pat2=re.compile(reg2)

    reg3='"image":"(.+?)"'
    pat3=re.compile(reg3)

    return_lista=[]
    request=urllib.urlopen(url)
    html=str(request.read())
    
    html=html
    titles=re.findall(pat1,html)
    links=re.findall(pat2,html)
    images=re.findall(pat3,html)
    for i in range(len(titles)):
        title=str(titles[i])
        link=str(links[i])
        image=str(images[i])
        return_lista+=[[link,title,image]]

    return return_lista

def convert(string):

    string=string.replace('%3A',':')
    string=string.replace('%3B',';')
    string=string.replace('%3C','<')
    string=string.replace('%3D','=')
    string=string.replace('%3E','>')
    string=string.replace('%3F','?')
    string=string.replace('%3D','=')
    string=string.replace('%3d','=')
    string=string.replace('%2A','*')
    string=string.replace('%2B','+')
    string=string.replace('%2C',',')
    string=string.replace('%2D','-')
    string=string.replace('%2E','.')
    string=string.replace('%2F','/')
    string=string.replace('%26','&')
    string=string.replace('%23','#')
    string=string.replace('%25','%')
    string=string.replace('%40','@')
    return string

def get_video_links_from_jabuka_show(show):
    request=urllib2.urlopen(show)
    html=request.read()
    soup=bs(html)
    tag=soup.findAll('div',{'class':'media-details-view'})[0]
    h2s=tag.findAll('h2')
    linksout=[]
    for i in range(len(h2s)):
        title=h2s[i]['title']
        link='http://videoteka.jabukatv.hr'+(h2s[i].findAll('a')[0]['href'])
        title=title.replace(':','')
        linksout+=[[link,title]]
    
    return linksout

def resolve_otv_link(link):
    request=urllib2.urlopen(link)
    html=request.read()
    soup=bs(html)
    tag=soup.findAll('meta',{'property':'og:video:url'})[0]['content']
    
    link=convert(tag)
    index=link.index('file=')
    link=link[index+5:]
    return(link)



def find_episodes(url):
    
    request=urllib.urlopen(url)
    html=request.read().decode('utf-8')
    soup=bs(html)
    tag=soup.find("div", {"class":"article-listing vertical"})
    articles=tag.findAll('article')
    links=[None]*len(articles)
    name=[None]*len(articles)
    ret_lista=[[None]]*len(articles)
    for i in range(len(articles)):
        inputTag = articles[i].findAll(attrs={"name" : "file"})
        inputTag2 = articles[i].findAll(attrs={"name" : "caption"})
        links[i] = 'http://radio.hrt.hr' + inputTag[0]['value']
        name[i]= inputTag2[0]['value']

        ret_lista+=[[links[i],name[i]]]
    ret_lista=[x for x in ret_lista if x != [None]]
    return ret_lista
def get_links_country(link):


    reg='<a href="(.+?)"'
    pattern=re.compile(reg)
    reg2='<b>(.+?)</b>'
    pattern2=re.compile(reg2)
    site = "http://www.listenlive.eu/"+link+".html"
    request = urllib.urlopen(site)
    html = request.read()
    soup = bs(html)
    table = soup.find("div", {"class":"thetable3"})
    tab=table.findAll('tr')

    stanice=[None]*(len(tab)+1)
    for i in range (len(tab)):
        stanice[i] =tab[i].findAll('td')
    
    links=[None]*(len(stanice)+1)
    imena=[None]*(len(stanice)+1)
    imenak=[None]*(len(stanice)+1)
    gradovi=[None]*(len(stanice)+1)
    lk=[None]*(len(stanice)+1)
    imena_st=[None]*(len(stanice)+1)
    linksout=[None]*600
    linkk=''
    grad=''
    for i in range (len(stanice)-1):
        links[i]=stanice[i][3]
        link=str(links[i])
        link=re.findall(pattern,link)
        
        if (i!=0):
            linkk=link[0]
        imena[i]=stanice[i][0]
        imenak[i]=stanice[i][3]
        gradovi[i]=stanice[i][1]
        if i!=0:
            grad=gradovi[i].getText().encode('utf-8')
        imena[i]=str(imena[i])
        ime=re.findall(pattern2,imena[i])
        #imenak[i]=str(imenak[i])
        kvaliteta=imenak[i].getText()
        if kvaliteta=='WebPlayer':
            kvaliteta='64 Kbps'
        if kvaliteta.count('Kbps')>1:
            a=kvaliteta.index('Kbps')
            kvaliteta=kvaliteta[:a+4]
        if '>' in ime[0]:
            l=len(ime[0])
            g=ime[0].index('>')
            ime[0]=ime[0][g+1:l]
        if '>' in ime[0]:
            l=len(ime[0])
            g=ime[0].index('>')
            ime[0]=ime[0][g+1:l].encode('utf-8')
        
        linksout += [[linkk, ime[0],kvaliteta,grad]]
    
    del linksout[0]
    del linksout[0]
    linksout=[x for x in linksout if x !=None]
    return linksout


def get_izet(year):
    if year==2015:
        id='LinkList2'
    elif year==2014:
        id='LinkList1'
    elif year==2013:
        id='LinkList3'
    elif year==2012:
        id='LinkList4'
    elif year==2011:
        id='LinkList5'
    elif year==2010:
        id='LinkList6'
    elif year==2009:
        id='LinkList7'
    elif year==2008:
        id='LinkList8'
    elif year==2007:
        id='LinkList9'
    lista=[]
    html=read_url('http://zbunjenludnormalan.blogspot.com')
    soup=bs(html)
    tag=soup.find('div',{'id':'%s'%id})
    list=tag.findAll('li')
    for i in range(len(list)):
        link=list[i].find('a')['href']
        name=list[i].getText()

        lista+=[[link,name]]
    return lista

def get_izet_video(url):
    html=read_url(url)

    try:
        reg="<iframe src='(.+?)'"
        listy=re.findall(re.compile(reg),html)[0]
    except:
        reg="<IFRAME SRC='(.+?)'"
        listy=re.findall(re.compile(reg),html)[0]
    return listy

