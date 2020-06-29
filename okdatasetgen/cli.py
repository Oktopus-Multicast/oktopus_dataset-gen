"""
okdatasetgen

Usage:
  okdatasetgen get_dataset_sfc -i <isp_topology> -t <topo_name> -d <dataset_dir> -o <output_dir> -s <session_count> --aux_ser_avail_p <aux_ser_avail_p> --ord_type <ord_type> --sfc_len <sfc_len> --sessions-with-services <num_sessions_with_services>
  okdatasetgen get_dataset -i <isp_topology> -o <output_directory> -s <sessions_count> -r <receivers_per> -b <bandwidth_per>
  okdatasetgen get_isp -i <isp_topology> -o <output_directory> --link=<link> --medium=<medium>
  okdatasetgen -h | --help
  okdatasetgen -v | --version


Arguments:
  -t <topo_name>          ISP topology name
  -d <dataset_dir>        Dataset directory
  -o <output_directory>   Dataset output directory
  -s <sessions_count>     Maximum sessions count
  -i <isp_topology>       ISP topology file (graphml format)
  -r <receivers_per>      Receivers percentage
  -b <bandwidth_per>      Bandwidth percentage
  --aux_ser_avail_p <aux_ser_avail_p>                   Percentage of auxiliary service available
  --ord_type <ord_type>                                 Chain ordering type
  --sfc_len  <sfc_len>                                  Length of any service chain
  --sessions-with-services <num_sessions_with_services> Number of sessions that require services' 10% - 20%
  --link=<link>                                         Link capacity (Mbps)
  --medium=<medium>                                     Medium type (fiber or copper) or Medium speed (float). Used in ISP network only

Options:
  -h --help     Displays this message
  -v --version  Displays script version

Examples:
  okdatasetgen get_isp -i data/topology_zoo/AttMpls.graphml -o example/ --link=10000 --medium='fiber'
  okdatasetgen get_dataset -i example/AttMpls_resources.graphml -o example/ -s 10 -r 0.1 -b 2000000
  okdatasetgen get_dataset_sfc -i example/AttMpls_resources.graphml -t AttMpls -d example/ -o example/ -s 10 --aux_ser_avail_p 0.25 --ord_type 1 --sfc_len 5 --sessions-with-services 10


Help:
  For help using this tool, please open an issue on the Github repository:
  https://cs-git-research.cs.surrey.sfu.ca/nsl/ISP/oktopus/dataset-gen
"""


from inspect import getmembers, isclass
from docopt import docopt
from commands import CMD_CONSTANTS
 
from . import __version__ as VERSION

def main():
    """Main CLI entrypoint."""    
    options = docopt(__doc__, version=VERSION)
 
    for cmd in options.keys():
      if cmd in CMD_CONSTANTS and options[cmd]:
        command = CMD_CONSTANTS[cmd](options)
        command.run()
