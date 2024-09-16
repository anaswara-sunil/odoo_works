{
    'name': "Import File",
    'version': '17.0.3.0.0',
    'description': """
                Import lot and serial number data from excel sheet
                    """,
    'installable': True,
    # 'application': True,
    'depends': ['base','stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_file_wizard.xml',
        'views/stock_lot.xml',

    ]
}