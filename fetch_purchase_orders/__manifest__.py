{
    'name': 'Fetch Purchase Orders',
    'version': '1.0',
    'description': """ Fetching all purchase orders created in the old database (version 16.0)
                        to the new database (version 17.0)""",
    'depends': ['base','purchase','account','stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/sync_wizard.xml',
        ],

}
