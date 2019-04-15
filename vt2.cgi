#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgitb, cgi, os
from jinja2 import Template, Environment, FileSystemLoader
import urllib as urllib
import simplejson as json

cgitb.enable(format="text")
print u"""Content-type: text/html; charset=utf-8\n"""

fields = cgi.FieldStorage()
try:
    size = int(fields.getfirst(u"x", default=8).decode("utf-8"))
    if size > 16 or size < 8: size = -1
except:
    size = -1
try:
    text = fields.getfirst(u"teksti").decode("utf-8")
except:
    text = u""
try:
    tmpl_path = os.path.join(os.path.dirname(os.environ['SCRIPT_FILENAME']), 'templates')
except:
    tmpl_path = "templates"
try:
    removed = json.loads('{"rmvd":%s}' % fields["xy"].value)["rmvd"]
except:
    removed = [None, None]
try:
    btns = json.loads('{"btns":%s}' % fields["btns"].value)["btns"]
    cont = True
    try:
        btns.remove(removed)
    except:
        pass
except Exception as ex: #NEW GAME
    cont = False
    btns = []
    blue = 0
    red = size
    for y in range(0, size):
        for x in range(0, size):
            if x == blue and y == blue: btns.append([x, y])
            elif x == red -1 and y == size - red: btns.append([x, y])
        red -= 1
        blue += 1
try:
    mde = fields[u"mode"].value.decode("utf-8")
except:
    mde = u""

class LinkTool:
    """Specialized link creation-tool for this application."""
    def __init__(self):
        pass

    @staticmethod
    def crt_link(size, text, btns, xy=(-1,-1), mode=""):
        try:
            result = "./vt2.cgi?%s&%s&%s&%s" % (urllib.urlencode({"xy": [xy[0], xy[1]]}),
                urllib.urlencode({"x": size}),
                #urllib.urlencode({"teksti": urllib.quote_plus(text.encode("utf-8"))}),
                "teksti=" + urllib.quote_plus(text.encode("utf-8")),
                urllib.urlencode({"btns": btns}))
        except:
            result = u""
        try:
            if mode == u"move": result += u"&" + urllib.urlencode({"mode": u"move"}) 
            elif mode == u"rmv": result += u"&" + urllib.urlencode({"mode": u"rmv"}) 
            return result
        except:
            return result

env = Environment(autoescape=True, loader=FileSystemLoader(tmpl_path),
                  extensions=["jinja2.ext.autoescape"])

template = env.get_template('vt2.html')
print template.render(btns=btns, size=size,
                      text=text, urllib=urllib,
                      cont=cont, removed=removed,
                      lk_tool=LinkTool(), mde=mde).encode("utf-8")
