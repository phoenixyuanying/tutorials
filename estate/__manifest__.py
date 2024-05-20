# -*- coding: utf-8 -*-
# Exercise: estate

{
    'name':"Real Estate",
    'summary': """
        Exercise module for "First step"
    """,

    'description': """
        Exercise module for "First step"
    """,

    'author': "Ian Yuan",
    'website': "https://www.odoo.com",
    'depends':['base', 'web'],
    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/settings_property_type_views.xml',
        'views/settings_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_res_user_views.xml',
        # 'data/estate.property.type.csv',
        'data/estate_property.xml'
    ],
    'application': True,
    'installable': True,
    'license': 'AGPL-3'
}