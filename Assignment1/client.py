import socket
import sys
import struct
import select

class DT_Request(object):
    def __init__(self, magicNo, packetType, requestType):
        self.magicNo = magicNo
        self.packetType = packetType 
        self.requestType = requestType
        self.packet = bytearray()
        self.checking()
        
    def checking(self):
        input_valid = False;
        if (self.magicNo == 0x497E and self.packetType == 0x0001 and self.requestType == 0x0001 
            or self.requestType == 0x0002):
            input_valid = True
            #print("Checked")
        else:
            input_valid = False
        self.input_valid = input_valid
    
    def encoding(self):
        if self.input_valid:
            self.packet = struct.pack(">hhh", self.magicNo, self.packetType, self.requestType)
            #self.packet.extend(self.magicNo.to_bytes(2, byteorder='big'))
            #self.packet.extend(self.packetType.to_bytes(2, byteorder='big'))
            #self.packet.extend(self.requestType.to_bytes(2, byteorder='big'))
            request = self.packet
        else:
            request = "Invalid Input"
        return request

def packetCheck(packet_length, header_length, magicNo, packetType, languageCode, year, month, day, hour,
                minute, length):
    """Checks the packet contains valid values"""
    valid = True
    if header_length < 13: 
        valid = False
    if magicNo != 0x497E:
        valid = False
    if packetType != 0x0002:
        valid = False
    if languageCode != 0x0001 and languageCode != 0x0002 and languageCode != 0x0003:
        valid = False
    if year > 2099:
        valid = False
    if month not in range(1, 13):
        valid = False
    if day not in range(1, 32):
        valid = False
    if hour not in range(0, 24):
        valid = False
    if minute not in range(0, 60):
        valid = False
    if (header_length + length) == packet_length:
        valid = False
    return valid
        

def main():

    packet = DT_Request(0x497E, 0x0001, 0x0001)
    packet.checking()
    packet.encoding()
    #print(packet.packet)
    
    try:
        request = sys.argv[1]
        UDP_IP = sys.argv[2]
        UDP_PORT = int(sys.argv[3])
        
    except IndexError:
        print("Error: expecting three paramaters (request, UDP_IP, UDP_PORT), terminating programme")
        sys.exit()
    
    try: 
        UDP_IP = socket.gethostbyname(UDP_IP)
    
    except UnicodeError:
        print("Error: IP address is not well-formed, terminating programme")
        sys.exit()
    
    except socket.gaierror:
        print("Error: name or service not known, terminating programme")
        sys.exit()
        
    running = True
    requestType = 0x0001
    while running:
        if request == 'date':
            requestType = 0x0001
        elif request == 'time':
            requestType = 0x0002
        else:
            print("Error: request type must be 'date' or 'time', terminating programme")
            sys.exit()
             
        Request = DT_Request(0x497E, 0x0001, requestType)    
        Request.checking()
        Request.encoding()
        
        # Convert host name to domain name (dotted format)
        
        if UDP_PORT < 1024 and UDP_PORT > 64000:
            print("Error: Port number is not in the valid range, terminating programme")
            sys.exit()
        else:
            running = False
    
    # Builds to socket for sending the request packet to server
    try:     
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(Request.packet, (UDP_IP, UDP_PORT))
        sock.settimeout(1)
    except socket.error():
        print("Error: failed to open UDP / datagram sicjets, terminating programme.")
        sys.exit()
        
    try:
        data, addr = sock.recvfrom(1024)
    # Tests for runtine error
    except socket.timeout:
        print("Timeout error, exiting time exceeded limit, terminating programme")
        sys.exit()
            #print("Recieved Message: ", (data, addr))
        #except socket.timeout:
            #print("Timeout error, waiting time exceeded limit")
            
    header = data[:13]
    body = data[14:]
    header_length = len(header)
    packet_length = len(data)
    recieved_message = body.decode('utf-8')     # Decoding the recieved message
            
    magicNo, packetType, languageCode, year, month, day, hour, minute, length = struct.unpack('>hhhhbbbbb', 
                                                                                              header)  
    passed = packetCheck(packet_length, header_length, magicNo, packetType, languageCode, year, month, day,
                         hour, minute, length)
        
    if passed:
        print(40*"-")
        print(recieved_message)
        print(40*"-")
    else:
        print("Error: Response packet is not valid, terminating programme")
        sys.exit()
    
    sock.close()

main()
