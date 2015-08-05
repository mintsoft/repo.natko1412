# -*- coding: utf-8 -*-


import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib2
import re
from BeautifulSoup import BeautifulSoup as bs
import itertools
from functions import *


def read_url(url):

        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link.decode('utf-8')

def otvori_epizodu(url,title,thumb):
    #prvo pogledaj ako ima vise dijelova
    try:
        html=read_url(url)
        soup=bs(html)
        tag=soup.find('div',{'id':'Playerholder'})
        frames=tag.findAll('iframe')
        if len(frames)>1:
            progress = xbmcgui.DialogProgress()
            progress.create('Ucitavam', 'Ucitavam dijelove epizoda u playlistu...')

            playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            playlist.clear()
            message ="0 od %s"%(len(frames))
            progress.update( 0, "", message, "" )  
            for i in range(len(frames)):

                
                link=frames[i]['src']
                print(link)
                import urlresolver

                resolved=urlresolver.resolve(link)
                print(resolved)
                li = xbmcgui.ListItem('%s'%title)
                li.setInfo('video', { 'title': '%s'%title })
                li.setThumbnailImage(thumb)
                playlist.add(resolved,li)


                message = str(i+1) + " od %s"%(len(frames))
                perc=((i+1)/(len(frames)))*100
                progress.update( perc, "", message, "" )

            
        xbmc.Player().play(playlist)
        return

    except:
        pass

    try:   
        html=read_url(url)
    
        soup=bs(html)
        link=soup.findAll('iframe')[1]['src']
        print(link)
        print('exit: ',1)
        
        
    except:

        try:
            html=read_url(url)

        
            soup=bs(html)
            link=soup.findAll('iframe')[1]['src']
            
            print(link)
            print('exit: ',2)
            
            
        except:
            try:
                html=read_url(url)
        
                soup=bs(html)
                try:
                    link=soup.find('div',{'id':'Playerholder'}).find('embed')['src']
                except:
                    link=soup.find('div',{'id':'Playerholder'}).find('iframe')['src']
                print(link)
                print('exit: ',3)
                
            except:
                html=read_url(url).lower()
                ind=html.index('player.src')
                html=html[ind:ind+80]
                
                reg=r'watch\?v=(.+?)"'
                link=re.findall(re.compile(reg),html)[0]
                
                link='http://www.youtube.com/watch?v=' + link

                print(link)
                print('exit: ',4)
                
    try:
        import urlresolver
        resolved=urlresolver.resolve(link)
    except:
        import resolver as srr
        resolved=srr.resolve(link)[0]['url']


    li = xbmcgui.ListItem('%s'%title)
    li.setInfo('video', { 'title': '%s'%title })
    li.setThumbnailImage(thumb)
    xbmc.Player().play(item=resolved, listitem=li)

def nadi_epizode(url,stranica,linky):

    html=read_url(url)

    soup=bs(html)
    tag=soup.find('ul',{'class':'pm-ul-browse-videos thumbnails'})

    lis=tag.findAll('li')
    results=[]
    for i in range(len(lis)):
        thumb=lis[i].find('img')['src']
        item=lis[i].find('h3').find('a')
        link=item['href']
        title=item['title']
        
        url = build_url({'mode': 'otvori_epizodu', 'link':'%s'%link, 'title':'%s'%title, 'thumb':'%s'%thumb})
        li = xbmcgui.ListItem('%s '%(title), iconImage=thumb)

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)

    url = build_url({'mode': 'otvori_seriju_balkanje', 'link':'%s'%linky, 'page':'%s'%(str(int(page)+1))})
    li = xbmcgui.ListItem('Sljedeca strana --> ', iconImage='http://www.basspirate.com/wp-content/uploads/2011/10/Right-Arrow.gif')

    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
################################################################################################################################################################################
################################################################################################################################################################################

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:
    url = build_url({'mode': 'vod', 'foldername': 'VoD'})
    li = xbmcgui.ListItem('Televizija na zahtjev', iconImage='http://rowandronelectrical.co.nz/dron/wp-content/uploads/2014/05/House-and-Appliances-Tv-icon.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'live', 'foldername': 'Tv_live'})
    li = xbmcgui.ListItem('Televizija uživo', iconImage='http://rowandronelectrical.co.nz/dron/wp-content/uploads/2014/05/House-and-Appliances-Tv-icon.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'radioNZ', 'foldername': 'AoD'})
    li = xbmcgui.ListItem('Radio na zahtjev', iconImage='https://cdn2.iconfinder.com/data/icons/windows-8-metro-style/512/radio.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'radio_live', 'foldername': 'radio_uzivo'})
    li = xbmcgui.ListItem('Radio uživo', iconImage='https://cdn2.iconfinder.com/data/icons/windows-8-metro-style/512/radio.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='vod':
    url = build_url({'mode': 'rtl', 'foldername': 'RTL Sada'})
    li = xbmcgui.ListItem('RTL Sada', iconImage='http://www.bnet.hr/var/ezflow_site/storage/images/b_net/novosti/rtl_sada_od_sada_na_b_netu/40484-1-cro-HR/rtl_sada_od_sada_na_b_netu_view_full.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'hrt', 'foldername': 'HRT Emisije'})
    li = xbmcgui.ListItem('HRT Emisije' ,iconImage='http://www.hrt.hr/static/v2/img/hrt_logo_fb.gif')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)


    url = build_url({'mode': 'mreza', 'foldername': 'Mreza TV'})
    li = xbmcgui.ListItem('Mreza TV' ,iconImage='http://teve.ba/img/articles/11349.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'jabuka', 'foldername': 'Jabuka TV'})
    li = xbmcgui.ListItem('Jabuka TV' ,iconImage='http://radionadlanu.com/games/images/jabuka-tv.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)


    url = build_url({'mode': 'serije_balkanje', 'foldername': 'serije'})
    li = xbmcgui.ListItem('Serije (Balkanje) ' ,iconImage='http://www.standard.co.uk/incoming/article8223968.ece/alternates/w460/televisonold.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
#####################################################################################################################################################################
#RTL
#####################################################################################################################################################################
elif mode[0]=='rtl':
    url = build_url({'mode': 'rtl_sada', 'foldername': 'RTL sada - najnovije epizode'})
    li = xbmcgui.ListItem('RTL sada - najnovije epizode' ,iconImage='http://www.bnet.hr/var/ezflow_site/storage/images/b_net/novosti/rtl_sada_od_sada_na_b_netu/40484-1-cro-HR/rtl_sada_od_sada_na_b_netu_view_full.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'rtl_arh', 'foldername': 'RTL sada - staro'})
    li = xbmcgui.ListItem('RTL sada - staro' ,iconImage='http://www.bnet.hr/var/ezflow_site/storage/images/b_net/novosti/rtl_sada_od_sada_na_b_netu/40484-1-cro-HR/rtl_sada_od_sada_na_b_netu_view_full.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='rtl_sada':
    kateg=[['Serije','serije'],['Dokumentarci','dokumentarci'],['Info i Magazini','magazini'],
            ['Gastro','gastro'],['RTL Kockica','rtl-kockica'],['Zabava','zabava'],['Humor','humor'],['Filmovi','filmovi']]

    for i in range(len(kateg)):
        if kateg[i][1]=='filmovi':
            site='http://www.rtl.hr/rtl-sada/filmovi'
            url = build_url({'mode': 'get_new_rtl', 'site':'%s'%site, 'index':'0'})
            li = xbmcgui.ListItem('%s'%kateg[i][0] ,iconImage='http://www.bnet.hr/var/ezflow_site/storage/images/b_net/novosti/rtl_sada_od_sada_na_b_netu/40484-1-cro-HR/rtl_sada_od_sada_na_b_netu_view_full.jpg')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
        else:


            url = build_url({'mode': 'rtl_open_cat', 'site':'%s'%kateg[i][1]})
            li = xbmcgui.ListItem('%s'%kateg[i][0] ,iconImage='http://www.bnet.hr/var/ezflow_site/storage/images/b_net/novosti/rtl_sada_od_sada_na_b_netu/40484-1-cro-HR/rtl_sada_od_sada_na_b_netu_view_full.jpg')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='rtl_open_cat':
    
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    mod=dicti['site'][0]

    site='http://www.rtl.hr/rtl-sada/' + mod

    kateg=get_shows_rtl(site)
    
    for i in range(len(kateg)):
        if kateg[i][1]!='http://www.vijesti.rtl.hr/sport/rtl-liga/':

            url = build_url({'mode': 'get_new_rtl', 'site': '%s'%kateg[i][1], 'index':'0'})
            li = xbmcgui.ListItem('%s'%kateg[i][0] ,iconImage='http://www.bnet.hr/var/ezflow_site/storage/images/b_net/novosti/rtl_sada_od_sada_na_b_netu/40484-1-cro-HR/rtl_sada_od_sada_na_b_netu_view_full.jpg')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='get_new_rtl':
    dicti=urlparse.parse_qs(sys.argv[2][1:])

    site=dicti['site'][0]
    
    index=int(dicti['index'][0])
    lista=get_new(site,index)

    for i in range(len(lista)):
        name=lista[i][1].encode().decode('ascii','ignore')
        li = xbmcgui.ListItem(' %s'%lista[i][1], iconImage='%s'%lista[i][2])
        down_uri = build_url({'mode': 'download_resolved', 'foldername': '%s'%(name), 'link': '%s'%lista[i][0]})
        li.addContextMenuItems([ ('Preuzmi video', 'RunPlugin(%s)'%down_uri)])
        
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=lista[i][0], listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='rtl_arh':
    reg2='img="(.+?)"'
    pat2=re.compile(reg2)
    reg3='show="(.+?)"'
    pat3=re.compile(reg3)
    urll='http://pastebin.com/raw.php?i=RtCmd8tX'
    a=urllib2.urlopen(urll)
    html=a.read().decode('utf-8')
    shows=html.split('#==#')
    for i in range(len(shows)):

        show_name=re.findall(pat3,shows[i])[0]
        show_img=re.findall(pat2,shows[i])[0]
        url = build_url({'mode': 'rtl_arh_op','index':'%s'%(str(i)), 'foldername': '%s'%show_name})
        li = xbmcgui.ListItem('%s'%show_name ,iconImage='%s'%show_img)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='rtl_arh_op':

    dicti=urlparse.parse_qs(sys.argv[2][1:])

    index=int(dicti['index'][0])

    reg='url="(.+?)"'
    pat=re.compile(reg)
    reg2='ep="(.+?)"'
    pat2=re.compile(reg2)
    reg3='show="(.+?)"'
    pat3=re.compile(reg3)
    reg4='img="(.+?)"'
    pat4=re.compile(reg4)
    urll='http://pastebin.com/raw.php?i=RtCmd8tX'
    a=urllib2.urlopen(urll)
    html=a.read().decode('utf-8')
    shows=html.split('#==#')
    html=shows[index]
    urls=[]
    urls=re.findall(pat,html)
    imena=[]
    imena=re.findall(pat2,html)
    imgs=[]
    imgs=re.findall(pat4,html)[0]
    show_name=re.findall(pat3,html)[0]
    for i in range(len(imena)):
        li = xbmcgui.ListItem('%s %s'%(show_name,imena[i]), iconImage='%s'%imgs)
        
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=urls[i], listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='download_resolved':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    name=dicti['foldername'][0]
    uri=link
    my_addon = xbmcaddon.Addon()
    desty= my_addon.getSetting('downloads_folder')
    download(name,uri,desty)
#####################################################################################################################################################################
#HRT
#####################################################################################################################################################################
elif mode[0] == 'hrt':

    letters=['0-9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','R','S','Š','T','V','Z','Ž']
    for i in range(len(letters)):
        url = build_url({'mode': 'hrt_open_letter','letter':'%s'%letters[i], 'foldername': 'letter'})
        li = xbmcgui.ListItem('%s'%letters[i] ,iconImage='http://www.hrt.hr/static/v2/img/hrt_logo_fb.gif')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='hrt_open_letter':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    letter=dicti['letter'][0]

    shows=hrt_get_shows_letter(letter)
    for i in range(len(shows)):
        url = build_url({'mode': 'open_show_hrt', 'link': '%s'%shows[i][0]})
        li = xbmcgui.ListItem('%s'%shows[i][1] ,iconImage='http://www.hrt.hr/static/v2/img/hrt_logo_fb.gif')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_show_hrt':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    url=dicti['link'][0]

    my_addon = xbmcaddon.Addon()
    broj_rez = my_addon.getSetting('broj_rezultata')

    episode=[]
    episode=get_episodes_hrt(url,broj_rez)
    name=get_show_name(url)


    for i in range(len(episode)):
        title=episode[i][1]
        title=remove_tags(title)
        try:
            li = xbmcgui.ListItem('%s: %s'%(name,title), iconImage='http://www.hrt.hr/static/v2/img/hrt_logo_fb.gif')
            down_uri = build_url({'mode': 'download_hrt', 'foldername': '%s: %s'%(name,title), 'link': '%s'%episode[i][0]})
        except:
            li = xbmcgui.ListItem('%s'%(title), iconImage='http://www.hrt.hr/static/v2/img/hrt_logo_fb.gif')
            down_uri = build_url({'mode': 'download_hrt', 'foldername': '%s'%(title), 'link': '%s'%episode[i][0]})

        

        li.addContextMenuItems([ ('Preuzmi video', 'RunPlugin(%s)'%down_uri)])

        #uri=a.get_episode_link(episode[i][0])
        try:
            uri = build_url({'mode': 'play_hrt', 'foldername': '%s: %s'%(name,title), 'link': '%s'%episode[i][0]})
        except:
            uri = build_url({'mode': 'play_hrt', 'foldername': '%s'%title, 'link': '%s'%episode[i][0]})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=li, isFolder=True)


    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='play_hrt':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    name=dicti['foldername'][0]
    uri=get_episode_link(link)

    li = xbmcgui.ListItem('%s'%name)
    li.setInfo('video', { 'title': '%s'%name })
    xbmc.Player().play(item=uri, listitem=li)

elif mode[0]=='download_hrt':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    name=dicti['foldername'][0]
    uri=get_episode_link(link)
    my_addon = xbmcaddon.Addon()
    desty= my_addon.getSetting('downloads_folder')
    download(name,uri,desty)
#####################################################################################################################################################################
#MREZA
#####################################################################################################################################################################
elif mode[0]=='mreza':

    mreza_cats=[['Informativne emisije', 'videoteka v-info-emisije'], ['Zabavno - mozaicni program', 'videoteka v-zm-program'], ['Ostale emisije', 'videoteka v-ostale-emisije']]
    for i in range(len(mreza_cats)):
        url = build_url({'mode': 'open_mreza_cat', 'tag': '%s'%mreza_cats[i][1]})
        li = xbmcgui.ListItem('%s'%mreza_cats[i][0],iconImage='http://teve.ba/img/articles/11349.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='open_mreza_cat':

    dicti=urlparse.parse_qs(sys.argv[2][1:])
    tag=dicti['tag'][0]
    emisije=get_shows_mreza(tag)
    
    for i in range(len(emisije)):    
        url = build_url({'mode': 'open_show_mreza', 'link':'%s'%emisije[i][0]})
        li = xbmcgui.ListItem('%s'%emisije[i][1] ,iconImage='http://teve.ba/img/articles/11349.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                               listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_show_mreza':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]

    epizode=get_episodes_mreza(link)

    for i in range (len(epizode)):
        li = xbmcgui.ListItem('%s'%(epizode[i][1]), iconImage='%s'%epizode[i][2])

        down_uri = build_url({'mode': 'download_resolved', 'foldername': '%s'%(epizode[i][1]), 'link': '%s'%epizode[i][0]})
        li.addContextMenuItems([ ('Preuzmi video', 'RunPlugin(%s)'%down_uri)])

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=epizode[i][0], listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)
#####################################################################################################################################################################
#JABUKA
#####################################################################################################################################################################
elif mode[0]=='jabuka':
    otv_emisije=[ ['2 u 9','http://videoteka.jabukatv.hr/index.php?option=com_hwdmediashare&view=category&id=9&Itemid=114'],['Hrana i vino','http://videoteka.jabukatv.hr/index.php?option=com_hwdmediashare&view=category&id=10&Itemid=115'],
                    ['Veto','http://videoteka.jabukatv.hr/index.php?option=com_hwdmediashare&view=category&id=11&Itemid=116'] ]

    for i in range(len(otv_emisije)):
        url = build_url({'mode': 'open_jabuka', 'link': '%s'%otv_emisije[i][1]})
        li = xbmcgui.ListItem('%s'%otv_emisije[i][0] ,iconImage='http://radionadlanu.com/games/images/jabuka-tv.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_jabuka':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    lista=get_video_links_from_jabuka_show(link)
    
    for i in range(len(lista)):
        li = xbmcgui.ListItem(' %s'%lista[i][1], iconImage='http://radionadlanu.com/games/images/jabuka-tv.png')
        link=resolve_otv_link(lista[i][0])

        down_uri = build_url({'mode': 'download_resolved', 'foldername': '%s'%(lista[i][1]), 'link': '%s'%link})
        li.addContextMenuItems([ ('Preuzmi video', 'RunPlugin(%s)'%down_uri)])

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=link, listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)
#####################################################################################################################################################################
#BALKANJE
#####################################################################################################################################################################
elif mode[0]=='serije_balkanje':


    url = build_url({'mode': 'serije_novo1', 'foldername': 'serije'})
    li = xbmcgui.ListItem('Zadnje dodane epizode' ,iconImage='http://www.standard.co.uk/incoming/article8223968.ece/alternates/w460/televisonold.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    
    url = build_url({'mode': 'serije_cat', 'foldername': 'hrv'})
    li = xbmcgui.ListItem('Domace' ,iconImage='http://www.standard.co.uk/incoming/article8223968.ece/alternates/w460/televisonold.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'serije_cat', 'foldername': 'esp'})
    li = xbmcgui.ListItem('Spanjolske' ,iconImage='http://www.standard.co.uk/incoming/article8223968.ece/alternates/w460/televisonold.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'serije_cat', 'foldername': 'tur'})
    li = xbmcgui.ListItem('Turske' ,iconImage='http://www.standard.co.uk/incoming/article8223968.ece/alternates/w460/televisonold.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'lzn', 'foldername': 'lud'})
    li = xbmcgui.ListItem('Lud, zbunjen, normalan' ,iconImage='http://bh-info.com/wp-content/uploads/2015/04/lud.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='serije_cat':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    cat=dicti['foldername'][0]
    
    if cat=='hrv':
        serije_balk=[['Vatre ivanjske','http://www.balkanje.com/browse-vatre-ivanjske-videos-','http://cdn-static.rtl-hrvatska.hr/image/1cfa4700fa18c949e9a2b3f377de9792_gallery_single_view.jpg?v=17'],
    ['Kud puklo da puklo','http://www.balkanje.com/browse-kud-puklo-da-puklo-videos-','http://image.dnevnik.hr/media/images/640x338/Sep2014/60990100-kud-puklo-da-puklo.jpg'],
    ['Pocivali u miru','http://www.balkanje.com/browse-pocivali-u-miru-videos-1-','https://i.vimeocdn.com/video/403000627_1280x720.jpg'],
    ['Kriza','http://www.balkanje.com/browse-kriza-videos-','http://serije.onlinebioskop.com/wp-content/themes/Filmovi/timthumb.php?src=serije.onlinebioskop.com/wp-content/uploads/2014/07/ksg.jpg&h=270&w=200&zc=1'],
    ['Stella','http://www.balkanje.com/browse-stella-videos-','http://www.cafe.hr/layout/i/header/th1_serijastella.jpg'],
    ['Stipe u gostima','http://www.balkanje.com/browse-stipe-u-gostima-videos-','http://halobing.net/serije/slike/stipe-m.jpg'],
    ['Larin izbor','http://www.balkanje.com/browse-larin-izbor-videos-','https://upload.wikimedia.org/wikipedia/sr/d/d5/Larin_izbor.jpg']]

    elif cat=='esp':
        serije_balk=[['Andeo i vrag','http://www.balkanje.com/browse-andjeo-i-vrag-videos-','http://www.lafiscalia.com/wp-content/uploads/pobre-diablo-telemundo.jpg'],
                    ['Avenida Brasil','http://www.balkanje.com/browse-Avenida-Brasil-videos-','http://avenida-brasil.org/wp-content/uploads/2013/12/personajes-de-avenida-brasil.jpg'],
                    ['Dona Barbara','http://www.balkanje.com/browse-dona-barbara-videos-','https://upload.wikimedia.org/wikipedia/en/4/40/Dona_Barbara_poster_2008.jpg'],
                    ['Pobjeda ljubavi','http://www.balkanje.com/browse-pobjeda-ljubavi-videos-','http://phazer.info/img/covers/img14918-tv0-triunfo-del-amor-200.jpg']]


    elif cat=='tur':
        serije_balk=[['Elif','http://www.balkanje.com/browse-elif-videos-','http://i.ytimg.com/vi/56yR1E-Bir8/maxresdefault.jpg'],
                    ['Nikad ne odustajem','http://www.balkanje.com/browse-nikad-ne-odustajem-videos-','https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTILAi68ixr34eM8NNb2kNebz8t6eHr2uV20aLrQH65w3aruNtk'],
                    ['Crna ruza','http://www.balkanje.com/browse-crna-ruza-videos-','http://proprofs-cdn.s3.amazonaws.com/images/QM/user_images/1736687/2315550970.jpg'],
                    ['Dila','http://www.balkanje.com/browse-dila-videos-','http://3.bp.blogspot.com/-HGqWwXRn-dg/UtvYOiA3TYI/AAAAAAAAAM8/rLrsVZTcNTQ/s1600/dila%2Bserija.jpg'],
                    ['Sulejman','http://www.balkanje.com/browse-sulejman-velicanstveni-videos-','http://www.telegraf.rs/wp-content/uploads/2013/03/04/Sulejman.jpg'],
                    ['Gumus','http://www.balkanje.com/browse-gumus-videos-','http://www.serije.biz/uploads/articles/53024efb.png']]

    for i in range(len(serije_balk)):
        url = build_url({'mode': 'otvori_seriju_balkanje', 'link':'%s'%serije_balk[i][1], 'page':'1'})
        li = xbmcgui.ListItem('%s'%serije_balk[i][0] ,iconImage='%s'%serije_balk[i][2])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='otvori_seriju_balkanje':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    page=dicti['page'][0]

    url=link+'%s-date.html'%page
    nadi_epizode(url,page,link)

elif mode[0]=='serije_novo1':

    url='http://www.balkanje.com/newvideos.html'

    html=read_url(url)

    soup=bs(html)
    tag=soup.find('ul',{'class':'pm-ul-new-videos thumbnails'})

    lis=tag.findAll('li')
    results=[]
    for i in range(len(lis)):
        thumb=lis[i].find('img')['src']
        item=lis[i].find('h3').find('a')
        link=item['href']
        title=item['title']
        
        url = build_url({'mode': 'otvori_epizodu', 'link':'%s'%link, 'title':'%s'%title, 'thumb':'%s'%thumb})
        li = xbmcgui.ListItem('%s '%(title), iconImage=thumb)

        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li,isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
    
elif mode[0]=='otvori_epizodu':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    title=dicti['title'][0]
    thumb=dicti['thumb'][0]

    otvori_epizodu(link,title,thumb)

elif mode[0]=='lzn':
    godine=[2015,2014,2013,2012,2011,2010,2009,2008,2007]


    for i in range(len(godine)):
        url = build_url({'mode': 'otvori_lzn_godinu', 'godina': '%s'%str(godine[i])})
        li = xbmcgui.ListItem('%s'%str(godine[i]) ,iconImage='http://bh-info.com/wp-content/uploads/2015/04/lud.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='otvori_lzn_godinu':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    godina=int(dicti['godina'][0])
    links=get_izet(godina)
    for i in range(len(links)):
        url = build_url({'mode': 'otvori_lzn_ep','url':'%s'%links[i][0], 'ep':'%s'%links[i][1]})
        li = xbmcgui.ListItem('%s'%links[i][1].replace('LZN','Epizoda') ,iconImage='http://bh-info.com/wp-content/uploads/2015/04/lud.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='otvori_lzn_ep':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    url=dicti['url'][0]
    print(url)
    named=dicti['ep'][0].replace('LZN','Epizoda')
    name='Lud, zbunjen, normalan: '+ named

    import urlresolver
    resolved=urlresolver.resolve(get_izet_video(url))

    li = xbmcgui.ListItem('%s'%name)
    li.setInfo('video', { 'title': '%s'%name })
    
    xbmc.Player().play(item=resolved, listitem=li)




#####################################################################################################################################################################
#Live TV
#####################################################################################################################################################################
elif mode[0]=='live':
    cats=[['Hrvatski','hrvatski','http://sprdex.com/wp-content/uploads/2012/07/RTL-televizija.jpg'],
        ['Dokumentarno','Dokumentarci-eng','http://cdn.fansided.com/wp-content/blogs.dir/280/files/2014/07/33506.jpg'],
        ['Sport','sport','http://www.hospitalityandcateringnews.com/wp-content/uploads/New-BT-Sport-TV-packages-for-hospitality-to-massively-undercut-Sky.jpg'],
        ['News','news','http://hub.tv-ark.org.uk/images/news/skynews/skynews_images/2001/skynews2001.jpg'],
        ['Filmovi/serije','film-serije','http://tvbythenumbers.zap2it.com/wp-content/uploads/2012/04/hbo_logo.jpg'],
        ['Lifestyle','lifestyle','http://pmcdeadline2.files.wordpress.com/2013/04/travelchannel_logo__130423191643.jpg'],
        ['Glazba','tv-music','http://www.hdtvuk.tv/mtv_logo.gif'],
        ['Djeca','djecji','http://upload.wikimedia.org/wikipedia/pt/archive/f/fe/20120623043934!Logo-TV_Kids.jpg'],
        ['Regionalni','regionalni','http://www.tvsrbija.net/wp-content/uploads/2013/01/pinktv.jpg'],
        ['Njemacki kanali','njemacki','http://upload.wikimedia.org/wikipedia/en/thumb/b/ba/Flag_of_Germany.svg/1280px-Flag_of_Germany.svg.png'],
        ['Ostalo','ostalo','http://www.globallistings.info/repository/image/6/445.jpg']]
    for i in range(len(cats)):
        url = build_url({'mode': 'open_live', 'tag': '%s'%cats[i][1]})
        li = xbmcgui.ListItem('%s'%cats[i][0],iconImage='%s'%cats[i][2])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_live':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['tag'][0]

    reg='url="(.+?)"'
    pat=re.compile(reg)
    reg2='ime="(.+?)"'
    pat2=re.compile(reg2)
    reg3='img="(.+?)"'
    pat3=re.compile(reg3)
    urll='https://raw.githubusercontent.com/natko1412/liveStreams/master/%s.txt'%link
    a=urllib2.urlopen(urll)
    html=a.read().decode('utf-8')
    urls=[]
    urls=re.findall(pat,html)
    imena=[]
    imena=re.findall(pat2,html)
    thumbs=[]
    thumbs=re.findall(pat3,html)
    for i in range(len(imena)):
        li = xbmcgui.ListItem(' %s'%imena[i], iconImage='%s'%thumbs[i])
        
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=urls[i], listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)
#####################################################################################################################################################################
#Radio HRT
#####################################################################################################################################################################
elif mode[0]=='radioNZ':
    url = build_url({'mode': 'open_radio', 'foldername': 'prvi'})
    li = xbmcgui.ListItem('Prvi program' ,iconImage='http://radio.hrt.hr/data/channel/000001_db2d163a63493dfb6988.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'open_radio', 'foldername': 'drugi'})
    li = xbmcgui.ListItem('Drugi program' ,iconImage='http://radio.hrt.hr/data/channel/000002_d30fe284de7db561a7a5.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'open_radio', 'foldername': 'treci'})
    li = xbmcgui.ListItem('Treci program' ,iconImage='http://radio.hrt.hr/data/channel/000003_206025ee3856385c797e.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_radio':
    radio_prvi=[['http://radio.hrt.hr/arhiva/glazbena-kutijica/106/','Glazbena kutijica','http://radio.hrt.hr/data/show/small/000106_dc8c3b107ed03fe1d72a.png'],
    ['http://radio.hrt.hr/arhiva/katapultura/124/','Katapultura','http://radio.hrt.hr/data/show/small/000124_7f8a2fc760da4ffb13fd.jpg'],
    ['http://radio.hrt.hr/arhiva/kutija-slova/121/','Kutija slova','http://radio.hrt.hr/data/show/small/000121_c915aa04c682cd4ceae9.png'],
    ['http://radio.hrt.hr/arhiva/lica-i-sjene/131/','Lica i sjene','http://radio.hrt.hr/data/show/small/000131_f1fccaf5f9deb049a2a8.png'],
    ['http://radio.hrt.hr/arhiva/oko-znanosti/123/','Oko znanosti','http://radio.hrt.hr/data/show/small/000123_9d42ba1671b607c73749.png'],
    ['http://radio.hrt.hr/arhiva/pod-reflektorima/103/','Pod reflektorima','http://radio.hrt.hr/data/show/small/000103_00f27f731e2db0a017b1.png'],
    ['http://radio.hrt.hr/arhiva/povijest-cetvrtkom/126/','Povijest cetvrtkom','http://radio.hrt.hr/data/show/small/000126_d237561e30ad805abd1b.png'],
    ['http://radio.hrt.hr/arhiva/putnici-kroz-vrijeme/582/','Putnici kroz vrijeme','http://radio.hrt.hr/data/show/small/000582_17ce2778878d5f74d4c5.png'],
    ['http://radio.hrt.hr/arhiva/slusaj-kako-zemlja-dise/120/','Slusaj kako zemlja dise','http://radio.hrt.hr/data/show/small/000120_1fa05c0fdaa00afca3a9.png'],
    ['http://radio.hrt.hr/arhiva/u-sobi-s-pogledom/112/','U sobi s pogledom','http://radio.hrt.hr/data/show/small/000112_587e449519318aa90b41.png'],
    ['http://radio.hrt.hr/arhiva/zasto-tako/114/','Zasto tako?','http://radio.hrt.hr/data/show/small/000114_176003cffe60b893e589.png'],
    ['http://radio.hrt.hr/arhiva/znanjem-do-zdravlja/117/','Znanjem do zdravlja','http://radio.hrt.hr/data/show/small/000117_582f3d27a0e52c7e78be.png']]
    radio_drugi=[['http://radio.hrt.hr/arhiva/andromeda/18/','Andromeda','http://radio.hrt.hr/data/show/000018_f48cf7a1b19bf447b1e5.png'],
    ['http://radio.hrt.hr/arhiva/drugi-pogled/993/','Drugi pogled','http://radio.hrt.hr/data/show/small/000993_6fa6ff53c88f1ed3e50e.jpg'],
    ['http://radio.hrt.hr/arhiva/gladne-usi/700/','Gladne usi','http://radio.hrt.hr/data/show/small/000700_cdcdeaf6c30f86069ffd.png'],
    ['http://radio.hrt.hr/arhiva/globotomija/817/','Globotomija','http://radio.hrt.hr/data/show/small/000817_ec6bddd7f2754bb19eb5.jpg'],
    ['http://radio.hrt.hr/arhiva/homo-sapiens/812/','Homo sapiens','http://radio.hrt.hr/data/show/small/000812_9d0f8f96fca9b3826dbf.jpg']]
    radio_treci=[['http://radio.hrt.hr/arhiva/bibliovizor/713/','Bibliovizor','http://radio.hrt.hr/data/show/small/000713_e1aaeb9afcb944db39ca.jpg'],
    ['http://radio.hrt.hr/arhiva/filmoskop/98/','Filmoskop','http://radio.hrt.hr/data/show/small/000098_0fbee68352530480fe0e.jpg'],
    ['http://radio.hrt.hr/arhiva/glazba-i-obratno/614/','Glazba i obratno','http://radio.hrt.hr/data/show/small/000614_8155a16df37fd274d77f.jpg'],
    ['http://radio.hrt.hr/arhiva/lica-okolice/717/','Lica okolice','http://radio.hrt.hr/data/show/small/000717_e5af40b1d5af68406fc3.jpg'],
    ['http://radio.hrt.hr/arhiva/mikrokozmi/102/','Mikrokozmi','http://radio.hrt.hr/data/show/small/000102_2f995b3b984cdd82f923.jpg'],
    ['http://radio.hrt.hr/arhiva/moj-izbor/91/','Moj izbor','http://radio.hrt.hr/emisija/moj-izbor/91/'],
    ['http://radio.hrt.hr/arhiva/na-kraju-tjedna/196/','Na kraju tjedna','http://radio.hrt.hr/data/show/small/000196_7c5997025a9bfcf45967.jpg'],
    ['http://radio.hrt.hr/arhiva/poezija-naglas/720/','Poezija naglas','http://radio.hrt.hr/data/show/small/000720_c2495423cd72b180482f.jpg'],
    ['http://radio.hrt.hr/arhiva/znanost-i-drustvo/950/','Znanost i drustvo','http://radio.hrt.hr/data/show/small/000950_6dd01f01230facbf40b0.jpg']]


    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['foldername'][0]
    if link=='prvi':
        rdio=radio_prvi
    elif link=='drugi':
        rdio=radio_drugi

    elif link=='treci':
        rdio=radio_treci


    for i in range (len(rdio)):
        title=rdio[i][1]
        url=rdio[i][0]
        img=rdio[i][2]
        url = build_url({'mode':'open_emisija','url': '%s'%url, 'foldername': '%s'%title, 'img':'%s'%img})
        li = xbmcgui.ListItem('%s'%title ,iconImage=img)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='open_emisija':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    title=dicti['foldername'][0]
    img=dicti['img'][0]
    url=dicti['url'][0]

    lista=find_episodes(url)
    
    for i in range (len(lista)):
        li = xbmcgui.ListItem('%s'%lista[i][1], iconImage='%s'%img)
        li.setInfo('music', { 'title': '%s'%lista[i][1] })
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=lista[i][0], listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)
#####################################################################################################################################################################
#Radio uzivo
#####################################################################################################################################################################
elif mode[0]=='radio_live':
    
    lista=get_links_country('croatia')

    for i in range(1,len(lista)):
        li = xbmcgui.ListItem('%s (%s)'%(lista[i][1],lista[i][3]), iconImage='https://cdn2.iconfinder.com/data/icons/windows-8-metro-style/512/radio.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=lista[i][0], listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)