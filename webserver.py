import socket
import os
import mimetypes
from template import Template

def tcp_server():
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 5050
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()
    print('Listen on http://127.0.0.1:5050')
    while True:
        client_connection, client_address = server_socket.accept()
        request = client_connection.recv(1024).decode()
        print('Request : %s'%(request))
        if(request and request.strip()):
            response = handle_request(request)
            client_connection.sendall(response)
        client_connection.close()
    server_socket.close()
def handle_request(request):
    request_message = str(request).split("\r\n")
    request_line = request_message[0]
    words = request_line.split()
    method = words[0]
    uri = words[1]
    http_version = words[2]
    if(uri == '/'):
        uri = '/praktek.html'
    if(method == 'GET'):
        return handle_get(uri, http_version)
    if(method == 'POST'):
        data = request_message[len(request_message)-1]
        return handle_post(uri, http_version, data)
    return b''
def handle_get(uri, http_version):
    uri = "htdocs/%s"%(uri)
    if os.path.exists(uri) and not os.path.isdir(uri):
        response_line = b''.join([http_version.encode(), b' 200 OK'])
        content_type = mimetypes.guess_type(uri)[0] or 'text/html'
        entity_header = b''.join([b'Content-type: ', content_type.encode()])
        file = open(uri, 'rb')
        message_body = file.read()
        file.close()
    else :
        response_line = b''.join([http_version.encode(), b' 404 Not Found'])
        entity_header = b'Content-Type: text/html'
        message_body = b'<h1>404 Not Found</h1>'
    crlf = b'\r\n'
    response = b''.join([response_line, crlf, entity_header, crlf, crlf, message_body])
    return response
def handle_post(uri, http_version, data):
    uri = "htdocs/%s"%(uri)
    if os.path.exists(uri) and not os.path.isdir(uri):
        response_line = b''.join([http_version.encode(), b' 200 OK'])
        content_type = mimetypes.guess_type(uri)[0] or 'text/html'
        entity_header = b''.join([b'Content-type: ', content_type.encode()])
        file = open(uri, 'r')
        html = file.read()
        file.close()
        _POST = {}
        if data: # Mengamankan jika data POST kosong (seperti saat logout)
                    for i in data.split("&"):
                        if "=" in i: # Memastikan ada tanda '=' di dalam teks data
                            x = i.split("=")
                            if len(x) == 2: # Mengamankan agar tidak terjadi IndexError list out of range
                                _POST[x[0]] = x[1]
                            else:
                                _POST[x[0]] = ""
        # for i in data.split("&"):
        #     x = i.split("=")
        #     _POST[x[0]] = x[1]
        context = {
            '_POST' : _POST
        }
        t = Template(html)
        message_body = t.render(context).encode()
    else :
        response_line = b''.join([http_version.encode(), b' 404', b'Not Found'])
        entity_header = b'Content-Type: text/html'
        message_body = b'<h1>404 Not Found</h1>'
    crlf = b'\r\n'
    response = b''.join([response_line, crlf, entity_header, crlf, crlf, message_body])
    return response

if __name__ == "__main__":
    tcp_server()