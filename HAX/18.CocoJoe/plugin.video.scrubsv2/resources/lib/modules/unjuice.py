# -*- coding: utf-8 -*-


import re

import six

from resources.lib.modules import jsunpack



def test(e):
    return True if re.search(r'JuicyCodes.Run\(', e, re.IGNORECASE) else False


def run(e):
    try:
        e = re.findall(r'JuicyCodes.Run\(([^\)]+)', e, re.IGNORECASE)[0]
        e = re.sub(r'\"\s*\+\s*\"','', e)
        e = re.sub(r'[^A-Za-z0-9+\\/=]','', e)
    except:
        return None
    Juice = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    t = ""
    n = r = i = s = o = u = a = f = 0
    while f < len(e):
        try:
            s = Juice.index(e[f]); f += 1; 
            o = Juice.index(e[f]); f += 1; 
            u = Juice.index(e[f]); f += 1; 
            a = Juice.index(e[f]); f += 1; 
            n = s << 2 | o >> 4; 
            r = (15 & o) << 4 | u >> 2; 
            i = (3 & u) << 6 | a
            t += chr(n)
            if 64 != u:
                t += chr(r)
            if 64 != a:
                t += chr(i)
        except:
            continue
        pass
    try:
        t = jsunpack.unpack(t)
        t = six.ensure_text(t)
    except:
        t = None
    return t


