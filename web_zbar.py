#!/usr/bin/python

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
        image = ZbarImage(width, height, 'Y800', raw)
        zbar_scanner.scan(image)
        for symbol in image:
            yield symbol
        del(image)
    return _f

if __name__ == '__main__':
    from sys import argv
    from pprint import pprint
    
    zbar_scanner = makeZbarScanner()

    for img_url in argv[1:]:
        img_feeder = makeImageFeeder(img_url)
        raw, size = img_feeder()
        scanner = makeZbarScanner()
        print img_url
        map(lambda x: pprint((str(x.type), x.data)),
            scanner(raw, *size))
