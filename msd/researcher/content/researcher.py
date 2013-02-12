"""Definition of the Researcher content type
"""
from AccessControl import ClassSecurityInfo
from Products.CMFCore import permissions

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from msd.researcher.content.schemata import mainSchema
from msd.researcher.content.schemata import researchSchema
from msd.researcher.content.schemata import biographySchema
from msd.researcher.content.schemata import collaborationSchema
from msd.researcher.content.schemata import contactSchema
from msd.researcher.content.schemata import affiliationsSchema
from msd.researcher.content.schemata import imageSchema

from msd.researchbase.interfaces import IResearcher
from msd.researchbase.content.researchschemas import classificationSchema

from Products.CMFPlone.utils import normalizeString

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.DataGridField.CheckboxColumn import CheckboxColumn

from Products.Archetypes.Schema import getSchemata

from msd.researcher import researcherMessageFactory as _

from msd.researchbase.utilities import getResearcherSettings
from msd.researchbase.content import defaultlists
from msd.researchbase.content.base import ResearcherMixin

# -*- Message Factory Imported Here -*-


from msd.researcher.interfaces import IMSDResearcher
from msd.researcher.config import PROJECTNAME

from Acquisition import ImplicitAcquisitionWrapper
from Products.Archetypes.interfaces import ISchema


ResearcherSchema = folder.ATFolderSchema.copy() + \
    mainSchema.copy() + \
    researchSchema.copy () + \
    affiliationsSchema.copy() + \
    biographySchema.copy () + \
    imageSchema.copy () + \
    collaborationSchema.copy () + \
    classificationSchema.copy () + \
    contactSchema.copy ()

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

ResearcherSchema['title'].widget.label = "Full Name"
ResearcherSchema['title'].widget.description = "This is the name which will appear at the top of your web page (do not include title or letters after the name, these  \
                        will be added automatically). You may wish to change this to the formal name you use for publications (e.g. John T. Smith)"
          

ResearcherSchema['description'].schemata = 'Research Summary'
ResearcherSchema['description'].widget.description = 'One or two lines indicating your main subject areas. Important.'
ResearcherSchema['description'].widget.rows = 3


schemata.finalizeATCTSchema(
    ResearcherSchema,
    folderish=True,
    moveDiscussion=False
)


for field in ResearcherSchema.values():
    # setCondition() is in Products.Archetypes.Widget
    # possible expression variables are_ object, portal, folder. 
    #field.widget.setCondition("python:object.restrictedTraverse('@@msd_widget_condition').isWidgetAvailable(" + field.getName() + ")")
    field.widget.setCondition("python:object.restrictedTraverse('@@msd_widget_condition')('" + field.schemata + "', '" + field.getName() + "')")


class Researcher(folder.ATFolder, ResearcherMixin):
    """A researcher base class """
    implements(IMSDResearcher, IResearcher)

    meta_type = "Researcher"
    schema = ResearcherSchema


    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        if 'title' not in kwargs:
            
            #kwargs['title'] = self.getImageCaption()
            #TODO: Why the style over this didn't work?
            kwargs['title'] = self.imageCaption
        image = self.getField('image')
        
        if image:
            return self.getField('image').tag(self, **kwargs)
        
        return ""
    
    def getSortableName(self):
        """Get the name in reverse for sorting"""
        name = None
        first = self.first_name
        last = self.last_name
        if first:
            name = normalizeString(last + ' ' + first)
        else:
            name = normalizeString(last)
        self.plone_log('SORTABLE NAME: %s (%s, %s)' % (name, first, last))
        return name
             
    def getPostNominals(self):
        """
        Posher accessor for letters_after_name
        """
        
        try:
            return self.getLetters_after_name()
        except KeyError:
            # workaround

            #          File "/Users/moo/code/oxford/eggs/Zope2-2.12.18-py2.6-macosx-10.6-i386.egg/Products/ZCatalog/Catalog.py", line 417, in recordify
            #            if(attr is not MV and safe_callable(attr)): attr=attr()
            #          File "/Users/moo/code/oxford/src/msd.researcher/msd/researcher/content/researcher.py", line 114, in getPostNominals
            #            return self.getLetters_after_name()
            #          File "/Users/moo/code/oxford/eggs/Products.Archetypes-1.6.6-py2.6.egg/Products/Archetypes/ClassGen.py", line 56, in generatedAccessor
            #            return schema[name].get(self, **kw)
            #          File "/Users/moo/code/oxford/eggs/Products.Archetypes-1.6.6-py2.6.egg/Products/Archetypes/Schema/__init__.py", line 237, in __getitem__
            #            return self._fields[name]
            #        KeyError: 'letters_after_name'            
            
            return ""
            
    def getJobTitle(self):
        """
        Concatenating lines into a string
        """
        
        JobTitles = self.getJob_titles()
        
        return ", ".join(JobTitles)

    def getJob_titles(self):
        """
        XXXX: Fix me (somehow?)
        """
        
        #- URL: file:/home/moo/code/oxford/src/msd.researchertemplates/msd/researchertemplates/skins/msd_researcher/researcher_listing_macros.pt
        #- Line 25, Column 18
        #- Expression: <PythonExpr ', '.join(item_object.getJob_titles())>
        return ""

    def Schema(self):
        """
        Must have this one here or Archetypes will overwrite this fuction with default one.
        """
        return ResearcherMixin.Schema(self) 
    
    def SearchableText(self):
        return ResearcherMixin.SearchableText(self)


    def getCollegeSearchableText(self):
        """ Convert stored college data to searchable text """        
        return self.getCollege()

    def getUnitsSearchableText(self):
        """ Convert stored unit data to searchable text """
                
        units = self.getUnits()
        if not units:
            return ""
        
        return " ".join(units)
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Researcher, PROJECTNAME)
