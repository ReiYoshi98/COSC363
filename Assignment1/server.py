import socket
import sys
import struct
import select
import datetime

UDP_IP = "127.0.0.1"

#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
#sock.bind((UDP_IP, UDP_PORT))

class DT_Response(object):
    def __init__(self, magicNo, packetType, languageCode, RequestType):
        """Initializes the DT_Response packet"""
        now = datetime.datetime.now()
        self.magicNo = magicNo
        self.packetType = packetType
        self.languageCode = languageCode        
        
        # Determines from the request whether the client wants to know today's date or current time of day.
        if RequestType == 1:
            self.languageDate()
            text, textByte = self.dateRepresentation(now)
        
        elif RequestType == 2:
            text, textByte = self.timeRepresentation(now)
            
        
        self.year = now.year
        self.month = now.month
        self.day = now.day
        self.hour = now.hour
        self.minute = now.minute
        self.length = len(textByte)         # |T|
        self.text = textByte
        self.printText = text
        self.packet = bytearray()
        self.encoding()
        #print(self.length)
    
    def languageDate(self):
        """Dicotionarys for the three language options 
        (English, Maori and German)"""
        language = ''
        english = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: 
                   "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
        maori = {1: "Kohitatea", 2: "Hui-tanguru", 3: "Poutu-te-rangi", 4: "Paenga-whawha", 5: 
                 "Haratua", 6: "Pipiri", 7: "Hongongoi", 8: "Here-turi-koka", 9: "Mahuru", 10: 
                 "Whiringa-a-nuku", 11: "Whiringa-a-rangi", 12: "Hakihea"}
        german = {1: "Januar", 2: "Februar", 3: "Marz", 4: "April", 5: "Mai", 6: "Juni", 7: "Juli",
                  8: "August", 9: "September", 10: "Oktober", 11: "November", 12: "Dezember"}
        
        if self.languageCode == 0x0001:
            language = english
        if self.languageCode == 0x0002:
            language = maori
        if self.languageCode == 0x0003:
            language = german
    
        self.language = language

    def dateRepresentation(self, now):
        """Formats the date in a textual representation, and encodes it into 
        byte format"""
        text = ""
 
        if self.languageCode == 0x0001:
            text = ("Today's date is %s %d, %d" % (self.language[now.month], now.day, now.year))
        if self.languageCode == 0x0002:
            text = ("Ko te ra o tenei ra ko %s %d, %d" % (self.language[now.month], now.day, now.year))       
        if self.languageCode == 0x0003:
            text = ("Heute ist der %d, %s %d" % (now.day, self.language[now.month], now.year))     
            
        textByte = text.encode('utf-8')      # Encoding the text message into bytes
        #print(textByte)
        return text, textByte
    
    def timeRepresentation(self, now):
        """Formats the date in a textual representation, and encodes it into 
        byte format"""
        text = ""
        if self.languageCode == 0x0001:
            text = ("The current time is %d:%d" % (now.hour, now.minute))
        if self.languageCode == 0x0002:
            text = ("Ko te wa o tenei wa %d:%d" % (now.hour, now.minute))  
        if self.languageCode == 0x0003:
            text = ("Die Uhrzeit ist %d:%d" % (now.hour, now.minute)) 
            
        textByte = text.encode('utf-8')      # Encoding the text message into bytes
        return text, textByte   

    def encoding(self):
        self.header = struct.pack('>hhhhbbbbb', self.magicNo, self.packetType, self.languageCode, 
                                  self.year, self.month, self.day, self.hour, self.minute, self.length)
        
        self.data = struct.pack("I", len(self.text)) + self.text
        self.packet = self.header + self.data

while True:
     
    port_numbers = []
    try:
        first_port = int(sys.argv[1])                           # Taking the first port number
        second_port = int(sys.argv[2])                          # Taking the second port number
        third_port = int(sys.argv[3])                           # Taking the third port number
        
    except IndexError:
        print("Error: Three port number parameters expected, Terminating programme.")
        break
    
    port_numbers.append(first_port)                         # Adding to an array for iterating 
    port_numbers.append(second_port)
    port_numbers.append(third_port)
    in_range = True
    
    # Checking if port number is in range
    for number in port_numbers:                         
        if number < 1024 or number > 64000:
            in_range = False   
    if not in_range:
        print("Error: Port number must be numbers between 1024 and 64000, Terminating programme.")                      
        break
    
    # Open three UDP / datagram sockets and bind the three given port numbers
    try:
        sock_eng = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     
        sock_mao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_ger = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
        sock_eng.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_mao.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_ger.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
        sock_eng.bind((UDP_IP, first_port))
        sock_mao.bind((UDP_IP, second_port))
        sock_ger.bind((UDP_IP, third_port))
        
    except socket.error:
        print("Error: failed to open UDP / datagram sicjets, Terminating programme.")
        
    running = True      
    while running:
        print("Server Running... Waiting for request packet")
        read_sockets, _, _ = select.select([sock_eng, sock_mao, sock_ger], [], [], None)
        for s in read_sockets:
            data, addr = s.recvfrom(1024) # buffer
            #if s == sock_eng
            print("received message:", addr)
            MagicNo, PacketType, RequestType = struct.unpack('>hhh', data)
        running = False
        
    # Performs the necessary checks to see whether the packet is a valid DT-Request packet
    if MagicNo == 0x497E and PacketType == 0x0001 and RequestType == 0x0001 or RequestType == 0x0002:
        pass 
    else:
        print("Error: request packet is not valid, terminating programme.")
        break
    
    port_number = s.getsockname()[1]            # the port number requested
    if port_number == first_port:               # Matching to appripriate language code
        languageCode = 0x0001
    if port_number == second_port:
        languageCode = 0x0002
    if port_number == third_port:
        languageCode = 0x0003
    Response = DT_Response(0x497E, 0x0002, languageCode, RequestType)
    Response.encoding()
    #print(response_packet.packet)
    while True:
        #print(response_packet.printText)
        if Response.length > 255:
            print("Error: text length exceeds limit, terminating programme.")
            break
        else:
            s.sendto(Response.packet, (UDP_IP, addr[1]))
            print("Response packet has been sent")
            break
    s.close()