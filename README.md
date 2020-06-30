# Oktopus Dataset Generator


This repository contain scripts to generate dataset to run on Oktopus.

## Install

First, download this repository and install the requirements of the Oktopus Dataset Generator by running:

    git clone https://github.com/oktopus-multicast/oktopus_dataset-gen.git
    cd oktopus_dataset-gen
    pip install -r requirements.txt

Then, you need to install the Oktopus Framework module which can be found in this [link](https://github.com/oktopus-multicast/oktopus_framework.git). Replace the `oktopus-framework-module-dir` line of the following command to the location, where the downloaded Oktopus Framework module directory is located. Then run the following command to install the module.

    pip install -e oktopus-framework-module-dir

Install the Oktopus Dataset Generator module by running:

    pip install -e .

## Usage

Oktopus Dataset Generator contain a set of commands which can be view by running:

    okdatasetgen -h

It should output:

```
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
```

## Commands

* ###  okdatasetgen get_isp 

    Given a ISP graph file from the Internet Topology Zoo, it generates a ISP graph file with the given link capacity and link medium.

    Example:

    ```bash
    okdatasetgen get_isp -i data/topology_zoo/AttMpls.graphml -o example/ --link=10000 --medium='fiber'
    ```

    It generates a ISP graph file with the given 10Gbps link capacity and fiber medium.

* ###  okdatasetgen get_dataset 

    Given a ISP graph file created with the `get_isp` command, it generates CSV files containing `sessions_count` number of multicast sessions with each session having `receivers_per` percentage of receivers and `bandwidth_per` bps bandwidth requirement.

    Example:

    ```bash
  okdatasetgen get_dataset -i example/AttMpls_resources.graphml -o example/ -s 10 -r 0.1 -b 2000000
    ```
    
    It generates CSV files containing 10 number of multicast sessions with each session having 10% percentage of the network nodes being receivers and with 2000000 bps bandwidth requirement.

* ###  okdatasetgen get_dataset_sfc

    Given a ISP graph file created with the `get_isp` command and the directory where the dataset created with the command `get_dataset`, it generates CSV files containing the service chain of each multicast session.

    Example:

    ```bash
    okdatasetgen get_dataset_sfc -i example/AttMpls_resources.graphml -t AttMpls -d example/ -o example/ -s 10 --aux_ser_avail_p 0.25 --ord_type 1 --sfc_len 5 --sessions-with-services 10
    ```

    It searches for the CSV files containing 10 number of multicast sessions generated with the `get_dataset` command. It generates service chain for 10 sessions with each service chian of length of 5, order type 1 (partial order type), and 25% of the network nodes deployed auxiliary service function.