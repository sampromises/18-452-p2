import re

# Create mapping from IP to Node
NODE_MAP_STR = '''
192.168.2.5 = NODE 1
192.168.2.37 = NODE 2
192.168.2.38 = NODE 3
192.168.2.39 = NODE 5
192.168.2.40 = NODE 6
192.168.2.41 = NODE 4
192.168.2.42 = NODE 7
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
[  7] local 192.168.2.5 port 8080 connected with 192.168.2.37 port 49378
[  4] local 192.168.2.5 port 8080 connected with 192.168.2.38 port 48266
[  5] local 192.168.2.5 port 8080 connected with 192.168.2.41 port 41190
[  6] local 192.168.2.5 port 8080 connected with 192.168.2.42 port 40084
[  9] local 192.168.2.5 port 8080 connected with 192.168.2.39 port 59236
[  8] local 192.168.2.5 port 8080 connected with 192.168.2.40 port 45248
[  9]  0.0-29.1 sec  5.40 MBytes  1.56 Mbits/sec
[  5]  0.0-29.6 sec  8.89 MBytes  2.52 Mbits/sec
[  6]  0.0-29.9 sec  6.45 MBytes  1.81 Mbits/sec
[  8]  0.0-30.0 sec  8.30 MBytes  2.32 Mbits/sec
[  7]  0.0-30.8 sec  12.5 MBytes  3.40 Mbits/sec
[  4]  0.0-30.0 sec  8.93 MBytes  2.49 Mbits/sec
'''):
    ip_to_node = get_ip_to_node() # Get IP to Node mapping
    trial_mapping = {} # Initialized in beginning
    results = [] # List of tuples, (time, data_size, data_speed)
    
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
            data_size = re.search(r'\d+ %s' % data_units, line).group()
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
