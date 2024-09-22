# import socket module
from socket import *
# In order to terminate the program
import sys

def webServer(port=13331):

  HOST = ""  #(localhost)
  serverSocket = socket(AF_INET, SOCK_STREAM)
  
  #Prepare a server socket
  serverSocket.bind((HOST, port))
  
  #listing with default backlog value this can be set to any number 
  serverSocket.listen()
  
  while True:
    #Establish the connection
    
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
        
    try:
      data = connectionSocket.recv(4096)
    
      #get requested file conetent as data object     
      message = data

      #print(data)  
      #extract filename from request received  (example: helloworld.html)
      
      filename = message.split()[1]
                
      #opens the client requested file. 
      #Plenty of guidance online on how to open and read a file in python. How should you read it though if you plan on sending it through a socket?
      f = open(filename[1:], 'r')
  
      #This variable can store the headers you want to send for any valid or invalid request.   What header should be sent for a response that is ok?    
      #Fill in start 

      #Request Line for Status 200 
      requestLine = 'HTTP/1.x 200 OK\r\n'
      
      #set header values
      #Note that a complete header must end with a blank line, creating the four-byte sequence "\r\n\r\n" Refer to https://w3.cs.jmu.edu/kirkpams/OpenCSF/Books/csf/html/TCPSockets.html
      #Content-Type is an example on how to send a header as bytes. There are more!
      headerdata =  'Content-Type: text/html; charset=UTF-8\r\nContent-Length: 3495\r\nDate: Sat, 21 Sep 2024 04:36:25 GMT\r\nExpires: Sat, 21 Sep 2024 22:36:25 GMT\r\n'
      headerdata += 'Last-Modified: Sat, 21 Sep 2024 03:50:37 GMT\r\n\r\n'

    
      #output data consist of request line status and heaader data
      outputdata =  requestLine + headerdata

      #Set filebody as null
      filebody = ''

      #loop through each line of html file and build html body to send back to client as requested page
      for i in f: #for line in file
          filebody = filebody + i
      
      #print(filebody)   
      #Send the content of the requested file to the client (don't forget the headers you created)!
      #Send everything as one send command, do not send one line/item at a time!

      outputdata = outputdata + filebody
      
      #print(outputdata)
      connectionSocket.send(outputdata.encode('utf-8'))

      #receivedData = connectionSocket.recv(1024);
      print("Status: 200 OK");
              
      connectionSocket.close() #closing the connection socket
      
    except FileNotFoundError as e:
      
      errmessage = "HTTP/1.1 404 Not Found\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>"
      
      # Send response message for invalid request due to the file not being found (404)
      # Remember the format you used in the try: block!
      
      connectionSocket.send(errmessage.encode('utf-8'))
      print("Status: 404 Not Found")
      #Close client socket
      connectionSocket.close()
      

  # Commenting out the below (some use it for local testing). It is not required for Gradescope, and some students have moved it erroneously in the While loop. 
  # DO NOT PLACE ANYWHERE ELSE AND DO NOT UNCOMMENT WHEN SUBMITTING, YOU ARE GONNA HAVE A BAD TIME
  #serverSocket.close()
  #sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(13331)
