# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Extremadura TV
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import scrapertools
from core.item import Item

DEBUG = False
CHANNELNAME = "extremaduratv"

def isGeneric():
    return True

def mainlist(item):
    logger.info("extremaduratv.mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Informativos"   , action="programas"    , url="http://www.canalextremadura.es/alacarta/tv/programas/informativos", category="informativos") )
    itemlist.append( Item(channel=CHANNELNAME, title="Programas"      , action="programas"    , url="http://www.canalextremadura.es/alacarta/tv/programas/programas", category="programas") )
    itemlist.append( Item(channel=CHANNELNAME, title="Deportes"       , action="programas"    , url="http://www.canalextremadura.es/alacarta/tv/programas/deportes", category="deportes") )
    itemlist.append( Item(channel=CHANNELNAME, title="Archivo"        , action="archivo"      , url="http://www.canalextremadura.es/alacarta/tv/programas/archivo", category="programas") )

    return itemlist

def programas(item):
    logger.info("extremaduratv.programas")
    itemlist = []

    # Descarga la página
    '''
    <div class="views-field views-field-field-programa-a-la-carta">
    <div class="field-content">
    <a href="/alacarta/tv/programas/programas/76148/52-minutos" title="Título del enlace"><div class="field-content"><img src="http://www.canalextremadura.es/sites/default/files/styles/alacarta_listado_programas/public/52_minutos_535-290.jpg?itok=E4F3DF9z" width="225" height="140" alt="" /></div></a>    </div>
    </div>
    <div class="views-field views-field-title">
    <div class="field-content">
    <a href="/alacarta/tv/programas/programas/76148/52-minutos" title="Título del enlace">52 minutos</a>    </div>
    '''
    data = scrapertools.cachePage(item.url)
    patron  = '<div class="views-field views-field-field-programa-a-la-carta"[^<]+'
    patron += '<div class="field-content"[^<]+'
    patron += '<a href="([^"]+)"[^<]+<div class="field-content"><img src="([^"]+)"[^<]+</div></a[^<]+</div[^<]+'
    patron += '</div[^<]+'
    patron += '<div class="views-field views-field-title"[^<]+'
    patron += '<div class="field-content"[^<]+'
    patron += '<a[^>]+>([^<]+)</a>'

    matches = re.findall(patron,data,re.DOTALL)

    for url,thumbnail,titulo in matches:
        scrapedtitle = titulo
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, show=scrapedtitle) )

    return itemlist

def archivo(item):
    logger.info("extremaduratv.archivo")
    itemlist = []

    # Descarga la página
    '''
    <div class="views-field views-field-field-programa-a-la-carta col-xs-7">
    <div class="field-content">
    <a href="/alacarta/tv/programas/programas/1027/castillos-de-extremadura" title="Título del enlace">
    <div class="field-content">
    <a href="/tv/programas/castillos-de-extremadura">
    <img src="http://www.canalextremadura.es/sites/default/files/styles/alacarta_categorias_programas_archivo/public/foto_cabecera.jpg?itok=OMC1fjc4" width="75" height="46" alt="Ver ficha del programa" title="Ver ficha del programa" />
    </a></div></a>        </div>
    </div>
    <div class="views-field views-field-title col-xs-17">
    <div class="field-content">
    <a href="/alacarta/tv/programas/programas/1027/castillos-de-extremadura" title="Título del enlace">Castillos de Extremadura</a>        </div>
    '''
    data = scrapertools.cachePage(item.url)
    patron  = '<div class="views-field views-field-field-programa-a-la-carta[^<]+'
    patron += '<div class="field-content"[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<div class="field-content"[^<]+'
    patron += '<a[^<]+'
    patron += '<img src="([^"]+)"[^<]+'
    patron += '</a></div></a[^<]+</div[^<]+'
    patron += '</div[^<]+'
    patron += '<div class="views-field views-field-title[^<]+'
    patron += '<div class="field-content"[^<]+'
    patron += '<a[^>]+>([^<]+)</a>'

    matches = re.findall(patron,data,re.DOTALL)

    for url,thumbnail,titulo in matches:
        scrapedtitle = titulo
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, show=scrapedtitle) )

    return itemlist

def episodios(item):
    logger.info("extremaduratv.episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    '''
    <a href="/alacarta/tv/videos/trastos-y-tesoros-260315">
    <img src="http://www.canalextremadura.es/sites/default/files/styles/alacarta_listado_programas/public/cadillac.jpg?itok=cAhwJKrp" width="225" height="140" alt="" />
    </a></div>  </div>  
    <div class="views-field views-field-title">        
    <span class="field-content">Trastos y tesoros (26/03/15)</span>
    '''
    patron  = '<a href="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)"[^<]+'
    patron += '</a></div[^<]+</div[^<]+'
    patron += '<div class="views-field views-field-title"[^<]+'
    patron += '<span class="field-content">([^<]+)</span>'

    matches = re.findall(patron,data,re.DOTALL)

    for url,thumbnail,titulo in matches:
        scrapedtitle = titulo.strip()
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = thumbnail
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="extremaduratv" , url=scrapedurl, thumbnail = scrapedthumbnail, show=item.show, folder=False) )

    #<li class="pager-next last"><a href="/alacarta/tv/programas/informativos/97/extremadura-noticias-1?page=1" 
    patron = 'href="([^"]+)">siguiente'
    matches = re.findall(patron,data,re.DOTALL)

    for url in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente" , action="episodios" , url=scrapedurl, show=item.show) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    
    # Todas las opciones tienen que tener algo
    items = mainlist(Item())
    for item in items:
        exec "itemlist="+item.action+"(item)"
    
        if len(itemlist)==0:
            print "La categoria '"+item.title+"' no devuelve programas"
            return False

    # El primer programa de la primera categoria tiene que tener videos
    mainlist_items = mainlist(Item())
    programas_items = programas(mainlist_items[0])
    submenu_episodios_items = episodios(programas_items[0])

    exec "episodios_itemlist="+submenu_episodios_items[0].action+"(submenu_episodios_items[0])"
    if len(episodios_itemlist)==0:
        print "El programa '"+programas_mainlist[0].title+"' no tiene videos en su seccion '"+submenu_episodios_items[0].title+"'"
        return False

    return True
