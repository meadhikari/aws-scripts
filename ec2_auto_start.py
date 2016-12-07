from optparse import OptionParser
import boto.ec2

def get_options():
    global options
    parser = OptionParser(usage="usage: %prog [options] start|stop|status", version="%prog 1.0")
    parser.add_option("-r", "--region", 
	help="Region (default eu-west-1)", 
	dest="region", 
	default="eu-west-1")

    parser.add_option("-e", "--environment",  
	help="Service (prod, dev, tmp or all)", 
	dest="environment", 
	default="tmp")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Error: You need to specify an action")
        sys.exit(1)
    else:
        setattr(options, 'action', args[0])

    return options

def main():
    options = get_options()
    action = options.action
    environment_tag = options.environment
    environment_tag = "tmp"
    STOPPED = "stopped"
    RUNNING = "running"
    region = "eu-west-1"
    ami_image_id = 'ami-a10897d6'
    aws_access_key_id = "<NOPE>"
    aws_secret_access_key="<NOPE>"
    conn = boto.ec2.connect_to_region(region,
         aws_access_key_id=aws_access_key_id,
         aws_secret_access_key=aws_secret_access_key)
    reservations = conn.get_all_reservations()
    for reservation in reservations:
    	for instance in reservation.instances:
        	if 'environment' in instance.tags:
            		if environment_tag in instance.tags['environment']:
                		if action == "start" and instance.state == STOPPED:
                    			conn.start_instances(instance_ids=[instance.id])
                    			print "starting "+instance.id
                		elif action == "stop" and instance.state == RUNNING:
                    			conn.stop_instances(instance_ids=[instance.id])
                    			print "stopping "+instance.id
                		elif action == "status":
                    			print "The instance with instance id "+instance.id +" is currently "+instance.state
                		else:
                    			print "Instance already "+ instance.state
            		else:
                		print "No server associated with tag "+ environment_tag+ " found"
if __name__ == "__main__":
    main()
