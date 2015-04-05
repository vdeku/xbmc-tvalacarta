# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Hispan TV
# creado por rsantaella
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "hispantv"
__category__ = "F"
__type__ = "generic"
__title__ = "hispantv"
__language__ = "ES"
__creationdate__ = "20121130"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("tvalacarta.channels.hispantv mainlist")    

    return programas(item)

def programas(item):
    logger.info("tvalacarta.channels.hispantv programas")    

    itemlist = []
    item.url="http://www.hispantv.com/programas"
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <li class="tile col-xs-12 col-sm-3">
    <div class="inner">
    <div class="img video">
    <a href="/showprogram/Al-Andalus/68">
    <img src="http://217.218.67.243/images/thumbnail/20150215/14434794_l.jpg" alt="Al Ándalus" />
    </a></div>
    <div class="desc"><h4><a href="/showprogram/Al-Andalus/68">Al Ándalus</a></h4></div></div></li>
    '''
    patron  = '<li class="tile[^<]+'
    patron += '<div class="inner"[^<]+'
    patron += '<div class="img video"[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)" alt="([^"]+)"'

    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        url = urlparse.urljoin(item.url,scrapedurl)
        plot = ""
        itemlist.append( Item(channel=__channel__, action="episodios", title=title, url=url, thumbnail=thumbnail,  plot=plot, viewmode="movie", folder=True))

    return itemlist

def episodios(item):
    logger.info("tvalacarta.channels.hispantv episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    promo_url = scrapertools.find_single_match(data,'<a href="([^"]+)" class="btn btn-default" target="_blank">Descargar')
    if promo_url!="":
        itemlist.append( Item(channel=__channel__, action="play", server="directo", title="Ver la promo del programa", url=promo_url, thumbnail=item.thumbnail, plot=item.plot, folder=False))

    logger.info(data)
    '''
    <li class="tile col-xs-12 col-sm-4">
    <a href="/showepisode/Al-Natural/68Al-Natural---Ensalada-de-Brocoli,-la-Alfalfa,-coctel-de-Tofu-y-Granada,-colirio-de-Eufrasia-y-Aciano-para-ojos/68">
    <div class="inner">
    <div class="img video">
    <img src="http://217.218.67.243/images/thumbnail/20150305/06360563_xl.jpg" alt="Al Natural - Ensalada de Brócoli, la Alfalfa, cóctel de Tofu y Granada, colirio de Eufrasia y Aciano para ojos" />
    '''
    patron  = '<li class="tile[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<div class="inner"[^<]+'
    patron += '<div class="img video"[^<]+'
    patron += '<img src="([^"]+)" alt="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail).replace(" ","%20")
        url = urlparse.urljoin(item.url,scrapedurl)
        plot = ""
        itemlist.append( Item(channel=__channel__, action="play", server="hispantv", title=title, url=url, thumbnail=thumbnail, plot=plot, folder=False))
        
    return itemlist

def play(item):
    logger.info("tvalacarta.channels.hispantv play")

    if item.server=="directo":
        return [item]
    
    itemlist = []
    data = scrapertools.cachePage(item.url)
    video_url = scrapertools.find_single_match(data,'<a href="([^"]+)" class="btn btn-default" target="_blank">Descargar')
    if video_url!="":
        itemlist.append( Item(channel=__channel__, action="play", server="directo", title=item.title, url=video_url, thumbnail=item.thumbnail, plot=item.plot, folder=False))

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    
    # Mainlist es la lista de programas
    programas_items = mainlist(Item())
    if len(programas_items)==0:
        print "No encuentra los programas"
        return False

    episodios_items = videos(programas_items[0])
    if len(episodios_items)==0:
        print "El programa '"+programas_items[0].title+"' no tiene episodios"
        return False

    return True
