﻿# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para http://conectate.gov.ar
# creado por rsantaella
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,reimport os, sys

from core import loggerfrom core import configfrom core import scrapertoolsfrom core.item import Itemfrom servers import servertools
__channel__ = "dwspan"
__category__ = "F"
__type__ = "generic"
__title__ = "dwspan"
__language__ = "ES"
__creationdate__ = "20121130"
__vfanart__ = "http://www.dw.de/cssi/dwlogo-print.gif"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):    logger.info("[dwlatam.py] mainlist")        # Descarga la página    data = scrapertools.cachePage("http://mediacenter.dw.de/ajax/spanish/programm/interval/all/")    logger.info(data)    import json    programas_json = json.loads(data)    if programas_json == None : programas_json = []    itemlist = []    for programa in programas_json:        scrapedtitle = programa['_name'].encode("utf8","ignore")        scrapedurl = str(programa['_id'])        itemlist.append( Item(channel=__channel__, title=scrapedtitle , action="episodios" , url=scrapedurl, folder=True) )    return itemlistdef episodios(item):    logger.info("[dwlatam.py] episodios")    if item.title =="!Página siguiente":        data=scrapertools.cachePage('http://mediacenter.dw.de/ajax/spanish/mediaselect/video/item/%s/after/true/nochildren/true/?programm=%s' % (item.extra, item.url))    else:        data = scrapertools.cachePage('http://mediacenter.dw.de/ajax/spanish/mediaselect/video/?programm=%s' % item.url)    logger.info(data)    import json    episodios_json = json.loads(data)    if episodios_json == None : episodios_json = []            itemlist = []    last_episodio = ''    for episodio in episodios_json['mediaselect']:        last_episodio = episodio        scrapedtitle = episodios_json['items'][episodio]['title'].encode("utf8","ignore") + ' (' + episodios_json['items'][episodio]['getPublicationDate'].encode("utf8","ignore") + ')'        scrapedthumbnail = episodios_json['items'][episodio]['getImages']['medium']['src'].replace("\\", "")        scrapedplot = episodios_json['items'][episodio]['getDescription'].encode("utf8","ignore")        playpath = "mp4:%s_sor.mp4" % episodios_json['items'][episodio]["getFlvFile"].replace("\\", "")        scrapedurl= "rtmp://tv-od.dw.de/flash/ playpath=%s" % playpath        #if ((episodios_json['items'][episodio]['title'].encode("utf8","ignore") == item.title) or (episodios_json['items'][episodio]['meta_title'].encode("utf8","ignore")== item.title)):        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, folder=False) )            scrapedurl = 'http://mediacenter.dw.de/ajax/spanish/mediaselect/video/item/%s/after/true/nochildren/true/?programm=%s' % (last_episodio, item.url)    data = scrapertools.cachePage(scrapedurl)    more_episodios_json = json.loads(data)    if more_episodios_json['mediaselect']:       itemlist.append( Item(channel=__channel__, action="episodios", title="!Página siguiente" , url=item.url, extra=last_episodio, folder=True) ) 	    return itemlist