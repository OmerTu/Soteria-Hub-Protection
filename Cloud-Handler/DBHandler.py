__author__ = 'omerturgeman'

import json,httplib,urllib, ssl

# Added to resolve SSL certificate issues with python 2.7.9:
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

connection = httplib.HTTPSConnection('api.parse.com', 443)


params = urllib.urlencode({"where": json.dumps({
    "commandType": "turnOn",
    "destination": "living_room"
    }
    )})
connection.connect()
connection.request('GET', '/1/classes/Command?%s' % params, '', {
       "X-Parse-Application-Id": "iLN1v3zqIM8mXfsbdqhZbTFjvYOwXZzHDXteGc3j",
       "X-Parse-REST-API-Key": "8M71FShn7tgq8Fih7WNGAclbxVABhNyNLrpaMXqJ"
     })
result = json.loads(connection.getresponse().read())
print "{0} results".format(len(result))
print "     First result:"
print "         commandType: {0}".format(result['results'][0]['commandType'])
print "         source: {0}".format(result['results'][0]['source'])
print "         destination: {0}".format(result['results'][0]['destination'])
#print result