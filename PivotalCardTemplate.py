"""
Based on https://github.com/psd/pivotal-cards but with none of the finesse

"""

options = {
  "filing-colours": True,
  "rubber-stamp": True,
  "double-sided": True,
  "white-backs": True
}

options_classes = ""

for (k,v) in options.iteritems():
  if v == True:
    options_classes += "%s " % k
    
if len(options_classes) > 0:
  options_classes = options_classes[:-1] #remove the final whitespace

options_classes = 'class="%s"' % options_classes

main = """<html>
  <head>
    <title>Pivotal Tracker Printable Cards</title>
    <link rel="stylesheet" href="pivotal-cards.css" type="text/css" />
  </head>
  <body>
    <div id="pivotal-cards-pages" %(options_classes)s>
      %(body)s
    </div>
  </body>
</html>"""

front_card = """
<div class="%(story_type)s card" id="front-%(cardno)s">
  <div class="front side">
    <div class="header">
      <span class="labels">
        %(labels)s
      <span>
    </div>
    <div class="middle">
      <div class="story-title">%(name)s</div>
      <div class="story-type">%(story_type)s</div>
    </div>
    <div class="footer">
      <span class="epic_name">%(epic_name)s</span>
      <span class="points points%(points)s"><span>%(points)s</span></span>
    </div>
  </div>
</div>"""

back_card = """
<div class="%(story_type)s card" id="back-%(cardno)s">
  <div class="back side">
    <div class="header">
      <span class="project">%(project_name)s</span>
      <span class="id">%(id)s</span>
    </div>
    <div class="middle">
      <div class="story-title">%(name)s</div>
      <div class="description">%(description)s</div>
      <table class="tasks">
        %(tasks)s
      </table>
    </div>
    <div class="footer">
      <span class="requester">%(requester)s</span>
      <span class="owner">%(owned_by)s</span>
    </div>
  </div>
</div>"""

front_page = """
<div class="page fronts">%(front)s
</div>"""
back_page = """
<div class="page backs">%(back)s
</div>""" 
