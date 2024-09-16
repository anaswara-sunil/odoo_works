{
    'name': "OWL Workshop",
    'version': '1.0',
    'installable': True,
    'application': True,
    'depends': ['base'],
    'data': [
        'views/client_action.xml',
    ],
    'assets':{
        'web.assets_backend':[
            'owl_workshop/static/src/js/**',
            'owl_workshop/static/src/xml/**'
        ]
    }
}