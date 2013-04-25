import requests
import sys
import argparse
from xml.dom import minidom

from StoryRenderer import StoryRenderer

class Tracker:
  def __init__(self, helper):
    self.helper = helper
    
  def reloadDetailsOfProjects(self):
    self.project_details = {}
    r = self.helper.get("projects")
    r_xml = minidom.parseString(r.text)
    projects_xml = r_xml.getElementsByTagName("project")
    for p in projects_xml:
      name = self.helper.getXMLElementData(p,"name")
      pid = int(self.helper.getXMLElementData(p,"id"))
      last_update = self.helper.getXMLElementData(p,"last_activity_at")
      self.project_details.update({name: {"name": name, 
        "id": pid, 
        "last_activity_at": last_update}})

  def getProjectIDByName(self, project_name):
    return self.project_details[project_name]["id"] 

class Project:
  def __init__(self, helper, pid):
    self.helper = helper
    self.pid = pid
    self.stories = {}

  def reinitialiseAllStories(self):
    self.stories = {}
    r = self.helper.get("projects/%s/stories" % (self.pid))
    r_xml = minidom.parseString(r.text)
    stories_xml = r_xml.getElementsByTagName("story")
    for s in stories_xml:
      story_id = int(self.helper.getXMLElementData(s, "id"))
      self.stories.update({story_id: Story(self, story_id)})
      
  def reloadDetailsOfAllStories(self):
    for story in self.stories.values():
      story.reloadStoryDetails()
    self.setIterationOfAllStories()
    
  def setIterationOfAllStories(self):
    # A bit of a hack because Pivotal Tracker does not report whether a story
    # is in the backlog, current or done.  Currently cannot spot if a story is
    # in the icebox.
    for iteration in ["current", "backlog", "done"]:
      r = self.helper.get("projects/%s/iterations/%s" % (self.pid, iteration))
      r_xml = minidom.parseString(r.text)
      stories_xml = r_xml.getElementsByTagName("story")
      for s in stories_xml:
        story_id = int(self.helper.getXMLElementData(s, "id"))
        self.stories.setdefault(story_id, Story(self, story_id)).setIteration(iteration)
      
      
class Story:
  def __init__(self, parent_project, story_id):
    self.parent_project = parent_project
    self.story_id = story_id
    self.details = {}
    self.helper = parent_project.helper
  
  def __str__(self):
    s = ""
    for (k,v) in self.details.iteritems():
      s += "%s:\t%s\n" % (k,v)
    if len(s) == 0:
      s = "id:\t%s" % (self.story_id)
    else:
      s = s[:-1]
    return s  
  
  def reloadStoryDetails(self):
    self.details = {}
    r = self.parent_project.helper.get("projects/%s/stories/%s" % 
      (self.parent_project.pid, self.story_id))
    r_xml = minidom.parseString(r.text)
    story_xml = r_xml.getElementsByTagName("story")[0]
    
    name = self.helper.getXMLElementData(story_xml,"name")
    description = self.helper.getXMLElementData(story_xml,"description")
    owned_by = self.helper.getXMLElementData(story_xml,"owned_by")
    labels = self.helper.getXMLElementData(story_xml,"labels")
    requester = self.helper.getXMLElementData(story_xml,"requested_by")
    self.details = {"id": self.story_id, 
      "name": name,
      "description": description,
      "owned_by": owned_by,
      "labels": labels,
      "requester": requester}
       
      
  def setIteration(self, iteration):
    self.details.update({"iteration": iteration})
  
class PivotalAPIHelper:
  def __init__(self, api_credential, base_url=None):
    self.api_credential = api_credential
    self.headers={'X-TrackerToken' : self.api_credential}
    if base_url == None:
      base_url = "https://www.pivotaltracker.com/services/v3/"
    self.base_url = base_url
  
  def get(self, url_suffix=""):
    return requests.get(self.base_url + url_suffix,
      verify = True,
      headers = self.headers) 
  
  def getXMLElementData(self, the_xml, tag_name):
    results = the_xml.getElementsByTagName(tag_name)
    if len(results) == 0:
      return ""
    elif results[0].firstChild == None:
      return ""
    else:
      return results[0].firstChild.data
    
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("token", help="Your Pivotal Tracker API Token from 'www.pivotaltracker.com/profile'")
  parser.add_argument("pid", help="Your Project ID (e.g. www.pivotaltracker.com/s/projects/<pid>)", type=int)
  parser.add_argument("-o", "--output", help="The HTML file you want to output to", default=None)
  args = parser.parse_args() 
  api_token = args.token
  
  helper = PivotalAPIHelper(api_token)
  tracker = Tracker(helper)
  tracker.reloadDetailsOfProjects()
  pid = args.pid
  print('Getting all stories for project %s' % pid)
  project = Project(helper, pid)
  project.reinitialiseAllStories()
  project.reloadDetailsOfAllStories()
  story_renderer = StoryRenderer()
  story_renderer.render(project.stories.values(), file_name=args.output) # renderer needs a list of stories
