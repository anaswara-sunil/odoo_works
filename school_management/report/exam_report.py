# -*- coding: utf-8 -*-
from odoo import models,fields, api, _
from odoo.exceptions import UserError


class ExamReport(models.AbstractModel):
    _name = 'report.school_management.report_exam'

    @api.model
    def _get_report_values(self,docids,data=None):
        """Setting datas to the template"""
        print(data,'data')
        # docs = self.env['manage.exam'].browse(docids)
        query =''
        if data.get('based_on') == 'class':
            query = """select me.name as exam,mc.name as class,md.name as department,res.name as hod,
                        me.start_date as start_date,me.end_date as end_date from  manage_exam as me
                                  inner join manage_class as mc on mc.id = me.class_id
                                  inner join manage_department as md on md.id = mc.department_id
                                  inner join res_partner as res on res.id = md.hod_id
                                  where 1=1"""
            if data.get('class_id'):
                query += """ and me.class_id= '%s'""" % (data.get('class_id'))
            if data.get('exam_id'):
                query += """ and me.id = '%s'""" % (data.get('exam_id'))
        elif data.get('based_on') == 'exam':
            query = """select  me.name as exam, sub.name as subject,sub.pass_mark as pass_mark,
                                  sub.max_mark as total,mc.name as class from  manage_exam as me
                                  inner join manage_exam_manage_subject_rel as es on es.manage_exam_id = me.id
                                  inner join manage_subject as sub on sub.id = es.manage_subject_id
                                  inner join manage_class as mc on mc.id = me.class_id  
                                  where 1=1"""
            if data.get('exam_id'):
                query += """ and me.id = '%s'""" % (data.get('exam_id'))
            if data.get('class_id'):
                query += """ and me.class_id= '%s'""" % (data.get('class_id'))
            query += """order by  me.name"""

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        exam_dict = {}
        for rec in report:
            if rec['exam'] not in exam_dict:
                exam_dict[rec['exam']] = rec['class']
        if not report:
            raise UserError(_('No Data Found'))
        print(report,'report')
        return {
            'doc_ids': docids,
            'doc_model': 'class_department_wizard',
            # 'docs': docs,
            'data': data,
            'report' : report,
            'exam_dict':exam_dict,
            'date': fields.Date.today()
        }


