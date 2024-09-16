{
    'name': "Purchase Orders",
    'version': '17.0.3.0.0',
    'description': """
                Purchase Orders
                ====================
                Automated Purchase Orders
                    """,
    'installable': True,
    'application': True,
    'depends': ['base','product','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template.xml',
        'views/purchase_order.xml',
        'wizard/product_order_wizard.xml',
    ]
}