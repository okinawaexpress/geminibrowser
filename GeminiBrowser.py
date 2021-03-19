'''
To-Do

- Parse data recieved from server to display correctly
  - Implement error code handling/MIME data type handling
- Useable hyperlinks
  - Assign each link on the page a number, user will type number to redirect
- Make a data structure that keeps track of the current directory, as well as
  previously visited pages.
   - For indirect links, and for back/forward buttons on final browser
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
        data = wrapped_socket.recv(2048)
        data = data.decode()
        binary.append(data)
        if (len(data) < 1):
            break

    #Compound the entire response body together
    headerInfo = binary.pop(0)
    binaryData = ''.join(binary)

    #Close socket, return data
    wrapped_socket.close()
    return headerInfo, binaryData
    print("closed")

#rly quick parser just seperates lines by \n breaks
#(according to gemini standard)
def parseData(data):
    #Check Error Codes first
    #Check MIME type
    newdata = data[1].split('\n')
    for i in newdata:
        if len(i) < 1:
            print('\n')
        else:
            print(i)

#Main Loop
while True:
    url = input("> ")
    parseData(getHostData(url))
