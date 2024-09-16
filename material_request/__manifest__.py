{
    'name': "Material Request",
    'version': '17.0.3.0.0',
    'description': """
                Material Request
                    """,
    'installable': True,
    'application': True,
    'depends': ['base','product','mail','stock','purchase'],
    'data': [
        'data/data.xml',
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/material_request.xml',
    ]
}