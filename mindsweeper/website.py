from functools import wraps
import http.server
import re

func = {}

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        response_status_code = 404
        body = ''
        
        for pattern, f in func.items():
            m = re.match(pattern, self.path)
            if m:
                print('got here, matched')
                print('Match', func[pattern].__name__, pattern, self.path)
                response_status_code, body = func[pattern](*m.groups())
                break
                
        self.send_response(response_status_code)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body.encode())

class Website:  
    def route(self, path):
        def decorator(f):
            global func
            func[re.compile(f'^{path}$')] = f
            @wraps(f)
            def wrapper(f):
                pass
            return wrapper
        return decorator
        
    def parse_address(address):
        res = address.split(":")
        res[1] = int(res[1])
        return tuple(res)

    def run(self, address):
        try:
            http_server = http.server.HTTPServer(address, Handler)
            http_server.serve_forever()
        except Exception as error:
            print(f'ERROR: {error}')
            return 1
            
