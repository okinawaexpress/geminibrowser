'''
Functions
- validURL
 - Check protocol
   - Deny anything other than gemini://
 - Absolutize any relative link (using currentPage)
 - Send to URL parser
- parseURL
 - Get hostname
 - Form URL request
 - Send to connectToHost
- connectToHost
 - Create and wrap socket in TLS
 - Send URL request
 - Get data
   - Compound response body together (small enough task to include here)
 - Send header to parseHeader
   - Send response data/call whatever function needed based on result
- parseHeader
 - Check first number of status code
 - Return number for connectToHost
- renderData
 - Render data according to text/gemini standard
   - Anything else gets displayed as raw text
- sendInput
 - Prompt user for input
 - Formulate request and send to Host

To-Do
1. Finish basic backend networking/protocol/rendering code
2. Write gui system
3. Combine the two
4. Write back/forward button system

?. Implement TOFU Cert whenever guide comes out

Flowchart
1. validURL
2. parseURL
3. connectToHost
4. recieveData
5. parseHeader
6. Back to main, sendInput, or renderData based on status code
7. Repeat

Features
- Only allows gemini protocol pages
- Only renders text/gemini
  - Everything else gets plain text
- Back/Forward buttons
'''
import socket, ssl, re

def goToURL(url):
    #Wrapper for the whole function chain
    validURL(url)

def validURL(url):
    if '://' and 'gemini://' in url:
        #Absolute URL
        currentPage = url
        parseURL(url)
    elif '://' in url:
        #Different protocol
        print("Protocol other than gemini, connection refused")
    else:
        #Finish relative URL based on current page
        currentPage = currentPage + url
        parseURL(currentPage)

def parseURL(url):
    #Regex to get hostname
    #Compile regex expressions
    protocolPattern = re.compile('://')
    directoryPattern = re.compile('/')

    #Remove protocol first (to avoid conflicts with directory pattern)
    protocolEnd = protocolPattern.search(url)
    protocolEndPoint = protocolEnd.end()
    host = url[protocolEndPoint:]

    #Remove directories
    directoryStart = directoryPattern.search(host)
    directoryStartPoint = directoryStart.start()
    host = host[0:directoryStartPoint]

    #Build URL request to send to server
    urlRequest = url + '\r\n'
    connectToHost(host, urlRequest)

def connectToHost(host, urlRequest):
    #Set up socket -> Wrap in TLS protocol
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    wrapped_socket = context.wrap_socket(s, server_hostname=host)

    #Connect to host, send URL request
    wrapped_socket.connect((host, 1965))
    wrapped_socket.send(urlRequest.encode())
    recieveData(wrapped_socket)

def recieveData(socket):
    #Data recieved from server
    response = []

    #Recieve data in 2048 byte chunks
    while True:
        data = socket.recv(2048)
        data = data.decode()
        response.append(data)
        if (len(data) < 1):
            break
    
    #Close socket
    socket.close()

    #Put response header into its own variable
    headerInfo = response.pop(0)

    #Concatenate 2048 byte chunks together
    bodyInfo = ''.join(response)
    parseData(headerInfo, bodyInfo)

def parseData(header, body):
    #Figures out what function to call based on status code
    if header[0] == 1:
        #Input
        sendInput(header)
    elif header[0] == 2:
        #Success
        renderData(header, body)
    elif header[0] == 3:
        #Redirect
        #goToURL()
        pass
    elif header[0] == 4 or 5:
        #Error
        pass
    elif header[0] == 6:
        #Client Certificate needed
        pass

def sendInput():
    pass

def renderData(header, body):
    #Render text/gemini accordingly
    #Everything else gets treated as plain text
    pass
