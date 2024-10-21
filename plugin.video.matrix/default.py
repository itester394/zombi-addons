# -*- coding: utf-8 -*-
# https://github.com/zombiB/zombi-addons
#import xbmc

# from resources.lib.statistic import cStatistic
from resources.lib.home import cHome
from resources.lib.gui.gui import cGui
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import progress, VSlog, addon, window, siteManager
from resources.lib.search import cSearch

import xbmcgui
import xbmcplugin

# New: Import for URL resolution, etc.
from resources.lib.resolver import resolve_url

####################
#  Debugging settings
####################
DEBUG = False

ADDON = addon()
icons = ADDON.getSetting('defaultIcons')

####################
# Auto-play Settings
####################
AUTO_PLAY = ADDON.getSetting('autoPlay') == 'true'
MAX_RETRIES = 3  # Number of times to retry a source before moving on to the next

if DEBUG:
    import sys
    sys.path.append('H:\Program Files\Kodi\system\Python\Lib\pysrc')
    try:
        import pysrc.pydevd as pydevd
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        try:
            import pydevd
            pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
        except ImportError:
            sys.stderr.write("Error: " + "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")


class main:
    def __init__(self):
        self.parseUrl()

    def parseUrl(self):
        oPluginHandler = cPluginHandler()
        pluginPath = oPluginHandler.getPluginPath()
        if pluginPath == 'plugin://plugin.video.matrix/extrafanart/':
            return

        oInputParameterHandler = cInputParameterHandler()

        if oInputParameterHandler.exist('function'):
            sFunction = oInputParameterHandler.getValue('function')
        else:
            VSlog('call load method')
            sFunction = "load"

        if sFunction == 'setSetting':
            self.setSetting(oInputParameterHandler)
            return

        if sFunction == 'DoNothing':
            return

        # New: Handling sources if available
        if sFunction == 'play':
            self.handlePlay()
            return

        # Fallback to load home if no function is defined
        if not oInputParameterHandler.exist('site'):
            plugins = cHome()
            plugins.load()
            return

        if oInputParameterHandler.exist('site'):
            sSiteName = oInputParameterHandler.getValue('site')
            VSlog(f'Loading site {sSiteName} and calling function {sFunction}')

            if self.isHosterGui(sSiteName, sFunction):
                return

            self.handleOtherFunctions(sSiteName, sFunction)

    # Added function to fetch and auto-play sources
    def handlePlay(self):
        # Fetch sources for the current item
        sources = self.fetchSources()

        if AUTO_PLAY:
            # Sort and select the best source
            best_source = self.selectBestSource(sources)
            self.playSource(best_source)
        else:
            # Let the user choose from the available sources
            self.chooseSource(sources)

    def fetchSources(self):
        # Here you would fetch sources from the site or external resolver
        VSlog("Fetching sources...")
        sources = [
            {"url": "https://source1.com", "quality": "1080p"},
            {"url": "https://source2.com", "quality": "720p"},
            {"url": "https://source3.com", "quality": "480p"}
        ]
        return sources

    def selectBestSource(self, sources):
        # Sort sources by quality, and return the best one
        VSlog("Selecting the best source...")
        sorted_sources = sorted(sources, key=lambda x: x['quality'], reverse=True)
        return sorted_sources[0]  # Return the best quality source

    def playSource(self, source):
        url = source['url']
        success = self.tryPlayUrl(url)

        # Retry logic if the source fails
        retries = 0
        while not success and retries < MAX_RETRIES:
            retries += 1
            VSlog(f"Retry {retries} for {url}")
            success = self.tryPlayUrl(url)

        if not success:
            xbmcgui.Dialog().notification("Stream Unavailable", "Failed to play stream after retries.", xbmcgui.NOTIFICATION_ERROR)

    def tryPlayUrl(self, url):
        # Resolve the URL if necessary (e.g., using URL resolver)
        resolved_url = resolve_url(url)
        if resolved_url:
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=resolved_url))
            return True
        return False

    def chooseSource(self, sources):
        # Present the user with a list of available sources
        VSlog("Allowing user to choose a source...")
        source_labels = [f"{source['quality']} - {source['url']}" for source in sources]
        selected = xbmcgui.Dialog().select("Choose Source", source_labels)

        if selected >= 0:
            self.playSource(sources[selected])

    ####################
    # Helper functions for the original plugin functions
    ####################
    def setSetting(self, oInputParameterHandler):
        if oInputParameterHandler.exist('id') and oInputParameterHandler.exist('value'):
            plugin_id = oInputParameterHandler.getValue('id')
            value = oInputParameterHandler.getValue('value')
            addons = addon()
            if addons.getSetting(plugin_id) != value:
                addons.setSetting(plugin_id, value)

    def handleOtherFunctions(self, sSiteName, sFunction):
        if self.isHosterGui(sSiteName, sFunction):
            return
        if self.isGui(sSiteName, sFunction):
            return
        if self.isFav(sSiteName, sFunction):
            return
        # Extend as needed for additional functionalities

    def isHosterGui(self, sSiteName, sFunction):
        if sSiteName == 'cHosterGui':
            plugins = __import__('resources.lib.gui.hoster', fromlist=['cHosterGui']).cHosterGui()
            function = getattr(plugins, sFunction)
            function()
            return True
        return False

    def isGui(self, sSiteName, sFunction):
        if sSiteName == 'cGui':
            oGui = cGui()
            exec("oGui." + sFunction + "()")
            return True
        return False

    def isFav(self, sSiteName, sFunction):
        if sSiteName == 'cFav':
            plugins = __import__('resources.lib.bookmark', fromlist=['cFav']).cFav()
            function = getattr(plugins, sFunction)
            function()
            return True
        return False

# Main entry point
main()
