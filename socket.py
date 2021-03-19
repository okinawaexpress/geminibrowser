'''
To-Do

- Parse data recieved from server to display correctly
  - In particular, for large websites > 2048 bytes, append all the data
    sent together
  - Implement error code handling/MIME data type handling
- Useable hyperlinks
  - getHostData should take one argument, and regex/append things based on
    relative links, changes in host, redirects, etc
- Refactor towards making a main loop (continual calls to getHostData() and
  parseData()
- Make a data structure that keeps track of what host you are on. (For indirect
  links)
'''

import socket, ssl, re

def getHostData(url):

    #Regex/append to get host/urlRequest
    
    #Get hostname
    #compile regex
    protocolPattern = re.compile('://')
    directoryPattern = re.compile('/')

    #remove protocol
    protocolEnd = protocolPattern.search(url)
    protocolEndPoint = protocolEnd.end()
    host = url[protocolEndPoint:]

    #remove directories
    directoryStart = directoryPattern.search(host)
    directoryStartPoint = directoryStart.start()
    host = host[0:directoryStartPoint]

    #Get urlRequest
    urlRequest = url + '\r\n'
 
    #Binary data from host
    binary = []

    #Set up socket -> Wrap in TLS protocol
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wrapped_socket = context.wrap_socket(s, server_hostname=host)

    #Connect to host, send the request
    wrapped_socket.connect((host, 1965))
    wrapped_socket.send(urlRequest.encode())

    #Recieve data in 2048 byte chunks
    while True:
        recieveddata = wrapped_socket.recv(2048)
        binary.append(recieveddata)
        if (len(recieveddata) < 1):
            break
    #Close socket, return data
    wrapped_socket.close()
    return binary

    print("closed")

#Main Loop
while True:
    url = input("> ")
    data = getHostData(url)

#rly quick parser just seperates lines by \n breaks
#(according to gemini standard)
    
    newdata = (data[1].decode()).split('\n')
    for i in newdata:
        if len(i) < 1:
            print('\n')
        else:
            print(i)

