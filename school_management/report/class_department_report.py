# -*- coding: utf-8 -*-
from odoo import models,fields, api, _
from odoo.exceptions import UserError


class ClassDepartmentReport(models.AbstractModel):
    _name = 'report.school_management.report_class_department'

    @api.model
    def _get_report_values(self,docids,data=None):
        """Setting datas to the template"""
        print(data,'data')
        # docs = self.env['manage.class'].browse(docids)
        query = """select mc.name as class,md.name as department,res.name as hod,mc.student_count as student_count,
                            mc.department_id from  manage_class as mc
                            inner join manage_department as md on md.id = mc.department_id
                            inner join res_partner as res on res.id = md.hod_id
                            where 1=1"""
        if data.get('based_on') == 'class':
            query = """select mc.name as class,md.name as department,sr.full_name as student,sr.name as student_reg_no,
                        sr.email as email,res.name as hod,mc.department_id from  manage_class as mc
                        inner join manage_department as md on md.id = mc.department_id
                        inner join res_partner as res on res.id = md.hod_id
                        inner join student_reg as sr on sr.current_class_id = mc.id """
            if data.get('class_id'):
                query += """where mc.id = '%s'""" % (data.get('class_id'))

        if data.get('dept_id'):
            query += """ and mc.department_id = '%s'""" % (data.get('dept_id'))
            if data.get('class_id'):
                query +=""" and mc.id = '%s'""" % (data.get('class_id'))

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        class_dict = {}
        for rec in report:
            if rec['class'] not in class_dict:
                class_dict[rec['class']] = rec['department']

        dept_dict = {}
        for rec in report:
            if rec['department'] not in dept_dict:
                dept_dict[rec['department']] = rec['hod']
        print(report,'report')
        if not report:
            raise UserError(_('No Data Found'))

        return {
            'doc_ids': docids,
            'doc_model': 'class_department_wizard',
            # 'docs': docs,
            'data': data,
            'report' : report,
            'class_dict':class_dict,
            'dept_dict':dept_dict,
            'date': fields.Date.today(),
        }


