import sys
import ssl
import socket
class URL:
    def __init__(self, url) -> None:
        scheme, url = url.split("://", 1)
        if '/' not in url:
            url += '/'
        host, url = url.split('/', 1)
        path = '/' + url
        assert scheme in ['http', 'https']
        if scheme=='http':
            port=80
        elif scheme=='https':
            port=443
        if ':' in path:
            path, port = path.split(':', 1)
        self.scheme = scheme
        self.host = host
        self.path = path 
        self.port = port
    def request(self):
        request = f"GET {self.path} HTTP/1.0\r\n"
        request+= f"Host: {self.host}\r\n\r\n"
        s=socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
        if self.scheme == 'https':
            context = ssl.create_default_context()
            s= context.wrap_socket(s,  server_hostname=self.host)
        s.connect((self.host, self.port))
        s.send(request.encode(encoding="utf-8"))
        fileobject = s.makefile(mode='r', encoding='utf-8', newline="\r\n")
        version, status, explanation = fileobject.readline().split(" ", 2)
        print(f"version= {version}, status={status}, explanation={explanation}")
        s.close()
        response = ""
        while True:
            data = fileobject.readline()
            if not data or data=="\n\r":
                break
            response +=data
        return response
def load(url):
    show(url.request())
def show(url):
    print(url)
load(URL(sys.argv[1]))