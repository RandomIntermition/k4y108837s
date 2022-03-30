# -*- coding: utf-8 -*-


from sys import argv

from six.moves.urllib_parse import parse_qsl


params = dict(parse_qsl(argv[2].replace('?','')))

action = params.get('action')
select = params.get('select')

url = params.get('url')
query = params.get('query')
id = params.get('id')
setting = params.get('setting')

source = params.get('source')
content = params.get('content')

image = params.get('image')
meta = params.get('meta')

imdb = params.get('imdb')
tmdb = params.get('tmdb')
tvdb = params.get('tvdb')

name = params.get('name')
title = params.get('title')
tvshowtitle = params.get('tvshowtitle')

season = params.get('season')
episode = params.get('episode')

year = params.get('year')
premiered = params.get('premiered')

windowedtrailer = params.get('windowedtrailer')
windowedtrailer = int(windowedtrailer) if windowedtrailer in ("0", "1") else 0


if action == None:
    from resources.lib.modules import cache
    from resources.lib.indexers import navigator
    cache.cache_version_check()
    navigator.navigator().root()


elif action == 'add_item':
    from resources.lib.modules import sources
    sources.sources().addItem(title)


elif action == 'add_view':
    from resources.lib.modules import views
    views.addView(content)


elif action == 'alter_sources':
    from resources.lib.modules import sources
    sources.sources().alterSources(url, meta)


elif action == 'artwork':
    from resources.lib.modules import control
    control.artwork()


elif action == 'auth_tmdb':
    from resources.lib.modules import tmdb_utils
    tmdb_utils.authTMDb()


elif action == 'auth_trakt':
    from resources.lib.modules import trakt
    trakt.authTrakt()


elif action == 'calendar':
    from resources.lib.indexers import episodes
    episodes.episodes().calendar(url)


elif action == 'calendars':
    from resources.lib.indexers import episodes
    episodes.episodes().calendars()


elif action == 'clean_settings':
    from resources.lib.indexers import navigator
    navigator.navigator().cleanSettings()


elif action == 'cleantools_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().cleantools()


elif action == 'cleantools_widget':
    from resources.lib.indexers import navigator
    navigator.navigator().cleantools_widget()


elif action == 'clear_all_cache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheAll()


elif action == 'clear_cache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCache()


elif action == 'clear_debuglog':
    from resources.lib.indexers import navigator
    navigator.navigator().clearDebugLog()


elif action == 'clear_meta_cache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheMeta()


elif action == 'clear_resolveurl_cache':
    from resources.lib.modules import control
    control.execute('RunPlugin(plugin://script.module.resolveurl/?mode=reset_cache)')


elif action == 'clear_search_cache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheSearch(select)


elif action == 'clear_sources':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheProviders()


elif action == 'color_choice':
    from resources.lib.modules import colorcode
    colorcode.colorChoice(params['setting'], params['query'])


elif action == 'devtools_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().devtools()


elif action == 'disable_all':
    from resources.lib.modules import sources
    sources.sources().disableAll()


elif action == 'download':
    import simplejson as json
    from resources.lib.modules import downloader
    from resources.lib.modules import sources
    downloader.download(name, image, sources.sources().sourcesResolve(json.loads(source)[0], True))


elif action == 'download_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().downloads()


elif action == 'enable_all':
    from resources.lib.modules import sources
    sources.sources().enableAll()


elif action == 'episode_widget':
    from resources.lib.indexers import episodes
    episodes.episodes().widget()


elif action == 'episodes':
    from resources.lib.indexers import episodes
    episodes.episodes().get(tvshowtitle, year, imdb, tmdb, meta, season, episode)


elif action == 'episodes_playcount':
    from resources.lib.modules import playcount
    playcount.episodes(imdb, tmdb, season, episode, query)


elif action == 'episodes_userlists':
    from resources.lib.indexers import episodes
    episodes.episodes().userlists()


elif action == 'library_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().library()


elif action == 'moreplugs_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().moreplugs()


elif action == 'movie_to_library':
    from resources.lib.modules import libtools
    libtools.libmovies().add(name, title, year, imdb, tmdb)


elif action == 'movies':
    from resources.lib.indexers import movies
    movies.movies().get(url)


elif action == 'movies_imdb_certificates':
    from resources.lib.indexers import movies
    movies.movies().imdb_certifications()


elif action == 'movies_imdb_decades':
    from resources.lib.indexers import movies
    movies.movies().imdb_decades()


elif action == 'movies_imdb_genres':
    from resources.lib.indexers import movies
    movies.movies().imdb_genres()


elif action == 'movies_imdb_hella_lifetime_hallmark':
    from resources.lib.indexers import movies
    movies.movies().hellaLifeTimeHallMark()


elif action == 'movies_imdb_keywords':
    from resources.lib.indexers import movies
    movies.movies().imdb_keywords()


elif action == 'movies_imdb_languages':
    from resources.lib.indexers import movies
    movies.movies().imdb_languages()


elif action == 'movies_imdb_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().movieIMDb()


elif action == 'movies_imdb_persons':
    from resources.lib.indexers import movies
    movies.movies().search_imdb_persons(url)


elif action == 'movies_imdb_userlists':
    from resources.lib.indexers import movies
    movies.movies().imdbUserLists()


elif action == 'movies_imdb_userlists_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().imdbMovieLists()


elif action == 'movies_imdb_years':
    from resources.lib.indexers import movies
    movies.movies().imdb_years()


elif action == 'movies_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().movies()


elif action == 'movies_playcount':
    from resources.lib.modules import playcount
    playcount.movies(imdb, query)


elif action == 'movies_tmdb_certifications':
    from resources.lib.indexers import movies
    movies.movies().tmdb_certifications()


elif action == 'movies_tmdb_collections':
    from resources.lib.indexers import movies
    movies.movies().tmdb_collections(url)


elif action == 'movies_tmdb_collections_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().tmdbMovieCollections()


elif action == 'movies_tmdb_years':
    from resources.lib.indexers import movies
    movies.movies().tmdb_years()


elif action == 'movies_tmdb_decades':
    from resources.lib.indexers import movies
    movies.movies().tmdb_decades()


elif action == 'movies_tmdb_genres':
    from resources.lib.indexers import movies
    movies.movies().tmdb_genres()


elif action == 'movies_tmdb_languages':
    from resources.lib.indexers import movies
    movies.movies().tmdb_languages()


elif action == 'movies_tmdb_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().movieTMDb()


elif action == 'movies_tmdb_popular_companies':
    from resources.lib.indexers import movies
    movies.movies().tmdb_popular_companies()


elif action == 'movies_tmdb_popular_keywords':
    from resources.lib.indexers import movies
    movies.movies().tmdb_popular_keywords()


elif action == 'movies_tmdb_popular_people':
    from resources.lib.indexers import movies
    movies.movies().tmdb_popular_people()


elif action == 'movies_search':
    from resources.lib.indexers import movies
    movies.movies().search_term_menu(select)


elif action == 'movies_searchterm':
    from resources.lib.indexers import movies
    movies.movies().search_term(select, name)


elif action == 'movies_tmdb_userlists':
    from resources.lib.indexers import movies
    movies.movies().tmdb_userlists_list(url)


elif action == 'movies_tmdb_userlists_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().tmdbMovieLists()


elif action == 'movies_to_library':
    from resources.lib.modules import libtools
    libtools.libmovies().range(url)


elif action == 'movies_to_library_silent':
    from resources.lib.modules import libtools
    libtools.libmovies().silent(url)


elif action == 'movies_trakt_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().movieTrakt()


elif action == 'movies_trakt_moviemosts':
    from resources.lib.indexers import navigator
    navigator.navigator().movieMosts()


elif action == 'movies_userlists':
    from resources.lib.indexers import movies
    movies.movies().userlists()


elif action == 'my_imdb_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().myimdb()


elif action == 'my_imdb_movies_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().myimdbmovies()


elif action == 'my_imdb_tvshows_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().myimdbtvshows()


elif action == 'my_tmdb_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().mytmdb()


elif action == 'my_tmdb_movies_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().mytmdbmovies()


elif action == 'my_tmdb_tvshows_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().mytmdbtvshows()


elif action == 'my_trakt_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().mytrakt()


elif action == 'my_trakt_movies_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().mytraktmovies()


elif action == 'my_trakt_tvshows_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().mytrakttvshows()


elif action == 'my_userlists_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().myuserlists()


elif action == 'mylists_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().mylists()


elif action == 'open_resolveurl_settings':
    import resolveurl
    resolveurl.display_settings()


elif action == 'open_settings':
    from resources.lib.modules import control
    control.openSettings(query, id)


elif action == 'play':
    from resources.lib.modules import sources
    sources.sources().play(title, year, imdb, tmdb, season, episode, tvshowtitle, premiered, meta, select)


elif action == 'play_item':
    from resources.lib.modules import sources
    sources.sources().playItem(title, source)


elif action == 'queue_item':
    from resources.lib.modules import control
    control.queueItem()


elif action == 'search_movies_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().search_movies()


elif action == 'search_tvshows_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().search_tvshows()


elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tmdb, meta)


elif action == 'service':
    from resources.lib.modules import libtools
    libtools.libepisodes().service()


elif action == 'tools_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().tools()


elif action == 'tmdb_manager':
    from resources.lib.modules import tmdb_utils
    tmdb_utils.manager(name, imdb, tmdb, content)


elif action == 'trakt_manager':
    from resources.lib.modules import trakt
    trakt.manager(name, imdb, tmdb, content)


elif action == 'tvshow_to_library':
    from resources.lib.modules import libtools
    libtools.libtvshows().add(tvshowtitle, year, imdb, tmdb)


elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)


elif action == 'tvshows_imdb_certificates':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().imdb_certifications()


elif action == 'tvshows_imdb_decades':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().imdb_decades()


elif action == 'tvshows_imdb_genres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().imdb_genres()


elif action == 'tvshows_imdb_keywords':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().imdb_keywords()


elif action == 'tvshows_imdb_languages':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().imdb_languages()


elif action == 'tvshows_imdb_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().tvIMDb()


elif action == 'tvshows_imdb_persons':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_imdb_persons(url)


elif action == 'tvshows_imdb_userlists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().imdbUserLists()


elif action == 'tvshows_imdb_userlists_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().imdbShowLists()


elif action == 'tvshows_imdb_years':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().imdb_years()


elif action == 'tvshows_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows()


elif action == 'tvshows_tvmaze_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().tvTVmaze()


elif action == 'tvshows_playcount':
    from resources.lib.modules import playcount
    playcount.tvshows(name, imdb, tmdb, season, query)


elif action == 'tvshows_tmdb_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().tvTMDb()


elif action == 'tvshows_tmdb_networks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().tmdb_networks()


elif action == 'tvshows_tmdb_genres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().tmdb_genres()


elif action == 'tvshows_tmdb_languages':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().tmdb_languages()


elif action == 'tvshows_tmdb_years':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().tmdb_years()


elif action == 'tvshows_tmdb_decades':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().tmdb_decades()


elif action == 'tvshows_tmdb_popular_companies':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().tmdb_popular_companies()


elif action == 'tvshows_tmdb_popular_keywords':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().tmdb_popular_keywords()


elif action == 'tvshows_tmdb_popular_people':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().tmdb_popular_people()


elif action == 'tvshows_search':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_term_menu(select)


elif action == 'tvshows_searchterm':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_term(select, name)


elif action == 'tvshows_tmdb_userlists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().tmdbTvLists()


elif action == 'tvshows_tmdb_userlists_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().tmdbShowLists()


elif action == 'tvshows_to_library':
    from resources.lib.modules import libtools
    libtools.libtvshows().range(url)


elif action == 'tvshows_to_library_silent':
    from resources.lib.modules import libtools
    libtools.libtvshows().silent(url)


elif action == 'tvshows_trakt_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().tvTrakt()


elif action == 'tvshows_trakt_showmosts':
    from resources.lib.indexers import navigator
    navigator.navigator().showMosts()


elif action == 'tvshows_tvmaze_networks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().tvmaze_networks()


elif action == 'tvshows_tvmaze_webchannels':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().webchannels()


elif action == 'tvshows_userlists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().userlists()


elif action == 'update_library':
    from resources.lib.modules import libtools
    libtools.libepisodes().update(query)


elif action == 'view_changelog':
    from resources.lib.modules import log_utils
    log_utils.changelog()


elif action == 'view_debuglog':
    from resources.lib.modules import log_utils
    log_utils.view_log()


elif action == 'views_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().views()


elif action == 'yt_trailer':
    from resources.lib.modules import control, trailer
    if not control.condVisibility('System.HasAddon(plugin.video.youtube)'):
        control.installAddon('plugin.video.youtube')
    trailer.YT_trailer().play(name, url, tmdb, imdb, season, episode, windowedtrailer)


elif action == 'tmdb_trailer':
    from resources.lib.modules import control, trailer
    if not control.condVisibility('System.HasAddon(plugin.video.youtube)'):
        control.installAddon('plugin.video.youtube')
    trailer.TMDb_trailer().play(tmdb, imdb, season, episode, windowedtrailer)


elif action == 'imdb_trailer':
    from resources.lib.modules import control, trailer
    if not control.condVisibility('System.HasAddon(plugin.video.youtube)'):
        control.installAddon('plugin.video.youtube')
    trailer.IMDb_trailer().play(imdb, name, tmdb, season, episode, windowedtrailer)


elif action == 'sky_channels_menu':
    from resources.lib.indexers.plugins import channels
    channels.channels().get()


elif action == 'nightride_streamsafe_menu':
    from resources.lib.indexers.plugins import music
    music.nightride().streamsafe()


elif action == 'nightride_stations_menu':
    from resources.lib.indexers.plugins import music
    music.nightride().stations()


elif action == 'music_play':
    from resources.lib.indexers.plugins import music
    music.play(url)


elif action == 'watchonline_menu':
    from resources.lib.indexers.plugins import watchonline
    watchonline.scraper().root()


elif action == 'watchonline_scrape_seasons':
    from resources.lib.indexers.plugins import watchonline
    watchonline.scraper().scrape_seasons(url)


elif action == 'watchonline_scrape_episodes':
    from resources.lib.indexers.plugins import watchonline
    watchonline.scraper().scrape_episodes(url)


elif action == 'watchonline_scrape_source':
    from resources.lib.indexers.plugins import watchonline
    watchonline.scraper().scrape_source(url)


elif action == 'watchonline_play':
    from resources.lib.indexers.plugins import watchonline
    watchonline.play(url)


elif action == 'installs_menu':
    from resources.lib.indexers import navigator
    navigator.navigator().installsmenu()


elif action == 'installAddon':
    from resources.lib.modules import control
    control.installAddon(id)


