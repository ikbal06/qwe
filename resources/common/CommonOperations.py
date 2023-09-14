import os
import socket
import json
import sys
import gzip
from globalProperties import *


def read_json_file(file_in):
    """Parse json file """
    try:
        with open(file_in) as f:
            parsed_json = json.load(f)
            return parsed_json
    except Exception as e:
        sys.exit("Json file parse error={}".format(e))
        

def create_symlink(src_in, dst_in):
    """It is used to create symlink
     """
    if os.path.exists(dst_in):
        for root, dirs, files in os.walk(src_in):
            for file in files:
                orig_host_vars_yaml = os.path.join(root, file)
                inventory_group_vars = os.path.join(dst_in, file)
                if not os.path.exists(inventory_group_vars):
                    os.symlink(orig_host_vars_yaml, inventory_group_vars)
    else:
        os.symlink(src_in, dst_in)
        
def check_connection(ip_in, port_in):
    """It is used to check socket connection is up or down."""

    test_socket = socket.socket()
    try:
        test_socket.connect((ip_in, port_in))
        print("[OK]{}:{} Connection successfull".format(ip_in, port_in))
    except Exception as e:
        print("[NOK]{}:{} connection failed!!".format(ip_in, port_in))
        sys.exit(e)

def unzip_file(zip_file_in, zip_file_out):
    with gzip.open(zip_file_in, 'rb') as f_in:
         with open(zip_file_out, 'wb') as f_out:
              f_out.write(f_in.read())           