{
    'name': "Customer Due Limit",
    'version': '17.0.3.0.0',
    'description': """
               Customer Due Limit and Payment validation 
                    """,
    'installable': True,
    'depends': ['base','point_of_sale',''],
    'data': [
        'views/res_partner.xml',
        # 'views/res_config_settings.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            '/pos_due_limit/static/src/js/payment_validation.js',
            '/pos_due_limit/static/src/xml/partner_list.xml',
            '/pos_due_limit/static/src/xml/partner_line.xml',
        ]
    }
}