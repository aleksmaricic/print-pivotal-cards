print-pivotal-cards
===================

Utility to print cards from [Pivotal Tracker](http://www.pivotaltracker.com). 

Tested with Python 2.7.x

1. You will need to install the [python requests module] (http://docs.python-requests.org/en/latest/)

2. Then you will need to get your own API token - this should be at the bottom of your Pivotal user profile page:
https://www.pivotaltracker.com/profile

3. Run 'python PivotalCardPrinter.py [your api token] [your project ID]' 

4. Optional Parameters:
  *  -o, --output [an html filename] - The file you want to output to (defaults to default_[timestamp].html)
  *  -s, --since [a date in mm/dd/yyyy format] - Specifies that you only want Stories created or modified since [date]<don't link> (defaults to the beginning of time)

5. This will create a HTML file with all stories from that project. 

6. Print in landscape

Coming up:
- filtering (probably via argparse) [somewhat done]
- more data on cards
- prettier cards
- making this simpler, faster, more robust and more useful (whoever gets to it first) 

Thanks to PSD for https://github.com/psd/pivotal-cards
