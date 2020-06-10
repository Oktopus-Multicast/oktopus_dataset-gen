"""The get_dataset command."""

import os, sys
from random import shuffle

from base import Base # cli

from oktopus.dataset import ensure_dir, read_isp_graph, random_pick, get_ip
from oktopus.dataset import OK_SESSIONS_FILE, OK_NODES_FILE, OK_LINKS_FILE
from oktopus.dataset import dump_objects
from oktopus import Session, Node, Link

class GetDataset(Base):
    """GetDataset"""

    def _create_nodes(self, graph):
        new_servers = []
        for node_id, node_data in graph.node.iteritems():
            lat = node_data.get('Latitude', 0.)
            lon = node_data.get('Longitude', 0.)
            new_server = Node(node_id=int(node_id), lat=lat, lon=lon)
            new_servers.append(new_server)
        return new_servers

    def _create_links(self, graph, nodes):
        new_links = []
        traversed_edges = []
        for node1 in nodes:
            node_edges = graph.edges(str(node1.node_id), data=True)
            for _, neighbor, edge_data in node_edges:
                tmp_nodes = [n for n in nodes if n.node_id == int(neighbor)]
                if tmp_nodes and len(tmp_nodes) == 1:
                    node2 = tmp_nodes[0]
                    if (node1.node_id, node2.node_id) not in traversed_edges:
                        link = Link(link_id='({0}_{1})'.format(node1.node_id, node2.node_id),
                                    src=node1.node_id, dst=node2.node_id,
                                    cap=edge_data.get('Capacity', 0.),
                                    distance=edge_data.get('Distance', 0.),
                                    delay=edge_data.get('Delay', 0.),
                                    port1=edge_data.get('src_port', -1),
                                    port2=edge_data.get('dst_port', -1))
                        traversed_edges.append((node1.node_id, node2.node_id))
                        # traversed_edges.append((node2.node_id, node1.node_id))
                        new_links.append(link)
        return new_links

    def _create_offline_dataset(self, graph, output_directory, sessions_count, receivers_per, bandwidth_per):
        sessions_per_region = int(sessions_count / float(len(graph.nodes())))
        if sessions_per_region == 0:
            sessions_per_region = 1
        if sessions_per_region * len(graph.nodes()) < sessions_count:
            sessions_per_region += 1
            
        ensure_dir(output_directory)
        sessions_file_path = os.path.join(output_directory, OK_SESSIONS_FILE % sessions_count)
        nodes_file_path = os.path.join(output_directory, OK_NODES_FILE)
        links_file_path = os.path.join(output_directory, OK_LINKS_FILE)

        nodes = self._create_nodes(graph)
        links = self._create_links(graph, nodes)
        sessions = []
        receivers_percentage_pdf = [(0.1, .1), (0.2, .2), (0.3, .3), (0.4, .4)]
        if receivers_per != 'variable':
            receivers_percentage_pdf = [(float(receivers_per), 1.0)]
        # 25Mbps, 30Mbps, 50Mbps
        bandwidth_pdf = [(2000000, .21), (7200000, .57), (18000000, .22)]
        if bandwidth_per != 'variable':
            bandwidth_pdf = [(float(bandwidth_per), 1)] 
        session_idx = 1
        for node in graph.nodes():
            node_id = int(node)
            for _ in range(sessions_per_region):
                max_receivers_percentage = random_pick(receivers_percentage_pdf)
                bandwidth = random_pick(bandwidth_pdf)
                max_receivers = int(max_receivers_percentage * len(graph.nodes()))
                # exclude the source
                candidate_dsts = [n.node_id for n in nodes if n.node_id != node_id]
                shuffle(candidate_dsts)
                dsts = candidate_dsts[:max_receivers]
                address = get_ip(session_idx, base='10.1.0.0')
                new_session = Session(addr=address, src=node_id, dsts=dsts, bw=bandwidth, t_class='vod')
                sessions.append(new_session)
                session_idx += 1
                
                if len(sessions) == sessions_count:
                    dump_objects(cls=Session, file_path=sessions_file_path, objects=sessions)
                    dump_objects(cls=Node, file_path=nodes_file_path, objects=nodes)
                    dump_objects(cls=Link, file_path=links_file_path, objects=links)
                    return


        dump_objects(cls=Session, file_path=sessions_file_path, objects=sessions)
        dump_objects(cls=Node, file_path=nodes_file_path, objects=nodes)
        dump_objects(cls=Link, file_path=links_file_path, objects=links)

    def run(self):
        isp_topo_file = self.options.get('-i', None)
        output_directory = self.options.get('-o', None)
        sessions_count = self.options.get('-s', None)
        bandwidth_per = self.options.get('-b', None)
        receivers_per = self.options.get('-r', None)
        isp_topo_file = self.options.get('-i', None)

        isp_graph = read_isp_graph(isp_topo_file)
        if not isp_graph:
            print 'Can\'t read the input graph file...'
            exit(1)

        try:
            sessions_count = int(sessions_count)
        except ValueError as ex:
            print 'Invalid values...'
            print ex
            exit(1)

        self._create_offline_dataset(graph=isp_graph, 
                                output_directory=output_directory, 
                                sessions_count=sessions_count, 
                                receivers_per=receivers_per, 
                                bandwidth_per=bandwidth_per)


