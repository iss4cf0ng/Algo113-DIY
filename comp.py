'''
113-1 ALGORITHM DIY ASSIGNMENT

REFREENCE:
    https://www.geeksforgeeks.org/python-program-for-topological-sorting/
    https://docs.python.org/3/library/argparse.html
    https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal

ALGORITHM:
    1. DFS(DEPTH FIRST SEARCH)
    2. TOPOLOGICAL SORT

DATA STRUCTURE:
    1. LIST
    2. QUEUE
    3. COLLECTIONS(GENERIC)

'''

from collections import defaultdict, deque
import argparse
import sys
import os

# ARGUMENT
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Input file')
parser.add_argument('-v', '--verbose', help='Show detail', action='store_true')
parser.add_argument('-o', '--output', help='Output file')
args = parser.parse_args()

# COLOR CODE
class bcolors:
    OKBLUE = '\033[94m' # BLUE [*]
    OKGREEN = '\033[92m' # GREEN [+]
    WARNING = '\033[93m' # YELLOW [!]
    FAIL = '\033[91m' # RED [-]
    ENDC = '\033[0m' # WHITE (RESET)

# CYCLE BREAKER
def break_cycle(edges):
    # BUILD ADJACENCY LIST
    graph = defaultdict(list)
    edge_weights = {}
    for edge in edges:
        start, end, weight = edge
        graph[start].append(end)
        edge_weights[(start, end)] = weight

    # DETECT AND BREAK CYCLE
    def detect_cycle(node, visited:set, rec_stack:set, cycle_edges:list) -> bool:
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                if detect_cycle(neighbor, visited, rec_stack, cycle_edges):
                    cycle_edges.append((node, neighbor))
                    return True
            elif neighbor in rec_stack:
                cycle_edges.append((node, neighbor))
                return True
        
        rec_stack.remove(node)
        return False

    def find_cycle():
        visited = set()
        for node in graph:
            if node not in visited:
                cycle_edges = []
                if detect_cycle(node, visited, set(), cycle_edges):
                    return cycle_edges
        return None

    # BREAK ALL CYCLE
    while True:
        cycle_edges = find_cycle()
        if not cycle_edges:
            break

        # ITERATION, FIND MAXIMUM WEIGHT EDGE
        max_weight = -float('inf')
        edge_to_remove = None
        for edge in cycle_edges:
            weight = edge_weights[edge]
            if weight > max_weight:
                max_weight = weight
                edge_to_remove = edge

        # REMOVE MAXIMUM WEIGHT EDGE
        if edge_to_remove:
            graph[edge_to_remove[0]].remove(edge_to_remove[1])
            del edge_weights[edge_to_remove]

    # Rebuild the edge list after breaking cycles
    final_edges = []
    for start, neighbors in graph.items():
        for end in neighbors:
            final_edges.append([start, end, edge_weights[(start, end)]])
    return final_edges

def topological_sort(edges):
    # BUILD ADJACENCY LIST AND IN-DEGREE MAPPING
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    # GRAPH INITIALIZATION
    vertices = set()
    for edge in edges:
        start, end, weight = edge
        graph[start].append(end)
        in_degree[end] += 1
        vertices.add(start)
        vertices.add(end)
    
    for vertex in vertices:
        if vertex not in in_degree:
            in_degree[vertex] = 0

    queue = deque([v for v in vertices if in_degree[v] == 0])
    topological_order = []

    while queue:
        current = queue.popleft()
        topological_order.append(current)

        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(topological_order) == len(vertices):
        return topological_order
    else:
        raise ValueError("Graph is not a DAG (contains a cycle)")

# PRINT MESSAGE WITH COLOR
# PRINT INFORMATION
def pf_info(msg):
    print(f'{bcolors.OKBLUE}[*]{bcolors.ENDC} {msg}')
# PRINT ERROR MESSAGE
def pf_err(msg):
    print(f'{bcolors.FAIL}[-]{bcolors.ENDC} {msg}')
# PRINT OK(SUCCESSFUL) MESSAGE
def pf_ok(msg):
    print(f'{bcolors.OKGREEN}[+]{bcolors.ENDC} {msg}')
# PRINT WARNING MESSAGE
def pf_warn(msg):
    print(f'{bcolors.WARNING}[!]{bcolors.ENDC} {msg}')
# PRINT VERBOSE MESSAGE
def pf_v(msg, mode = 'i'):
    if args.verbose:
        if mode == 'i':
            pf_info(msg)
        elif mode == 'w':
            pf_warn(msg)
        elif mode == 'o':
            pf_ok(msg)

# INITIALIZATION
def init():
    if 'nt' in os.name:
        os.system('color')
        pf_v('Enabled color')

    pf_info('-' * 60)
    pf_ok('\t\t[Simple Compiler Optimization]\t\t')
    pf_info('-' * 60)

    # USER INPUT NOTHING
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)

def main():
    try:
        # INIT
        init()

        # PROCESS INPUT FILE
        edges = []
        pf_v(f'File: {args.file}')
        with open(args.file, 'r') as f:
            for line in f.readlines():
                line = line.strip().split()
                edges.append([int(x) for x in line])
                # VALIDATE INPUT DATA
                if len(edges[len(edges) - 1]) != 3:
                    raise Exception('Format error: ' + edges[len(edges) - 1])
        
        # CHECK INPUT DATA
        if len(edges) == 0:
            pf_warn('Empty file')

        # REMOVE DUPLICATE EDGE
        unique_list = []
        red_list = []
        pf_v('Checking duplicate edge')
        for edge in edges:
            if edge not in unique_list:
                unique_list.append(edge)
            else:
                red_list.append(edge)

        # CHECK DUPLICATE
        if len(edges) != len(unique_list):
            pf_v('Exist duplicate edge', 'w')
        edges = unique_list

        # REMOVE AMBIGUOUS EDGE
        pf_v('Checking ambiguous edge')
        for i in range(0, len(edges)):
            for j in range(i, len(edges)):
                if edges[i][0] == edges[j][0] and edges[i][1] == edges[j][1] and edges[i][2] != edges[j][2]:
                    raise Exception(f'Exist ambiguous edge: {edges[i]} and {edges[j]}')
                
        # DETECT NON-POSITIVE WEIGHT
        for i in range(0, len(edges)):
            edge = edges[i]
            if edge[2] <= 0:
                raise Exception(f'Non-positive edge is forbidden: {edge}')

        pf_v(f'Removed repeated import libraries.(Breaking cycle):\n\t{red_list}')

        break_cycle(edges)

        updated_edges = break_cycle(edges)

        pf_v(f'Updated edges.(After breaking cycles): {updated_edges}')
        pf_v('Sorting import libraries.(Topological sort)')

        try:
            topo_order = topological_sort(updated_edges)
            pf_ok('Import order:\n ' + '\n'.join([f'\t=> {x}' for x in topo_order]))

            if args.output:
                with open(args.output, 'w') as f:
                    f.write('\n'.join([str(x) for x in topo_order]))
                pf_ok('Saved result: ' + args.output)

        except ValueError as e:
            raise e
    except Exception as e:
        pf_err(e)

if __name__ == "__main__":
    main()