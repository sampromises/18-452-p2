import argparse

"""
Parses args from command line:
  - host ip address
  - input csv file with medical data
  - the 0-indexed channel of medical data at stake
"""
def parseCommandLine():
	parser = argparse.ArgumentParser(description="Command line argument parser") 
	parser.add_argument('--host', type=str, help='Required host ip address')
	parser.add_argument('--port', type=int, help='Required port number')
	parser.add_argument('--file', type=str, help='Required cvs file')
	parser.add_argument('--channel', type=int, help="Required data channel")
	args = parser.parse_args()

	return [args.host, args.port, args.file, args.channel]