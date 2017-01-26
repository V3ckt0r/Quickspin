#! /usr/bin/python

import boto3
import argparse
import sys

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

# Set up acceptable arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s","--start", nargs='+', help="List of EC2 ids", required=False)
parser.add_argument("-l", "--list", help="show all EC2 instances running", action="store_true")
parser.add_argument("-v", "--verbose", help="show api call to googleapi", action="store_true")
args = parser.parse_args()

# List running instances
def listRunning():
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        for tag in instance.tags:
            if tag['Key'] == 'Name':
                print(instance.id, tag['Value'], instance.instance_type, instance.public_ip_address)

# Spin up from a list of instances ids
def upIt(instance_list):

    response = client.start_instances( InstanceIds=instance_list, AdditionalInfo='string', DryRun=False)

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print "Instance have all started sucessfully..."
        return 0
    else:
        error_reponse = response['ResponseMetadata']['HTTPStatusCode']
        print "Error code {} returned.".format(error_reponse)
        return 1

def runIt():
    pass

def main():
    if args.start == None:
        print "You must use a flag to tell quickspin what to do... use -h for help"
        sys.exit(1)

    if args.list == True:
        listRunning()
        sys.exit(0)

    upIt(args.start)
    print "thats it"
    sys.exit(0)

if __name__ == "__main__":
    main()
