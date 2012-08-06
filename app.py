#!/usr/bin/python
from flask import Flask, request
from flask.views import MethodView

from couchdb import Server
from json import dumps as json_dumps, loads as json_loads
    
########################################
# makeImageFeeder: returns function    #
########################################

def makeImageFeeder(url):
    from urllib import urlopen
    import ImageFile # PIL image loader
    """
    return function for fetching PIL images from url
    (useful for snapping images from a video feed)
    """
    def _f():
        """
	returns (raw PIL image, (width, height))
        """
        f = urlopen(url)
        p = ImageFile.Parser()
        while True:
            buf = f.read(1024)
            if not buf: break
            else: p.feed(buf)
        pil = p.close() # i.e. PIL image
        pilbuf = pil.convert("L").tostring()
        return pilbuf, pil.size
    return _f

def makeZbarScanner():
    """
    returns a scanner function for process raw data
    """
    from zbar import ImageScanner as ZbarImageScanner
    from zbar import Image as ZbarImage
    
    zbar_scanner = ZbarImageScanner()
    zbar_scanner.parse_config('enable')
    
    def _f(raw_pil, width, height):
        image = ZbarImage(width, height, 'Y800', raw_pil)
        zbar_scanner.scan(image)
        for symbol in image:
            yield symbol
        del(image)
    return _f

########################################
# flask/app setup:                     #
########################################

app = Flask(__name__, static_folder="www")
app.debug = True

zbar_scanner = makeZbarScanner()
img_feeder = makeImageFeeder("http://192.168.1.142:8080/shot.jpg")

class ZbarAPI(MethodView):
    def get(self):
        raw, size = img_feeder()
        results = map(lambda x: (str(x.type), x.data),
                      zbar_scanner(raw, *size))
        return json_dumps(list(results))
    
    def post(self):
        raw, size = img_feeder()
        results = zbar_scanner(raw, *size)
        return 'OK'

app.add_url_rule('/zbar/',
                 view_func=ZbarAPI.as_view('zbar'))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
                    
