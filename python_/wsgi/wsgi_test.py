from wsgiref.simple_server import make_server

def app(environ, callback):
    path = environ.get('PATH_INFO')    
    if path == '/':
        response = 'index'
    else:
        response = 'hello'

    status = '200 OK'
    headers = [('Content-Length', str(len(response)))]
    callback(status, headers)
    return [response.encode('utf-8')]

def main():
    httpd = make_server('0.0.0.0', 9000, app)
    httpd.serve_forever()

if __name__ == '__main__':
    main()