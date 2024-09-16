# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import UserError


class LeaveReport(models.AbstractModel):
    _name = 'report.school_management.report_leave'

    @api.model
    def _get_report_values(self,docids,data=None):
        """Setting datas to the template"""
        # print(data,'data')
        # docs = self.env['manage.leave'].browse(docids)
        query = """select sr.full_name as student,mc.name as class,
                           ml.start_date,ml.end_date,ml.total_days,ml.half_day from manage_leave as ml
                           inner join student_reg as sr on sr.id = ml.student_id
                           inner join manage_class as mc on mc.id = sr.current_class_id 
                           where 1=1"""
    # class
        if data.get('class_id') :
            query += """ and mc.id = '%s'""" % (data.get('class_id'))
    # student
        if data.get('student_id') :
            query += """ and sr.id = '%s'""" % (data.get('student_id'))
    # month based
        if data.get('month_week_day') == 'month':
            query += """ and ml.start_date >= '%s' """ % (
                fields.Date.to_string(fields.Date.today().replace(day=1)))
    #week based
        if data.get('month_week_day') == 'week':
            start = fields.Date.today() - timedelta(days=fields.Date.today().weekday())
            end = start + timedelta(days=6)
            query += """ and ml.start_date >= '%s' and ml.start_date <= '%s'""" % ((start),(end))
    # custom date based
        if  data.get('start_date'):
            query += (""" and ml.start_date >= '%s'"""
                      % (data.get('start_date')))
        if data.get('end_date'):
            query += ("""and ml.end_date <= '%s'""" %(data.get('end_date')))

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report, 'report pdf')

# validation error
        if not report:
            raise UserError(_('No Data Found'))


        class_list = []
        for rec in report:
            if rec['class'] not in class_list:
                class_list.append(rec['class'])

        stud_list = []
        for rec in report:
            if rec['student'] not in stud_list:
                stud_list.append(rec['student'])
        print(stud_list)

        return {
            'doc_ids': docids,
            'doc_model': 'leave_wizard',
            # 'docs': docs,
            'data': data,
            'report' : report,
            'class_list':class_list,
            'stud_list':stud_list,
            'date':fields.Date.today(),
        }


