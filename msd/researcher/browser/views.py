from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from msd.researcher import researcherMessageFactory as _
from msd.researchbase.browser.researcherview import BaseResearcherCollaborationsView, BaseResearcherView, BaseResearcherContactView
        
class MSDResearcherView(BaseResearcherView):

    def getLettersAfterName(self):
        
        return self.context.getPostNominals()
    
    def getGroupName(self):
        
        return self.context.getGroup_name()
    
    def getFundingSources(self):
        
        return self.context.getFundingSources()
        
    def getImageURL(self):
        url = ""
        image = self.context.getImage()
        
        if image != "":
            url = image.absolute_url()
        
        return url

    def getImageURLThumb(self):
        url = ""
        image = self.context.getImage()

        if image != "":
            url = self.context.absolute_url() + '/image_thumb'

        return url

    def getImageURLMini(self):
        url = ""
        image = self.context.getImage()

        if image != "":
            url = self.context.absolute_url() + '/image_mini'

        return url
        
    
    def getImageCaption(self):
        
        return self.context.getImageCaption()
    
class MSDResearcherContactView(BaseResearcherContactView):
    
    def getUnits(self):
        return self.context.getUnits()

        
    def getCollege(self):
        return self.context.getCollege()
        
        
    def getCollegeWithURL(self):
        college = self.getCollege()
        
        return self.collegeData.get(college, {})
    

    def getUrl(self):
        
        webpages = []
        webpage = self.context.getWebpage()
        webpages.append(webpage)
        
        return webpages
    
class MSDResearcherCollaborationsView(BaseResearcherCollaborationsView):
    
    """ """
    def getCollaborations(self):
        """
        return a list of dicts?
        [{fullname:(string),role:(string),url:(valid url),institution:(string),type:(string)},]
        NOTE: we don't include email in this as we want to keep this behind the scenes as much as possible
        the idea is to use it as an identifier
        ORA will only have the fullname in each dict.
        Is there a clever way to ensure that the templates aren't tripped up by this?
        
        """
        
        collaborations = self.context.getCollaborators()
        
        collablist = []
        for line in collaborations:
            if line.has_key('email'):
                del(line['email'])
            collablist.append(line)
        
        return collablist
    
    