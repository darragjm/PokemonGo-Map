from cStringIO import StringIO
import urllib


def getStaticMap(lat, long):
    url = "http://maps.googleapis.com/maps/api/staticmap?center=%(lat)s,%(long)s&size=800x800&zoom=16&markers=%(lat)s,%(long)s&sensor=false" % dict(lat=lat, long=long)
    buffer = StringIO(urllib.urlopen(url).read())
    return buffer
