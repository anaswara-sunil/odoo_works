{
    'name': "Video Icon POS",
    'version': '17.0.3.0.0',
    'description': """
               Video icon in the pos product 
                    """,
    'installable': True,
    'depends': ['base','product','point_of_sale'],
    'data': [
        'views/product_product.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            '/pos_video_icon/static/src/js/product_video_popup.js',
            '/pos_video_icon/static/src/xml/ProductVideoPopup.xml',
            '/pos_video_icon/static/src/js/video_btn.js',
            '/pos_video_icon/static/src/xml/product_widget_template.xml',
            '/pos_video_icon/static/src/xml/product_card_template.xml',
            '/pos_video_icon/static/src/css/product_card.css',
        ]
    }
}