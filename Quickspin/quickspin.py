#! /usr/bin/python

import boto3
import argparse
import sys
import inspect
import getpass
import os.path
import time
from os.path import expanduser

# Set up acceptable arguments
parser = argparse.ArgumentParser()
parser.add_argument("-u","--up", nargs='+', help="List of EC2 ids to bring up", required=False)
parser.add_argument("-d","--down", nargs='+', help="List of EC2 ids to bring down", required=False)
parser.add_argument("-c","--create", nargs='+', help="Create an EC2 instance", required=False)
parser.add_argument("-r","--remove", nargs='+', help="Create an EC2 instance", required=False)
parser.add_argument("-k", "--config", help="Configure Quickspin with your AWS credentials", action="store_true")
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

def createInstance(name,count=1):
    client = boto3.client('ec2')
    ec2 = boto3.resource('ec2')
    user = getpass.getuser()

    # create instance
    instance = ec2.create_instances(
        DryRun=False,
        ImageId='ami-e4c63e8b',
        MinCount=count,
        MaxCount=count,
        KeyName='BDA-graphana',
        InstanceType='t2.small',
        SecurityGroups=[
            'BDA-zen-dev',
        ],
    )
    instance_id = instance[0].id

    # check state of new instance
    response = ''
    state = ''
    info = 'Waiting for instance to start up..'
    while state != "running":
        info += '.'
        print info
        time.sleep(1)
        response = client.describe_instances(InstanceIds=[instance_id])
        state = response[u'Reservations'][0][u'Instances'][0][u'State'][u'Name']

    # Tag new instance
    tag = ec2.create_tags(Resources=[instance_id], Tags=[{'Key':'Name', 'Value': user+"-"+name}])

    if state == "running":
        print "Instance {} created succesfully, instance id is {}".format(user+"-"+name, instance_id)
        return 0
    else:
        print "Something went wrong"
        return 1

# Destroy instance
def deleteInstance(ids):
    ec2 = boto3.resource('ec2')
    try:
        ec2.instances.filter(InstanceIds=ids).terminate()
        for e in ids:
            print "Instance {} terminated...".format(e)
    except boto3.exceptions.botocore.exceptions.ClientError:
        print "Invalid id given, check id is correct and try again"
        sys.exit(1)

# List all instance in Region using client
def listAllRunning():
    client = boto3.client('ec2')
    response = client.describe_instances()
    print "InstanceID        Tags        InstanceType          PrivateIP                LaunchTime"
    for i in response["Reservations"]:
        for ins in i["Instances"]:
            print(ins["InstanceId"], ins["Tags"][0]["Value"], ins["InstanceType"], ins["PrivateIpAddress"]), ins["LaunchTime"], "\n"

# List all running instances in Region
def listRunning():
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    try:
        for instance in instances:
            for tag in instance.tags:
                if tag['Key'] == 'Name':
                    print(instance.id, tag['Value'], instance.instance_type, instance.public_ip_address)
    except boto3.exceptions.botocore.exceptions.EndpointConnectionError:
        print "Check that you have internet connection and the correct proxy settings"
        sys.exit(1)

# Spin up from a list of instances ids
def upIt(instance_list):
    client = boto3.client('ec2')
    response = client.start_instances( InstanceIds=instance_list, AdditionalInfo='string', DryRun=False)
    responseCheck(response)

# Bring down from a list of instances ids
def downIt(instance_list):
    client = boto3.client('ec2')
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

    if args.create:
        createInstance(args.create[0])
        sys.exit(0)

    if args.remove:
        deleteInstance(args.remove)
        sys.exit(0)

    if args.list:
        listRunning()
        sys.exit(0)

    if args.listall:
        listAllRunning()
        sys.exit(0)

    if args.up:
        upIt(args.up)
        sys.exit(0)

    if args.down:
        downIt(args.down)
        sys.exit(0)

    print "An error occured"
    sys.exit(1)


if __name__ == "__main__":
    main()