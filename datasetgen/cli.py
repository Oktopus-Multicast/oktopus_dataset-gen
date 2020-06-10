"""
datasetgen

Usage:
  datasetgen get_sfc -i <isp_topology> -t <topo_name> -d <dataset_dir> -o <output_dir> -s <session_count> --aux_ser_avail_p <aux_ser_avail_p> --ord_type <ord_type> --sfc_len <sfc_len> --sessions-with-services <num_sessions_with_services>
  datasetgen get_dataset -i <isp_topology> -o <output_directory> -s <sessions_count> -r <receivers_per> -b <bandwidth_per>
  datasetgen get_isp_dataset -i <isp_topology> -o <output_directory> --link=<link> --medium=<medium>
  datasetgen -h | --help
  datasetgen -v | --version


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
  datasetgen hello

Help:
  For help using this tool, please open an issue on the Github repository:
  https://cs-git-research.cs.surrey.sfu.ca/nsl/ISP/oktopus/dataset-gen
"""
 
 
from inspect import getmembers, isclass
from docopt import docopt
 
from . import __version__ as VERSION
 
def main():
    """Main CLI entrypoint."""
    import commands
    options = docopt(__doc__, version=VERSION)
 
    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for cmd in options.keys():
        if hasattr(commands, cmd) and options[cmd]:
            module = getattr(commands, cmd)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()