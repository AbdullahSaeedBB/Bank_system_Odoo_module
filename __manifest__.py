# -*- coding: utf-8 -*-

{
    'name': 'Bank System',
    'version': '1.0',
    'summary': 'Bank system management',
    'sequence': 10,
    'description': """
    Bank system management
    """,
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/vip_view.xml',
        # 'report/templetes_record.xml',
        'report/consumer_report.xml',
        'data/sequence.xml',
        'views/consumers.xml',
        'views/banks_bank.xml',
        'views/banks_atm.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
}
