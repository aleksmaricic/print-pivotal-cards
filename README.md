print-pivotal-cards
===================

Utility to print cards from Pivotal tracker. 

Tested with Python 2.7.x


1. You will need to install the python requests module
http://docs.python-requests.org/en/latest/


2. Then you will need to get your own API token - this should be at the bottom of your Pivotal user profile page:
https://www.pivotaltracker.com/profile

3. Run python PivotalCardPrinter.py [your api token] [your project ID] [optionally: an html filename to output to]

This will create a HTML file with all stories from that project. 

The file name will default to default_[timestamp].html
It will expect to find pivotal-cards.css in the same directory

Change the paper orientation to landscape when printing this.


Coming up:
- filtering (probably via argparse)
- more data on cards
- prettier cards
- making this simpler, faster, more robust and more useful (whoever gets to it first) 


Thanks to PSD for https://github.com/psd/pivotal-cards
and to Ben T who actually wrote most of this but didn't dare put it here ;-)

