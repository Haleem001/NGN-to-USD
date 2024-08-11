from http.server import BaseHTTPRequestHandler
from scraper import get_average_value
import json
import time
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        average = get_average_value()
        with open('/tmp/average_value.json', 'w') as f:
            json.dump({'average': average, 'timestamp': time.time()}, f)
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'updated'}).encode())

# This handler will be called by the Vercel cron job to update the average value
