# -*- coding: utf-8 -*-

import re
import os

from six.moves import urllib_parse

from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import log_utils


def keyboard(response):
    try:
        i = os.path.join(control.dataPath, 'img')
        f = control.openFile(i, 'w')
        f.write(client.request(response))
        f.close()
        f = control.image(450, 5, 375, 115, i)
        d = control.windowDialog
        d.addControl(f)
        control.deleteFile(i)
        d.show()
        k = control.keyboard('', 'Type the letters in the image')
        k.doModal()
        c = k.getText() if k.isConfirmed() else None
        if c == '':
            c = None
        d.removeControl(f)
        d.close()
        return c
    except:
        log_utils.log('keyboard', 1)
        return


def solvemedia(data):
    try:
        url = client.parseDOM(data, 'iframe', ret='src')
        url = [i for i in url if 'api.solvemedia.com' in i]
        if not len(url) > 0:
            return
        result = client.request(url[0], referer='')
        response = client.parseDOM(result, 'iframe', ret='src')
        response += client.parseDOM(result, 'img', ret='src')
        response = [i for i in response if '/papi/media' in i][0]
        response = 'http://api.solvemedia.com' + response
        response = keyboard(response)
        post = {}
        f = client.parseDOM(result, 'form', attrs={'action': 'verify.noscript'})[0]
        k = client.parseDOM(f, 'input', ret='name', attrs={'type': 'hidden'})
        for i in k:
            post.update({i: client.parseDOM(f, 'input', ret='value', attrs={'name': i})[0]})
        post.update({'adcopy_response': response})
        client.request('http://api.solvemedia.com/papi/verify.noscript', post=urllib_parse.urlencode(post))
        return {'adcopy_challenge': post['adcopy_challenge'], 'adcopy_response': 'manual_challenge'}
    except:
        log_utils.log('solvemedia', 1)
        pass


def recaptcha(data):
    try:
        url = []
        if data.startswith('http://www.google.com'):
            url += [data]
        url += client.parseDOM(data, 'script', ret='src', attrs={'type': 'text/javascript'})
        url = [i for i in url if 'http://www.google.com' in i]
        if not len(url) > 0:
            return
        result = client.request(url[0])
        challenge = re.compile("challenge\s+:\s+'(.+?)'").findall(result)[0]
        response = 'http://www.google.com/recaptcha/api/image?c=' + challenge
        response = keyboard(response)
        return {'recaptcha_challenge_field': challenge, 'recaptcha_challenge': challenge, 'recaptcha_response_field': response, 'recaptcha_response': response}
    except:
        log_utils.log('recaptcha', 1)
        pass


def capimage(data):
    try:
        url = client.parseDOM(data, 'img', ret='src')
        url = [i for i in url if 'captcha' in i]
        if not len(url) > 0:
            return
        response = keyboard(url[0])
        return {'code': response}
    except:
        log_utils.log('capimage', 1)
        pass


def numeric(data):
    try:
        url = re.compile("left:(\d+)px;padding-top:\d+px;'>&#(.+?);<").findall(data)
        if not len(url) > 0:
            return
        result = sorted(url, key=lambda ltr: int(ltr[0]))
        response = ''.join(str(int(num[1])-48) for num in result)
        return {'code': response}
    except:
        log_utils.log('numeric', 1)
        pass


def request(data):
    try:
        captcha = solvemedia(data)
        if not captcha == None:
            return captcha
        captcha = recaptcha(data)
        if not captcha == None:
            return captcha
        captcha = capimage(data)
        if not captcha == None:
            return captcha
        captcha = numeric(data)
        if not captcha == None:
            return captcha
    except:
        log_utils.log('request', 1)
        return


