{
    'name': "Hospital",
    'version': '1.0',
    'installable': True,
    'application': True,
    'depends': ['base','hr', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient.xml',
        'views/ticket.xml',
        'views/doctor.xml',
        'views/department.xml',
        'views/consultation.xml',
    ]
}