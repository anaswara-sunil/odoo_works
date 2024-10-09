{
    'name': 'Payment Provider: Multisafepay',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'description': """ MultiSafepay is a leading end-to-end processing and acquirer
                    payment platform for European merchants """,
    'depends': ['base','account', 'payment'],
    'data': [
        'views/payment_provider_views.xml',
        'views/payment_templates.xml',
        'data/res_config.xml',
        'data/account_payment_method_data.xml',
        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
    ],
}
