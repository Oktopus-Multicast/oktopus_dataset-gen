"""The get_sfc_dataset command."""

import os, sys, random
from math import ceil
import numpy as np

from base import Base # cli

from oktopus import load_sessions as ok_load_sessions
from oktopus import App, Session, Node, make_service
from oktopus.dataset import OK_SESSIONS_FILE, OK_NODES_SERVICES_FILE, OK_SESSIONS_SERVICES_FILE
from oktopus.dataset import dump_objects

SERVICES = [1, 2, 3, 4, 5, 6]
ESSENTIAL_SER = [1, 2]
AUXILIARY_SER = [3, 4, 5, 6]


class GetDatasetSfc(Base):
    """GetDatasetSfc"""

    def _create_sfc(self, topo_name, topo_path, in_dir, session_count,
            aux_ser_dis, ord_type, sfc_len,
            num_sessions_with_services, output_dir):

        # Check SFC variable
        is_variable = False
        if sfc_len == "variable":
          is_variable = True
        else:
          sfc_len = int(sfc_len)

        # Load sessions
        sessions_file = os.path.join(in_dir, OK_SESSIONS_FILE)
        sessions = ok_load_sessions(sessions_file % session_count)

        sessions_with_services = random.sample(sessions, num_sessions_with_services)

        # Create a new Oktopus Application
        app = App(topo_name, topo_path)

        # Load sessions to Oktopus App
        app.add_sessions(sessions)

        # Services Placement
        for srv_name in ESSENTIAL_SER:
          node_services = np.random.choice(app.get_nodes(), len(app.get_nodes()), replace=False)
          for node in node_services:
              srv = make_service(str(srv_name), ordered=True, resources_cap_dict={'cpu': 0})
              node.add_service(srv)
        
        for srv_name in AUXILIARY_SER:
          node_services = np.random.choice(app.get_nodes(), int(ceil(aux_ser_dis*len(app.get_nodes()))), replace=False)
          for node in node_services:
              srv = make_service(str(srv_name), ordered=True, resources_cap_dict={'cpu': 0})
              node.add_service(srv)

        # Chain Ordering
        for session in sessions_with_services:
          srv_names = []
          if is_variable:
            sfc_len = list(np.random.choice([3, 4, 5, 6], 1, replace=False)).pop()
          if ord_type == 1:
            while len(srv_names) < sfc_len:
              if len(srv_names) < 2:
                srv_names += list(np.random.choice(ESSENTIAL_SER, min(2, sfc_len), replace=False))
              else:
                srv_names += list(np.random.choice(AUXILIARY_SER, sfc_len-len(srv_names), replace=False))
          else:
            srv_names += list(np.random.choice(ESSENTIAL_SER + AUXILIARY_SER, sfc_len, replace=False))

          for srv_name in srv_names:
              session.mod_resource_req(srv_name, 'cpu', 0)
          session.traverse(srv_names)

        nodes_file_path = os.path.join(output_dir, OK_NODES_SERVICES_FILE )
        sessions_file_path = os.path.join(output_dir, OK_SESSIONS_SERVICES_FILE % session_count)
        dump_objects(cls=Node, file_path=nodes_file_path, objects=app.get_nodes())
        dump_objects(cls=Session, file_path=sessions_file_path, objects=app.get_sessions())

    def run(self):
      topo_name = self.options.get('-t', None)
      graph_path = self.options.get('-i', None)
      input_dir = self.options.get('-d', None)
      output_dir = self.options.get('-o', None)
      sessions_count = self.options.get('-s', None)
      aux_ser_avail_p = float(self.options.get('--aux_ser_avail_p', None))
      ord_type = self.options.get('--ord_type', None)
      sfc_len = self.options.get('--sfc_len', None)
      num_sessions_with_services = int(self.options.get('--sessions-with-services', None))


      self._create_sfc(topo_name, graph_path, input_dir, sessions_count,
          aux_ser_avail_p, ord_type,
          sfc_len,
          num_sessions_with_services, output_dir)
      print('GetDatasetSfc Done!')