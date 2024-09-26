{
    'name': "Discount Tag",
    'version': '17.0.3.0.0',
    'description': """
               Discount price tag in the POs Screen in the product view 
                    """,
    'installable': True,
    'depends': ['base','product','point_of_sale'],
    'data': [
        'views/product_product.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            '/pos_discount_tag/static/src/xml/product_widget_template.xml',
            '/pos_discount_tag/static/src/xml/product_card_template.xml',
            '/pos_discount_tag/static/src/css/product_card.css',
            '/pos_discount_tag/static/src/js/orderline.js',

        ]
    }
}