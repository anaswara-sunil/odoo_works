# -*- coding: utf-8 -*-
from odoo import models,fields, api, _
from odoo.exceptions import UserError


class ClubReport(models.AbstractModel):
    _name = 'report.school_management.report_club'

    @api.model
    def _get_report_values(self,docids,data=None):
        """Setting datas to the template"""
        # print(data,'data')
        # docs = self.env['manage.club'].browse(docids)
        query = """select sr.full_name as student,mcl.name as class,mc.name as club,
                            mcs.student_reg_id from  manage_club_student_reg_rel as mcs 
                            inner join manage_club as mc on mc.id = mcs.manage_club_id
                            inner join student_reg as sr on sr.id = mcs.student_reg_id
                            inner join manage_class as mcl on mcl.id = sr.current_class_id
                            where 1=1"""
        if data.get('club_id'):
            if len(data.get('club_id'))==1:
                query +=  f"and mcs.manage_club_id={data['club_id'][0]}"
            else:
                query += f" and mcs.manage_club_id in {tuple(data['club_id'])}"
        query += """order by mc.name """
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()

        club_list = []
        for rep in report:
           # print(rep,'rep')
           if rep['club'] not in club_list:
               club_list.append(rep['club'])
        # print(report,'report')
        if not report:
            raise UserError(_('No Data Found'))

        return {
            'doc_ids': docids,
            'doc_model': 'club_wizard',
            # 'docs': docs,
            'data': data,
            'report' : report,
            'club_list':club_list,
            'date': fields.Date.today()
        }




