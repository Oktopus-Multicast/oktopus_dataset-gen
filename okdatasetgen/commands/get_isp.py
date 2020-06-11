"""The get_isp command."""

import os
import sys

from networkx import write_graphml, relabel_nodes, MultiDiGraph
from vincenty import vincenty

from base import Base # cli

from oktopus.dataset import read_isp_graph, get_resources_file, parse_capacities

class GetIsp(Base):
    """GetIsp"""

    def run(self):
        isp_topology_path = self.options.get('-i', None)
        output_directory = self.options.get('-o', None)
        link_capacity = self.options.get('--link', None)
        medium = self.options.get('--medium', None)

        medium_speed = 0.
        if medium == 'fiber':
            medium_speed = 300*10**6
        elif medium == 'copper':
            medium_speed = 210*10**6
        else:
            try:
                medium_speed = float(medium)
            except ValueError as ex:
                print ex
                print '--medium is either (1) Medium type (fiber or copper) or (2) Medium speed (float)'
                exit(1)
        assert medium_speed > 0

        link = parse_capacities(link_capacity)
        link = 10000000000 # special case

        isp_graph = read_isp_graph(isp_topology_path)
        if not isp_graph:
            print 'Can\'t read the input graph file...'
            exit(1)

        if not isinstance(isp_graph, MultiDiGraph):
            isp_graph = MultiDiGraph(isp_graph)

        has_zero_id = False
        for node, node_data in isp_graph.nodes_iter(data=True):
            try:
                node_data['id'] = int(node)
                if node_data['id'] == 0:
                    has_zero_id = True
            except ValueError as ex:
                print ex
                print 'Node ID should be integer...'
                exit(1)

        for node, node_data in isp_graph.nodes_iter(data=True):
            node_data['id'] += int(has_zero_id)

        relabel_nodes(isp_graph, {node: str(node_data['id']) for node, node_data in isp_graph.nodes_iter(data=True)}, copy=False)

        sorted_nodes = map(str, sorted([int(node) for node in isp_graph]))
        ports = {}
        for node in sorted_nodes:
            s_port = 2
            sorted_neighbors = map(str, sorted([int(x[1]) for x in isp_graph.edges(node)]))
            for neighbor in sorted_neighbors:
                if (node, neighbor) not in ports:
                    ports[node, neighbor] = (s_port, -1)
                    s_port += 1

        for node in sorted_nodes:
            sorted_neighbors = map(str, sorted([int(x[1]) for x in isp_graph.edges(node)]))
            for neighbor in sorted_neighbors:
                if (neighbor, node) in ports:
                    ports[node, neighbor] = (ports[node, neighbor][0], ports[neighbor, node][0])

        max_dist = 0.
        traversed_edges = {}
        for node, node_data in isp_graph.nodes_iter(data=True):
            for n, neighbor, key, data in isp_graph.edges(node, data=True, keys=True):
                edge_key = n, neighbor
                if edge_key not in traversed_edges:
                    src_lat = isp_graph.node[n].get('Latitude', -1)
                    src_lon = isp_graph.node[n].get('Longitude', -1)
                    dst_lat = isp_graph.node[neighbor].get('Latitude', -1)
                    dst_lon = isp_graph.node[neighbor].get('Longitude', -1)
                    if src_lat == -1 or src_lon == -1 or dst_lat == -1 or dst_lon == -1:
                        distance = 1
                    else:
                        distance = 1000 * vincenty((src_lat, src_lon), (dst_lat, dst_lon))
                    delay = 1000.0 * distance / medium_speed
                    if max_dist < distance:
                        max_dist = distance
                    isp_graph.edge[n][neighbor][key] = {'Capacity': link,
                                                        'Distance': distance,
                                                        'Delay': delay,
                                                        'src_port': ports[n, neighbor][0],
                                                        'dst_port': ports[n, neighbor][1],
                                                        'BandwidthCost': 1}
                    traversed_edges[edge_key] = key
                    # traversed_edges[edge_key] = neighbor, n
                else:
                    pass
                    # isp_graph.edge[n][neighbor][traversed_edges[edge_key]]['Capacity'] += link

        for node, node_data in isp_graph.nodes_iter(data=True):
            for n, neighbor, key, data in isp_graph.edges(node, data=True, keys=True):
                if 'Capacity' not in data:
                    del isp_graph.edge[n][neighbor][key]

        write_graphml(isp_graph, get_resources_file(isp_topology_path, output_directory))
        print "GetIsp DONE!"
