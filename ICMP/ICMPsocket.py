import socket #This module allows access to interfaces available 		     in OSs
import sys #This module allows access to functions strongly      		   interacting with the interpreter.
import time #Allows access to time related functions.
from struct import pack, unpack #Helps to pack and unpack

#creating Raw sockets to receive and send data in python
try:
	s1 = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
	s2=s2 = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
except socket.error , msg:
	print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit() #displaying error messages if sockets weren't 				created

#creating the ip header
source_ip = '10.1.1.2' #The sender's IP address
dest_ip = '10.1.3.3'  #The receiver's IP address
 
# ip header fields taken as variables
ip_ihl = 5
ip_ver = 4 #version 4 (ipv4)
ip_tos = 0 #type of service
ip_tot_len = 0  # kernel will fill the correct total length
ip_id = 54321   #Id of this packet
ip_frag_off = 0
ip_ttl = 1 #The packet should fall of initially after going one    			round(Time To Live)
ip_proto = socket.IPPROTO_TCP
ip_check = 0    # kernel will fill the correct checksum
ip_saddr = socket.inet_aton ( source_ip )   #Spoof the source ip address if you want to
ip_daddr = socket.inet_aton ( dest_ip )
 
ip_ihl_ver = (ip_ver << 4) + ip_ihl
 
# the ! in the pack format string means network order
ip_header = pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr) #used to pack values in to 1 variable	
	
