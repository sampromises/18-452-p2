import re

# Create mapping from IP to Node
NODE_MAP_STR = '''
? (192.168.2.5) at 16:3a:43:2b:be:34 = NODE 1
? (192.168.2.27) at 4e:3b:46:c6:6e:c8  = NODE 7
? (192.168.2.28) at ae:5d:73:84:71:b6  = NODE 3
? (192.168.2.29) at 6e:3c:19:9d:1b:74  = NODE 2
? (192.168.2.30) at 8e:ab:87:93:93:d3  = NODE 4
? (192.168.2.31) at 86:9:ed:95:2b:82  = NODE 5
? (192.168.2.32) at a2:ca:e2:93:75:6b  = NODE 6
'''
def get_ip_to_node(input_str=NODE_MAP_STR):
    ip_to_node = {}

    # Regex matches
    ip_matches = re.findall(r'(192.168.2.\d+)', input_str)
    node_matches = re.findall(r'(NODE \d)', input_str)

    # Assertion
    if len(ip_matches) != len(node_matches):
        print('# of IPs != # of Nodes')
        exit(-1)

    # Create mapping
    for i in range(len(ip_matches)):
        ip = ip_matches[i]
        node = node_matches[i].replace('NODE ', '')
        ip_to_node[ip] = node

    return ip_to_node

def get_results_one_trial(input_str='''
[  9] local 192.168.2.5 port 8080 connected with 192.168.2.30 port 46330
[  4] local 192.168.2.5 port 8080 connected with 192.168.2.29 port 38600
[  5] local 192.168.2.5 port 8080 connected with 192.168.2.28 port 42118
[  6] local 192.168.2.5 port 8080 connected with 192.168.2.32 port 51028
[  7] local 192.168.2.5 port 8080 connected with 192.168.2.31 port 43472
[  8] local 192.168.2.5 port 8080 connected with 192.168.2.27 port 49416
[  4]  0.0-30.5 sec  28.6 MBytes  0.94 MBytes/sec <-- NODE 2
[  5]  0.0-30.5 sec  25.0 MBytes  0.82 MBytes/sec <-- NODE 3
[  9]  0.0-30.6 sec  15.9 MBytes  0.52 MBytes/sec <-- NODE 4
[  7]  0.0-29.1 sec  18.7 MBytes  0.64 MBytes/sec <-- NODE 5
[  6]  0.0-29.3 sec  5.50 MBytes  0.19 MBytes/sec <-- NODE 6
[  8]  0.0-29.1 sec  6.97 MBytes  0.24 MBytes/sec <-- NODE 7
'''):
    ip_to_node = get_ip_to_node() # Get IP to Node mapping
    trial_mapping = {} # Initialized in beginning
    results = [] # List of each result (each result is a dict)
    
    for line in input_str.split('\n'):
        if not re.search(r'\[.*\d\]', line): continue # Ignore these lines

        # Every line starts with the iperf ID
        iperf_id = re.search(r'\[.*\d\]', line).group()
        iperf_id = int(''.join(c for c in iperf_id if c.isdigit()))
        
        # Create trial mapping (should be first lines)
        if 'connected with' in line:
            ip = re.search(r'with 192.168.2.\d+', line).group()
            ip = ip.replace('with ', '')

            trial_mapping[iperf_id] = ip
        else:
            # Get time interval
            time = re.search(r'\d+\.\d sec', line).group()
            time = time.replace(' sec', '')

             # Get data units
            data_units = re.search(r'\w+/sec', line).group()
            data_units = data_units.replace('/sec', '')
            
            # Get data size
            data_size = re.search(r'[\d+\.]*\d %s' % data_units, line).group()
            data_size = data_size.replace(' %s' % data_units, '')

            # Get data speed
            data_speed = re.search(r'[\d+\.]*\d \w+/sec', line).group()
            data_speed = data_speed[:data_speed.index(' ')]


            
            results.append({
                'node' : ip_to_node[trial_mapping[iperf_id]],
                'time' : time,
                'data_units' : data_units,
                'data_size' : data_size,
                'data_speed' : data_speed,
            })

    return results

# Helper to sort by node ID
def node_as_sorted_key(elem):
    return int(elem['node'])

def main():
    results = get_results_one_trial()
    results_by_id = sorted(results, key=node_as_sorted_key)
    for result in results_by_id:
        print(result)

main()
