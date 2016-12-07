# autoscale_trigger.py
Instances need to be scaled up or scaled down based on the load, but before scaling down or up we need to determine if we are over the limit or not this little python script checks the maximum and minimum limits of the autoscale group and act accordingly

# zones.py
Instances in a autoscale group sometimes are spinned off in the same zone, which is not good. We want our replication to be as far as possible physically so that in case of disaster our data on one replication is safe. This script achieve exactly that.

# find_unused_reserved_instances.py
need to find out how much reserved instances are used? if you are under using or over using it. This script would be handy in such scenario.
