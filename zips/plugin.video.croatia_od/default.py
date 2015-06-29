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


#######################################################################
#======================================================================
# FUNKCIJE

# url='http://www.dailymotion.com/embed/video/k7kK5DKi13Tcp9bM2A0'
# import urlresolver
# resolved=urlresolver.resolve(url)
# xbmc.Player().play(resolved)


def read_url(url):

        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link.decode('utf-8')



def serije_novo():
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
                import urlresolver

                resolved=urlresolver.resolve(link)
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

def resolve_otv_link(link):
    request=urllib2.urlopen(link)
    html=request.read()
    soup=bs(html)
    tag=soup.findAll('meta',{'property':'og:video:url'})[0]['content']
    
    link=convert(tag)
    index=link.index('file=')
    link=link[index+5:]
    return(link)


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


def get_vijesti():
    site='http://www.rtl.hr/video/vijesti/'
    base_url='http://www.rtl.hr'
    

    reg='![CDATA[(.+?)]]'
    pat=re.compile(reg)




    request=urllib2.urlopen(site)
    html=request.read()
    soup=bs(html)

    tags=soup.findAll('ul',{'class':'left clearfix m_0'})

    first=tags[0]
    second=tags[1]

    first_a=first.findAll('a')
    second_a=second.findAll('a')
    linksout=[]

    for i in range(len(first_a)):
        link=base_url+first_a[i]['href']
        title=first_a[i]['title']
        img=(first_a[i].findAll('span')[0]).findAll('img')[0]['src']
        link=resolve_rtl_link(link)
        linksout+=[[link,title,img]]

    for i in range(len(second_a)):
        link=base_url+second_a[i]['href'] 
        title=second_a[i]['title']
        img=(second_a[i].findAll('span')[0]).findAll('img')[0]['src']
        link=resolve_rtl_link(link)
        linksout.append([link,title,img])
    return linksout

        






def get_new(site,category):
    
    
    base_url=''
    #base_url='http://www.rtl.hr'
    url=site
    
    try:
        resp = urllib2.urlopen(url)
        contents = resp.read()
    except urllib2.HTTPError, error:
        contents = error.read()
    html=contents
    soup=bs(html)
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
                title=aas[i].findAll('span',{'class':'subtitle'})[0].getText().strip('\n').strip(' ').replace('                                                 ','')
                title=tit+': '+title
                img=(aas[i].findAll('span')[0]).findAll('img')[0]['src']
                
                link=resolve_rtl_link(link)
                linksout.append([link,title,img])

        return linksout


def get_cats_mreza():
    url='http://mreza.tv/video/'

    request=urllib.urlopen(url)
    html=request.read().decode('utf-8')
    soup=bs(html)

    tag=soup.find("div", {"id":"wrapper-glavni"})

    emisije=tag.findAll('h2')
    em_tag=tag.findAll('section')
    popis_emisija=[]
    for i in range(len(emisije)):
        em=emisije[i].getText().encode('utf-8').decode('latin2')
        image=em_tag[i].get('src')
        try:
            em_tagg=str(em_tag[i].get('id'))
        except:
            em_tagg=em_tag[i].get('class')
            idd=''
            for g in range (len(em_tagg)):
                idd+=' '
                idd+=em_tagg[g]
                idd=str(idd)
            em_tagg=idd
            em_tagg=em_tagg[1:]

        popis_emisija+=[[em,em_tagg,image]]
    del popis_emisija[0]
    del popis_emisija[0]
    return(popis_emisija)

def get_shows_mreza(tagy):
    url='http://mreza.tv/video/'
    shows=[]
    request=urllib.urlopen(url)
    html=request.read().decode("ascii", "ignore")
    soup=bs(html)

    tag=soup.find("div", {"id":"wrapper-glavni"})
    tag=tag.find("section",{"class":"%s"%tagy})
   
    pom=tag.findAll("h5")
    for i in range(len(pom)):
        pomy=pom[i].findAll("a")[0]
        ime=str(pomy.get("title")).decode("ascii", "ignore")
        link=str(pomy.get("href")).decode("ascii", "ignore")
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

shows=[['http://www.hrt.hr/enz/7-dana/', '7 dana'], ['http://www.hrt.hr/enz/abeceda-zdravlja/', 'Abeceda zdravlja'], ['http://www.hrt.hr/enz/alpe-dunav-jadran/', 'Alpe Dunav Jadran'],
     ['http://www.hrt.hr/enz/biblija/', 'Biblija'], ['http://www.hrt.hr/enz/bozic-u-ciboni/', 'Bozic u Ciboni'], ['http://www.hrt.hr/enz/briljanteen/','Briljanteen'], 
     ['http://www.hrt.hr/enz/carpe-diem/', 'Carpe Diem'], ['http://www.hrt.hr/enz/dalekozor/', 'Dalekozor'], ['http://www.hrt.hr/enz/damin-gambit/', 'Damin gambit'], 
     ['http://www.hrt.hr/enz/djecja-usta/', 'Djecja usta'], ['http://www.hrt.hr/enz/dnevnik/', 'Dnevnik'], ['http://www.hrt.hr/enz/dnevnik-3/', 'Dnevnik 3'], 
     ['http://www.hrt.hr/enz/dnevnik-u-podne/', 'Dnevnik u podne'], ['http://www.hrt.hr/enz/dobro-jutro-kultura/', 'Dobro jutro: Kultura'], 
     ['http://www.hrt.hr/enz/dokumentarna-produkcija-hrt-a/', 'Dokumentarna produkcija HRT-a'], ['http://www.hrt.hr/enz/dorucak-s-autorom/', 'Dorucak s autorom'], 
     ['http://www.hrt.hr/enz/drustvena-mreza/', 'Drustvena mreza'], ['http://www.hrt.hr/enz/druga-strana/', 'Druga strana'], ['http://www.hrt.hr/enz/drugi-format/', 'Drugi format'], 
     ['http://www.hrt.hr/enz/duhovni-izazovi/', 'Duhovni izazovi'], ['http://www.hrt.hr/enz/eko-zona/', 'Eko zona'], ['http://www.hrt.hr/enz/ekumena/', 'Ekumena'], 
     ['http://www.hrt.hr/enz/emisija-pucke-i-predajne-kulture/', 'Emisija pucke i predajne kulture'], ['http://www.hrt.hr/enz/eurogradani/', 'Eurogradani'], 
     ['http://www.hrt.hr/enz/filozofski-teatar/', 'Filozofski teatar'], ['http://www.hrt.hr/enz/fokus/', 'Fokus'], 
     ['http://www.hrt.hr/enz/fotografija-u-hrvatskoj/', 'Fotografija u Hrvatskoj'], ['http://www.hrt.hr/enz/garaza/', 'Garaza'], ['http://www.hrt.hr/enz/generacija-y/', 'Generacija Y'], 
     ['http://www.hrt.hr/enz/glas-domovine/', 'Glas domovine'], ['http://www.hrt.hr/enz/glas-za-covjeka/', 'Glas za covjeka'], ['http://www.hrt.hr/enz/govornica/', 'Govornica'],
     ['http://www.hrt.hr/enz/hrvatska-uzivo/', 'Hrvatska uzivo'], ['http://www.hrt.hr/enz/inauguracija-kolinde-grabar-kitarovic/', 'Inauguracija Kolinde Grabar-Kitarovic'], 
     ['http://www.hrt.hr/enz/indeks/', 'Indeks'], ['http://www.hrt.hr/enz/intervju-tjedna/', 'Intervju tjedna'], ['http://www.hrt.hr/enz/iza-ekrana/', 'Iza ekrana'],
     ['http://www.hrt.hr/enz/izlaz-broj-4/', 'Izlaz broj 4'], ['http://www.hrt.hr/enz/javna-stvar/', 'Javna stvar'], ['http://www.hrt.hr/enz/jezik-za-svakoga/', 'Jezik za svakoga'], 
     ['http://www.hrt.hr/enz/kauc-surferica/', 'Kauc surferica'], ['http://www.hrt.hr/enz/klasici-narodu/', 'Klasici narodu'], 
     ['http://www.hrt.hr/enz/knjiga-ili-zivot/', 'Knjiga ili zivot'], ['http://www.hrt.hr/enz/kod-buducnosti/', 'Kod buducnosti'], 
     ['http://www.hrt.hr/enz/kulturna-bastina/', 'Kulturna bastina'], ['http://www.hrt.hr/enz/kulturni-kolodvor/', 'Kulturni kolodvor'], ['http://www.hrt.hr/enz/labirint/', 'Labirint'], 
     ['http://www.hrt.hr/enz/laboratorij-na-kraju-svemira/', 'Laboratorij na kraju svemira'], ['http://www.hrt.hr/enz/lijepom-nasom/', 'Lijepom nasom'], 
     ['http://www.hrt.hr/enz/manjinski-mozaik/', 'Manjinski mozaik'], ['http://www.hrt.hr/enz/mir-i-dobro/', 'Mir i dobro'], ['http://www.hrt.hr/enz/misa/', 'Misa'], 
     ['http://www.hrt.hr/enz/more/', 'More'], ['http://www.hrt.hr/enz/na-rubu-znanosti/', 'Na rubu znanosti'], ['http://www.hrt.hr/enz/navrh-jezika/', 'Navrh jezika'], 
     ['http://www.hrt.hr/enz/nedjeljom-u-2/', 'Nedjeljom u 2'], ['http://www.hrt.hr/enz/ni-da-ni-ne/', 'Ni da ni ne'], ['http://www.hrt.hr/enz/nocna-kavana/', 'Nocna kavana'], 
     ['http://www.hrt.hr/enz/normalan-zivot/', 'Normalan zivot'], ['http://www.hrt.hr/enz/notica/', 'Notica'], ['http://www.hrt.hr/enz/novogodisnji-program/', 'Novogodisnji program'], 
     ['http://www.hrt.hr/enz/olimp/', 'Olimp'], ['http://www.hrt.hr/enz/otvoreno/', 'Otvoreno'], ['http://www.hrt.hr/enz/pamet-u-glavu/', 'Pamet u glavu'], 
     ['http://www.hrt.hr/enz/paralele/', 'Paralele'], ['http://www.hrt.hr/enz/peti-dan/', 'Peti dan'], ['http://www.hrt.hr/enz/piramida/', 'Piramida'], 
     ['http://www.hrt.hr/enz/plodovi-klasike/', 'Plodovi klasike'], ['http://www.hrt.hr/enz/plodovi-zemlje/', 'Plodovi zemlje'], 
     ['http://www.hrt.hr/enz/pogled-preko-granice/', 'Pogled preko granice'], ['http://www.hrt.hr/enz/pola-ure-kulture/', 'Pola ure kulture'], ['http://www.hrt.hr/enz/porin/', 'Porin'], 
     ['http://www.hrt.hr/enz/poslovna-zona/', 'Poslovna zona'], ['http://www.hrt.hr/enz/poslovne-vijesti/', 'Poslovne vijesti'], ['http://www.hrt.hr/enz/potrosacki-kod/', 'Potrosacki kod'],
     ['http://www.hrt.hr/enz/pozitivno/', 'Pozitivno'], ['http://www.hrt.hr/enz/pravilo-72/', 'Pravilo 72'], 
     ['http://www.hrt.hr/enz/prekid-programa-zbog-citanja/', 'Prekid programa zbog citanja'], ['http://www.hrt.hr/enz/press-klub/', 'Press klub'], 
     ['http://www.hrt.hr/enz/pricigin/', 'Pricigin'], ['http://www.hrt.hr/enz/prizma/', 'Prizma'], ['http://www.hrt.hr/enz/puni-krug/', 'Puni krug'], 
     ['http://www.hrt.hr/enz/rec-i/', 'REC-i'], ['http://www.hrt.hr/enz/regionalni-dnevnik/', 'Regionalni dnevnik'], ['http://www.hrt.hr/enz/rijec-i-zivot/', 'Rijec i zivot'], 
     ['http://www.hrt.hr/enz/seoska-gozba/', 'Seoska gozba'], ['http://www.hrt.hr/enz/skitancije/', 'Skitancije'], ['http://www.hrt.hr/enz/snaga-volje/', 'Snaga volje'], 
     ['http://www.hrt.hr/enz/sport-dnevnik/', 'Sport dnevnik'], ['http://www.hrt.hr/enz/stand-up-3/', 'Stand up 3'], ['http://www.hrt.hr/enz/strip-u-hrvatskoj/', 'Strip u Hrvatskoj'], 
     ['http://www.hrt.hr/enz/studio-4/', 'Studio 4 '], ['http://www.hrt.hr/enz/stvarajmo-zajedno/', 'Stvarajmo zajedno'], ['http://www.hrt.hr/enz/subotom-ujutro/', 'Subotom ujutro'], 
     ['http://www.hrt.hr/enz/suvremenici/', 'Suvremenici'], ['http://www.hrt.hr/enz/svaki-dan-dobar-dan/', 'Svaki dan dobar dan'], ['http://www.hrt.hr/enz/svlacionica/', 'Svlacionica'], 
     ['http://www.hrt.hr/enz/symposium/', 'Symposium'], ['http://www.hrt.hr/enz/sahovski-komentar/', 'Sahovski komentar'], ['http://www.hrt.hr/enz/skolski-sat/', 'Skolski sat'], 
     ['http://www.hrt.hr/enz/slep-sou/', 'Slep sou'], ['http://www.hrt.hr/enz/sto-vas-zulja/', 'Sto vas zulja'], ['http://www.hrt.hr/enz/tjedni-pregled/', 'Tjedni pregled'], 
     ['http://www.hrt.hr/enz/ton-i-ton/', 'Ton i ton'], ['http://www.hrt.hr/enz/treca-dob/', 'Treca dob'], ['http://www.hrt.hr/enz/treca-runda/', 'Treca runda'], 
     ['http://www.hrt.hr/enz/treci-element/', 'Treci element'], ['http://www.hrt.hr/enz/trikultura/', 'Trikultura'], ['http://www.hrt.hr/enz/turisticka-klasa/', 'Turisticka klasa'], 
     ['http://www.hrt.hr/enz/tv-student/', 'TV student'], ['http://www.hrt.hr/enz/vecer-na-8-katu/', 'Vecer na 8. katu'], ['http://www.hrt.hr/enz/vedranovi-velikani/', 'Vedranovi velikani'],
     ['http://www.hrt.hr/enz/veterani-mira/', 'Veterani mira'], ['http://www.hrt.hr/enz/vijesti-iz-kulture/', 'Vijesti iz kulture'], ['http://www.hrt.hr/enz/vjetar-u-kosi/', 'Vjetar u kosi'], 
     ['http://www.hrt.hr/enz/vrtlarica/', 'Vrtlarica'], ['http://www.hrt.hr/enz/znanstveni-krugovi/', 'Znanstveni krugovi'], ['http://www.hrt.hr/enz/zuti-marker/', 'Zuti marker']]

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
class main():
    def __init__(self):
        self.link='http://www.hrt.hr/enz/dnevnik/'
        self.request = urllib2.urlopen(self.link)
        self.html = self.request.read()

    def get_shows(self):#=====>  vraca listu tipa likovi[index]=[link_emisije[index],ime_emisije[index]]
        br=0
        linksout = []
        soup = bs(self.html)
        tag = soup.find("div", {"class":"all_shows"})
        letters=tag.findAll('ul')
        emisija=[None]*len(letters)
        emisije=[None]*200
        name=[None]*200
        for i in range(len(letters)):
            emisija[i]=letters[i].findAll('li')
        
        for j in range(len(emisija)):
            for k in range(len(emisija[j])):
                for a in emisija[j][k].findAll('a'):
                    link=a['href']
                    br+=1
                    link='http:'+link
                    emisije[br]=link
                    name[br]=emisija[j][k].getText()
               
                
        emisije = [x for x in emisije if x != None]
        name = [x for x in name if x != None]
        linkovi=[None]*len(emisije)
        for g in range(len(emisije)):
            linkovi[g]=[emisije[g],name[g]]
        
        return linkovi

        #==========================================================================
        #

    def get_episodes(self,link): #======> vraca listu tipa linkovi[0]=[link_epizode[0],ime_epizode[0]]

        
        my_addon = xbmcaddon.Addon()
        broj_rez = my_addon.getSetting('broj_rezultata')
        
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

        
    def get_episode_link(self,link):                #====> vraca .mp4 link
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



TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)
imena=['Dnevnik','Nedjeljom u 2','Olimp','Otvoreno','Piramida','Sahovski komentar']
linkovi=[ 'http://www.hrt.hr/enz/dnevnik/','http://www.hrt.hr/enz/nedjeljom-u-2/',  'http://www.hrt.hr/enz/olimp/', 
    'http://www.hrt.hr/enz/otvoreno/', 'http://www.hrt.hr/enz/piramida/', 'http://www.hrt.hr/enz/sahovski-komentar/', ]
mreza_cats=[['Informativne emisije', 'videoteka v-info-emisije'], ['Zabavno - mozaicni program', 'videoteka v-zm-program'], ['Ostale emisije', 'videoteka v-ostale-emisije']]
    
a=main()   
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:
    url = build_url({'mode': 'rtl', 'foldername': 'RTL Sada'})
    li = xbmcgui.ListItem('RTL Sada', iconImage='http://www.bnet.hr/var/ezflow_site/storage/images/b_net/novosti/rtl_sada_od_sada_na_b_netu/40484-1-cro-HR/rtl_sada_od_sada_na_b_netu_view_full.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'hrt', 'foldername': 'HRT Emisije'})
    li = xbmcgui.ListItem('HRT Emisije' ,iconImage='http://www.hrt.hr/static/v2/img/hrt_logo_fb.gif')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    
    url = build_url({'mode': 'radio', 'foldername': 'Radio emisije'})
    li = xbmcgui.ListItem('Radio emisije' ,iconImage='http://www.hrt.hr/static/v2/img/hrt_logo_fb.gif')
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

    url = build_url({'mode': 'tv', 'foldername': 'TV uzivo'})
    li = xbmcgui.ListItem('TV uzivo' ,iconImage='http://www.standard.co.uk/incoming/article8223968.ece/alternates/w460/televisonold.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'serije_novo', 'foldername': 'serije'})
    li = xbmcgui.ListItem('Serije' ,iconImage='http://www.standard.co.uk/incoming/article8223968.ece/alternates/w460/televisonold.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    
    url = build_url({'mode': 'radioo', 'foldername': 'Radio uzivo'})
    li = xbmcgui.ListItem('Radio uzivo' ,iconImage='http://www.wooden-radio.com/gb/pics/bild-wooden-radio-wr01a-1-gross.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    
    # url = build_url({'mode': 'playlist', 'foldername': 'User liste'})
    # li = xbmcgui.ListItem('User liste' ,iconImage='http://driftmycatch.be/Layout/playlisticon.png')
    # xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
    #                             listitem=li, isFolder=True)



    xbmcplugin.endOfDirectory(addon_handle)





elif mode[0]=='serije_novo':

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
    serije_novo()

elif mode[0]=='otvori_epizodu':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    title=dicti['title'][0]
    thumb=dicti['thumb'][0]

    otvori_epizodu(link,title,thumb)




elif mode[0]=='jabuka':
    otv_emisije=[ ['2U9','http://videoteka.jabukatv.hr/index.php?option=com_hwdmediashare&view=category&id=9&Itemid=114'],['Hrana i vino','http://videoteka.jabukatv.hr/index.php?option=com_hwdmediashare&view=category&id=10&Itemid=115'],
                    ['Veto','http://videoteka.jabukatv.hr/index.php?option=com_hwdmediashare&view=category&id=11&Itemid=116'] ]

    for i in range(len(otv_emisije)):
        url = build_url({'mode': 'jabuka_%s'%i, 'foldername': '%s'%otv_emisije[i][0]})
        li = xbmcgui.ListItem('%s'%otv_emisije[i][0] ,iconImage='http://radionadlanu.com/games/images/jabuka-tv.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)



    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='jabuka_0':
    lista=get_video_links_from_jabuka_show('http://videoteka.jabukatv.hr/index.php?option=com_hwdmediashare&view=category&id=9&Itemid=114')
    
    for i in range(len(lista)):
        li = xbmcgui.ListItem(' %s'%lista[i][1], iconImage='http://radionadlanu.com/games/images/jabuka-tv.png')
        link=resolve_otv_link(lista[i][0])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=link, listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='jabuka_1':
    lista=get_video_links_from_jabuka_show('http://videoteka.jabukatv.hr/index.php?option=com_hwdmediashare&view=category&id=10&Itemid=115')
    
    for i in range(len(lista)):
        li = xbmcgui.ListItem(' %s'%lista[i][1], iconImage='http://radionadlanu.com/games/images/jabuka-tv.png')
        link=resolve_otv_link(lista[i][0])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=link, listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='jabuka_2':
    lista=get_video_links_from_jabuka_show('http://videoteka.jabukatv.hr/index.php?option=com_hwdmediashare&view=category&id=11&Itemid=116')
    
    for i in range(len(lista)):
        li = xbmcgui.ListItem(' %s'%lista[i][1], iconImage='http://radionadlanu.com/games/images/jabuka-tv.png')
        link=resolve_otv_link(lista[i][0])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=link, listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)



elif mode[0]=='mreza':

    mreza_cats=[['Informativne emisije', 'videoteka v-info-emisije'], ['Zabavno - mozaicni program', 'videoteka v-zm-program'], ['Ostale emisije', 'videoteka v-ostale-emisije']]
    for i in range(len(mreza_cats)):
        url = build_url({'mode': 'mreza%s'%i, 'foldername': '%s'%mreza_cats[i][0]})
        li = xbmcgui.ListItem('%s'%mreza_cats[i][0],iconImage='http://teve.ba/img/articles/11349.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)




elif mode[0]=='radioo':
    
    lista=get_links_country('croatia')

    for i in range(1,len(lista)):
        li = xbmcgui.ListItem('%s (%s)'%(lista[i][1],lista[i][3]), iconImage='http://www.wooden-radio.com/gb/pics/bild-wooden-radio-wr01a-1-gross.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=lista[i][0], listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='radio':
    url = build_url({'mode': 'prvi', 'foldername': 'Prvi program'})
    li = xbmcgui.ListItem('Prvi program' ,iconImage='http://radio.hrt.hr/data/channel/000001_db2d163a63493dfb6988.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'drugi', 'foldername': 'Drugi program'})
    li = xbmcgui.ListItem('Drugi program' ,iconImage='http://radio.hrt.hr/data/channel/000002_d30fe284de7db561a7a5.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    url = build_url({'mode': 'treci', 'foldername': 'Treci program'})
    li = xbmcgui.ListItem('Treci program' ,iconImage='http://radio.hrt.hr/data/channel/000003_206025ee3856385c797e.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='prvi':
    for i in range (len(radio_prvi)):
        title=radio_prvi[i][1]
        url=radio_prvi[i][0]
        img=radio_prvi[i][2]
        url = build_url({'mode': '%s'%url, 'foldername': '%s'%title})
        li = xbmcgui.ListItem('%s'%title ,iconImage=img)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='drugi':
    for i in range (len(radio_drugi)):
        title=radio_drugi[i][1]
        url=radio_drugi[i][0]
        img=radio_drugi[i][2]
        url = build_url({'mode': '%s'%url, 'foldername': '%s'%title})
        li = xbmcgui.ListItem('%s'%title ,iconImage=img)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='treci':
    for i in range (len(radio_treci)):
        title=radio_treci[i][1]
        url=radio_treci[i][0]
        img=radio_treci[i][2]
        url = build_url({'mode': '%s'%url, 'foldername': '%s'%title})
        li = xbmcgui.ListItem('%s'%title ,iconImage=img)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

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

elif mode[0]=='rtl_novosti':

    lista=get_vijesti()
    for i in range(len(lista)):
        li = xbmcgui.ListItem(' %s'%lista[i][1], iconImage='%s'%lista[i][2])
        
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=lista[i][0], listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='rtl_sada':
    kateg=[['Najnoviji video','rtl_latest_new'],['Serije','rtl_latest_serije'],['Info i Magazini','rtl_latest_mag'],
            ['Zabava','rtl_latest_zabava'],['Dokumentarci','rtl_latest_doc'],['Humor','rtl_latest_humor'],['Gastro','rtl_latest_gastro'],['RTL Kockica','rtl_latest_kockica']]

    for i in range(len(kateg)):
        url = build_url({'mode': '%s!'%kateg[i][1], 'foldername': '%s'%kateg[i][0]})
        li = xbmcgui.ListItem('%s'%kateg[i][0] ,iconImage='http://www.bnet.hr/var/ezflow_site/storage/images/b_net/novosti/rtl_sada_od_sada_na_b_netu/40484-1-cro-HR/rtl_sada_od_sada_na_b_netu_view_full.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
elif 'rtl_latest' in mode[0]:
    
    reg='rtl_latest_(.+?)!'
    pat=re.compile(reg)
    mod=re.findall(pat,mode[0])[0]
    
    if mod =='new':
        kateg=[['Najnoviji video',0],['Serije',1],['Info i magazini',2],['Zabava',4],['Dokumentarci',5],['Humor',6],['Gastro',7]]
        site='http://www.rtl.hr/rtl-sada/'
    elif mod=='serije':
        kateg=[ ['Vatre ivanjske', 'http://www.rtl.hr/rtl-sada/serije/vatre-ivanjske/'], ['Hitna','http://www.rtl.hr/rtl-sada/serije/hitna/'],['Ponos Ratkajevih','http://www.rtl.hr/rtl-sada/serije/ponos-ratkajevih/'],['Pomorska ophodnja','http://www.rtl.hr/rtl-sada/serije/pomorska-ophodnja/'],
                ['Mr.Bean','http://www.rtl.hr/rtl-sada/serije/mr-bean-serija/'],['K.T.2','http://www.rtl.hr/rtl-sada/serije/kt-2/'] ,['Cobra 11','http://www.rtl.hr/rtl-sada/serije/cobra-11/'],['Sulejman','http://www.rtl.hr/rtl-sada/serije/sulejman/'],
                ['Kriza','http://www.rtl.hr/rtl-sada/serije/kriza/'], ['Avenida Brasil','http://www.rtl.hr/rtl-sada/serije/avenida-brasil/'] ,['Odbacena','http://www.rtl.hr/rtl-sada/serije/odbacena/'] ,
                 ['Divlja ruza','http://www.rtl.hr/rtl-sada/serije/divlja-ruza/'],['Villa Maria','http://www.rtl.hr/rtl-sada/serije/villa-maria/']]
        
    elif mod=='mag':
        kateg=[ ['RTL Danas','http://www.rtl.hr/rtl-sada/magazini/rtl-danas/'],['RTL Direkt','http://www.rtl.hr/rtl-sada/magazini/rtl-direkt/'],['Sve u sest','http://www.rtl.hr/rtl-sada/magazini/sve-u-sest/'] ,
        ['RTL Vijesti','http://www.rtl.hr/rtl-sada/magazini/rtl-vijesti/'] ,['TOP.HR','http://www.rtl.hr/rtl-sada/magazini/top-hr/'],
        ['RTL Liga','http://www.rtl.hr/rtl-sada/magazini/rtl-liga/']]
    elif mod=='zabava':
        kateg=[ ['X Factor','http://www.rtl.hr/rtl-sada/zabava/x-factor/'] ,['Kolo srece','http://www.rtl.hr/rtl-sada/zabava/kolo-srece/'],['Shopping kraljica','http://www.rtl.hr/rtl-sada/zabava/shopping-kraljica/'],
        ['Skoro','http://www.rtl.hr/rtl-sada/zabava/skoro/'],['Cirkus','http://www.rtl.hr/rtl-sada/zabava/cirkus/'],['Dynamo: Majstor nemoguceg','http://www.rtl.hr/rtl-sada/zabava/dynamo-majstor-nemoguceg/'],
        ['Sef na tajnom zadatku','http://www.rtl.hr/rtl-sada/zabava/sef-na-tajnom-zadatku/'],['Pet na pet','http://www.rtl.hr/rtl-sada/zabava/pet-na-pet/'],
        ['Indizajn','http://www.rtl.hr/rtl-sada/zabava/indizajn/'],['Sudnica','http://www.rtl.hr/rtl-sada/zabava/sudnica/'],
        ['Prijatelj na kvadrat','http://www.rtl.hr/rtl-sada/zabava/prijatelj-na-kvadrat/'],['Koledzicom po svijetu','http://www.rtl.hr/rtl-sada/zabava/koledzicom-po-svijetu/'],
        ['Mjenjacnica','http://www.rtl.hr/rtl-sada/zabava/mjenjacnica/'],['Ljubav je na selu','http://www.rtl.hr/rtl-sada/zabava/ljubav-je-na-selu/'],['Mijenjam zenu','http://www.rtl.hr/rtl-sada/zabava/mijenjam-zenu/'],
        ['Krv nije voda','http://www.rtl.hr/rtl-sada/zabava/krv-nije-voda/']]
    elif mod=='doc':
        kateg=[ ['Moderna cuda','http://www.rtl.hr/rtl-sada/dokumentarci/moderna-cuda/'],['Javne tajne','http://www.rtl.hr/rtl-sada/dokumentarci/javne-tajne/'],
        ['Mayday','http://www.rtl.hr/rtl-sada/dokumentarci/mayday-tajna-crne-kutije/'],['Kraljevi leda','http://www.rtl.hr/rtl-sada/dokumentarci/kraljevi-leda-smrtonosne-ceste/'],['Smrtonosnih 60','http://www.rtl.hr/rtl-sada/dokumentarci/smrtonosnih-60/'],
        ['Galileo','http://www.rtl.hr/rtl-sada/dokumentarci/galileo/'] ,['Lovci na nekretnine','http://www.rtl.hr/rtl-sada/dokumentarci/lovci-na-nekretnine/'],
        ['Javne tajne','http://www.rtl.hr/rtl-sada/dokumentarci/javne-tajne/'],['Lice s naslovnice','http://www.rtl.hr/rtl-sada/dokumentarci/lice-s-naslovnice/'],
        ['Policijska patrola','http://www.rtl.hr/rtl-sada/dokumentarci/policijska-patrola/']]
    elif mod=='humor':
        kateg=[ ['Klub smijeha','http://www.rtl.hr/rtl-sada/humor/klub-smijeha/'],['Moja tri zida','http://www.rtl.hr/rtl-sada/humor/moja-tri-zida/'],
        ['Newsbar','http://www.rtl.hr/rtl-sada/humor/newsbar/'],['Nadreality show','http://www.rtl.hr/rtl-sada/humor/nadreality-show/'],
        ['Pervanov dnevnik','http://www.rtl.hr/rtl-sada/humor/pervanov-dnevnik/']]
    elif mod =='gastro':
        kateg=[ ['Tri, dva, jedan kuhaj!','http://www.rtl.hr/rtl-sada/gastro/tri-dva-jedan-kuhaj/'], ['Vecera za 5','http://www.rtl.hr/rtl-sada/gastro/vecera-za-5/'] ,
        ['Kuhar i pol','http://www.rtl.hr/rtl-sada/gastro/kuhar-i-pol/'],['David Rocco: Dolce Vita','http://www.rtl.hr/rtl-sada/gastro/david-rocco-dolce-vita/']]

    elif mod =='kockica':
        kateg=[ ['Mali znanstvenici','http://www.rtl.hr/rtl-sada/rtl-kockica/mali-znanstvenici/'], ['Divlji u srcu','http://www.rtl.hr/rtl-sada/rtl-kockica/divlji-u-srcu/'],
        ['Fora patrola','http://www.rtl.hr/rtl-sada/rtl-kockica/fora-patrola/'],['Hlapiceve sportske igre','http://www.rtl.hr/rtl-sada/rtl-kockica/hlapiceve-sportske-igre/'],
        ['Crtalica','http://www.rtl.hr/rtl-sada/rtl-kockica/crtalica/'],['Leteci medvjedi','http://www.rtl.hr/rtl-sada/rtl-kockica/mali-leteci-medvjedi/'],
        ['Crvene kapice','http://www.rtl.hr/rtl-sada/rtl-kockica/crvene-kapice/'] , ['Mali svijet','http://www.rtl.hr/rtl-sada/rtl-kockica/mali-svijet/'],
        ['Johnny Test','http://www.rtl.hr/rtl-sada/rtl-kockica/johnny-test/'],['Bilo jednom...Istrazivaci','http://www.rtl.hr/rtl-sada/rtl-kockica/bilo-jednomistrazivaci/'],
        ['Idemo u ZOO','http://www.rtl.hr/rtl-sada/rtl-kockica/idemo-u-zoo/'],['Skola za vampire','http://www.rtl.hr/rtl-sada/rtl-kockica/skola-za-vampire/'],
        ['Vragolasti Denis','http://www.rtl.hr/rtl-sada/rtl-kockica/vragolasti-denis/'],['Vremeplov','http://www.rtl.hr/rtl-sada/rtl-kockica/vremeplov/'],
        ['Sto je sto','http://www.rtl.hr/rtl-sada/rtl-kockica/sto-je-sto/'],['Mala sportska akademija','http://www.rtl.hr/rtl-sada/rtl-kockica/mala-sportska-akademija/'],
        ['Baka prica najljepse price','http://www.rtl.hr/rtl-sada/rtl-kockica/baka-prica-najljepse-price/'],
        ['Hitovi djecje televizije','http://www.rtl.hr/rtl-sada/rtl-kockica/hitovi-djecje-televizije/'],
        ['TOP lista djecje televizije','http://www.rtl.hr/rtl-sada/rtl-kockica/top-lista-djecje-televizije/'],['Uvrnuti cupavci','http://www.rtl.hr/rtl-sada/rtl-kockica/uvrnuti-cupavci/'],
        ['Filmovi','http://www.rtl.hr/rtl-sada/rtl-kockica/filmovi/']]

    
    for i in range(len(kateg)):
        url = build_url({'mode': 'get_new&site="%s"&index="0"'%kateg[i][1], 'foldername': '%s'%kateg[i][0]})
        li = xbmcgui.ListItem('%s'%kateg[i][0] ,iconImage='http://www.bnet.hr/var/ezflow_site/storage/images/b_net/novosti/rtl_sada_od_sada_na_b_netu/40484-1-cro-HR/rtl_sada_od_sada_na_b_netu_view_full.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif 'get_new' in mode[0]:
    reg1='get_new&site="(.+?)"'
    pat1=re.compile(reg1)
    reg2='&index="(.+?)"'
    pat2=re.compile(reg2)


    site=re.findall(pat1,mode[0])[0]
    
    index=int(re.findall(pat2,mode[0])[0])
    

    lista=get_new(site,index)

    for i in range(len(lista)):
        li = xbmcgui.ListItem(' %s'%lista[i][1], iconImage='%s'%lista[i][2])
        
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
        url = build_url({'mode': 'rtl%s'%(str(i)), 'foldername': '%s'%show_name})
        li = xbmcgui.ListItem('%s'%show_name ,iconImage='%s'%show_img)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='tv':
    cats=[['Hrvatski','tv-cro','http://sprdex.com/wp-content/uploads/2012/07/RTL-televizija.jpg'],['Dokumentarno','tv-doc','http://cdn.fansided.com/wp-content/blogs.dir/280/files/2014/07/33506.jpg'],
        ['Sport','tv-sport','http://www.hospitalityandcateringnews.com/wp-content/uploads/New-BT-Sport-TV-packages-for-hospitality-to-massively-undercut-Sky.jpg'],
        ['News','tv-news','http://hub.tv-ark.org.uk/images/news/skynews/skynews_images/2001/skynews2001.jpg'],['Filmovi/serije','tv-film','http://tvbythenumbers.zap2it.com/wp-content/uploads/2012/04/hbo_logo.jpg'],
        ['Lifestyle','tv-life','http://pmcdeadline2.files.wordpress.com/2013/04/travelchannel_logo__130423191643.jpg'],
        ['Glazba','tv-music','http://www.hdtvuk.tv/mtv_logo.gif'],['Djeca','tv-kids','http://upload.wikimedia.org/wikipedia/pt/archive/f/fe/20120623043934!Logo-TV_Kids.jpg'],
        ['Regionalni','tv-reg','http://www.tvsrbija.net/wp-content/uploads/2013/01/pinktv.jpg'],['Njemacki kanali','tv-njem','http://upload.wikimedia.org/wikipedia/en/thumb/b/ba/Flag_of_Germany.svg/1280px-Flag_of_Germany.svg.png'],['Ostalo','tv-ostalo','http://www.globallistings.info/repository/image/6/445.jpg']]
    for i in range(len(cats)):
        url = build_url({'mode': '%s'%cats[i][1], 'foldername': '%s'%cats[i][0]})
        li = xbmcgui.ListItem('%s'%cats[i][0],iconImage='%s'%cats[i][2])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0]=='tv-njem':
    


    reg='url="(.+?)"'
    pat=re.compile(reg)
    reg2='ime="(.+?)"'
    pat2=re.compile(reg2)
    reg3='img="(.+?)"'
    pat3=re.compile(reg3)
    urll='https://raw.githubusercontent.com/natko1412/liveStreams/master/njemacki.txt'
    


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
elif mode[0]=='tv-film':
    


    reg='url="(.+?)"'
    pat=re.compile(reg)
    reg2='ime="(.+?)"'
    pat2=re.compile(reg2)
    reg3='img="(.+?)"'
    pat3=re.compile(reg3)
    urll='https://raw.githubusercontent.com/natko1412/liveStreams/master/film-serije.txt'
    


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
elif mode[0]=='tv-life':
    


    reg='url="(.+?)"'
    pat=re.compile(reg)
    reg2='ime="(.+?)"'
    pat2=re.compile(reg2)
    reg3='img="(.+?)"'
    pat3=re.compile(reg3)
    urll='https://raw.githubusercontent.com/natko1412/liveStreams/master/lifestyle.txt'


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
elif mode[0]=='tv-cro':
    


    reg='url="(.+?)"'
    pat=re.compile(reg)
    reg2='ime="(.+?)"'
    pat2=re.compile(reg2)
    reg3='img="(.+?)"'
    pat3=re.compile(reg3)
    urll='https://raw.githubusercontent.com/natko1412/liveStreams/master/hrvatski.txt'
    


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

elif mode[0]=='tv-news':
    


    reg='url="(.+?)"'
    pat=re.compile(reg)
    reg2='ime="(.+?)"'
    pat2=re.compile(reg2)
    reg3='img="(.+?)"'
    pat3=re.compile(reg3)
    urll='https://raw.githubusercontent.com/natko1412/liveStreams/master/news.txt'
    


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

elif mode[0]=='tv-reg':
    


    reg='url="(.+?)"'
    pat=re.compile(reg)
    reg2='ime="(.+?)"'
    pat2=re.compile(reg2)
    reg3='img="(.+?)"'
    pat3=re.compile(reg3)
    urll='https://raw.githubusercontent.com/natko1412/liveStreams/master/regionalni.txt'
    


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
elif mode[0]=='tv-ostalo':
    
    #folderi:






    reg='url="(.+?)"'
    pat=re.compile(reg)
    reg2='ime="(.+?)"'
    pat2=re.compile(reg2)
    reg3='img="(.+?)"'
    pat3=re.compile(reg3)
    urll='https://raw.githubusercontent.com/natko1412/liveStreams/master/ostalo.txt'
    


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

elif mode[0]=='tv-kids':
    


    reg='url="(.+?)"'
    pat=re.compile(reg)
    reg2='ime="(.+?)"'
    pat2=re.compile(reg2)
    reg3='img="(.+?)"'
    pat3=re.compile(reg3)
    urll='https://raw.githubusercontent.com/natko1412/liveStreams/master/djecji.txt'
    


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

elif mode[0]=='tv-doc':
    


    reg='url="(.+?)"'
    pat=re.compile(reg)
    reg2='ime="(.+?)"'
    pat2=re.compile(reg2)
    reg3='img="(.+?)"'
    pat3=re.compile(reg3)
    urll='https://raw.githubusercontent.com/natko1412/liveStreams/master/Dokumentarci-eng.txt'
    


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

elif mode[0]=='tv-sport':
    


    reg='url="(.+?)"'
    pat=re.compile(reg)
    reg2='ime="(.+?)"'
    pat2=re.compile(reg2)
    reg3='img="(.+?)"'
    pat3=re.compile(reg3)
    urll='https://raw.githubusercontent.com/natko1412/liveStreams/master/sport.txt'
    


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

elif 'mreza' in mode[0] and 'mreza.tv' not in mode[0] :

    index=int(mode[0].replace('mreza',''))
    j=index
    emisije=get_shows_mreza(mreza_cats[j][1])
    
    for g in range(len(emisije)):    
        url = build_url({'mode': '%s'%emisije[g][0], 'foldername': '%s'%emisije[g][1]})
        li = xbmcgui.ListItem('%s'%emisije[g][1] ,iconImage='http://teve.ba/img/articles/11349.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                               listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0]=='tv-music':
    


    reg='url="(.+?)"'
    pat=re.compile(reg)
    reg2='ime="(.+?)"'
    pat2=re.compile(reg2)
    reg3='img="(.+?)"'
    pat3=re.compile(reg3)
    urll='https://raw.githubusercontent.com/natko1412/liveStreams/master/glazba.txt'
    


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

elif 'mreza' in mode[0] and 'mreza.tv' not in mode[0] :

    index=int(mode[0].replace('mreza',''))
    j=index
    emisije=get_shows_mreza(mreza_cats[j][1])
    
    for g in range(len(emisije)):    
        url = build_url({'mode': '%s'%emisije[g][0], 'foldername': '%s'%emisije[g][1]})
        li = xbmcgui.ListItem('%s'%emisije[g][1] ,iconImage='http://teve.ba/img/articles/11349.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                               listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0]=='play_hrt':
    dicti=urlparse.parse_qs(sys.argv[2][1:])
    link=dicti['link'][0]
    name=dicti['foldername'][0]
    uri=a.get_episode_link(link)

    li = xbmcgui.ListItem('%s'%name)
    li.setInfo('video', { 'title': '%s'%name })
    xbmc.Player().play(item=uri, listitem=li)

elif mode[0] == 'hrt':
    
    
    

    for i in range(len(shows)):
        url = build_url({'mode': '%s'%i, 'foldername': '%s'%shows[i][1]})
        li = xbmcgui.ListItem('%s'%shows[i][1] ,iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/img%%20-%%20kopija%%20(%s).jpg'%(str(i)))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
    
else:
    for j in range(len(shows)):
        if mode[0]==str(j):
            dicti=urlparse.parse_qs(sys.argv[2][1:])
            
            name=dicti['foldername'][0]
            url=shows[j][0]
            episode=[]
            episode=a.get_episodes(url)
    
    
            for i in range(len(episode)):
                title=episode[i][1]
                title=remove_tags(title)
                li = xbmcgui.ListItem('%s: %s'%(name,title), iconImage='https://raw.githubusercontent.com/natko1412/repo.natko1412/master/img/img%%20-%%20kopija%%20(%s).jpg'%(str(mode[0])))
                #uri=a.get_episode_link(episode[i][0])
                uri = build_url({'mode': 'play_hrt', 'foldername': '%s: %s'%(name,title), 'link': '%s'%episode[i][0]})
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=uri, listitem=li, isFolder=True)


            xbmcplugin.endOfDirectory(addon_handle)
            break
        else:
            if mode[0]=='rtl%s'%(str(j)):
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
                html=shows[j]
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
                break

            else:
                if j<len(radio_prvi):

                    if mode[0]==radio_prvi[j][0]:
                        lista=find_episodes(radio_prvi[j][0])
                        img=radio_prvi[j][2]
                        for i in range (len(lista)):
                            li = xbmcgui.ListItem('%s'%(lista[i][1]), iconImage='%s'%img)
                        
                            xbmcplugin.addDirectoryItem(handle=addon_handle, url=lista[i][0], listitem=li)
                        xbmcplugin.endOfDirectory(addon_handle)
                if j<(len(radio_drugi)):   
                    if mode[0]==radio_drugi[j][0]:
                        lista=find_episodes(radio_drugi[j][0])
                        img=radio_drugi[j][2]
                        for i in range (len(lista)):
                            li = xbmcgui.ListItem('%s'%(lista[i][1]), iconImage='%s'%img)
                        
                            xbmcplugin.addDirectoryItem(handle=addon_handle, url=lista[i][0], listitem=li)
                        xbmcplugin.endOfDirectory(addon_handle)
                if j<len(radio_treci):
                    if mode[0]==radio_treci[j][0]:
                        lista=find_episodes(radio_treci[j][0])
                        img=radio_treci[j][2]
                        for i in range (len(lista)):
                            li = xbmcgui.ListItem('%s'%(lista[i][1]), iconImage='%s'%img)
                        
                            xbmcplugin.addDirectoryItem(handle=addon_handle, url=lista[i][0], listitem=li)
                        xbmcplugin.endOfDirectory(addon_handle)
                else:
                    try:
                        
                        if 'mreza.tv' in mode[0]:
                            epizode=get_episodes_mreza(mode[0])

                            for i in range (len(epizode)):
                                li = xbmcgui.ListItem('%s'%(epizode[i][1]), iconImage='%s'%epizode[i][2])
                        
                                xbmcplugin.addDirectoryItem(handle=addon_handle, url=epizode[i][0], listitem=li)
                            xbmcplugin.endOfDirectory(addon_handle)
                    except:
                        
                        pass
                
                    


