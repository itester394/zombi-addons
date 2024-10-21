﻿# -*- coding: utf-8 -*-
# zombi https://github.com/zombiB/zombi-addons/
	
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog, siteManager, addon
from resources.lib.parser import cParser
 
ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

SITE_IDENTIFIER = 'tvfun'
SITE_NAME = 'Tvfun'
SITE_DESC = 'arabic vod'
 
URL_MAIN = https://olk.tvfhd.com/

RAMADAN_SERIES = (URL_MAIN + '/ts/mosalsalat-ramadan-2024/', 'showSeries')
SERIE_TR = (URL_MAIN + '/cat/mosalsalat-torkia/', 'showSeries')
SERIE_DUBBED = (URL_MAIN + '/cat//mosalsalat-modablaja/', 'showSeries')
SERIE_SUBED = (URL_MAIN + '/cat//mosalsalat-motarjama/', 'showSeries')
SERIE_HEND = (URL_MAIN + '/cat//mosalsalat-hindia/', 'showSeries')
SERIE_AR = (URL_MAIN + '/cat/mosalsalat-3arabia/', 'showSeries')

SERIE_KR = (URL_MAIN + '/cat//mosalsalat-korea/', 'showSeries')
SERIE_LATIN = (URL_MAIN + '/cat//mosalsalat-latinia/', 'showSeries')
REPLAYTV_NEWS = (URL_MAIN + '/cat//zee-alwan/', 'showSeries')

URL_SEARCH = (URL_MAIN + '/q/', 'showSeriesSearch')
FUNCTION_SEARCH = 'showSeriesSearch'
 
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    # oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Search Series', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'SEARCH_SERIES', icons + '/Search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_AR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات عربية', icons + '/Arabic.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_KR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات كورية', icons + '/Korean.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_TR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات تركية', icons + '/Turkish.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HEND[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات هندية', icons + '/Hindi.png', oOutputParameterHandler)  

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LATIN [0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات لاتنية', icons + '/Latin.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_DUBBED [0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مدبلجة', icons + '/Dubbed.png', oOutputParameterHandler)
        
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SUBED [0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مترجمة', icons + '/Subtitled.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', RAMADAN_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات رمضان', icons + '/Ramadan.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', 'https://m.tvfun.me/cat/mosalsalat-maghribia/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'مسلسلات مغربية', icons + '/Moroccan.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_MAIN + '/q/' +sSearchText 

        showSeriesSearch(sUrl)
        oGui.setEndOfDirectory()
        return
  
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
  # ([^<]+) .+? (.+?)

    sPattern = '<div class="thumb series-.+?">.+?<a href="(.+?)">.+?src="(.+?)" alt.+?<br>(.+?)</a>'



    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        for aEntry in aResult[1]:
 
            sTitle = aEntry[2].replace("مشاهدة وتحميل","").replace("اون لاين","").replace("مترجمة","").replace("مترجم","")
            siteUrl = aEntry[0]
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            if URL_MAIN not in siteUrl:
                siteUrl = URL_MAIN + siteUrl
            sThumb = aEntry[1]
            sDesc = ''
            sYear = ''


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
			
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)


    sPattern = 'class="pagination.+?">(.+?)id="footer">'  
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) 
     

    if aResult[0]:
        sHtmlContent3 = aResult[1][0]
  # ([^<]+) .+?

        sPattern = '<a href="([^<]+)">([^<]+)</a>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent3, sPattern)
	
	
        if aResult[0]:
            for aEntry in aResult[1]:
 
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]
                if URL_MAIN not in siteUrl:
                    siteUrl = URL_MAIN + siteUrl
                sThumb = ""
                sDesc = ""


                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, '', oOutputParameterHandler)

        
    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', icons + '/Next.png', oOutputParameterHandler)
    oGui.setEndOfDirectory() 
  
def showSeriesSearch(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch+'/'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
      # (.+?) ([^<]+) .+?
	
    sPattern = '<span class="video.+?">.+?<a href="(.+?)">.+?src="(.+?)" alt.+?>(.+?)<br>(.+?)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) 
     	
    if aResult[0]:
        for aEntry in aResult[1]:
 
            sTitle = aEntry[2]+aEntry[3]
            sTitle = sTitle.replace("الحلقة "," E").replace("حلقة "," E").replace("مشاهدة وتحميل","").replace("اون لاين","").replace("والاخيرة","")
            siteUrl = aEntry[0]
            sThumb = aEntry[1]
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            if URL_MAIN not in siteUrl:
                siteUrl = URL_MAIN + siteUrl

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)


    sPattern = '<ul class="pagination.+?">(.+?)id="footer">'  
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) 
     

    if aResult[0]:
        sHtmlContent3 = aResult[1][0]
  # ([^<]+) .+?

        sPattern = '<li><a href="([^<]+)">([^<]+)</a></li>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent3, sPattern)
	
	
        if aResult[0]:
            for aEntry in aResult[1]:
 
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]
                if URL_MAIN not in siteUrl:
                    siteUrl = URL_MAIN + siteUrl
                sThumb = ""
                sDesc = ""


                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', sTitle, '', oOutputParameterHandler)
        

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    #([^<]+) .+?
    
    sPattern = '<ul class="pagination">(.+?)div id="footer">'  
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) 
     
    if aResult[0]:
        sHtmlContent3 = aResult[1][0]
      
        sPattern = '<a class=\"current\" href=\"([^<]+)\">([^<]+)</a>'
        CurrentPage = oParser.parse(sHtmlContent3, sPattern)
        
        if CurrentPage[0]:
            sPattern = '<li><a href="([^<]+)">([^<]+)</a></li>'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent3, sPattern)
            #VSlog(aResult)
            if aResult[0]:
                for aEntry in aResult[1]:
                    
                    
                    if int(aEntry[1]) - int(CurrentPage[1][0][1]) ==1:
                        VSlog('Next Page: ' + aEntry[0])
                        return URL_MAIN + aEntry[0]
        else:
            sPattern = '<li><a href="([^<]+)">2</a></li>'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent3, sPattern)
            VSlog('Next Page: ' + aResult[1][0])
            return URL_MAIN + aResult[1][0]
        
    return False
            
        
def showEpisodes():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   # ([^<]+) .+? (.+?)
    sPattern = '<div class="episode video-.+?"><a href="(.+?)" title=.+?<br>(.+?)</a>'
	
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        for aEntry in aResult[1]:
 
            sTitle = " E"+aEntry[1].replace("الحلقة "," E").replace("حلقة "," E").replace("مدبلج للعربية","مدبلج").replace("مشاهدة وتحميل","").replace("اون لاين","")
            sTitle = sMovieTitle+sTitle
            siteUrl = aEntry[0]
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            if URL_MAIN not in siteUrl:
                siteUrl = URL_MAIN + siteUrl
            sThumb = sThumb
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
   #([^<]+) .+?
    sPattern = 'class="videocontainer"> <iframe src="([^<]+)" id="([^<]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
	
    if aResult[0]:
        for aEntry in aResult[1]:
 
            sTitle = "playlist"
            siteUrl = 'https:'+aEntry[0]
            if siteUrl.startswith('//'):
                siteUrl = 'http:' + siteUrl
            if URL_MAIN not in siteUrl:
                siteUrl = URL_MAIN + siteUrl
            sThumb = sThumb
            sDesc = ""
			


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)


    sPattern = '<ul class="pagination">(.+?)id="footer">'  
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern) 
     

    if aResult[0]:
        sHtmlContent3 = aResult[1][0]
  # ([^<]+) .+?

        sPattern = '<li><a href="([^<]+)">([^<]+)</a></li>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent3, sPattern)
	
	
        if aResult[0]:
            for aEntry in aResult[1]:
 
                sTitle = aEntry[1]
            
                sTitle =  "PAGE " + sTitle
                sTitle =   '[COLOR red]'+sTitle+'[/COLOR]'
                siteUrl = aEntry[0]
                if URL_MAIN not in siteUrl:
                    siteUrl = URL_MAIN + siteUrl
                sThumb = ""
                sDesc = ""


                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl',siteUrl)
			
                oGui.addDir(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', oOutputParameterHandler)

       
    oGui.setEndOfDirectory()

def showHosters():
    import base64
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    if '/video/' in sUrl:
        sUrl = sUrl.replace("/video/","/watch/")
        VSlog(sUrl)
    oParser = cParser()    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern =  'onclick="setVideo(.+?);'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            m3url = aEntry.replace("('","").replace("')","")
            # Try to fix string to make it decodable:
            m3url = m3url[2:]

            sHtmlContent2 = base64.b64decode(m3url).decode('ascii',errors='ignore')
   
            sPattern = 'src="(.+?)".+?allowfullscreen'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if aResult[0]:
               for aEntry in aResult[1]:
        
                   url = aEntry.replace("https://dai.ly/","https://www.dailymotion.com/video/")
                   sTitle = " " 
                   if url.startswith('//'):
                       url = 'http:' + url
            
                   sHosterUrl = url 
                   oHoster = cHosterGui().checkHoster(sHosterUrl)
                   if oHoster:
                       sDisplayTitle = sMovieTitle+sTitle
                       oHoster.setDisplayName(sDisplayTitle)
                       oHoster.setFileName(sDisplayTitle)
                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                
    oGui.setEndOfDirectory()