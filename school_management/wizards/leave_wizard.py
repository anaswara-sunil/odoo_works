# -*- coding: utf-8 -*-
from odoo import models, fields, _,api
from odoo.exceptions import ValidationError
from datetime import timedelta
from odoo.exceptions import UserError
import html2text
import io
import json
import xlsxwriter
from odoo.tools import date_utils


class LeaveWizard(models.TransientModel):
   _name = "leave.wizard"
   _description = "Leave Wizard"

   class_student = fields.Selection(selection=[('class', 'Class'), ('student', 'Student')],
                                    string='Class/Student Based', default='class',required=True)
   month_week_day = fields.Selection(selection=[('month', 'Month'), ('week', 'Week'), ('day', 'Day'),
                                          ('custom', 'Custom Date')], string='Based on',default='month',required=True)
   class_id = fields.Many2one('manage.class', string='Class')
   student_id = fields.Many2one('student.reg', string='Student')
   start_date = fields.Date()
   end_date = fields.Date()

   @api.constrains('end_date')
   def _check__custom_date(self):
      """Custom Date Error message"""
      for rec in self:
         if rec.start_date and rec.end_date:
            if rec.start_date > rec.end_date:
               raise ValidationError(_("Check the Start date and End date"))
         # if rec.start_date and not rec.end_date:
         #    rec.end_date=fields.Date.today()

   @api.onchange('class_student')
   def reset_class_id_student_id(self):
      self.class_id = False
      self.student_id = False

   def action_leave_report(self):
      """Passing data to report action"""
      report_name = "LEAVE REPORT "

      if self.month_week_day == 'day':
         report_name += "- Day Wise"
      elif self.month_week_day == 'week':
         report_name += "- Week Wise"
      elif self.month_week_day == 'month':
         report_name += "- Month Wise"
      data = {
         'model_id': self.id,
         'class_student': self.class_student,
         'class_id': self.class_id.id,
         'student_id': self.student_id.id,
         'month_week_day': self.month_week_day,
         'start_date': self.start_date,
         'end_date': self.end_date,
         'report_name': report_name
      }
      return self.env.ref('school_management.action_report_manage_leave').report_action(None, data=data)

   def action_leave_xlsx_report(self):
      """Excel report for Leave"""
      report_name = "LEAVE REPORT "
      if self.month_week_day == 'day':
         report_name += "- Day Wise"
      elif self.month_week_day == 'week':
         report_name += "- Week Wise"
      elif self.month_week_day == 'month':
         report_name += "- Month Wise"
      data = {
         'model_id': self.id,
         'class_student': self.class_student,
         'class_id': self.class_id.id,
         'student_id': self.student_id.id,
         'month_week_day': self.month_week_day,
         'start_date': self.start_date,
         'end_date': self.end_date,
         'company_details' : html2text.html2text(self.env.company.company_details),
         'report_heading': report_name
      }
      print(data,'data')
      return {
         'type': 'ir.actions.report',
         'data': {'model': 'leave.wizard',
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

      query = """select sr.full_name as student,mc.name as class,
                                 ml.start_date,ml.end_date,ml.total_days,ml.half_day from manage_leave as ml
                                 inner join student_reg as sr on sr.id = ml.student_id
                                 inner join manage_class as mc on mc.id = sr.current_class_id 
                                 where 1=1"""
      # class
      if data.get('class_id'):
         query += """ and mc.id = '%s'""" % (data.get('class_id'))
      # student
      if data.get('student_id'):
         query += """ and sr.id = '%s'""" % (data.get('student_id'))
      # month based
      if data.get('month_week_day') == 'month':
         query += """ and ml.start_date >= '%s' """ % (
            fields.Date.to_string(fields.Date.today().replace(day=1)))
      # week based
      if data.get('month_week_day') == 'week':
         start = fields.Date.today() - timedelta(days=fields.Date.today().weekday())
         end = start + timedelta(days=6)
         query += """ and ml.start_date >= '%s' and ml.start_date <= '%s'""" % ((start), (end))
      # custom date based
      if data.get('start_date'):
         query += (""" and ml.start_date >= '%s'"""
                   % (data.get('start_date')))
      if data.get('end_date'):
         query += ("""and ml.end_date <= '%s'""" % (data.get('end_date')))

      self.env.cr.execute(query)
      report = self.env.cr.dictfetchall()
      print(report, 'report')

# User error
      if not report:
         raise UserError(_('No Data Found'))

      class_list = []
      for rec in report:
         if rec['class'] not in class_list:
            class_list.append(rec['class'])
      print(class_list,'cls lst')

      stud_list = []
      for rec in report:
         if rec['student'] not in stud_list:
            stud_list.append(rec['student'])

# Excel data
      sheet.merge_range('A1:A3', 'Company :', details)
      sheet.merge_range('B1:B3',  data['company_details'], details)
      if data['class_student'] == 'class':
         sheet.merge_range('A5:D5', 'CLASS-LEAVE REPORT', head)
         sheet.set_column(0,7,25)
         sheet.set_row(4,30)
         sheet.write('A7','Based on :', sub_head)
         sheet.write('B7', data['class_student'], sub_head)
         i = 7
         for cls in class_list:
            i +=1
            sheet.write(f'A{i}', 'Class :', sub_head)
            sheet.write(f'B{i}', cls, sub_head)
            i += 2
            sheet.write(f'A{i}', 'Students', cell_format)
            sheet.write(f'B{i}', 'Start Date', cell_format)
            sheet.write(f'C{i}', 'End Date', cell_format)
            sheet.write(f'D{i}', 'Total Days', cell_format)

            i += 1
            for rep in report:
               if rep.get('class') == cls:
                  sheet.write(f'A{i}', rep['student'], txt)
                  sheet.write(f'B{i}', str(rep['start_date']), txt)
                  sheet.write(f'C{i}', str(rep['end_date']), txt)
                  sheet.write(f'D{i}', rep['total_days'], txt)
                  i+=1

      if data['class_student'] == 'student':
         sheet.merge_range('A5:C5', 'STUDENT-LEAVE REPORT', head)
         sheet.set_column(0, 7, 25)
         sheet.set_row(4, 30)
         sheet.write('A7', 'Based on :', sub_head)
         sheet.write('B7', data['class_student'], sub_head)
         i = 7
         for stud in stud_list:
            print(stud, 'stud')
            i += 1
            sheet.write(f'A{i}', 'Student :', sub_head)
            sheet.write(f'B{i}', f'- {stud}', sub_head)
            i += 2
            sheet.write(f'A{i}', 'Start Date', cell_format)
            sheet.write(f'B{i}', 'End Date', cell_format)
            sheet.write(f'C{i}', 'Total Days', cell_format)

            i += 1  # 6
            for rep in report:
               if rep.get('student') == stud:
                  sheet.write(f'A{i}',str(rep['start_date']), txt)
                  sheet.write(f'B{i}', str(rep['end_date']), txt)
                  sheet.write(f'C{i}', rep['total_days'], txt)
                  i += 1


      workbook.close()
      output.seek(0)
      response.stream.write(output.read())
      output.close()
