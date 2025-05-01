import socket
import os

SERVER_IP = '127.0.0.1'
PORT = 2000
counter = 0

def create_server(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(4)
    return server

def start_server():
    server = create_server(SERVER_IP, PORT)
    global counter
    
    print("Server started: " + f"http://{SERVER_IP}:{PORT}")
    
    try:
        while True:
            client, address = server.accept()
            counter += 1
            data = client.recv(1024).decode('utf-8')
            print('Connected by: |', address, "|, counter =", counter)

            content = load_page_from_get(data)
            client.send(content)

            client.shutdown(socket.SHUT_WR)
            
    except KeyboardInterrupt:
        server.close()
        print("Server closed")


def load_page_from_get(request_data:str):
    HDRS = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n".encode('utf-8')
    path = request_data.split(" ")[1]
    response = ""
    
    if not os.path.exists("views" + path):
        path = "/404.html"
    
    if path in ["/", "/home"]:
        path = "/index.html"

    with open("views" + path, "rb") as f:
        response = f.read()
    
    return HDRS + response

if __name__ == '__main__':
    start_server()