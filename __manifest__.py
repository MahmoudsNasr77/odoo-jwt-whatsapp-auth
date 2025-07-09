{
    'name': 'Custom WhatsApp API',
    'version': '1.0',
    'summary': 'API to send WhatsApp messages and store them',
    'category': 'Tools',
    'author': 'Mahmoud Sabry',
    'depends': ['base', 'web', 'auth_signup'],
    'data': [
        'security/ir.model.access.csv',
            'views/whatsapp_message_views.xml',
      

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    
       'web_icon': '/school/static/description/icon.png',
}
