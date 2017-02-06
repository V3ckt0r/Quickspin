##Quickspin

Quickspin is a simple CLI tool for spinning up a series of EC2 instances.

###How to install
You can install Quickspin using **pip**

    pip install Quickspin

source install via:

    python setup.py install


####Configure
Quickspin expects to find your aws credentials in ~/.aws folder in a file called "credentials". An example of the file can be seen below:
    
    [default]
    aws_access_key_id = <your_key>
    aws_secret_access_key = <your_secret>

There is a roadmap item to make this setup easier.

####Quick Start
Once installed use you can get help on use Quickspin as follows:

    quickspin -h

You can list all running EC2 instances like so:

    quickspin -l
    ('i-d70f6216', 'puppetmaster', 't2.medium', '52.28.187.12')
    ('i-ff85f13e', 'stage-sumo2siren', 't2.micro', '52.28.161.100')

or all instances like:

    quickspin -la

####Roadmap
- Add config option to setup AWS credentials
- Add method for creating EC2 instances
- Add cloundformation api
- 
