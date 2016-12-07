#This script given a aws hostname and option to either scale up or scale down, does the work.

from optparse import OptionParser
import boto.ec2
import boto.ec2.autoscale
usage = "script.py -i hostname -s scale"
region = boto.config.get('Boto', 'ec2_region_name', 'us-east-1')
parser = OptionParser(usage)
parser.add_option("-i", "--host", dest="hostname",help="give the hostname to scale")
parser.add_option("-s", "--scale", dest="scale",help="scale host either 'up' or 'down'")
(options, args) = parser.parse_args()

def get_asgroup(region,hostname):
    """takes region and hostname as argument returns the autoscale group of the hostname"""
    conn = boto.ec2.connect_to_region(region) #getting the ec2 connection object
    reservations = conn.get_all_instances() # get all the reservations
    instances = [i for r in reservations for i in r.instances] #here we use pythin list comprehension to get an array with all instances
    for i in instances: #looping through all the instances
        if "Name" in i.tags and hostname in i.tags['Name']: # checking the tags array of instance object to find instance with the hostname
            return i.tags["aws:autoscaling:groupName"] # returns the autoscale group of our hostname
        
def get_current_stats(region,asgroup):
    """takes region and asgroup as argument returns the group object"""
    autoscale = boto.ec2.autoscale.connect_to_region(region)
    group = autoscale.get_all_groups([str(asgroup)])[0]
    return group

def scale_up_or_down(up_or_down, group):
    if (up_or_down == "UP"):
    if (len(group.instances) == group.max_size):
        print "We gotta send email as we reached max size"
        elif (len(group.instances) < group.max_size):
            group.desired_capacity = group.desired_capacity + 1
            group.update()
            print "Increased Desired capacity"
        else:
            print "scale up triggered no action done"
    elif (up_or_down == "DOWN"):
    if (len(group.instances) <= group.min_size):
            print "Current Instance Equal min size. What are we doing here?"
        elif (len(group.instances) > group.min_size):
            group.desired_capacity = group.desired_capacity -1
            group.update()
                print "Decreased Desired capacity"
        else:
            print "scale down triggered no action done"

if options.hostname == None or options.scale == None:
    parser.print_help()
else:    
    hostname = options.hostname
    scale = options.scale.upper()
    
    if (scale == "DOWN" or scale == "UP"):
        asgroup = get_asgroup(region,hostname) #getting the asgroup object
        group = get_current_stats(region,asgroup) #get current stats
    try:
            scale_up_or_down(scale,group)
    except BotoServerError:
            print "Operation could not be completed because of invalid operation request"
    else:
        parser.print_help()


