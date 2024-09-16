# -*- coding: utf-8 -*-
from odoo import models, fields, _
from datetime import timedelta
from odoo.exceptions import UserError
import html2text
import io
import json
import xlsxwriter
from odoo.tools import date_utils


class ClubWizard(models.TransientModel):
   _name = "club.wizard"
   _description = "Club Wizard"

   club_ids = fields.Many2many('manage.club', string='Club')

   def action_club_report(self):
      """Passing data to report action"""
      data = {
         'model_id': self.id,
         'club_id': self.club_ids.ids,

      }
      return self.env.ref('school_management.action_report_manage_club').report_action(None, data=data)

   def action_club_xlsx_report(self):
      """Excel report for Club"""
      data = {
          'model_id': self.id,
          'club_id': self.club_ids.ids,
          'company_details': html2text.html2text(self.env.company.company_details),
      }
      return {
         'type': 'ir.actions.report',
         'data': {'model': 'club.wizard',
                  'options': json.dumps(data,
                                        default=date_utils.json_default),
                  'output_format': 'xlsx',
                  'report_name': 'Excel Report',
                  },
         'report_type': 'xlsx',
      }

   def get_xlsx_report(self, data, response):
      """setting datas to the report"""
      output = io.BytesIO()
      workbook = xlsxwriter.Workbook(output, {'in_memory': True})
      sheet = workbook.add_worksheet()
      cell_format = workbook.add_format({'bold': True, 'font_size': '12px', 'align': 'center', 'border': 1})
      head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '15px'})
      sub_head = workbook.add_format({'bold': True, 'font_size': '12px'})
      txt = workbook.add_format({'font_size': '10px', 'align': 'center', 'border': 1})
      details = workbook.add_format({'font_size': '10px', 'bold': True, 'align': 'top'})

      query = """select sr.full_name as student,mcl.name as class,mc.name as club,
                                 mcs.student_reg_id from  manage_club_student_reg_rel as mcs 
                                 inner join manage_club as mc on mc.id = mcs.manage_club_id
                                 inner join student_reg as sr on sr.id = mcs.student_reg_id
                                 inner join manage_class as mcl on mcl.id = sr.current_class_id
                                 where 1=1"""
      if data.get('club_id'):
          if len(data.get('club_id')) == 1:
              query += f"and mcs.manage_club_id={data['club_id'][0]}"
          else:
              query += f" and mcs.manage_club_id in {tuple(data['club_id'])}"
      query += """order by mc.name """
      self.env.cr.execute(query)
      report = self.env.cr.dictfetchall()

      club_list = []
      for rep in report:
          print(rep, 'rep')
          if rep['club'] not in club_list:
              club_list.append(rep['club'])

      print(report, 'report')
# User Error
      if not report:
          raise UserError(_('No Data Found'))

      sheet.merge_range('A1:A3', 'Company :', details)
      sheet.merge_range('B1:B3', data['company_details'], details)
      sheet.merge_range('A5:C5', 'CLUB REPORT', head)
      sheet.set_column(0, 7, 25)
      sheet.set_row(4, 30)
      i = 5
      for club in club_list:
          i += 1
          sheet.write(f'A{i}', 'Club :', sub_head)
          sheet.write(f'B{i}', club , sub_head)
          i += 2
          sheet.write(f'A{i}', 'Student Reg.No', cell_format)
          sheet.write(f'B{i}', 'Student', cell_format)
          sheet.write(f'C{i}', 'Class', cell_format)

          i += 1
          for rep in report:
              if rep.get('club') == club:
                  sheet.write(f'A{i}', rep['student_reg_id'], txt)
                  sheet.write(f'B{i}', rep['student'], txt)
                  sheet.write(f'C{i}', str(rep['class']), txt)
                  i += 1

      workbook.close()
      output.seek(0)
      response.stream.write(output.read())
      output.close()
