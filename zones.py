#this script help in determinig if all replication inside a autoscale group are in the same or different zones
from optparse import OptionParser
import boto.ec2
import sys
usage = "zones -h hostname"
region = boto.config.get('Boto', 'ec2_region_name', 'eu-west-1')

parser = OptionParser(usage)
parser.add_option("-i", "--hostname", dest="hostname",help="hostname")
(options, args) = parser.parse_args()


def get_all_replication_hostname(hostname):
    """here we get all hostnames that are replication of the given hostname, the assumption is we only have 3 replications"""
    hostname_without_number = hostname[:-2]
    numbers = ["01","02","03"]
    return [hostname_without_number+n for n in numbers]
def get_instance(hostname,region):
    """get instance object for a particular hostname"""
    conn = boto.ec2.connect_to_region(region)
    reservations = conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    for i in instances:
        if "Name" in i.tags:
            return i 
def get_zones_of_instances(hostnames,region):
    """returns an array of zone name for given hostnames"""
    zones = []
    for hostname in hostnames:
        instance = get_instance(hostname,region)
        zones.append(instance.placement)
    return zones
    
def how_many_unique(zones):
     """this function checks how many are replications are in unique zones"""
     return len(zones) - len(set(zones))

if options.hostname == None:
    parser.print_help()
else:    
    hostname = options.hostname
    hostnames = get_all_replication_hostname(hostname)
    zones = get_zones_of_instances(hostnames,region)
    unique_number = how_many_unique(zones)
    if unique_number == 0:
        print "OK - All replications are in different zones" 
        sys.exit(0)
    elif unique_number == 1:
        print "WARNING - Two replications are in same zone"
        sys.exit(1)
    elif unique_number == 2:
        print "CRITICAL - All replications are in same zone"
        sys.exit(2)
    else:
        print "UKNOWN - No information available"
        sys.exit(3)

    

