# {
#     'm': '',
#     'n': '',
#     'total_givens': '',
#     'bridge_givens': '',

#     'original_clauses': '',
#     'original_literals': '',
#     'learnt_limit': '',
#     'learnt_clauses': '',
#     'learnt_literals': '',
#     'learnt_lit_cl': '',

#     'restarts': '',
#     'conflicts': '',
#     'decisions': '',
#     'propagations': '',
#     'conflict_literals': '',
#     'memory_used': '',
#     'cpu_time': ''
# }

def parse_minisat_output(output, m, n, total_givens, bridge_givens):

    results = output.split('\n')

    packet = {}

    for line in results:
        parsed_line = ' '.join(line.split())
        if line.find('restarts') > -1:
            try:
                packet['restarts'] = parsed_line.split()[2]
            except Exception as e:
                print('Exception in parse_minisat_output + restarts: ', str(e))
        elif line.find('conflicts') > -1:
            try:
                packet['conflicts'] = parsed_line.split()[2]
            except Exception as e:
                packet['conflicts'] = 'NaN'
                print('Exception in parse_minisat_output + conflicts: ', str(e))
        elif line.find('decisions') > -1:
            try:
                packet['decisions'] = parsed_line.split()[2]
            except Exception as e:
                packet['decisions'] = 'NaN'
                print('Exception in parse_minisat_output + decisions: ', str(e))
        elif line.find('propagations') > -1:
            try:
                packet['propagations'] = parsed_line.split()[2]
            except Exception as e:
                packet['propagations'] = 'NaN'
                print('Exception in parse_minisat_output + propagations: ', str(e))
        elif line.find('conflict literals') > -1:
            try:
                packet['conflict_literals'] = parsed_line.split()[3]
            except Exception as e:
                packet['conflict_literals'] = 'NaN'
                print('Exception in parse_minisat_output + conflict_literals: ', str(e))
        elif line.find('Memory used') > -1:
            try:
                #TODO: Add check for
                packet['memory_used'] = parsed_line.split()[3]
            except Exception as e:
                packet['memory_used'] = 'NaN'
                print('Exception in parse_minisat_output + Memory used: ', str(e))
        elif line.find('CPU time') > -1:
            try:
                #TODO: Add check for seconds
                packet['cpu_time'] = parsed_line.split()[3]
            except Exception as e:
                packet['cpu_time'] = 'NaN'
                print('Exception in parse_minisat_output + CPU time: ', str(e))

    packet['m'] = m
    packet['n'] = n
    packet['total_givens'] = total_givens
    packet['bridge_givens'] = bridge_givens

    print("results")
    print("-----------------")
    print (packet)
    print("-----------------")

    return packet
