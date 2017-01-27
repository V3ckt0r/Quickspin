#! /usr/bin/python

import boto3
import argparse
import sys
import inspect

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

# Set up acceptable arguments
parser = argparse.ArgumentParser()
parser.add_argument("-u","--up", nargs='+', help="List of EC2 ids to bring up", required=False)
parser.add_argument("-d","--down", nargs='+', help="List of EC2 ids to bring down", required=False)
parser.add_argument("-l", "--list", help="show all EC2 instances running", action="store_true")
parser.add_argument("-v", "--verbose", help="show api call to googleapi", action="store_true")
args = parser.parse_args()


# List all running instances in Region
def listRunning():
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                print(instance.id, tag['Value'], instance.instance_type, instance.public_ip_address)

# Spin up from a list of instances ids
def upIt(instance_list):

    response = client.start_instances( InstanceIds=instance_list, AdditionalInfo='string', DryRun=False)
    responseCheck(response)

# Bring down from a list of instances ids
def downIt(instance_list):

    response = client.stop_instances( InstanceIds=instance_list, Force=False, DryRun=False)
    responseCheck(response)

# Check the response for a given action and evaluate the calling function from the stack.
def responseCheck(response):
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    callingFrame = calframe[1][3]

    if response['ResponseMetadata']['HTTPStatusCode'] == 200 and callingFrame == "upIt":
        print "Instance have all started sucessfully..."
        return 0
    elif response['ResponseMetadata']['HTTPStatusCode'] == 200 and callingFrame == "downIt":
        print "Instance have all been stopped sucessfully..."
        return 0
    else:
        error_reponse = response['ResponseMetadata']['HTTPStatusCode']
        print "Error code {} returned.".format(error_reponse)
        return 1

def main():
    if len(sys.argv) <= 1:
        print "You must use a flag to tell quickspin what to do... use -h for help"
        sys.exit(1)

    if args.list:
        listRunning()
        sys.exit(0)

    if args.up:
        upIt(args.up)
        sys.exit(0)

    if args.down:
        downIt(args.down)
        sys.exit(0)

    print "thats it"
    sys.exit(0)

if __name__ == "__main__":
    main()
