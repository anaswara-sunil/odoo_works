# -*- coding: utf-8 -*-
from odoo import models, fields, _,api
from odoo.exceptions import UserError
import html2text
import io
import json
import xlsxwriter
from odoo.tools import date_utils


class ExamWizard(models.TransientModel):
   _name = "exam.wizard"
   _description = "Exam Wizard"

   based_on = fields.Selection(selection=[('exam', 'Exam'), ('class', 'Class')], string='Based on',default='exam',required=True)
   exam_id = fields.Many2one('manage.exam', string='Exam')
   class_id = fields.Many2one('manage.class', string='Class')
   alternate_ids = fields.Many2many('manage.class', compute='_compute_alternate_ids')

   @api.depends('exam_id')
   def _compute_alternate_ids(self):
      """Class field based on exam field"""
      for rec in self:
         rec.alternate_ids = False
         if rec.exam_id:
            rec.alternate_ids = self.env['manage.class'].search([('id', '=', self.exam_id.class_id.id)])
         if not rec.exam_id:
            rec.alternate_ids = self.env['manage.class'].search([])

   @api.onchange('based_on')
   def reset_class_id_exam_id(self):
      self.class_id = False
      self.exam_id = False

   @api.onchange('exam_id')
   def reset_exam_id(self):
      self.class_id = False

   def action_exam_report(self):
      """Passing data to report action"""
      report_name = ''
      if self.based_on == 'exam':
         report_name = "EXAM REPORT"
      elif self.based_on == 'class':
         report_name = "CLASS BASED EXAM REPORT"

      data = {
         'model_id': self.id,
         'based_on': self.based_on,
         'exam_id': self.exam_id.id,
         'exam_name': self.exam_id.name,
         'exam_class' : self.exam_id.class_id.name,
         'class_id': self.class_id.id,
         'class_name': self.class_id.name,
         'dept_name': self.class_id.department_id.name,
         'hod_name': self.class_id.head_of_department_id.name,
         'report_name' : report_name
      }
      # print(data,'data')
      return self.env.ref('school_management.action_report_manage_exam').report_action(None, data=data)

   def action_exam_xlsx_report(self):
      """Excel report for Exam"""
      report_name = ''
      if self.based_on == 'exam':
         report_name = "EXAM REPORT"
      elif self.based_on == 'class':
         report_name = "CLASS BASED EXAM REPORT"

      data = {
         'model_id': self.id,
         'based_on': self.based_on,
         'exam_id': self.exam_id.id,
         'exam_name': self.exam_id.name,
         'exam_class': self.exam_id.class_id.name,
         'class_id': self.class_id.id,
         'class_name': self.class_id.name,
         'dept_name': self.class_id.department_id.name,
         'hod_name': self.class_id.head_of_department_id.name,
         'report_name': report_name,
         'company_details': html2text.html2text(self.env.company.company_details),
      }
      # print(data, 'data')
      return {
         'type': 'ir.actions.report',
         'data': {'model': 'exam.wizard',
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

      query = ''
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
# User Error
      if not report:
         raise UserError(_('No Data Found'))
      # print(report, 'report')

# Excel table
      sheet.merge_range('A1:A3', 'Company :', details)
      sheet.merge_range('B1:B3', data['company_details'], details)
      sheet.set_column(0, 7, 25)
      sheet.set_row(4, 30)
      i = 5
      if data['based_on'] == 'class':
         sheet.merge_range('A5:C5', data['report_name'], head)
         for rep in report:
            i += 2
            sheet.write(f'A{i}', 'Class :', sub_head)
            sheet.write(f'B{i}',  rep['class'], sub_head)
            i += 1
            sheet.write(f'A{i}', 'Department :', sub_head)
            sheet.write(f'B{i}',  rep['department'], sub_head)
            i += 1
            sheet.write(f'A{i}', 'HOD :', sub_head)
            sheet.write(f'B{i}',  rep['hod'], sub_head)
            i += 2
            sheet.write(f'A{i}', 'Exam', cell_format)
            sheet.write(f'B{i}', 'Start Date', cell_format)
            sheet.write(f'C{i}', 'End Date', cell_format)
            i += 1
            sheet.write(f'A{i}', rep['exam'], txt)
            sheet.write(f'B{i}', str(rep['start_date']), txt)
            sheet.write(f'C{i}',str(rep['end_date']), txt)

      if data['based_on'] == 'exam':
         sheet.merge_range('A5:C5', data['report_name'], head)
         for exam in exam_dict:
            i += 2
            sheet.write(f'A{i}', 'Exam :', sub_head)
            sheet.write(f'B{i}', exam, sub_head)
            i += 1
            sheet.write(f'A{i}', 'Class :', sub_head)
            sheet.write(f'B{i}', exam_dict[exam], sub_head)
            i += 2
            sheet.write(f'A{i}', 'Students', cell_format)
            sheet.write(f'B{i}', 'Pass Mark', cell_format)
            sheet.write(f'C{i}', 'Total Mark', cell_format)
            i += 1
            for rep in report:
               if rep.get('exam') == exam:
                  sheet.write(f'A{i}', rep['subject'], txt)
                  sheet.write(f'B{i}', str(rep['pass_mark']), txt)
                  sheet.write(f'C{i}', str(rep['total']), txt)
                  i += 1
      workbook.close()
      output.seek(0)
      response.stream.write(output.read())
      output.close()