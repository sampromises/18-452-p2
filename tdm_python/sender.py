import csv
import socket
import time
import CmdLnParser

[host, port, file, channel] = CmdLnParser.parseCommandLine()

"""
Filters out the important channel from the input file
"""
channel_data = []
with open(file) as csvfile:
	reader = csv.reader(csvfile)
	i = 0
	for row in reader:
		if i != 0: channel_data.append(row[channel])
		i += 1
csvfile.close()

"""
By convention, there's 1 data point for each millisecond
  - Send 1 packet every 1 sec -> 1000 data points 
  - Package 1000 data points into a string separated by spaces
  - (Could add more info into the packet for resiliency)
"""
packet_size = 1000 # can modify this
packets = [channel_data[i:i+packet_size] for i in range(0, len(channel_data), packet_size)]
packets_marshalled = []
for packet in packets:
	s = " ".join(str(data) for data in packet)
	packets_marshalled.append(s)

"""
Sets up communication between current device and central node
"""
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((host, port))


"""
Send packets at 1 second intervals
"""
i = 0
while True:
	soc.send(packets_marshalled[i])
	# blocking - always wait for ACK before sending the next packet
	#          - can change this and handle out of order packets
	ACK = soc.recv(1024)

	# wait for 1 sec before sending next packet
	# simulate a real time situation
	time.sleep(1)