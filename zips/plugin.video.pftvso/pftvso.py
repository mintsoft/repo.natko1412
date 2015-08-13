# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from BeautifulSoup import BeautifulSoup as bs
import urllib2
import urllib
import HTMLParser
import sys
import json
import re
try:
    from addon.common.net import Net
except:
    print 'Failed to import script.module.addon.common'
    xbmcgui.Dialog().ok("PFTV Import Failure", "Failed to import addon.common", "A component needed by PFTV is missing on your system", "Please visit www.xbmchub.com for support")



domain="http://projectfreetv.so"




def read_url(url):
    net = Net()

    html=net.http_GET(url).content
    
    h = HTMLParser.HTMLParser()
    html = h.unescape(html)
    return html.encode('utf-8')



def get_last_days():
	html=read_url(domain + '/calendar/')
	soup=bs(html)
	days=soup.findAll('div',{'class':'column5'})
	out=[]
	a=len(days)
	for i in range(a-1,-1,-1):
		day=days[i].find('h4').getText()

		out+=[[day, i]]
	return out



def get_day_eps(ind):
	html=read_url(domain + '/calendar/')
	soup=bs(html)
	out=[]
	day=soup.findAll('div',{'class':'column5'})[ind]
	
	links=day.findAll('li')
	for i in range(len(links)):
		link=links[i].find('a')['href']

		name=links[i].find('a').getText()
		try:
				s_ind=name.index('Season')
				season=name[s_ind+7:s_ind+8]
				if name[s_ind+8].isdigit():
					season=name[s_ind+7:s_ind+9]
				if name[s_ind+9].isdigit():
					season=name[s_ind+7:s_ind+10]
				if name[s_ind+10].isdigit():
					season=name[s_ind+7:s_ind+11]
				if name[s_ind+11].isdigit():
					season=name[s_ind+7:s_ind+12]
		except:
				s_ind=name.index('season')
				season=name[s_ind+7:s_ind+8]
				if name[s_ind+8].isdigit():
					season=name[s_ind+7:s_ind+9]
				if name[s_ind+9].isdigit():
					season=name[s_ind+7:s_ind+10]
				if name[s_ind+10].isdigit():
					season=name[s_ind+7:s_ind+11]
				if name[s_ind+11].isdigit():
					season=name[s_ind+7:s_ind+12]

		try:
			
				s_ind=name.index('Episode')
				episode=name[s_ind+8:s_ind+9]
				try:
					if name[s_ind+9].isdigit():
						episode=name[s_ind+8:s_ind+10]
				except:
					pass
				try:
					if name[s_ind+10].isdigit():
						episode=name[s_ind+8:s_ind+11]
				except:
					pass
				try:
					if name[s_ind+11].isdigit():
						episode=name[s_ind+8:s_ind+12]
				except:
					pass

		except:
				s_ind=name.index('episode')
				episode=name[s_ind+8:s_ind+9]
				try:
					if name[s_ind+9].isdigit():
						episode=name[s_ind+8:s_ind+10]
				except:
					pass
				try:
					if name[s_ind+10].isdigit():
						episode=name[s_ind+8:s_ind+11]
				except:
					pass
				try:
					if name[s_ind+11].isdigit():
						episode=name[s_ind+8:s_ind+12]
				except:
					pass

		try:
				s_ind=name.index('Season')
				show=name[:s_ind-1]

		except:
				s_ind=name.index('season')
				show=name[:s_ind-1]

		out+=[[show,season,episode,link]]
	return out

def get_last_eps():
	html=read_url(domain )
	soup=bs(html)
	out=[]
	day=soup.findAll('div',{'class':'column5'})
	for i in range(1,-1,-1):
		links=day[i].findAll('li')
		for i in range(len(links)):


			link=links[i].find('a')['href']
			name=links[i].find('a').getText()

			

			try:
				s_ind=name.index('Season')
				season=name[s_ind+7:s_ind+8]
				if name[s_ind+8].isdigit():
					season=name[s_ind+7:s_ind+9]
				if name[s_ind+9].isdigit():
					season=name[s_ind+7:s_ind+10]
				if name[s_ind+10].isdigit():
					season=name[s_ind+7:s_ind+11]
				if name[s_ind+11].isdigit():
					season=name[s_ind+7:s_ind+12]
			except:
				s_ind=name.index('season')
				season=name[s_ind+7:s_ind+8]
				if name[s_ind+8].isdigit():
					season=name[s_ind+7:s_ind+9]
				if name[s_ind+9].isdigit():
					season=name[s_ind+7:s_ind+10]
				if name[s_ind+10].isdigit():
					season=name[s_ind+7:s_ind+11]
				if name[s_ind+11].isdigit():
					season=name[s_ind+7:s_ind+12]

			try:
			
				s_ind=name.index('Episode')
				episode=name[s_ind+8:s_ind+9]
				try:
					if name[s_ind+9].isdigit():
						episode=name[s_ind+8:s_ind+10]
				except:
					pass
				try:
					if name[s_ind+10].isdigit():
						episode=name[s_ind+8:s_ind+11]
				except:
					pass
				try:
					if name[s_ind+11].isdigit():
						episode=name[s_ind+8:s_ind+12]
				except:
					pass

			except:
				s_ind=name.index('episode')
				episode=name[s_ind+8:s_ind+9]
				try:
					if name[s_ind+9].isdigit():
						episode=name[s_ind+8:s_ind+10]
				except:
					pass
				try:
					if name[s_ind+10].isdigit():
						episode=name[s_ind+8:s_ind+11]
				except:
					pass
				try:
					if name[s_ind+11].isdigit():
						episode=name[s_ind+8:s_ind+12]
				except:
					pass

			try:
				s_ind=name.index('Season')
				show=name[:s_ind-1]

			except:
				s_ind=name.index('season')
				show=name[:s_ind-1]

			out+=[[show,season,episode,link]]

	return out

def get_shows_by_letter(letter):
	abc=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' , '1', '2', '3', '5', '9']

	html=read_url(domain + '/watch-tv-series/')
	soup=bs(html)
	tags=soup.findAll('div',{'class':'tagindex'})
	for i in range(len(abc)):
		if abc[i]==letter:
			index=i
	out=[]
	tag=tags[index]
	lis=tag.findAll('li')
	for i in range(len(lis)):
		link=lis[i].find('a')['href']
		name=lis[i].find('a')['title']
		out+=[[name,link]]
	return out

def get_seasons(url):
	html=read_url(url)
	soup=bs(html)
	tag=soup.find('ul')
	seasons=tag.findAll('li')
	out=[]
	for i in range(len(seasons)):
		link=seasons[i].find('a')['href']
		name=seasons[i].getText()#.strip()
		ind=name.index('Season')
		name=name[ind:]

		out+=[[name,link]]
	return out


def get_episodes(url):
	html=read_url(url)
	soup=bs(html)
	trs=soup.findAll('tr')
	out=[]
	aa=len(trs)-1
	
	for i in range(aa,-1,-1):
		link=trs[i].find('a')['href']
		name=trs[i].find('a').getText()
		try:
			s_ind=name.index('Season')
			season=name[s_ind+7:s_ind+8]
			if name[s_ind+8].isdigit():
				season=name[s_ind+7:s_ind+9]
			if name[s_ind+9].isdigit():
				season=name[s_ind+7:s_ind+10]
			if name[s_ind+10].isdigit():
				season=name[s_ind+7:s_ind+11]
			if name[s_ind+11].isdigit():
				season=name[s_ind+7:s_ind+12]
		except:
			s_ind=name.index('season')
			season=name[s_ind+7:s_ind+8]
			if name[s_ind+8].isdigit():
				season=name[s_ind+7:s_ind+9]
			if name[s_ind+9].isdigit():
				season=name[s_ind+7:s_ind+10]
			if name[s_ind+10].isdigit():
				season=name[s_ind+7:s_ind+11]
			if name[s_ind+11].isdigit():
				season=name[s_ind+7:s_ind+12]

		try:
		
			s_ind=name.index('Episode')
			episode=name[s_ind+8:s_ind+9]
			try:
				if name[s_ind+9].isdigit():
					episode=name[s_ind+8:s_ind+10]
			except:
				pass
			try:
				if name[s_ind+10].isdigit():
					episode=name[s_ind+8:s_ind+11]
			except:
				pass
			try:
				if name[s_ind+11].isdigit():
					episode=name[s_ind+8:s_ind+12]
			except:
				pass

		except:
			s_ind=name.index('episode')
			episode=name[s_ind+8:s_ind+9]
			try:
				if name[s_ind+9].isdigit():
					episode=name[s_ind+8:s_ind+10]
			except:
				pass
			try:
				if name[s_ind+10].isdigit():
					episode=name[s_ind+8:s_ind+11]
			except:
				pass
			try:
				if name[s_ind+11].isdigit():
					episode=name[s_ind+8:s_ind+12]
			except:
				pass

		try:
			s_ind=name.index('Season')
			show=name[:s_ind-1]

		except:
			s_ind=name.index('season')
			show=name[:s_ind-1]




		

		out+=[[show,season,episode,link]]
	return out

def get_latest_movies(page):
	if page!='1':
		url=domain + '/movies/page/%s/'%page
	else:
		url=domain + '/movies/'
	html=read_url(url)
	soup=bs(html)
	out=[]
	tags=soup.findAll('a',{'id':'featured-thumbnail'})
	for i in range(len(tags)):
		link=tags[i]['href']
		thumb=tags[i].find('img')['src']
		title=tags[i]['title']
		try:
			b_ind=title.index('(')
			year=title[b_ind+1:len(title)-1]
		except:
			year=''
		title=title[:b_ind-1]

		out+=[[title,year,thumb,link]]
	return out

def get_movies_year(year,page):

	if page!='1':
		url=domain + '/movies/search/%s/page/%s'%(year,page)
	else:
		url=domain + '/movies/search/%s'%year

	html=read_url(url)
	soup=bs(html)
	out=[]
	tags=soup.findAll('a',{'id':'featured-thumbnail'})
	for i in range(len(tags)):
		link=tags[i]['href']
		thumb=tags[i].find('img')['src']
		title=tags[i]['title']
		try:
			b_ind=title.index('(')
			year=title[b_ind+1:len(title)-1]
		except:
			year=''
		title=title[:b_ind-1]

		out+=[[title,year,thumb,link]]
	return out

def get_movies_genre(genre,page):
	#/movies/free/action/
	if page!='1':
		url=domain + '/movies/free/%s/page/%s'%(genre,page)
	else:
		url=domain + '/movies/free/%s'%genre

	html=read_url(url)
	soup=bs(html)
	out=[]
	tags=soup.findAll('a',{'id':'featured-thumbnail'})
	for i in range(len(tags)):
		link=tags[i]['href']
		thumb=tags[i].find('img')['src']
		title=tags[i]['title']
		try:
			b_ind=title.index('(')
			year=title[b_ind+1:len(title)-1]
		except:
			year=''
		title=title[:b_ind-1]

		out+=[[title,year,thumb,link]]
	return out



def search(query,type):
	if type=='tv':
		url= 'http://projectfreetv.so/search/' + urllib.quote(query)
		html=read_url(url)
		soup=bs(html)
		trs=soup.findAll('tr')
		out=[]
		aa=len(trs)-1
		if 'search' in url:
			aa=aa-2
		for i in range(1,aa):
			link=trs[i].find('a')['href']
			name=trs[i].find('a').getText()

			try:
				s_ind=name.index('Season')
				season=name[s_ind+7:s_ind+8]
				if name[s_ind+8].isdigit():
					season=name[s_ind+7:s_ind+9]
				if name[s_ind+9].isdigit():
					season=name[s_ind+7:s_ind+10]
				if name[s_ind+10].isdigit():
					season=name[s_ind+7:s_ind+11]
				if name[s_ind+11].isdigit():
					season=name[s_ind+7:s_ind+12]
			except:
				s_ind=name.index('season')
				season=name[s_ind+7:s_ind+8]
				if name[s_ind+8].isdigit():
					season=name[s_ind+7:s_ind+9]
				if name[s_ind+9].isdigit():
					season=name[s_ind+7:s_ind+10]
				if name[s_ind+10].isdigit():
					season=name[s_ind+7:s_ind+11]
				if name[s_ind+11].isdigit():
					season=name[s_ind+7:s_ind+12]

			try:
		
				s_ind=name.index('Episode')
				episode=name[s_ind+8:s_ind+9]
				try:
					if name[s_ind+9].isdigit():
						episode=name[s_ind+8:s_ind+10]
				except:
					pass
				try:
					if name[s_ind+10].isdigit():
						episode=name[s_ind+8:s_ind+11]
				except:
					pass
				try:
					if name[s_ind+11].isdigit():
						episode=name[s_ind+8:s_ind+12]
				except:
					pass

			except:
				s_ind=name.index('episode')
				episode=name[s_ind+8:s_ind+9]
				try:
					if name[s_ind+9].isdigit():
						episode=name[s_ind+8:s_ind+10]
				except:
					pass
				try:
					if name[s_ind+10].isdigit():
						episode=name[s_ind+8:s_ind+11]
				except:
					pass
				try:
					if name[s_ind+11].isdigit():
						episode=name[s_ind+8:s_ind+12]
				except:
					pass

			try:
				s_ind=name.index('Season')
				show=name[:s_ind-1]

			except:
				s_ind=name.index('season')
				show=name[:s_ind-1]




		

			out+=[[show,season,episode,link]]
		return out



	elif type=='movie':
		url='http://projectfreetv.so/movies/search/' + urllib.quote(query)

		html=read_url(url)
		soup=bs(html)
		out=[]
		tags=soup.findAll('a',{'id':'featured-thumbnail'})
		for i in range(len(tags)):
			link=tags[i]['href']
			thumb=tags[i].find('img')['src']
			title=tags[i]['title']
			try:
				b_ind=title.index('(')
				year=title[b_ind+1:len(title)-1]
			except:
				year=''
			title=title[:b_ind-1]

			out+=[[title,year,thumb,link]]
		return out


def get_link(url):
	html=read_url(url)
	soup=bs(html)
	link=soup.find('div',{'style':'float:left;width:300px;height:150px;'}).find('a')['href']
	return link

def get_show_from_ep(url):
	html=read_url(url)
	soup=bs(html)
	return soup.find('span',{'class':'thecategory'}).find('a')['href']
def get_all_shows():
	out=[]
	html=read_url('http://projectfreetv.so/watch-tv-series/')
	soup=bs(html)
	tags=soup.findAll('ul',{'class':'links'})
	reg='<a title="(.+?)" href="(.+?)">'
	for tag in tags:


		listy=re.findall(re.compile(reg),str(tag))
		items=[]
		for i in range(len(listy)):
			lista=list(listy[i])
			out+=[lista]
	return out

def get_show_img(url):
	html=read_url(url)
	soup=bs(html)
	return soup.find('div',{'style':'float:left; margin-right:20px;'}).find('img')['src']

