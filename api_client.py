import urllib.request, urllib.error
import json, base64

class APIClient:
    def __init__(self, base_url):
        self.username = None
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url

    #
    # Send Get
    #
    # Issues a GET request (read) against the API and returns the result
    # (as Python dict).
    #
    def send_get(self, uri):
        return self.__send_request('GET', uri, None)

    #
    # Send POST
    #
    # Issues a POST request (write) against the API and returns the result
    # (as Python dict).
    #
    #
    def send_post(self, uri, data):
        return self.__send_request('POST', uri, data)

    def __send_request(self, method, uri, data):
        url = self.__url + uri
        request = urllib.request.Request(url)
        if (method == 'POST'):
            request.data = bytes(json.dumps(data), 'utf-8')
            
        if self.username:
            auth = str(
                base64.b64encode(
                    bytes(self.username, 'utf-8')
                ),
                'ascii'
            ).strip()
            request.add_header('x-auth', auth)
            
        request.add_header('Content-Type', 'application/json')

        e = None
        try:
            response = urllib.request.urlopen(request).read()
        except urllib.error.HTTPError as ex:
            response = ex.read()
            e = ex

        if response:
            print(response)
            result = json.loads(response.decode())
        else:
            result = {}

        if e != None:
            if result and 'error' in result:
                error = '"' + result['error'] + '"'
            else:
                error = 'No additional error message received'
            raise APIError('API returned HTTP %s (%s)' % 
                (e.code, error))

        return result

class APIError(Exception):
    pass