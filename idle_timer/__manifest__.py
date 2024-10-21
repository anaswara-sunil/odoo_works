# -*- coding: utf-8 -*-
{
    'name': "idle_timer",
    'version': '17.0.1.0.0',
    'summary': "Setting required idle timing for a quiz",
    'description': """
                    """,
    'depends': ['base','base_setup','survey'],
    'data': [
        'views/res_config_settings.xml',
        'views/survey_timer.xml'
    ],
    'assets': {
        'survey.survey_assets': [
            # 'idle_timer/static/src/js/survey_form.js',
            'idle_timer/static/src/js/survey_timer.js'
    ]}
}

