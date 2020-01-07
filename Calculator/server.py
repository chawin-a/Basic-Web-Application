from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from cgi import FieldStorage

IP_ADDRESS = '0.0.0.0'
PORT = 8000

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
    	# Header
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Render
        f = open('index.html', 'rb')
        self.wfile.write(f.read())
        f.close()
    
    def do_POST(self):
    	# Input
        form = FieldStorage(fp=self.rfile, 
        					headers=self.headers,
        					environ={
        						'REQUEST_METHOD':'POST',
		          				'CONTENT_TYPE':self.headers['Content-Type']
		          			})
        
        # Header
        self.send_response(200)
        self.end_headers()

        # Process
        result = int(form['A'].value) + int(form['B'].value)
        
        # Render
        response = ('Result = ' + str(result)).encode('utf8')
        self.wfile.write(response)

try:
	httpd = HTTPServer((IP_ADDRESS, PORT), SimpleHTTPRequestHandler)
	print('Server is started on %s port %d' % (IP_ADDRESS, PORT))
	httpd.serve_forever()
except KeyboardInterrupt:
    print('Server is closed.')
    httpd.shutdown()