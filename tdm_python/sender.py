import csv
import socket
import time
import argparse

# TCP sockets
host = '127.0.0.1'
port = 8080
skt = None # Glocal socket

# CSV file
CSV_PATH = ''

# Connect to socket
def connect():
	global skt
	skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	skt.connect((host, port))

def get_data_from_csv():
	ecg = []
	emg = []
	gsr = []
	with open(CSV_PATH) as csvfile:
		reader = csv.reader(csvfile)
		i = 0
		for row in reader:
			if i != 0: 
				ecg.append(row[1])
				emg.append(row[2])
				gsr.append(row[3])
			i += 1
	csvfile.close()
	return [ecg, emg, gsr]

def marshall(data):
	"""
	By convention, there's 1 data point for each millisecond
	  - Send 1 packet every 1 sec -> 1000 data points 
	  - Package 1000 data points into a string separated by spaces
	  - (Could add more info into the packet for resiliency)
	"""
	packet_size = 1000 # can modify this
	packets = [data[i:i+packet_size] for i in range(0, len(data), packet_size)]
	packets_marshalled = []
	for packet in packets:
		s = " ".join(str(data) for data in packet)
		packets_marshalled.append(s)

	return packets_marshalled

def send_data_control_experiment(ecg, emg, gsr):
	"""
	Send packets at 1 second intervals
	"""
	i = 0
	j = 0
	k = 0
	while True:
		if i == len(ecg): break
		skt.send(bytes(ecg[i], 'utf-8'))
		i += 1
		# blocking - always wait for ACK before sending the next packet
		#          - can change this and handle out of order packets
		# ACK = soc.recv(1024)

		# wait for 1 sec before sending next packet
		# simulate a real time situation
		# time.sleep(1)

	while True:
		if j == len(emg): break
		skt.send(bytes(emg[j], 'utf-8'))
		j += 1

	while True:
		if k == len(gsr): break
		skt.send(bytes(gsr[k], 'utf-8'))
		k += 1

	start = time.time()
	skt.sendall(b'A'*1024)
	end = time.time()
	print(end - start)

def main():
	global skt
	connect()
	[ecg, emg, gsr] = get_data_from_csv()
	send_data_control_experiment(ecg, emg, gsr)
	skt.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Command line argument parser") 
	parser.add_argument('--host', type=str, help='Required host ip address')
	parser.add_argument('--port', type=int, help='Required port number')
	parser.add_argument('--file', type=str, help='Required cvs file')
	args = parser.parse_args()

	# set optional host/port if provided
	if (args.host != None):
		host = args.host
	if (args.port != None):
		port = args.port

	CSV_PATH = args.file

	main()
