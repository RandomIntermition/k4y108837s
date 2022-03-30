# -*- coding: utf-8 -*-

import re
import sys
import xbmc
import requests
import resolveurl

from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils
from resources.lib.modules import scrape_sources


class scraper:
    def __init__(self):
        self.list = []
        self.sites = [
            {'title': 'Watch 30 Rock', 'url': 'https://watch30rockonline.com/seasons/', 'image': 'https://i.ibb.co/wK9R4KC/30-rock.jpg'},
            {'title': 'Watch According To Jim', 'url': 'https://watchaccordingtojimonline.com/seasons/', 'image': 'https://i.ibb.co/TtSg6Zb/jim.png'},
            {'title': 'Watch Archer', 'url': 'https://watcharcheronline.cc/seasons/', 'image': 'https://i.ibb.co/D937Lsc/archer.jpg'},
            {'title': 'Watch Bates Motel', 'url': 'https://watchbatesmotelonline.com/seasons/', 'image': 'https://i.ibb.co/gR8bQmV/batesmotel.png'},
            {'title': 'Watch Baywatch', 'url': 'https://watchbaywatchonline.com/seasons/', 'image': 'https://i.ibb.co/7QRBzQB/baywatch.png'},
            {'title': 'Watch Bojack Horseman', 'url': 'https://watchbojackhorseman.online/seasons/', 'image': 'https://i.ibb.co/0yGqSqJ/bojack-horseman.jpg'},
            {'title': 'Watch Bones', 'url': 'https://watchbonesonline.com/seasons/', 'image': 'https://i.ibb.co/w7dQKw7/bones.jpg'},
            {'title': 'Watch Californication', 'url': 'https://watchcalifornicationonline.com/seasons/', 'image': 'https://i.ibb.co/pPPg4WC/californication.jpg'},
            {'title': 'Watch Castle', 'url': 'https://watchcastleonline.com/seasons/', 'image': 'https://i.ibb.co/2P6C7cH/castle.jpg'},
            {'title': 'Watch Charmed', 'url': 'https://watchcharmedonline.com/seasons/', 'image': 'https://i.ibb.co/FwX6kVF/charmed.jpg'},
            {'title': 'Watch Cheers', 'url': 'https://watchcheersonline.com/seasons/', 'image': 'https://i.ibb.co/kgqJz0s/cheers.jpg'},
            {'title': 'Watch Curb Your Enthusiasm', 'url': 'https://watchcurbyourenthusiasm.com/seasons/', 'image': 'https://i.ibb.co/Smvg51B/curb-your-enthusiasm.jpg'},
            {'title': 'Watch Desperate Housewives', 'url': 'https://watchdesperatehousewives.com/seasons/', 'image': 'https://i.ibb.co/LZxbJ2V/desperate-housewives.jpg'},
            {'title': 'Watch Doctor Who', 'url': 'https://watchdoctorwhoonline.com/season/', 'image': 'https://i.ibb.co/Wp0fD9D/doctor-who.jpg'},
            {'title': 'Watch Downton Abbey', 'url': 'https://watchdowntonabbeyonline.com/seasons/', 'image': 'https://i.ibb.co/n0DK7Ff/downton-abbey.jpg'},
            {'title': 'Watch Elementary', 'url': 'https://watchelementaryonline.com/seasons/', 'image': 'https://i.ibb.co/xDxx87M/elementary.jpg'},
            {'title': 'Watch ER', 'url': 'https://watcheronline.net/seasons/', 'image': 'https://i.ibb.co/vxm1YZ7/er.jpg'},
            {'title': 'Watch Everybody Loves Raymond', 'url': 'https://watcheverybodylovesraymond.com/seasons/', 'image': 'https://i.ibb.co/JrnbHKG/everybody-loves-raymond.jpg'},
            {'title': 'Watch Fugget About It', 'url': 'https://watchfuggetaboutit.online/seasons/', 'image': 'https://i.ibb.co/Sx2CVt6/fugget-about-it.jpg'},
            {'title': 'Watch Gilmore Girls', 'url': 'https://watchgilmoregirlsonline.com/seasons/', 'image': 'https://i.ibb.co/wdKMLgX/gilmoregirls.png'},
            {'title': 'Watch Glee', 'url': 'https://watchgleeonline.com/seasons/', 'image': 'https://i.ibb.co/sCxsFHn/glee.jpg'},
            {'title': 'Watch Gossip Girl', 'url': 'https://watchgossipgirlonline.net/seasons/', 'image': 'https://i.ibb.co/F5Z8RGQ/gossip-girl.jpg'},
            {'title': 'Watch Greek', 'url': 'https://watchgreekonline.com/seasons/', 'image': 'https://i.ibb.co/x23gLyG/greek.png'},
            {'title': 'Watch Greys Anatomy', 'url': 'https://watchgreysanatomy.online/seasons/', 'image': 'https://i.ibb.co/8rBrScY/greysanatomy.jpg'},
            {'title': 'Watch Hawaii Five0', 'url': 'https://watchhawaiifive0online.com/seasons/', 'image': 'https://i.ibb.co/wSNnyj9/hawaii-five-0.png'},
            {'title': 'Watch Heroes', 'url': 'https://watchheroes.online/seasons/', 'image': 'https://i.ibb.co/fNYZfSm/heroes.jpg'},
            {'title': 'Watch Hogans Heroes', 'url': 'https://watchhogansheroes.online/seasons/', 'image': 'https://i.ibb.co/F7k1hcC/hogan-s-heroes.jpg'},
            {'title': 'Watch House', 'url': 'https://watchhouseonline.net/season_free/', 'image': 'https://i.ibb.co/KsR0LvV/house.jpg'},
            {'title': 'Watch How I Met Your Mother', 'url': 'https://watchhowimetyourmother.online/seasons/', 'image': 'https://i.ibb.co/0VR2Vvg/how-i-met-your-mother.jpg'},
            {'title': 'Watch Impractical Jokers', 'url': 'https://watchimpracticaljokers.online/seasons/', 'image': 'https://i.ibb.co/tc4dWX8/impractical-jokers.jpg'},
            {'title': 'Watch Lost', 'url': 'https://watchlostonline.net/seasons/', 'image': 'https://i.ibb.co/jb8fGxd/lost.jpg'},
            {'title': 'Watch Malcolm In The Middle', 'url': 'https://watchmalcolminthemiddle.com/seasons/', 'image': 'https://i.ibb.co/GPBZ2gr/malcolm-in-the-middle.jpg'},
            {'title': 'Watch Mash', 'url': 'https://watchmash.online/seasons/', 'image': 'https://i.ibb.co/R9GKrT5/mash.jpg'},
            {'title': 'Watch Monk', 'url': 'https://watchmonkonline.com/seasons/', 'image': 'https://i.ibb.co/g6gWxd2/monk.jpg'},
            {'title': 'Watch My Name Is Earl', 'url': 'https://watchmynameisearl.com/seasons/', 'image': 'https://i.ibb.co/RH4mTky/my-name-is-earl.jpg'},
            {'title': 'Watch New Girl', 'url': 'https://watchnewgirlonline.net/seasons/', 'image': 'https://i.ibb.co/dQTtHy9/new-girl.jpg'},
            {'title': 'Watch Once Upon A Time', 'url': 'https://watchonceuponatimeonline.com/seasons/', 'image': 'https://i.ibb.co/WBLdkMh/once-upon-a-time.jpg'},
            {'title': 'Watch One Tree Hill', 'url': 'https://watchonetreehillonline.com/season/', 'image': 'https://i.ibb.co/z5Df1rQ/one-tree-hill.jpg'},
            {'title': 'Watch Only Fools And Horses', 'url': 'https://watchonlyfoolsandhorses.com/seasons/', 'image': 'https://i.ibb.co/XsVkFBP/only-fools-and-horses.jpg'},
            {'title': 'Watch Parks And Recreation', 'url': 'https://watchparksandrecreation.net/season/', 'image': 'https://i.ibb.co/Qc36dhv/parks-and-recreation.jpg'},
            {'title': 'Watch Pretty Little Liars', 'url': 'https://watchprettylittleliarsonline.com/seasons/', 'image': 'https://i.ibb.co/r7p5YtS/pretty-little-liars.jpg'},
            {'title': 'Watch Psych', 'url': 'https://watchpsychonline.net/seasons/', 'image': 'https://i.ibb.co/kDRzvTp/psych.jpg'},
            {'title': 'Watch Roseanne', 'url': 'https://watchroseanneonline.com/seasons/', 'image': 'https://i.ibb.co/zJ57DYd/roseanne.png'},
            {'title': 'Watch Rules Of Engagement', 'url': 'https://watchrulesofengagementonline.com/seasons/', 'image': 'https://i.ibb.co/PxPRcCh/rules-of-engagement.jpg'},
            {'title': 'Watch Scrubs', 'url': 'https://watchscrubsonline.com/seasons/', 'image': 'https://i.ibb.co/0Gg15r6/scrubs.jpg'},
            {'title': 'Watch Seinfeld', 'url': 'https://watchseinfeld.com/season/', 'image': 'https://i.ibb.co/Dw2PbP9/seinfeld.jpg'},
            {'title': 'Watch Sex And The City', 'url': 'https://watchsexandthecity.com/seasons/', 'image': 'https://i.ibb.co/6NQsLPP/sex-and-the-city.jpg'},
            {'title': 'Watch Southpark', 'url': 'https://watchsouthpark.tv/seasons/', 'image': 'https://i.ibb.co/bRb32GK/south-park.jpg'},
            {'title': 'Watch Spongebob Squarepants', 'url': 'https://watchspongebobsquarepantsonline.com/seasons/', 'image': 'https://i.ibb.co/xzvM2rN/spongebob.png'},
            {'title': 'Watch Suits', 'url': 'https://watchsuitsonline.net/seasons/', 'image': 'https://i.ibb.co/pdPh3Wx/suits.jpg'},
            {'title': 'Watch Teenwolf', 'url': 'https://watchteenwolfonline.net/seasons/', 'image': 'https://i.ibb.co/b2rx3p7/teen-wolf.jpg'},
            {'title': 'Watch That 70s Show', 'url': 'https://watchthat70show.net/seasons/', 'image': 'https://i.imgur.com/vCiYiXr.png'},
            {'title': 'Watch The 100', 'url': 'https://watchthe100online.com/seasons/', 'image': 'https://i.ibb.co/W0pPnmh/the100.png'},
            {'title': 'Watch The Big Bang Theory', 'url': 'https://watchthebigbangtheory.com/seasons/', 'image': 'https://i.ibb.co/GpDpQt8/the-big-bang-theory.jpg'},
            {'title': 'Watch The Flintstones', 'url': 'https://watchtheflintstones.online/seasons/', 'image': 'https://i.ibb.co/NCxzsYk/the-flintstones.jpg'},
            {'title': 'Watch The Fresh Prince Of Bel-Air', 'url': 'https://watchthefreshprinceofbel-air.com/seasons/', 'image': 'https://i.ibb.co/Z23xp5s/the-fresh-prince-of-bel-air.jpg'},
            {'title': 'Watch The King Of Queens', 'url': 'https://watchthekingofqueens.com/seasons/', 'image': 'https://i.ibb.co/2q5FV6t/the-king-of-queens.jpg'},
            {'title': 'Watch The Middle', 'url': 'https://watchthemiddleonline.com/seasons/', 'image': 'https://i.ibb.co/wcS0Gmf/the-middle.jpg'},
            {'title': 'Watch The Office', 'url': 'https://watchtheofficetv.com/season-lists/', 'image': 'https://i.ibb.co/ZJ2cfHX/the-office.jpg'},
            {'title': 'Watch The Ricky Gervais Show', 'url': 'https://watchtherickygervaisshow.online/seasons/', 'image': 'https://i.ibb.co/4V5d3Yv/the-ricky-gervais-show.jpg'},
            {'title': 'Watch The Vampire Diaries', 'url': 'https://watchthevampirediaries.com/seasons/', 'image': 'https://i.ibb.co/HFBhT5x/the-vampire-diaries.jpg'},
            {'title': 'Watch Two And A Half Men', 'url': 'https://watchtwoandahalfmenonline.com/season/', 'image': 'https://i.ibb.co/5h2RWPJ/two-and-a-half-men.jpg'},
            {'title': 'Watch Weeds', 'url': 'https://watchweedsonline.com/seasons/', 'image': 'https://i.ibb.co/d0fRd1B/weeds.png'}
        ]


    def root(self):
        try:
            for i in self.sites:
                self.list.append({'title': i['title'], 'url': i['url'], 'image': i['image'], 'action': 'watchonline_scrape_seasons'})
            addDirectory(self.list)
            return self.list
        except:
            log_utils.log('root', 1)
            return self.list


    def scrape_seasons(self, url):
        try:
            html = client.scrapePage(url).text
            if '/page/2/' in html:
                page2 = url + 'page/2/'
                html += client.scrapePage(page2).text
            if '/page/3/' in html:
                page3 = url + 'page/3/'
                html += client.scrapePage(page3).text
            r = client.parseDOM(html, 'article', attrs={'class': 'item se seasons'})
            for i in r:
                link = client.parseDOM(i, 'a', ret='href')[0]
                title = client.parseDOM(i, 'img', ret='alt')[0]
                label = client.replaceHTMLCodes(title)
                try:
                    art = client.parseDOM(i, 'img', ret='data-src')[0]
                except:
                    art = client.parseDOM(i, 'img', ret='src')[0]
                self.list.append({'title': label, 'url': link, 'image': art, 'action': 'watchonline_scrape_episodes'})
            addDirectory(self.list)
            return self.list
        except:
            log_utils.log('scrape_seasons', 1)
            return self.list


    def scrape_episodes(self, url):
        try:
            html = client.scrapePage(url).text
            if '/page/2/' in html:
                page2 = re.findall('href="(.+?/page/2/)"', html)[0]
                html += client.scrapePage(page2).text
            if '/page/3/' in html:
                page3 = re.findall('href="(.+?/page/3/)"', html)[0]
                html += client.scrapePage(page3).text
            r = client.parseDOM(html, 'li', attrs={'class': 'mark-.+?'})
            for i in r:
                link = client.parseDOM(i, 'a', ret='href')[0]
                title = client.parseDOM(i, 'a')[0]
                info = re.findall('/(?:episodes|stream|stream-free|episode-lists)/(?:watch-|)([A-Za-z0-9-]+)', link)[0]
                label = '%s - %s' % (info, title)
                label = client.replaceHTMLCodes(label)
                try:
                    art = client.parseDOM(i, 'img', ret='data-src')[0]
                except:
                    art = client.parseDOM(i, 'img', ret='src')[0]
                self.list.append({'title': label, 'url': link, 'image': art, 'action': 'watchonline_scrape_source'})
            addDirectory(self.list)
            return self.list
        except:
            log_utils.log('scrape_episodes', 1)
            return self.list


    def scrape_source(self, url):
        try:
            html = client.scrapePage(url).text
            domain = source_utils.get_host(url)
            session = requests.Session()
            customheaders = {
                'Host': domain,
                'Accept': '*/*',
                'Origin': 'https://%s' % domain,
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': client.UserAgent,
                'Referer': url,
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            post_link = 'https://%s/wp-admin/admin-ajax.php' % domain
            results = re.compile("data-type='(.+?)' data-post='(.+?)' data-nume='(\d+)'>", re.DOTALL).findall(html)
            for data_type, data_post, data_nume in results:
                payload = {'action': 'doo_player_ajax', 'post': data_post, 'nume': data_nume, 'type': data_type}
                r = session.post(post_link, headers=customheaders, data=payload)
                i = r.json()
                if not i['type'] == 'iframe':
                    continue
                p = i['embed_url'].replace('\\', '')
                link = scrape_sources.prepare_link(p)
                host = source_utils.get_host(link)
                self.list.append({'title': host, 'url': link, 'image': None, 'action': 'watchonline_play'})
            if self.list == []:
                control.infoDialog('Error : No Stream Available.', sound=False, icon='INFO')
            addDirectory(self.list)
            return self.list
        except:
            log_utils.log('scrape_source', 1)
            return self.list


def play(url):
    try:
        resolved = resolveurl.resolve(url)
        if resolved:
            url = resolved
        player = xbmc.Player()
        return player.play(url)
    except:
        log_utils.log('play', 1)
        return


def addDirectory(items, queue=False, isFolder=True):
    if items == None or len(items) == 0:
        control.idle()
    sysaddon = sys.argv[0]
    syshandle = int(sys.argv[1])
    addonFanart = control.addonFanart()
    for i in items:
        try:
            url = '%s?action=%s&url=%s' % (sysaddon, i['action'], i['url'])
            title = i['title']
            thumb = i['image'] or 'DefaultVideo.png'
            item = control.item(label=title)
            item.setProperty('IsPlayable', 'true')
            item.setArt({'icon': thumb, 'thumb': thumb, 'fanart': addonFanart})
            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
        except Exception:
            log_utils.log('addDirectory', 1)
            pass
    control.content(syshandle, 'addons')
    control.directory(syshandle, cacheToDisc=True)


