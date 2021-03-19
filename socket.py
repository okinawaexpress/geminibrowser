import socket, ssl

HOST = "gemini.circumlunar.space"
PORT = 1965

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

wrapped_socket = context.wrap_socket(s, server_hostname=HOST)
wrapped_socket.connect((HOST, PORT))
wrapped_socket.send("gemini://gemini.circumlunar.space/\r\n".encode())

while True:
    data = wrapped_socket.recv(2048)
    if (len(data) < 1):
        break
    print(data)

wrapped_socket.close()
print("closed")
