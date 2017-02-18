##Quickspin

Quickspin is a simple CLI tool for spinning up a series of EC2 instances.

###How to install
You can install Quickspin using **pip**

    pip install Quickspin

source install via:

    python setup.py install


####Configure
To configure Quickspin with your credentials follow the example below:
    quickspin -k
    Enter your AWS key:
    Enter your AWS secret:
    What region do you want to connect to? (regions can be found here http://docs.aw    s.amazon.com/general/latest/gr/rande.html):

Thats it, you will be good to go. If you already have your credentials and configuration stored under ~/.aws then you don't need to configure quickspin and doing the above will give you the following output:
    Your credentials are already setup
    Your config is already setup

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
- Add cloundformation api.
