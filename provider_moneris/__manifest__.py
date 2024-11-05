# -*- coding: utf-8 -*-
{
    'name': "provider_moneris",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,
    'version': '17.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','account', 'payment'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/payment_provider.xml',
        'views/payment_templates.xml',
        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
    ],

}

