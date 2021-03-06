# -*- coding: utf-8 -*-
# Copyright: (c) 2018, SylvainCecchetto
# GNU General Public License v2.0+ (see LICENSE.txt or https://www.gnu.org/licenses/gpl-2.0.txt)

# This file is part of Catch-up TV & More

from __future__ import unicode_literals
import json
import re

from codequick import Listitem, Resolver, Route
import urlquick

from resources.lib import resolver_proxy
from resources.lib.menu_utils import item_post_treatment


# TO DO

# Live
URL_LIVE_JSON = 'https://player.api.stv.tv/v1/streams/%s/'
# channel name

URL_PROGRAMS_JSON = 'https://player.api.stv.tv/v1/programmes/?limit=300&orderBy=name'

URL_VIDEOS_JSON = 'https://player.api.stv.tv/v1/episodes'
# guidProgramm

URL_BRIGHTCOVE_DATAS = 'https://player.stv.tv/player-web/players/vod/bundle.js'


@Route.register
def list_programs(plugin, item_id, **kwargs):
    """
    Build programs listing
    - Les feux de l'amour
    - ...
    """
    resp = urlquick.get(URL_PROGRAMS_JSON)
    json_parser = json.loads(resp.text)

    for program_datas in json_parser["results"]:
        program_title = program_datas["name"]
        program_image = program_datas["images"][0]["_filepath"]
        program_plot = program_datas["longDescription"]
        program_guid = program_datas["guid"]

        item = Listitem()
        item.label = program_title
        item.art['thumb'] = item.art['landscape'] = program_image
        item.info['plot'] = program_plot
        item.set_callback(list_videos,
                          item_id=item_id,
                          program_guid=program_guid)
        item_post_treatment(item)
        yield item


@Route.register
def list_videos(plugin, item_id, program_guid, **kwargs):

    payload = {'programme_guid': program_guid, 'limit': '300'}
    resp = urlquick.get(URL_VIDEOS_JSON, params=payload)
    json_parser = json.loads(resp.text)

    for video_datas in json_parser["results"]:
        video_title = video_datas["programme"]["name"] + ' - ' + video_datas[
            "title"]
        video_image = video_datas["images"][0]["_filepath"]
        video_plot = video_datas["summary"]
        video_duration_datas = video_datas["video"]["_duration"].split(' ')
        if (len(video_duration_datas) > 2):
            video_duration = 3600 * int(video_duration_datas[0]) + 60 * int(video_duration_datas[2])
        else:
            video_duration = 60 * int(video_duration_datas[0])
        video_id = video_datas["video"]["id"]

        item = Listitem()
        item.label = video_title
        item.art['thumb'] = item.art['landscape'] = video_image
        item.info['plot'] = video_plot
        item.info['duration'] = video_duration

        if video_datas["schedule"] is not None:
            date_value = video_datas["schedule"]["startTime"].split('T')[0]
            item.info.date(date_value, '%Y-%m-%d')

        item.set_callback(
            get_video_url,
            item_id=item_id,
            video_id=video_id,
        )
        item_post_treatment(item, is_playable=True, is_downloadable=True)
        yield item


@Resolver.register
def get_video_url(plugin,
                  item_id,
                  video_id,
                  download_mode=False,
                  **kwargs):

    resp = urlquick.get(URL_BRIGHTCOVE_DATAS)

    data_account = re.compile(r'ACCOUNT_ID\:\"(.*?)\"').findall(resp.text)[1]
    data_player = re.compile(r'PLAYER_ID\:\"(.*?)\"').findall(resp.text)[1]
    data_video_id = video_id

    return resolver_proxy.get_brightcove_video_json(plugin, data_account,
                                                    data_player, data_video_id,
                                                    download_mode)


@Resolver.register
def get_live_url(plugin, item_id, **kwargs):

    if item_id == 'stv_plusone':
        item_id = 'stv-plus-1'

    resp = urlquick.get(URL_LIVE_JSON % item_id)
    json_parser = json.loads(resp.text)
    return json_parser["results"]["streamUrl"]
