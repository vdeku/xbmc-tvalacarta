﻿# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para http://conectate.gov.ar
# creado por rsantaella
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re

from core import logger
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

def mainlist(item):