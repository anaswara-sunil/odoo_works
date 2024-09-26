# -*- coding: utf-8 -*-
from odoo import models, fields, _,api,Command
from datetime import timedelta
from odoo.exceptions import UserError
import html2text
import io
import json
import xlsxwriter
from odoo.tools import date_utils


class ClassDepartmentWizard(models.TransientModel):
   _name = "class.department.wizard"
   _description = "Class Department Wizard"

   based_on = fields.Selection(selection=[('class', 'Class'), ('department', 'Department')],
                                    string='Based on', default='class',required=True)
   class_id = fields.Many2one('manage.class', string='Class')
   dept_id = fields.Many2one('manage.department', string='Department')
   alternate_ids = fields.Many2many('manage.class', compute='_compute_alternate_ids')

   @api.depends('dept_id')
   def _compute_alternate_ids(self):
      """Class field based on department field"""
      for rec in self:
         rec.alternate_ids = False
         if rec.dept_id:
            rec.alternate_ids = self.env['manage.class'].search([('department_id', '=', self.dept_id.id)])
         if not  rec.dept_id:
            rec.alternate_ids = self.env['manage.class'].search([])

   @api.onchange('dept_id')
   def reset_class_id(self):
      self.class_id = False

   @api.onchange('based_on')
   def reset_class_id_student_id(self):
      self.class_id = False
      self.dept_id = False

   def action_class_department_report(self):
      """Passing data to report action"""
      data = {
         'model_id': self.id,
         'based_on' : self.based_on,
         'class_id': self.class_id.id,
         'dept_name' : self.class_id.department_id.name,
         'hod_name' : self.dept_id.hod_id.name,
         'dept_id': self.dept_id.id,
      }
      # print(data)
      return self.env.ref('school_management.action_report_manage_class_department').report_action(None, data=data)

   def action_class_department_xlsx_report(self):
      """Excel report for Class and Department"""
      data = {
         'model_id': self.id,
         'based_on': self.based_on,
         'class_id': self.class_id.id,
         'dept_name': self.class_id.department_id.name,
         'hod_name': self.dept_id.hod_id.name,
         'dept_id': self.dept_id.id,
         'company_details': html2text.html2text(self.env.company.company_details),
      }
      # print(data, 'data')
      return {
         'type': 'ir.actions.report',
         'data': {'model': 'class.department.wizard',
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
      cell_format = workbook.add_format({'bold': True,'font_size': '12px', 'align': 'center', 'border':1})
      head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '15px'})
      sub_head = workbook.add_format({'bold': True, 'font_size': '12px'})
      txt = workbook.add_format({'font_size': '10px', 'align': 'center','border':1})
      details = workbook.add_format({'font_size': '10px','bold': True,'align': 'top'})

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
            query += """ and mc.id = '%s'""" % (data.get('class_id'))

      self.env.cr.execute(query)
      report = self.env.cr.dictfetchall()
      class_dict = {}
      stud_count = 0
      for rec in report:
         if rec['class'] not in class_dict:
            class_dict[rec['class']] = rec['department']
      # print(class_dict,'cls dict')

      dept_dict = {}
      for rec in report:
         if rec['department'] not in dept_dict:
            dept_dict[rec['department']] = rec['hod']
      # print(report, 'report')
# User Error
      if not report:
         raise UserError(_('No Data Found'))

      sheet.merge_range('A1:A3', 'Company :', details)
      sheet.merge_range('B1:B3', data['company_details'], details)

      if data['based_on'] == 'class':
         sheet.merge_range('A5:C5', 'CLASS REPORT', head)
         sheet.set_column(0, 7, 25)
         sheet.set_row(4, 30)
         i = 6
         for cls in class_dict:
            i += 1
            sheet.write(f'A{i}', 'Class :', sub_head)
            sheet.write(f'B{i}', cls, sub_head)
            i += 1
            sheet.write(f'A{i}', 'Department :', sub_head)
            sheet.write(f'B{i}', class_dict[cls], sub_head)
            i += 2
            sheet.write(f'A{i}', 'Student Reg.No', cell_format)
            sheet.write(f'B{i}', 'Student', cell_format)
            sheet.write(f'C{i}', 'Student Email', cell_format)

            i += 1
            for rep in report:
               if rep.get('class') == cls:
                  sheet.write(f'A{i}', rep['student_reg_no'], txt)
                  sheet.write(f'B{i}', str(rep['student']), txt)
                  sheet.write(f'C{i}', str(rep['email']), txt)
                  i+=1

      if data['based_on'] == 'department':
         sheet.merge_range('A5:B5', 'DEPARTMENT REPORT', head)
         sheet.set_column(0, 7, 25)
         sheet.set_row(4, 30)
         i = 6
         for dept in dept_dict:
            i += 1
            sheet.write(f'A{i}', 'Department :', sub_head)
            sheet.write(f'B{i}', dept, sub_head)
            i += 1
            sheet.write(f'A{i}', 'HOD :', sub_head)
            sheet.write(f'B{i}', dept_dict[dept], sub_head)
            i += 2
            sheet.write(f'A{i}', 'Class', cell_format)
            sheet.write(f'B{i}', 'Total Students', cell_format)
            i += 1
            for rep in report:
               if rep.get('department') == dept:
                  sheet.write(f'A{i}', rep.get('class'), txt)
                  sheet.write(f'B{i}', rep.get('student_count'), txt)
                  i += 1

      workbook.close()
      output.seek(0)
      response.stream.write(output.read())
      output.close()


