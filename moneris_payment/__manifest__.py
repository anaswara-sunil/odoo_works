# -*- coding: utf-8 -*-
{
    'name': "moneris_payment",
    'summary': "moneris_payment in POS",
    'version': '17.0.1.0.0',
    'depends': ['base','point_of_sale'],
    'installable': True,

    'data': [
        'views/pos_payment_method.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'moneris_payment/static/**/*',
        ],
    },

}

