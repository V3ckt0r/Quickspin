#! /usr/bin/python

import boto3
import argparse
import sys
import inspect
import getpass
import os.path
from os.path import expanduser

# Set up acceptable arguments
parser = argparse.ArgumentParser()
parser.add_argument("-u","--up", nargs='+', help="List of EC2 ids to bring up", required=False)
parser.add_argument("-d","--down", nargs='+', help="List of EC2 ids to bring down", required=False)
parser.add_argument("-c", "--config", help="Configure Quickspin with your AWS credentials", action="store_true")
parser.add_argument("-l", "--list", help="Show all EC2 instances running", action="store_true")
parser.add_argument("-la", "--listall", help="Show all EC2 instances running", action="store_true")
args = parser.parse_args()

# Configure AWS credentials 
def configaws():

    # User's home
    home = expanduser("~")

    # create aws credentials file
    if os.path.isfile(home+"/.aws/credentials"):
        print "Your credentials are already setup"
    else:
        aws_key = raw_input("Enter your AWS key: ")
        aws_secret = getpass.getpass(prompt='Enter your AWS secret: ')

        file_name = os.path.join(home+"/.aws/", "credentials")
        file = open(file_name, "w")
        file.write("[default]")
        file.write("\n")
        file.write("aws_access_key_id = {}".format(aws_key))
        file.write("\n")
        file.write("aws_secret_access_key = {}".format(aws_secret))
        file.write("\n")
        file.close()

    # create AWS config file
    if os.path.isfile(home+"/.aws/config"):
        print "Your config is already setup"
    else:
        aws_region = raw_input("What region do you want to connect to? (regions can be found here http://docs.aws.amazon.com/general/latest/gr/rande.html): ")
        conf_file_name = os.path.join(home+"/.aws/", "config")
        conf_file = open(conf_file_name, "w")
        conf_file.write("[default]")
        conf_file.write("\n")
        conf_file.write("# AWS regions")
        conf_file.write("\n")
        conf_file.write("region = {}".format(aws_region))
        conf_file.write("\n")
        conf_file.close()

# Establish boto connections
def connect():
    ec2 = boto3.resource('ec2')
    client = boto3.client('ec2')

# List all instance in Region using client
def listAllRunning():
    response = client.describe_instances()
    print "InstanceID        Tags        InstanceType          PrivateIP                LaunchTime"
    for i in response["Reservations"]:
        for ins in i["Instances"]:
            print(ins["InstanceId"], ins["Tags"][0]["Value"], ins["InstanceType"], ins["PrivateIpAddress"]), ins["LaunchTime"], "\n"

# List all rinstance in Region using resource
def listAllRunningRes():
    instances = ec2.instances.filter(InstanceIds=[])
    try:
        for i in instances:
            print i
    except boto3.exceptions.botocore.exceptions.EndpointConnectionError:
        print "Check that you have internet connection and the correct proxy settings"

# List all running instances in Region
def listRunning():
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    try:
        for instance in instances:
            for tag in instance.tags:
                if tag['Key'] == 'Name':
                    print(instance.id, tag['Value'], instance.instance_type, instance.public_ip_address)
    except boto3.exceptions.botocore.exceptions.EndpointConnectionError:
        print "Check that you have internet connection and the correct proxy settings"

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

    if args.config:
        configaws()
        sys.exit(0)

    if args.list:
        connect()
        listRunning()
        sys.exit(0)

    if args.listall:
        connect()
        listAllRunning()
        sys.exit(0)

    if args.up:
        connect()
        upIt(args.up)
        sys.exit(0)

    if args.down:
        connect()
        downIt(args.down)
        sys.exit(0)

    print "An error occured"
    sys.exit(1)


if __name__ == "__main__":
    main()