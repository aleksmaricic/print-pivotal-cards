from datetime import datetime
from collections import defaultdict
import itertools

import PivotalCardTemplate as template

class StoryRenderer():
  def __init__(self):
    pass
  
  def constantFactory(self, value):
    return itertools.repeat(value).next
  
  def createDefaultStory(self, story):
    """Makes templating easier.  Default stories are a bit like a dictionary but
    return '' if a key is not found.  This makes the poor man's templating easier"""
    default_story = defaultdict(self.constantFactory(''))
    for (k,v) in story.details.iteritems():
      default_story[k] = v
    return default_story
    
  def render(self, stories, file_name=None, stories_per_page=4):
    if file_name == None:
      file_name = "default_%s.html" % datetime.strftime(datetime.now(),"%Y%m%d-%H%M%S")
    
    if len(stories) == 1:
      stories = [stories]
    
    cardno = 0
    
    front_stories = []
    back_stories = []
    
    for story in stories:
      default_story = self.createDefaultStory(story) # A bit like a dictionary
      default_story["cardno"] = cardno
      front_stories += [template.front_card % default_story]
      back_stories += [template.back_card % default_story]
      cardno+=1
    
    """This is a horrible hack to template some HTML.  Someone competent should
    replace this with a proper framework at their ealiest convenience"""
    
    body = "%(front)s%(back)s%(next_bit)s"      
    cardno = 0
    for (f,b) in zip(front_stories, back_stories):
        if cardno % 4 == 0:
          payload = {'front': '', 'back': '', 'next_bit': template.front_page+template.back_page+"%(next_bit)s"}
          body = body % payload
        payload = {'front': f+"%(front)s", 'back': b+"%(back)s", 'next_bit': "%(next_bit)s"}
        body = body % payload
        cardno+=1
    
    payload = {'front': '', 'back': '', 'next_bit': ''}
    body = body % payload
    
    payload = {'body': body, 'options_classes': template.options_classes}
    html = template.main % payload
    
    with open(file_name, 'w') as f:
      f.write(html.encode('utf-8'))    
