# -*- coding: utf-8 -*-
#
# File: Schemata.py

# Copyright (c) 2007 by ACDT
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """ACDT <acdt@oucs.ox.ac.uk>"""
__docformat__ = 'plaintext'


from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.CMFCore import permissions

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.Archetypes.atapi import *

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.DataGridField.CheckboxColumn import CheckboxColumn

from msd.researchbase.content import defaultlists


mainSchema = atapi.Schema((

    # atapi.StringField(
    #     # name='strTitle',
    #     name='testSelection',
    #     widget=atapi.SelectionWidget(
    #         label="Test widget",
    #     ),
    #     vocabulary=[],
    #     schemata="Test"
    #     # export_csv=True,
    # ),


    atapi.StringField(
        # name='strTitle',
        name='honorific',
        widget=atapi.SelectionWidget(
            label="Title",
        ),
        vocabulary="getHonorificTitlesVocabulary",
        # export_csv=True,
    ),

    atapi.StringField(
        name='first_name',
#        index="FieldIndex:brains",
        widget=StringWidget(
            label="First Name",
        ),
        # export_csv=True,
    ),

    atapi.StringField(
        name='last_name',
#        index="FieldIndex:brains",
        widget=StringWidget(
            label="Last Name",
        ),
        # searchable=1,
        # export_csv=True,
    ),

    atapi.StringField(
        name='letters_after_name',
        widget=StringWidget(
            label="Letters after name",
        )
    ),
    
# removing isPI field as I don't think we need it
    
#    atapi.BooleanField(
#        name='isPI',
#        index="FieldIndex:brains",
#        widget=BooleanWidget(
#            label="Principal Investigator?",
#            description="Tick this box if you are a PI",
#            label_msgid='Researcher_label_isPI',
#            description_msgid='Researcher_help_isPI',
#            i18n_domain='msd.researcher',
#            condition='python: object.showField("isPI")',
#        ),
#        searchable=0
#    ),

# Note I've converted two fields here (job_title and univ_job_title)
# to a single linesfield
    
    atapi.LinesField(
        name='job_titles',
        widget=LinesWidget(
            label="Job Title",
            description="Enter your job titles here one per line",
        ),
        schemata="Affiliations",
        # export_csv=True,
    ),

    # atapi.StringField(
    #     name='univ_job_title',
    #     widget=StringWidget(
    #         label="University Job Title",
    #         description="Your University job title, if applicable",
    #         label_msgid='Researcher_label_univ_job_title',
    #         description_msgid='Researcher_help_univ_job_title',
    #         i18n_domain='msd.researcher',
    #         size=50,
    #     ),
    #     schemata="Affiliations"
    # ),
    
# These fields are hardly used and the 'categories' 
# fields could be deployed instead
    
#    atapi.StringField(
#        name='status',
#        index="FieldIndex:brains",
#        widget=atapi.SelectionWidget(
#            label="Status",
#            description="Useful for grouping people according to University status (not displayed)",
#            label_msgid='Researcher_label_status',
#            description_msgid='Researcher_help_status',
#           i18n_domain='msd.researcher',
#            condition='python: object.showField("status")',
#        ),
#        schemata="Affiliations",
#        searchable=1,
#       vocabulary=[]
#    ),

#    atapi.StringField(
#        name='localstatus',
#        index="FieldIndex:brains",
#       widget=atapi.SelectionWidget(
#            label="Unit Category",
#            description="Useful for creating an organised department list with subheadings.",
#            label_msgid='Researcher_label_localstatus',
#            description_msgid='Researcher_help_localstatus',
#            i18n_domain='msd.researcher',
#            condition='python: object.showField("localstatus")',
#        ),
#        schemata="Affiliations",
 #       vocabulary=[]
 #   ),

    atapi.StringField(
        name='oxford_username',
        widget=StringWidget(
            label="Oxford Username",
            description="Oxford Username (not displayed)",
        ),
        schemata="Affiliations",
        # export_csv=True,
    ),
    
# NB I've removed here University card ID 
# and imsu_username as they aren't used

),
)

researchSchema = atapi.Schema((
    
    atapi.StringField(
        name='group_name',
        widget=StringWidget(
            label="Group Name",
            description="If you are a PI, enter the name of your group (optional).",
            size=50,
        ),
        schemata="Research Summary"
    ),
    
    # atapi.TextField(
    #     name='institution',
    #     widget=StringWidget(
    #         label="Institution",
    #         description="University or research institution",
    #         label_msgid='Researcher_label_institution',
    #         description_msgid='Researcher_help_institution',
    #         i18n_domain='msd.researcher',
    #         condition='python: object.showField("institution")',
    #     ),
    #     schemata="Affiliations",
    #     searchable=1
    # ),

    atapi.TextField(
        name='summary',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Summary",
            description="Enter a short summary of your research activities here. If you want to separate out biographical information use the biography section.",
         ),
        default_output_type="text/x-html-safe",
        schemata="Research Summary",
        # searchable=1
    ),
    
    DataGridField('fundingSources',
                searchable = True,
                columns=("fundingbody", "url", "startYear", "endYear"),
                widget = DataGridWidget(
                    label='Sources of Funding and Grants',
                    description='Enter your major sources of funding. Use the "from" column for a single year.',
                    columns={
                        'fundingbody' : Column("Funding Body"),
                        'url' : Column("URL of funding body if available"),
                        'startYear' : Column("From (year) - optional"),
                        'endYear' : Column("To (year) - optional"),
                    },
                 ),
                schemata = "Research Summary",
         ),

    #  atapi.StringField(
    #     name='country_of_research',
    #     index="FieldIndex:brains",
    #     widget=atapi.SelectionWidget(
    #         label="Country of Research",
    #         label_msgid='Researcher_label_country_of_research',
    #         i18n_domain='msd.researcher',
    #         condition='python: object.showField("country_of_research")',
    #     ),
    #     vocabulary=[],
    #     schemata="Research Summary",
    #     # export_csv=True,
    # ),
    # 
    # atapi.TextField(
    #     name='interests',
    #     allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
    #     widget=RichWidget(
    #         label="Interests",
    #         description="Enter a short summary of your personal interests here",
    #         label_msgid='Researcher_label_interests',
    #         description_msgid='Researcher_help_interests',
    #         i18n_domain='msd.researcher',
    #         condition='python: object.showField("interests")',
    #     ),
    #     default_output_type="text/x-html-safe",
    #     schemata="Research Summary",
    #     searchable=1
    # ),
         
),
)

biographySchema = atapi.Schema((
         
    atapi.TextField(
        name='biography',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Biography",
            description="A short biographical description (optional)",
        ),
        rows="3",
        schemata="Biography",
        # searchable=1,
        default_output_type="text/x-html-safe"
    ),
    
    DataGridField('academicBackground',
        searchable = True,
        columns=("award", "institution", "url", "startYear", "endYear"),
        widget = DataGridWidget(
            label='Awards and Qualifications',
            description='Enter your awards and qualifications. Use the "from" column for a single year.',
            columns={
                'award' : Column("Award or Qualification"),
                'institution' : Column("Awarding Institution"),
                'url': Column("Institution Website"),
                'startYear' : Column("From (year)"),
                'endYear' : Column("To (year)"),
            },
         ),
        schemata = "Biography",
    ),
    
),
)

contactSchema = atapi.Schema((

    atapi.StringField(
        # name='url',
        name='webpage',
        widget=StringWidget(
            label="Web Page",
            description="Enter the URL of your personal webpage",
            size=50,
        ),
        schemata="Contact",
        # export_csv=True,
        validators="isURL"
    ),
    
    # don't see a need to split this field up - exact address details are
    # stored in other systems, we don't need granulated storage

# NB should this be a string field or a lines field????
    
    atapi.StringField(
        name='contact_address',
        widget=StringWidget(
            label="Address",
            description = "Your mailing address.",
        ),
        schemata="Contact",
    ),
    
    
    # atapi.StringField(
    #     name='contact_address',
    #     widget=ComputedWidget(
    #         label="Address",
    #         description = "Your mailing address. If you want to change this, please enter new values in the following street/town/county fields and then clear this field.",
    #         label_msgid='Researcher_label_contact_address',
    #         description_msgid='Researcher_help_contact_address',
    #         i18n_domain='msd.researcher',
    #         visible=True,
    #     ),
    #     schemata="Contact",
    #     # export_csv=True,
    # ),
    # 
    # # ADDRESS START
    # atapi.StringField(
    #     name='contact_address_street1',
    #     widget=StringWidget(
    #         label="Address (Street 1)",
    #         label_msgid='Researcher_label_contact_address_street1',
    #         i18n_domain='msd.researcher',
    #     ),
    #     schemata="Contact",
    #     # export_csv=True,
    # ),
    # atapi.StringField(
    #     name='contact_address_street2',
    #     widget=StringWidget(
    #         label="Address (Street 2)",
    #         label_msgid='Researcher_label_contact_address_street2',
    #         i18n_domain='msd.researcher',
    #     ),
    #     schemata="Contact",
    #     # export_csv=True,
    # ),
    # atapi.StringField(
    #     name='contact_address_street3',
    #     widget=StringWidget(
    #         label="Address (Street 3)",
    #         label_msgid='Researcher_label_contact_address_street3',
    #         i18n_domain='msd.researcher',
    #     ),
    #     schemata="Contact",
    #     # export_csv=True,
    # ),
    # atapi.StringField(
    #     name='contact_address_town',
    #     widget=StringWidget(
    #         label="Address (Town/City)",
    #         label_msgid='Researcher_label_contact_address_town',
    #         i18n_domain='msd.researcher',
    #     ),
    #     schemata="Contact",
    #     # export_csv=True,
    # ),
    # atapi.StringField(
    #     name='contact_address_county',
    #     widget=StringWidget(
    #         label="Address (County/Region/Area)",
    #         label_msgid='Researcher_label_contact_address_county',
    #         i18n_domain='msd.researcher',
    #     ),
    #     schemata="Contact",
    #     # export_csv=True,
    # ),
    # atapi.StringField(
    #     name='contact_address_postcode',
    #     widget=StringWidget(
    #         label="Address (Post/Zip Code)",
    #         label_msgid='Researcher_label_contact_address_postcode',
    #         i18n_domain='msd.researcher',
    #     ),
    #     schemata="Contact",
    #     # export_csv=True,
    # ),
    # atapi.StringField(
    #     name='contact_address_postcode',
    #     widget=StringWidget(
    #         label="Address (Post/Zip Code)",
    #         label_msgid='Researcher_label_contact_address_postcode',
    #         i18n_domain='msd.researcher',
    #     ),
    #     schemata="Contact",
    #     # export_csv=True,
    # ),
    # atapi.StringField(
    #     name='contact_address_country',
    #     # index="FieldIndex:brains",
    #     widget=atapi.SelectionWidget(
    #         label="Address (Country)",
    #         label_msgid='Researcher_label_contact_address_country',
    #         i18n_domain='msd.researcher',
    #     ),
    #     vocabulary=[],
    #     schemata="Contact",
    #     # export_csv=True,
    # ),
    # ADDRESS END

    atapi.StringField(
        name='phone',
        widget=StringWidget(
            label="Telephone",
        ),
        schemata="Contact",
        # export_csv=True,
    ),

    atapi.StringField(
        name='alternate_phone',
        widget=StringWidget(
            label="Alternate Telephone",
        ),
        schemata="Contact",
        # export_csv=True,
    ),

    atapi.StringField(
        name='fax',
        widget=StringWidget(
            label="Fax",
        ),
        schemata="Contact",
        # export_csv=True,
    ),

    atapi.StringField(
        name='email',
        # index="FieldIndex:brains",
        widget=StringWidget(
            label="Email Address",
            size=50,
        ),
        validators=('isEmail',),
        schemata="Contact",
        # export_csv=True,
    ),

    atapi.StringField(
        name='pa_name',
        widget=StringWidget(
            label="Secretary or PA",
            size=50,
        ),
        schemata="Contact",
        # export_csv=True,
    ),


    atapi.StringField(
        name='pa_phone',
        widget=StringWidget(
            label="Secretary or PA Telephone",
        ),
        schemata="Contact",
        # export_csv=True,
    ),

    atapi.StringField(
        name='pa_fax',
        widget=StringWidget(
            label="Secretary or PA Fax",
        ),
        schemata="Contact",
        # export_csv=True,
    ),

    atapi.StringField(
        name='pa_email',
        widget=StringWidget(
            label="Secretary or PA Email Address",
            size=50,
        ),
        validators=('isEmail',),
        schemata="Contact",
        # export_csv=True,
    ),

),
)

imageSchema = atapi.Schema((

    atapi.ImageField(
        name='image',
        widget=ImageWidget(
            label="Image",
            description="Upload an image (jpg or gif format), this will be resized to 300 x 300. This should be a representative image of you or your research.",
        ),
        schemata="Image",
        original_size=(300,300),
        sizes={'large':(768, 768),'preview':(400, 400),'mini':(200, 200),'thumb':(128, 128), 'tile':(64, 64),'icon':(32, 32),'listing':(16, 16),},
        storage=AttributeStorage(),
        max_size=(300,300),
        allowable_content_types=('image/gif','image/jpeg','image/png'),
    ),

    atapi.StringField(
        name='imageCaption',
        widget=StringWidget(
            label="Image Caption",
        ),
        schemata="Image"
    ),

),
)

affiliationsSchema = atapi.Schema((

    atapi.LinesField(
        name='units',
        # index="KeywordIndex:brains",
        widget=PicklistWidget(
            label="Departments",
            description="Select any departments or units you are associated with.",
       ),
        schemata="Affiliations",
        multiValued=1,
        vocabulary="getDepartmentVocabulary",
        # searchable=1,
    ),
    
    atapi.StringField(
        name='college',
        default='http://oxpoints.oucs.ox.ac.uk/id/00000000',
        # index="FieldIndex:brains",
        widget=atapi.SelectionWidget(
            label='College',
        ),
        schemata="Affiliations",
        vocabulary="getCollegeVocabulary",
        # searchable=1,
    ),

),
)

# The following is the people with whom a researcher collaborates
# A long time ago, I split this list into three, simply because it seemed
# like it would be easier for display purposes, however, with a browser view
# it ought to be easier to separate them out

collaborationSchema = atapi.Schema((

    DataGridField('collaborators',
            searchable = True,
            columns=("fullName", "url", "email", "role", "institution", "type"),
            widget = DataGridWidget(
                label='Group Members',
                description='Enter your collaborators here.',
                columns={
                    'fullName' : Column("Full Name"),
                    'url' : Column("Website"),
                    'email': Column("Email"),
                    'role' : Column("Role or Job Title"),
                    'institution' : Column("Group or Institution"),
                    'type': SelectColumn("Type of Collaboration", vocabulary="listCollabTypes")
                },
             ),
            schemata = "Collaboration",
     ),

    # DataGridField('groupMembers',
    #         searchable = True,
    #         columns=("fullName", "url", "role", "isOxford"),
    #         widget = DataGridWidget(
    #             label='Group Members',
    #             description='Enter your group members here. A url and role or job title are optional.',
    #             columns={
    #                 'fullName' : Column("Full Name"),
    #                 'url' : Column("Website"),
    #                 'role' : Column("Role or Job Title"),
    #                 'isOxford' : CheckboxColumn("at Oxford?"),
    #             },
    #          ),
    #         schemata = "Collaboration",
    #  ),
    #  
    #  DataGridField('pastGroupMembers',
    #         searchable = True,
    #         columns=("fullName", "url", "institution", "isOxford"),
    #         widget = DataGridWidget(
    #             label='Former Group Members',
    #             description='Enter former group members here. A url, group or institution name are optional.',
    #             columns={
    #                 'fullName' : Column("Full Name"),
    #                 'url' : Column("Website"),
    #                 'institution' : Column("Institution or Group"),
    #                 'isOxford' : CheckboxColumn("at Oxford?"),
    #             },
    #          ),
    #         schemata = "Collaboration",
    #  ),
    #  
    #  DataGridField('allCollaborators',
    #         searchable = True,
    #         columns=("fullName", "url", "institution", "isOxford"),
    #         widget = DataGridWidget(
    #             label='Other Oxford and External Collaborators',
    #             description='Enter your collaborators here. A url, group or institution name are optional.',
    #             label_msgid='Researcher_label_allcollaborators',
    #             description_msgid='Researcher_help_allcollaborators',
    #             i18n_domain='msd.researcher',
    #             columns={
    #                 'fullName' : Column("Full Name"),
    #                 'url' : Column("Website"),
    #                 'institution' : Column("Institution or Group"),
    #                 'isOxford' : CheckboxColumn("at Oxford?"),
    #             },
    #          ),
    #         schemata = "Collaboration",
    #  ),
    #  
),
)


