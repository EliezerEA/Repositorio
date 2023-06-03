# -*- coding: utf-8 -*-
{
    'name': "presupuesto_tecnoplus",

    'summary': """
        Desarrollo de formato personalizado 
        """,

    'description': """
        Desarrollo de formato personalizado 
    """,

    'author': "Noduu-Eliezer",
    'website': "erp.noduu.com",
    'category': 'Sale',
    'version': '1.0.0',
    'depends': ['sale','sale_management', 'contacts'],

    'data': [
        'report/sale_report.xml',
        'report/sale_report_views.xml',
        'views/sale_order.xml',
        'views/asesor_views.xml',
        'views/garantia_views.xml',
        'security/ir.model.access.csv',

    ],
    'assets': {
            'point_of_sale.assets': [
            ],
            'web.assets_common': [
            ],
            'web.assets_qweb': [
        ],
    },
    
}
