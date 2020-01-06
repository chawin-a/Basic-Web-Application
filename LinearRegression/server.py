from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from cgi import FieldStorage
import time

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.linear_model import LinearRegression

IP_ADDRESS = 'localhost'
PORT = 8000

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        mimetype='text/html'
        if self.path.endswith(".png"):
            mimetype='image/png'
        # Header
        self.send_response(200)
        self.send_header('Content-type', mimetype)
        self.end_headers()
        
        if mimetype == 'image/png':
            f = open(self.path[1:], 'rb')
            self.wfile.write(f.read())
            f.close()
            return

        # Render
        head = open('head.html', 'rb')
        self.wfile.write(head.read())
        head.close()

        inp = open('input.html', 'rb')
        self.wfile.write(inp.read())
        inp.close()

        body = open('body.html', 'rb')
        self.wfile.write(body.read())
        body.close()

        tail = open('tail.html', 'rb')
        self.wfile.write(tail.read())
        tail.close()
    
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
        xt = np.linspace(0, 10, 11)
        yt = model.predict( xt.reshape(-1, 1))
        plt.scatter(x, y, c='b')
        plt.plot(xt, yt,'ro-')
        X = np.array([float(form['X'].value)])
        Y = model.predict(X.reshape(-1, 1))
        plt.plot(X, Y,'go')
        plt.yticks(np.arange(10, 110, 10))
        plt.xticks(np.arange(-1, 11, 1))
        plt.savefig('img/model.png')
        
        # Render
        head = open('head.html', 'rb')
        self.wfile.write(head.read())
        head.close()

        inp = open('input.html', 'rb')
        self.wfile.write(inp.read())
        inp.close()

        result = 'Y = ' + str(Y[0])
        self.wfile.write(result.encode('utf8'))

        body = open('body.html', 'rb')
        self.wfile.write(body.read())
        body.close()

        tail = open('tail.html', 'rb')
        self.wfile.write(tail.read())
        tail.close()

np.random.seed(12345671)

x = 10 * np.random.rand(20)
y = 8*x +8 + 5*np.random.randn(20)
plt.scatter(x, y,c='b')
plt.yticks(np.arange(10, 110, 10))
plt.xticks(np.arange(-1, 11, 1))
plt.savefig('img/input_data.png')

model = LinearRegression(fit_intercept=True)
x.reshape(-1, 1)
model.fit(x.reshape(-1, 1), y)

xt = np.linspace(0, 10, 11)
yt = model.predict( xt.reshape(-1, 1))
plt.scatter(x, y, c='b')
plt.plot(xt, yt,'ro-')
plt.yticks(np.arange(10, 110, 10))
plt.xticks(np.arange(-1, 11, 1))
plt.savefig('img/model.png')

try:
    httpd = HTTPServer((IP_ADDRESS, PORT), SimpleHTTPRequestHandler)
    print('Server is started on %s port %d' % (IP_ADDRESS, PORT))
    httpd.serve_forever()
except KeyboardInterrupt:
    print('Server is closed.')
    httpd.shutdown()