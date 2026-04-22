APPLICATION_ID = '123456789987654321'  # Put your Discord applicaition/client id here before running the server!
PORT = 2342

from http.server import BaseHTTPRequestHandler
import socketserver
import logging
import base64
import requests
from pypresence import Presence,ActivityType
from urllib.parse import unquote
logging.disable(logging.CRITICAL)

STATUS_ARG = '/?status='
NEW_ARG = '/?deconflict='
video = None

rpc = Presence(APPLICATION_ID)
rpc.connect()

def send(self, status, headers, body):
    self.send_response(status or 200)
    if len(headers)>0:
        for k in headers:
            self.send_header(k, headers[k])
        self.end_headers()
    self.wfile.write(body)

cache = {}
def get_yt_title(url):
    try:
        if len(cache)>20:
            cache.clear()
        return cache[url]
    except:
        params = {"format": "json", "url": url}
        target_url = "https://www.youtube.com/oembed"

        response = requests.get(target_url, params=params)

        if response.status_code == 200:
            cache[url] = response.json().get('title')
            return cache[url]
        return "Error: Could not retrieve title"

def status(path):
    raw = unquote(path[len(STATUS_ARG):])
    try:
        data = base64.b64decode(raw).decode('utf-8').split(' ; ')
        status = data[0].replace('_a','▶').replace('_b','⏸')
        url = data[1]
        if url == video:
            print('STATUS RECEIVED |', status, url, video)

            title = get_yt_title('https://youtube.com/watch?v='+video)
            truncated_title = title[:20 - 3]
            if len(title) > 20 - 3:
                truncated_title += '...'
            rpc.update(
                state=truncated_title+' | '+status,
                details='Watching a video',
                activity_type=ActivityType.WATCHING,
                name='Youtube',
                large_image=('https://img.youtube.com/vi/'+video+'/maxresdefault.jpg') if video is not None else None,
                buttons=[
                    {'label':'Watch','url':'https://www.youtube.com/watch?v='+video}
                ]
            )
        else:
            print('CONFLICT |', url, video)
        return b'OK'
    except:
        return b'ERROR'

def deconflict(path):
    global video
    raw = unquote(path[len(NEW_ARG):])
    try:
        video = raw
        print('DECONFLICT RECEIVED |', video)
        return b'OK'
    except Exception as e:
        print(e)
        return b'ERROR'

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path.startswith(STATUS_ARG):
            send(self,200,{'Content-Type':'text/plain'},status(self.path))
        elif self.path.startswith(NEW_ARG):
            send(self,200,{'Content-Type':'text/plain'},deconflict(self.path))
        else:
            send(self,200,{'Content-Type': 'text/plain'},b'ERROR')

print('Started server on port', PORT)
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        exit()
