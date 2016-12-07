#!/usr/bin/env python 
#script to find info on the unused and overused instances
import boto.ec2
import sys
region = boto.config.get('Boto', 'ec2_region_name', 'eu-west-1')

ec2_conn = boto.ec2.connect_to_region(region) #getting the ec2 connection object
reservations = ec2_conn.get_all_instances() # get all the reservations
running_instances = {}
for reservation in reservations:
    for instance in reservation.instances:
        if instance.state != "running":
            continue
        elif instance.spot_instance_request_id:
            continue
        else:
            if instance.vpc_id:
                continue
            else:
                az = instance.placement
                instance_type = instance.instance_type
                running_instances[ (instance_type, az ) ] = running_instances.get( (instance_type, az ) , 0 ) + 1


# pprint( running_instances )


reserved_instances = {}
for reserved_instance in ec2_conn.get_all_reserved_instances():
    if reserved_instance.state != "active":
        continue
    else:
        az = reserved_instance.availability_zone
        instance_type = reserved_instance.instance_type
        reserved_instances[( instance_type, az) ] = reserved_instances.get ( (instance_type, az ), 0 )  + reserved_instance.instance_count

# pprint( reserved_instances )


# this dict will have a positive number if there are unused reservations
# and negative number if an instance is on demand
instance_diff = dict([(x, reserved_instances[x] - running_instances.get(x, 0 )) for x in reserved_instances])

# instance_diff only has the keys that were present in reserved_instances. There's probably a cooler way to add a filtered dict here
for placement_key in running_instances:
    if not placement_key in reserved_instances:
        instance_diff[placement_key] = -running_instances[placement_key]

# pprint ( instance_diff )

unused_reservations = dict((key,value) for key, value in instance_diff.iteritems() if value > 0)
if unused_reservations == {}:
    print "Congratulations, you have no unused reservations"
else:
    for unused_reservation in unused_reservations:
        print "UNUSED RESERVATION!\t(%s)\t%s\t%s" % ( unused_reservations[ unused_reservation ], unused_reservation[0], unused_reservation[1] )



unreserved_instances = dict((key,-value) for key, value in instance_diff.iteritems() if value < 0)
if unreserved_instances == {}:
    print "Congratulations, you have no unreserved instances"
else:
    for unreserved_instance in unreserved_instances:
        print "Instance not reserved:\t(%s)\t%s\t%s" % ( unreserved_instances[ unreserved_instance ], unreserved_instance[0], unreserved_instance[1] )
