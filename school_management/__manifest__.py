{
    'name': "School Management",
    'version': '17.0.3.0.0',
    'description': """
                School Management
                ====================
                The specific and easy-to-use School Management system in Odoo allows you to keep track of your Department,employees,and Students.
                    """,
    'installable': True,
    'application': True,
    'depends': ['base', 'web','sale_management','mail'],
    'data': [
        'data/default_record_data.xml',
        'data/ir_sequence_data.xml',
        'data/ir_cron_data.xml',
        'data/mail_template_data.xml',
        'data/base_automation_data.xml',
        'data/ir_actions_server_data.xml',
        'security/security_groups.xml',
        'security/security_rules.xml',
        'security/ir.model.access.csv',
        'views/student_registration_views.xml',
        'views/manage_department_views.xml',
        'views/manage_class_views.xml',
        'views/manage_subject_views.xml',
        'views/manage_academic_views.xml',
        'views/manage_club_views.xml',
        'views/manage_event_views.xml',
        'views/manage_saleorder_views.xml',
        'views/manage_teacher_views.xml',
        'views/manage_office_staff_views.xml',
        'views/manage_leave_views.xml',
        'views/manage_contact_views.xml',
        'views/manage_exam_views.xml',
        'wizards/leave_wizard.xml',
        'report/manage_leave_templates.xml',
        'wizards/event_wizard.xml',
        'report/manage_event_templates.xml',
        'wizards/club_wizard.xml',
        'report/manage_club_template.xml',
        'wizards/class_department_wizard.xml',
        'report/manage_class_dept_template.xml',
        'wizards/exam_wizard.xml',
        'report/manage_exam_template.xml',
        'report/manage_reports_action.xml',
        'templates/students_list_template.xml',
        'templates/registration_form_template.xml',
        'templates/student_details_template.xml',
        'templates/leave_form_template.xml',
        'templates/leave_list_template.xml',
        'templates/event_list_template.xml',
        'templates/event_detail_template.xml',
        'templates/event_registration_template.xml',
        'templates/thank_you_template.xml',

        'templates/home_templates.xml',
        'views/snippet.xml',

        'views/school_management_menus.xml',
    ],
    'assets':{
            'web.assets_backend':[
               'school_management/static/src/js/action_manager.js',
            ],
            'web.assets_frontend':  [
                'school_management/static/src/js/address_check.js',
                'school_management/static/src/js/leave_check.js',
                'school_management/static/src/js/event_check.js',
                'school_management/static/src/js/latest_event.js',
                'school_management/static/src/xml/latest_events_snippet_templates.xml',
                'school_management/static/src/css/snippet_css.css',
                'school_management/static/src/img/thumbnail.svg',
            ],
    }
}


