'''
To-Do
- Switchable modes for user input (direct url entry, link number, forwards/backwards)
- Handle Meta codes and formatting
- Assign each link on the page a number, user will type number to redirect
- Keep a log of pages/sites visted for a backwards/forwards feature
'''

import socket, ssl, re

#Page browser is currently on
currentPage = ''

def parseURL(url):
  #Should always be an absolute link
  #gets hostname/urlRequest out of url given

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
  return host, urlRequest

def connectToHost(connectionInfo):

  #Connects to host, recieves data, returns header (error code/MIME type) and response body

  binary = []

  #Set up socket -> Wrap in TLS protocol
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  wrapped_socket = context.wrap_socket(s, server_hostname=connectionInfo[0])

  #Connect to host, send the request
  wrapped_socket.connect((connectionInfo[0], 1965))
  wrapped_socket.send(connectionInfo[1].encode())

  #Recieve data in 2048 byte chunks
  while True:
    data = wrapped_socket.recv(2048)
    data = data.decode()
    binary.append(data)
    if (len(data) < 1):
      break

  #Compound the entire response body together
  headerInfo = binary.pop(0)
  responseInfo = ''.join(binary)

  #Close socket, return data
  wrapped_socket.close()
  return headerInfo, responseInfo
  print("closed")

def parseData(data):
    print(data[0])
    #Check status Codes first
    #Check MIME type
    #parse/display data (including link handling)
    newdata = data[1].split('\n')
    for i in newdata:
        if len(i) < 1:
            print('\n')
        else:
            print(i)

while True:
    url = input("> ")
    if '://' and 'gemini://' in url:
      #absolute url
      currentPage = url
      parseData(connectToHost(parseURL(url)))
    elif '://' in url:
      #different protocol (refuse)
      print("Different protocol, connection refused")
    else:
      #relative url
      currentPage = currentPage + url
      url = currentPage
      parseData(connectToHost(parseURL(url)))
