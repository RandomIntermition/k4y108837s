import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import HTMLParser,json
import net

net=net.Net()

#ee3fa
ADDON = xbmcaddon.Addon(id='plugin.video.bbciplayerapp')
ICON = ADDON.getAddonInfo('icon')
FANART = ADDON.getAddonInfo('fanart')
######PROXYBASE=ADDON.getSetting('PROXYBASE')
SHOWLIVE=ADDON.getSetting('SHOWLIVE')
ART = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.bbciplayerapp/img/'))





json_query = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Application.GetProperties", '
                                 '"params": {"properties": ["version", "name"]}, "id": 1 }')
json_query = unicode(json_query, 'utf-8', errors='ignore')
json_query = json.loads(json_query)

xbmc_version = str(json_query['result']['version']['major'])+'.'+str(json_query['result']['version']['minor'])


if xbmc_version:
    xbmc_version = float(xbmc_version)

else:
    xbmc_version = 1       


    
######if 'speedproxy' in PROXYBASE:
######    PROXYURL = 'http://www.speedproxy.co.uk/'
######    PROXYREF = 'http://www.speedproxy.co.uk/'
######    
######
######if 'england' in PROXYBASE:
######    PROXYURL = 'http://www.englandproxy.co.uk/'
######    PROXYREF = 'http://www.englandproxy.co.uk/'
  

def fixImage(image, resolution):
    image = image.replace('80x80',     resolution)
    #image = image.replace('192x108',   resolution)
    #image = image.replace('240x135',   resolution)
    #image = image.replace('304x171',   resolution)
    image = image.replace('304x304',   resolution)
    image = image.replace('672x378',   resolution)
    image = image.replace('832x468',   resolution)
    image = image.replace('1408x1408', resolution)
    return image


def CATEGORIES():
    addDir('Most Popular','http://www.bbc.co.uk/iplayer/group/popular?page=0',4,ART+'iplay.jpg','')
    addDir('By Channel','url',15,ART+'iplay.jpg','')
    addDir('iPlayer A to Z','url',3,ART+'iplay.jpg','')
    addDir('Categories','url',7,ART+'iplay.jpg','')
    addDir('My Searches','',11,ART+'search.png','')
    addDir('Live','url',2,ART+'iplay.jpg','')
    if SHOWLIVE == 'true':
        try:GetLive('dont')
        except:pass

    xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')

 
       
                                                                      
def char_range(c1, c2):
    
    for c in xrange(ord(c1), ord(c2)+1):
        yield chr(c)
 


def GetOnNow(html,name):
    r='%s-on-now.+?rcset="(.+?)".+?alt="(.+?)">.+?"schedule__sub-title">(.+?)<' % name
    link=html.split('aria-labelledby="')
    yo=[]
    for p in link:
        haha = p.split('"')[0]
        try:
            match=re.compile(r,re.DOTALL).findall(p)

                
            icon = match[0][0]
            
            title = match[0][1]
            time = match[0][2]
            if name in haha:
                
                yo.append([icon ,title,time])
        except:pass
      
    if yo:
        return yo[0][0],yo[0][1],yo[0][2]



    
def GetLive(url):
    html=OPEN_URL('https://www.bbc.co.uk/iplayer/guide',False)
    if url=='url':
        addDir('[COLOR red]Red Button[/COLOR]','url',13,'','')     
    extra =''
    channel_list = [
                    ('bbc_one_london','bbc_one_hd',                   'BBC One','choose','true'),
                    ('bbc_two_england','bbc_two_hd',                  'BBC Two','choose','true'),
                    ('bbc_four_hd','bbc_four_hd',                     'BBC Four','choose','true'),
                    ('cbbc_hd','cbbc_hd',                             'CBBC','choose','true'),
                    ('cbeebies_hd','cbeebies_hd',                     'CBeebies','choose','true'),
                    ('bbc_news24','bbc_news24',                       'BBC News Channel','choose','true'),
                    ('bbc_parliament','bbc_parliament',               'BBC Parliament','hls_tablet','true'),
                    ('bbc_alba','bbc_alba',                           'Alba','hls_tablet','true'),
                    ('s4c','s4cpbs',                                  'S4C','hls_tablet','true'),
                    ('bbc_one_hd','bbc_one_london',                   'BBC One London','hls_tablet','false'),
                    ('bbc_one_hd','bbc_one_scotland_hd',              'BBC One Scotland','hls_tablet','false'),
                    ('bbc_one_hd','bbc_one_northern_ireland_hd',      'BBC One Northern Ireland','hls_tablet','false'),
                    ('bbc_one_hd','bbc_one_wales_hd',                 'BBC One Wales','hls_tablet','false'),
                    ('bbc_two_hd','bbc_two_scotland',                 'BBC Two Scotland','hls_tablet','false'),
                    ('bbc_two_hd','bbc_two_northern_ireland_digital', 'BBC Two Northern Ireland','hls_tablet','false'),
                    ('bbc_two_hd','bbc_two_wales_digital',            'BBC Two Wales','hls_tablet','false'),
                    ('bbc_two_hd','bbc_two_england',                  'BBC Two England','hls_tablet','false'),
                    ('bbc_one_hd','bbc_one_cambridge',                'BBC One Cambridge','hls_tablet','false'),
                    ('bbc_one_hd','bbc_one_channel_islands',          'BBC One Channel Islands','hls_tablet','false'),
                    ('bbc_one_hd','bbc_one_east',                     'BBC One East','hls_tablet','false'),
                    ('bbc_one_hd','bbc_one_east_midlands',            'BBC One East Midlands','hls_tablet','false'),
                    ('bbc_one_hd','bbc_one_east_yorkshire',           'BBC One East Yorkshire','hls_tablet','false'),
                    ('bbc_one_hd','bbc_one_north_east',               'BBC One North East','hls_tablet','false'),
                    ('bbc_one_hd','bbc_one_north_west',               'BBC One North West','hls_tablet','false'),
                    ('bbc_one_hd','bbc_one_oxford',                   'BBC One Oxford','hls_tablet','false'),
                    ('bbc_one_hd','bbc_one_south',                    'BBC One South','hls_tablet','false'),
                    ('bbc_one_hd','bbc_one_south_east',               'BBC One South East','hls_tablet','false'),
                    ('bbc_one_hd','bbc_one_west',                     'BBC One West','hls_tablet','false'),
                    ('bbc_one_hd','bbc_one_west_midlands',            'BBC One West Midlands','hls_tablet','false'),
                    ('bbc_one_hd','bbc_one_yorks',                    'BBC One Yorks','hls_tablet','false')
                ]
    
    for id, img, name , device, Pass  in channel_list :
        if url=='dont':
            name = '[COLOR plum]On Now[/COLOR] - [COLOR green]%s[/COLOR]' % name
        if device == 'choose':
            if ADDON.getSetting('livehd')=='true':
                device='abr_hdtv'
            else:
                device='hls_mobile_wifi'
                
        URL='http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/%s/ak/%s.m3u8' % (device, img)
        iconimage = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.bbciplayerapp/img',img+'.png'))

        if Pass=='true':
            try:
                iconimage , extra , time= GetOnNow(html,id.replace('_hd',''))
                extra = ' - [COLOR orange]%s [/COLOR][COLOR royalblue](%s)[/COLOR]' % (extra,time)                            
            except:pass                                
            addDir(name + extra,URL,6,iconimage.replace('288x162','1280x720'),'')
        else:
            if url=='url':
                addDir(name,URL,6,iconimage.replace('288x162','1280x720'),'')

def ListRedButton():
    channel_list = [
        ('sport_stream_01', 'BBC Red Button 1','choose'),
        ('sport_stream_02', 'BBC Red Button 2','choose'),
        ('sport_stream_03', 'BBC Red Button 3','choose'),
        ('sport_stream_04', 'BBC Red Button 4','choose'),
        ('sport_stream_05', 'BBC Red Button 5','choose'),
        ('sport_stream_06', 'BBC Red Button 6','choose'),
        ('sport_stream_07', 'BBC Red Button 7','choose'),
        ('sport_stream_08', 'BBC Red Button 8','choose'),
        ('sport_stream_09', 'BBC Red Button 9','choose'),
        ('sport_stream_10', 'BBC Red Button 10','choose'),
        ('sport_stream_11', 'BBC Red Button 11','choose'),
        ('sport_stream_12', 'BBC Red Button 12','choose'),
        ('sport_stream_13', 'BBC Red Button 13','choose'),
        ('sport_stream_14', 'BBC Red Button 14','choose'),
        ('sport_stream_15', 'BBC Red Button 15','choose'),
        ('sport_stream_16', 'BBC Red Button 16','choose'),
        ('sport_stream_17', 'BBC Red Button 17','choose'),
        ('sport_stream_18', 'BBC Red Button 18','choose'),
        ('sport_stream_19', 'BBC Red Button 19','choose'),
        ('sport_stream_20', 'BBC Red Button 20','choose'),
        ('sport_stream_21', 'BBC Red Button 21','choose'),
        ('sport_stream_22', 'BBC Red Button 22','choose'),
        ('sport_stream_23', 'BBC Red Button 23','choose'),
        ('sport_stream_24', 'BBC Red Button 24','choose'),
    ]
    for id, name , device in channel_list:

        if device == 'choose':
            if ADDON.getSetting('livehd')=='true':
                device='abr_hdtv'
            else:
                device='hls_mobile_wifi'
        
        url='http://a.files.bbci.co.uk/media/live/manifesto/audio_video/webcast/hls/uk/%s/ak/%s.m3u8' % (device, id)
        addDir(name,url,6,'','')
        

def GetAtoZ(url):
    nameurl=[]
    urlurl=[]
    for name in char_range('A', 'Z'):
        nameurl.append(name)
        urlurl.append(name.lower())

    nameurl.append('0-9')
    urlurl.append('0-9'.lower())
            
    NEW_URL='http://www.bbc.co.uk/iplayer/a-z/%s'%urlurl[xbmcgui.Dialog().select('Select letter:', nameurl)]

    GetEpisodes(NEW_URL)
    

def GetByChannel(url):

    if not len(url)> 3:
        nameurl=[]
        urlurl=[]
        link=OPEN_URL('http://www.bbc.co.uk/iplayer')
        # <li class="scrollable-nav__item"><a href="/bbcone" class="lnk channels-nav__item"><span class="lnk__label"><span class="tvip-hide">BBC One</span><svg
        prematch  = re.findall('<ul class="scrollable-nav__track">(.+?)</ul>',link, flags=re.DOTALL)[0]
        addclose  = prematch+'<a href="/VOID/Close">VOID<span class="tvip-hide">Close</span>' ### remove and change belows findall back to prematch, just here to stop auto open last option on exit
        match     = re.compile('<a href="(.+?)".+?tvip-hide">(.+?)</span>').findall(addclose)
        for url , name in match:
            if not '{' in name:
                h = HTMLParser.HTMLParser()
                nameurl.append(h.unescape(name))
                urlurl.append(url+'/a-z')

        NEW_URL='http://www.bbc.co.uk%s?page=0'%urlurl[xbmcgui.Dialog().select('Please Select Category', nameurl)]
    else:
        NEW_URL = url

    if not 'Close' in NEW_URL:
        GetEpisodes(NEW_URL.replace('featured','a-z'))
    else:
        xbmcgui.Dialog().notification('Channels', 'Closed', xbmcgui.NOTIFICATION_INFO, 1000)
        CATEGORIES()
        
        return


def Genre(url):
    
    if not len(url)> 3:
        nameurl=[]
        urlurl=[]
        link=OPEN_URL('http://www.bbc.co.uk/iplayer')
        # <li class="scrollable-nav__item"><div><a href="/iplayer/categories/arts/featured" class="lnk categories-sub-nav__item typo typo--canary"><span class="lnk__label">Arts</span></a></div></li>
        prematch  = re.findall('<ul class="scrollable-nav__track">(.+?)</ul>',link, flags=re.DOTALL)[1]
        addclose  = prematch+'<a href="/iplayer/categories/Close"VOID<span class="lnk__label">Close</span>' ### remove and change belows findall back to prematch, just here to stop auto open last option on exit
        match     = re.compile('<a href="/iplayer/categories/(.+?)".+?<span class="lnk__label">(.+?)</span>').findall(addclose)
        for url , name in match:
            if not '{' in name:
                h = HTMLParser.HTMLParser()
                nameurl.append(h.unescape(name))
                urlurl.append('/iplayer/categories/'+url)
        
        NEW_URL='http://www.bbc.co.uk%s?sort=dateavailable&page=0'%urlurl[xbmcgui.Dialog().select('Please Select Category', nameurl)]
    else:
        NEW_URL = url

    if not 'Close' in NEW_URL:
        GetEpisodes(NEW_URL.replace('featured','a-z'))
    else:
        xbmcgui.Dialog().notification('Genre', 'Closed', xbmcgui.NOTIFICATION_INFO, 1000)
        CATEGORIES()
        
        return


def MySearch():
    addDir('[COLOR blue]Home[/COLOR]','',900,ART+'iplay.jpg','')
    addDir('Search','',9,ART+'iplay.jpg','')
    favs = ADDON.getSetting('favs').split(',')
    for title in favs:
        NEW_URL='http://www.bbc.co.uk/iplayer/search?q=%s' % title.replace(' ','%20')        
        addDir(title,NEW_URL,8,ART+'iplay.jpg','')
    

def Search(search_entered):
    favs = ADDON.getSetting('favs').split(',')
    if not search_entered:
        keyboard = xbmc.Keyboard('', 'Search iPlayer')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText()

    search_entered = search_entered.replace(',', '')

    if len(search_entered) == 0:
        return

    if not search_entered in favs:
        favs.append(search_entered)
        ADDON.setSetting('favs', ','.join(favs))

    search_entered = search_entered.replace(' ','%20')

    NEW_URL='http://www.bbc.co.uk/iplayer/search?q=%s' % search_entered

    GetEpisodes(NEW_URL)


def GetEpisodes(id, page=1):

    if not 'http' in id:
        url  = 'http://www.bbc.co.uk/iplayer/episodes/%s?page=%d' % (id, page)
        link = OPEN_URL(url)
        showlink=''

        # FIX fixes issue with shows that link to 'programmes' page instead of iplayer e.g. DRAMA-SOAP-CBBC-CBEEBIES
        if '"searchPlaceholderWrapperEnd"' in link:
            url  = 'http://www.bbc.co.uk/iplayer/episode/%s' % (id)
            showlink = OPEN_URL(url)

######     ########## OLD CODE NOW DOUBLED UP WITH ABOVE, REMOVE LATER, ALSO FIXES OTHERS
######        # CBBC AND CBEEBIES
######        if '"searchPlaceholderWrapperEnd"' in link:
######            url  = 'http://www.bbc.co.uk/iplayer/episode/%s' % (id)
######            showlink = OPEN_URL(url)

        if not 'episodes' in url:
            if ' href="/iplayer/episodes/' in showlink:
                NEW_IPID = re.compile(' href="/iplayer/episodes/(.+?)"').findall (showlink)[0]
                url = 'http://www.bbc.co.uk/iplayer/episodes/%s?page=%d' % (NEW_IPID, page)
                link = OPEN_URL(url)
            else:
                link = showlink ### only hear to prevent errors as shows with few episodes don't have 'all episodes' AKA 'view all' pages
        else:pass
        
    
    else:
        url= id
        if '?page' in id:
            page = id.split('?page=')[1]
            page = int(page)+1
            id = id.split('?')[0]
            url = id+'?page=%d' % page
        elif '&page' in id:
            page = id.split('&page=')[1]
            page = int(page)+1
            id = id.split('&')[0]
            url = id+'&page=%d' % page
         
        link = OPEN_URL(url)


    if '<li class="programme-episode-section__item' in link:   #### FIX for shows with very few episodes even once passed programmes to episode with no view all.
        html = link.split('<li class="programme-episode-')
    else:
        html = link.split('<li class="grid__item')
                
    for p in html:
        try:
            #IPID=p.split('"')[0]
            if 'all episodes' in p:
                amount = 3
                
            else:
                amount = 0

            URL=re.compile(' href="(.+?)"').findall (p)[amount]
            name=re.compile('skylark typo--bold">(.+?)<').findall (p)[0]
 
            try:iconimage=re.compile('srcSet="(.+?),').findall (p)[0]
            except:iconimage=''
            if ',' in iconimage:
                iconimage=iconeimage.split(',')[1]

            ### PLOT DETAILS AND INFO
            try:duration_skim=re.compile('content-item__label--with-separator">(.*?)<').findall (p)[0]
            except:duration_skim=''

            try:available_skim=re.compile('class="typo typo--bullfinch content-item__label">(.*?)<').findall (p)[0]
            except:available_skim=''
            
            try:ep_skim=re.compile('<div class="content-item__info__primary"><div class="content-item__description typo typo--bullfinch">(.*?)<').findall (p)[0]
            except:ep_skim=''
            
            ep_format=ep_skim.replace(': ',')' + ' \n')
            if ')' in ep_format:
                ep_format= '(' + ep_format
            episode= 'Episode:' + ' \n' + ep_format + ' \n' + ' \n'
            duration= ' \n' + ' \n' + 'Duration: (' + duration_skim + ')'
            available= ' \n' + ' \n'  + available_skim + ')'
            available=available.replace('Available for ','Available for: (').replace('Available until ','Available until: (').replace('Expires ','Expires: (')


            try:plot_skim=re.compile('<div class="content-item__info__secondary"><div class="content-item__description typo typo--bullfinch">(.+?)<').findall (p)[0]
            except:plot_skim=''

            plotformat=plot_skim.replace("&#x27;","'").replace("&amp;","&")
            plotfinal= 'Plot:' + ' \n' + plotformat

            if plot_skim=='':
                plotfinal= 'Plot: (Plot unknown)'               

            if ep_skim=='':
                episode= 'Episode: (Episode unknown)'
            
            # FIXES problem with single episodes listing first part of plot as primary info instead of episode
            if ep_skim in plotformat:
                episode= ''

            if duration_skim=='':
                duration= ' \n' + ' \n' +'Duration: (unknown)'

            if available_skim=='':
                available= ' \n' + ' \n' +'Available for: (unknown)'


            if ADDON.getSetting('kill.ep')=='true':
                episode= 'Episode: (DISABLED)' + ' \n' + ' \n'

            if ADDON.getSetting('kill.plot')=='true':
                plotfinal='Plot: (DISABLED)'

            if ADDON.getSetting('kill.plot')=='true' and ADDON.getSetting('kill.ep')=='false':
                episode= 'Episode:' + ' \n' + ep_format + ' \n' + ' \n'

            
            plot= episode + plotfinal + duration + available
            
            ## END OF PLOT DETAILS AND INFO
            
            if 'http://www.bbc.co.uk' not in URL:
                
                _URL_='http://www.bbc.co.uk%s' %URL
            else:
                _URL_ = URL
                ### BELOW IPID (doesn't work in some popular AtoZ as no ipid aka "episode/" but no "episodes/")
                ### should now work, cycles round through programme page then episode then view all if exist, or shos with very show episode fix above
            try:
                IPID= URL.split('episode/')[1].split('/')[0]

                if 'a-z' in id:
                    mode=4
                elif ADDON.getSetting('autoplay')=='true':
                    mode=14
                else:
                    mode=5
            except:
                IPID= URL.split('episodes/')[1].split('/')[0]
                _URL_ = IPID
                mode= 4
            ### BELOW CHANGES MODE FOR SHOWS WITH LOW EPISODES, SETS CONTEXT TO SAY 'other episodes' instead of 'all episdes' no other changes are made
            if 'section__item' in p:
                mode= 800
            else:pass
                
            addDir(name,_URL_,mode,iconimage.replace('464x261','832x468').replace('416x234','832x468').replace('304x171','832x468') ,plot,IPID)
        except:
            pass

######    page = page + 1    ## SETS PAGE FOR EPISODES VIEW        ### OLD CODE FOR PAGE UP, NOW USED ABOVE CODE BLOCK SAME AS CAT POP PAGES.
######    if '/iplayer/episodes/%s?page=%d' % (id, page) in link:
######        GetEpisodes(id, page=page)
        
    

    try:
        if 'episode' in url and '"Next Page">' in link and not 'search?' in url:
            if ADDON.getSetting('autosortorder') == 'false':
                ### BELOW IS SHOWN FOR EPISODES VIEW WITH MULTI-PAGE, MAKES SORT POSSIBLE WITHOUT AFFECTING OTHER LISTS
                addDir('[COLOR blue]>> More Episodes >>[/COLOR]',url,4,ART+'nextpage.jpg' ,'','')
                xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
                xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
            else:
                addDir('[COLOR blue]>> More Episodes >>[/COLOR]',url,4,ART+'nextpage.jpg' ,'','')                
            
        elif '"Next Page">' in link and not 'search?' in url:
            ### BELOW IS SHOWN FOR CATAGORIES VIEW
            addDir('[COLOR blue]>> Next Page >>[/COLOR]',url,4,ART+'nextpage.jpg' ,'','')
            
        else:
            if ADDON.getSetting('autosortorder') == 'false':
                ### BELOW IS SHOWN FOR EPISODES VIEW THAT DONT HAVE MULTI-PAGE, MAKES SORT POSSIBLE WITHOUT AFFECTING OTHER LISTS
                ### WITHOUT BELOW SERIES ORDER WOULD BE REVERSED, IF PLACED OUTSIDE OF IF WOULD PLACE 'NEXT PAGE' AT TOP OF CAT LIST
                xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
                xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
                xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)
            else:pass

            ### FULL LIST OF SORTMETHODS
######            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
######            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
######            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
######            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)
######            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)
######            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
######            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE)
######            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
######            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL_IGNORE_FOLDERS)
    except:
        pass
    
    setView('movies', 'episode-view')


def GetAutoPlayable(name,url,iconimage):
    if int(ADDON.getSetting('catchup'))==2:
            if xbmc_version <= 16.9:
                dialog = xbmcgui.Dialog()
                return dialog.ok("BBC iPlayer", 'DASH only works with Kodi Versions','higher than 17', '')

            
    if 'http://www.bbc.co.uk' not in url:
                
        url='http://www.bbc.co.uk%s' %url

    _NAME_=name
    if 'plugin.video.bbciplayerapp' in iconimage:

        vpid=url

    else:
        xbmc.log('GW> ' + str(url))    
        html = OPEN_URL(url)
        
      
        vpid=re.compile('"versions":\[\{"id":"(.+?)"').findall(html)[0]
                 ##ORIG '"versions":\[.+?"id":"(.+?)"
    



    URL=[]
    uniques=[]
    NEW_URL= "http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/iptv-all/vpid/%s" % vpid
    
######    if ADDON.getSetting('new_proxy')=='true':
######        NEW_URL= "http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/apple-ipad-hls/vpid/%s" % vpid
######        html = OPEN_URL(NEW_URL,True)
######
######        match=re.compile('application="(.+?)".+?String="(.+?)".+?identifier="(.+?)".+?protocol="(.+?)".+?server="(.+?)".+?supplier="(.+?)"').findall(html.replace('amp;',''))
######        
######        for app,auth , playpath ,protocol ,server,supplier in match:
######
######            port = '1935'
######            if protocol == 'rtmpt': port = 80
######
######            if 'bbcmedia' in server.lower():
######                url="%s://%s:%s/ app=%s?%s tcurl=%s://%s:%s/%s?%s playpath=%s" % (protocol,server,port,app,auth,protocol,server,port,app,auth,playpath)
######                res=playpath.split('secure_auth/')[1]
######                resolution=res.split('kbp')[0]
######                
######                URL.append([(eval(resolution)),url])
######                     
######
######
######    elif int(ADDON.getSetting('catchup'))==1:
######        
######        NEW_URL= "http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/pc/vpid/%s" % vpid
        
        
    html = OPEN_URL(NEW_URL,False)
    match=re.compile('application="(.+?)".+?String="(.+?)".+?identifier="(.+?)".+?protocol="(.+?)".+?server="(.+?)".+?supplier="(.+?)"').findall(html.replace('amp;',''))
    for app,auth , playpath ,protocol ,server,supplier in match:

        port = '1935'
        if protocol == 'rtmpt': port = 80
        if int(ADDON.getSetting('supplier'))==1: 
            if supplier == 'limelight':
                url="%s://%s:%s/ app=%s?%s tcurl=%s://%s:%s/%s?%s playpath=%s" % (protocol,server,port,app,auth,protocol,server,port,app,auth,playpath)
                res=playpath.split('secure_auth/')[1]
                resolution=res.split('kbps')[0]
                URL.append([(eval(resolution)),url])                
      
               
        if int(ADDON.getSetting('supplier'))==0:
            url="%s://%s:%s/%s?%s playpath=%s?%s" % (protocol,server,port,app,auth,playpath,auth)
            if supplier == 'akamai':
                res=playpath.split('secure/')[1]
                resolution=res.split('kbps')[0]
                URL.append([(eval(resolution)),url])

    else:
        html = OPEN_URL(NEW_URL,False)

        link=html.split('width="')
        for p in link:
            try:
                res=p.split('"')[0]
                match=re.compile('href="(.+?)".+?supplier="(.+?)".+?transferFormat="(.+?)"').findall(p)
            
                for url , supplier, Format in match:
                    url=url.replace('amp;','')
                    
                    Format = Format.lower()

                       
                    if int(ADDON.getSetting('catchup'))==2:
                        if 'dash' in Format.lower():

                            if xbmc_version >= 16.9:
                                if int(ADDON.getSetting('supplier'))==0:
                                    if 'akamai' in supplier.lower():
                                        
                                    
                                        URL.append([(eval(res)),url])
                                if int(ADDON.getSetting('supplier'))==1:
                                    if 'limelight' in supplier.lower():
                              
                                        URL.append([(eval(res)),url])
                                if int(ADDON.getSetting('supplier'))==2:
                                    if 'bidi' in supplier.lower():

                                        URL.append([(eval(res)),url])
                    else:
                        if Format == 'hls':
                            if int(ADDON.getSetting('supplier'))==0:
                                if 'akamai' in supplier.lower():
                                
                                    URL.append([(eval(res)),url])
                            if int(ADDON.getSetting('supplier'))==1:
                                if 'limelight' in supplier.lower():
                          
                                    URL.append([(eval(res)),url])
                            if int(ADDON.getSetting('supplier'))==2:
                                if 'bidi' in supplier.lower():

                                    URL.append([(eval(res)),url])
                                

            except:pass    
    URL=max(URL)[1]
   
    PLAY_STREAM(name,str(URL),iconimage)


def GetPlayable(name,url,iconimage):
    
    if 'http://www.bbc.co.uk' not in url:
                
        url='http://www.bbc.co.uk%s' %url
    _NAME_=name
    if 'plugin.video.bbciplayerapp' in iconimage:

        vpid=url

    else:    
        html = OPEN_URL(url)
      
        vpid=re.compile('"versions":\[.+?"id":"(.+?)"').findall(html)[0]
    


    uniques=[]
    NEW_URL= "http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/iptv-all/vpid/%s" % vpid
    
######    if ADDON.getSetting('new_proxy')=='true':
######        NEW_URL= "http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/apple-ipad-hls/vpid/%s" % vpid
######        html = OPEN_URL(NEW_URL,True)
######        match=re.compile('application="(.+?)".+?String="(.+?)".+?identifier="(.+?)".+?protocol="(.+?)".+?server="(.+?)".+?supplier="(.+?)"').findall(html.replace('amp;',''))
######        for app,auth , playpath ,protocol ,server,supplier in match:
######
######            port = '1935'
######            if protocol == 'rtmpt': port = 80
######            if supplier == 'limelight':
######                url="%s://%s:%s/ app=%s?%s tcurl=%s://%s:%s/%s?%s playpath=%s" % (protocol,server,port,app,auth,protocol,server,port,app,auth,playpath)
######                res=playpath.split('secure_auth/')[1]
######                
######            else:
######               url="%s://%s:%s/%s?%s playpath=%s?%s" % (protocol,server,port,app,auth,playpath,auth)
######               
######            if supplier == 'akamai':
######                res=playpath.split('secure/')[1]
######                
######            if supplier == 'level3':
######                res=playpath.split('mp4:')[1]
######                
######            resolution=res.split('kbps')[0]
######            if int(resolution) > 1400 :
######                TITLE='[COLOR green][%s kbps][/COLOR] - [COLOR white]RTMP %s[/COLOR] - %s'%(resolution, supplier.upper(),server.upper())
######            else:
######                TITLE='[COLOR red][%s kbps][/COLOR] - [COLOR white]RTMP %s[/COLOR] - %s'%(resolution, supplier.upper(),server.upper())
######            if not '.xml' in url:
######                addDir(TITLE + ' : ' + _NAME_,url,200,iconimage,'')
######        NEW_URL= "http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/iptv-all/vpid/%s" % vpid
######        html = OPEN_URL(NEW_URL,True)
######    else:
    html = OPEN_URL(NEW_URL,False)

    link=html.split('height="')
    for p in link:
        try:
            res=p.split('"')[0]
            match=re.compile('href="(.+?)".+?supplier="(.+?)".+?transferFormat="(.+?)"').findall(p)
        
            for url , supplier, Format in match:
                url=url.replace('amp;','')
                if 'akamai' in supplier:
                    supplier ='AKAMAI'
                elif 'limelight' in supplier:
                    supplier ='LIMELIGHT'
                elif 'bidi' in supplier:
                    supplier ='BIDI'
                else:
                    supplier ='UNKOWN'
                    
                Format = Format.lower()
                if int(res)>1000:
                    color='green'
                elif int(res)>700 and int(res)<1000:
                    color='orange'
                else:
                    color='red' 
                TITLE='[COLOR %s][%sP][/COLOR] - [COLOR white]%s[/COLOR] [COLOR royalblue]- %s [/COLOR]'%(color,res, supplier.upper(),Format.upper())

                if 'dash' in Format.lower():
                    if xbmc_version >= 16.9:
                        if not '.xml' in url:
                            addDir(TITLE + ' : ' + _NAME_,url,200,iconimage,'')
                else:
                    if not '.xml' in url:
                        addDir(TITLE + ' : ' + _NAME_,url,200,iconimage,'')
        except:pass
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)

def GetLivePlayable(name,url,iconimage):

        
    STREAM = url  

    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(STREAM)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

            

        #self.AddLiveLink( list, id.replace('_',' ').upper(), url, language = language.title(),host= 'BBC iPLAYER '+supplier,quality=quality_dict.get(res, 'NA'))       

 
def OPEN_URL(url,resolve=False):
 
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    
######    if ADDON.getSetting('new_proxy')=='false':
######        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
######        
######    else:
######        if resolve==True:
######            import base64
######            if 'england' in PROXYREF:
######                url=url.split('//')[1]
######                url=PROXYURL + url
######                headers = {'Referer':PROXYREF,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
######
######            else:
######                thedata={'data':url.split('//')[1]}
######
######                data = thedata
######
######                headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
######                        'Accept-Encoding':'gzip, deflate',
######                        'Accept-Language':'en-US,en;q=0.9',
######                        'Content-Type': 'application/x-www-form-urlencoded',
######                        'Pragma': 'no-cache',
######                        'Upgrade-Insecure-Requests': '1',
######                        'Host':'www.speedproxy.co.uk',
######                        'Origin':'http://www.speedproxy.co.uk',
######                        'Referer':'http://www.speedproxy.co.uk/',
######                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
######
######
######
######                grr = net.http_GET('http://www.speedproxy.co.uk',headers=headers).get_headers()
######                for k in grr:
######                    if 'token' in k:
######                        token = 'token='+k.split('token=')[1].split(';')[0]
######
######                headers['Cookie'] = token
######
######
######                link = net.http_POST('http://www.speedproxy.co.uk/?do=search',data,headers=headers).content
######                return link
                
              
            
        
    link = net.http_GET(url,headers).content
                                  
    
    
    return link
    
    
    
def PLAY_STREAM(name,url,iconimage):
    name = name.split(' : ', 1)[-1]

    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    if '.mpd' in url:
        liz.setProperty('inputstreamaddon', 'inputstream.adaptive')
        liz.setProperty('inputstream.adaptive.manifest_type', 'mpd')
    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    

def addDir(name,url,mode,iconimage,description,IPID=''):
        if not name =='':
             if not'search the bbc' in name.lower():
                try:
                    h = HTMLParser.HTMLParser()
                    name =h.unescape(name)
                except:pass

                try:
                    name = name.encode('ascii', 'ignore')
                except:
                    name = name.decode('utf-8').encode('ascii', 'ignore')


                u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)+"&IPID="+urllib.quote_plus(IPID)
                ok=True

                liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
                liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
                #liz.setArt({ 'thumb': iconimage, 'icon' : 'DefaultFolder.png' })
                liz.setProperty('Fanart_Image', fixImage(iconimage, '1280x720'))
                menu=[]
                if not IPID == '':
                    if mode == 800:
                        menu.append(('[COLOR orange]Show Other Episodes[/COLOR]','XBMC.Container.Update(%s?mode=4&url=%s)'% (sys.argv[0],IPID)))
                        liz.addContextMenuItems(items=menu, replaceItems=False)
                    else:
                        menu.append(('[COLOR orange]Show All Episodes[/COLOR]','XBMC.Container.Update(%s?mode=4&url=%s)'% (sys.argv[0],IPID)))
                        liz.addContextMenuItems(items=menu, replaceItems=False)
                if mode == 8:
                    menu.append(('[COLOR orange]Remove from history[/COLOR]','XBMC.Container.Update(%s?mode=12&name=%s)'% (sys.argv[0],name)))
                    liz.addContextMenuItems(items=menu, replaceItems=False)
                if mode == 9:
                    menu.append(('[COLOR orange]Clear Search history[/COLOR]','XBMC.Container.Update(%s?mode=12&name=%s)'% (sys.argv[0],'clearall')))
                    liz.addContextMenuItems(items=menu, replaceItems=False)
                if mode ==200 or mode ==6 or mode ==14 or mode ==800:
                    liz.setProperty("IsPlayable","true")
                    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
                else:
                    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
                return ok


def setView(content, viewType):
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
def get_params(path):
    params = {}
    path   = path.split('?', 1)[-1]
    pairs  = path.split('&')

    for pair in pairs:
        split = pair.split('=')
        if len(split) > 1:
            params[split[0]] = urllib.unquote_plus(split[1])

    return params
   
params      = get_params(sys.argv[2])            
url         = None
name        = None
mode        = None
iconimage   = None
description = None
IPID        = None

try:    url=params["url"]
except: pass

try:    name = params["name"]
except: pass

try:    iconimage = params["iconimage"]
except: pass

try:    mode = int(params["mode"])
except: pass

try:    description = params["description"]
except: pass

try:    IPID = params["IPID"]
except: pass    

# START OF MODES
       
if mode==1:
        
        GetMain(url)

elif mode==2:
        
        GetLive(url)        
        
elif mode==3:
        
        GetAtoZ(url)
     
elif mode==4:
        
        GetEpisodes(url)

elif mode==5:
        GetPlayable(name,url,iconimage)

elif mode==6:
        GetLivePlayable(name,url,iconimage)

elif mode==7:
        Genre(url)

elif mode==8: ## use this getepisodes for search results (adds clear history to context)
        GetEpisodes(url)

elif mode==9:
        Search(url)    

### MODE 10 was POPULAR()        

elif mode==11:
        MySearch()
        
elif mode == 12:
    favs = ADDON.getSetting('favs').split(",")

    try:
        if name=='clearall':
            ADDON.setSetting('favs', "")
        else:pass
    except:pass
    try:
        favs.remove(name)
        ADDON.setSetting('favs', ",".join(favs))
    except:pass
    MySearch()
    
elif mode==13:
        ListRedButton()

elif mode==14:
        GetAutoPlayable(name,url,iconimage)

elif mode==15:
    GetByChannel(url)
    
elif mode==200:

        PLAY_STREAM(name,url,iconimage)

elif mode==800:

    GetAutoPlayable(name,url,iconimage)

elif mode==900:
    CATEGORIES()
    
else:
    CATEGORIES()
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
