# -*- coding: utf-8 -*-
from odoo import models, fields, _
from datetime import timedelta
from odoo.exceptions import UserError
import html2text
import io
import json
import xlsxwriter
from odoo.tools import date_utils

class EventWizard(models.TransientModel):
   _name = "event.wizard"
   _description = "Event Wizard"

   club_id = fields.Many2one('manage.club', string='Club')
   month_week_day = fields.Selection(selection=[('month', 'Month'), ('week', 'Week'), ('day', 'Day'),
                                          ('custom', 'Custom Date')], string='Based on',default='month',required=True)
   start_date = fields.Date()
   end_date = fields.Date()


   def action_event_report(self):
      """Passing data to report action"""
      report_name = "EVENT REPORT - "

      if self.month_week_day == 'day':
         report_name += "Day Wise"
      elif self.month_week_day == 'week':
         report_name += "Week Wise"
      elif self.month_week_day == 'month':
         report_name += "Month Wise"
      data = {
         'model_id': self.id,
         'club_id': self.club_id.id,
         'month_week_day': self.month_week_day,
         'start_date': self.start_date,
         'end_date': self.end_date,
         'report_name' : report_name
      }
      return self.env.ref('school_management.action_report_manage_event').report_action(None, data=data)

   def action_event_xlsx_report(self):
      """Excel report for Event"""
      report_name = "EVENT REPORT - "

      if self.month_week_day == 'day':
         report_name += "Day Wise"
      elif self.month_week_day == 'week':
         report_name += "Week Wise"
      elif self.month_week_day == 'month':
         report_name += "Month Wise"

      data = {
         'model_id': self.id,
         'club_id': self.club_id.id,
         'month_week_day': self.month_week_day,
         'start_date': self.start_date,
         'end_date': self.end_date,
         'report_name': report_name,
         'company_details' : html2text.html2text(self.env.company.company_details)
      }
      print(data,'data')
      return {
         'type': 'ir.actions.report',
         'data': {'model': 'event.wizard',
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

      query = """select mc.name as club,
                                  me.start_date,me.end_date,me.name,me.state from manage_event as me
                                  inner join manage_club_manage_event_rel as mce on mce.manage_event_id = me.id
      							inner join manage_club as mc on mc.id = mce.manage_club_id
                                  where 1=1"""
      # club based
      if data.get('club_id'):
         query += """ and mce.manage_club_id = '%s'""" % (data.get('club_id'))
      # month based
      if data.get('month_week_day') == 'month':
         query += """ and me.start_date >= '%s' """ % (
            fields.Date.to_string(fields.Date.today().replace(day=1)))
      # week based
      if data.get('month_week_day') == 'week':
         start = fields.Date.today() - timedelta(days=fields.Date.today().weekday())
         end = start + timedelta(days=6)
         query += """ and me.start_date >= '%s' and me.start_date <= '%s' """ % (start, end)
      # Day based
      if data.get('month_week_day') == 'day':
         query += """ and me.start_date <= '%s' and me.end_date >= '%s' """ % (fields.Date.today(), fields.Date.today())
      # custom date based
      if data.get('start_date'):
         query += (""" and me.start_date >= '%s' and me.end_date <= '%s'"""
                   % (data.get('start_date'), data.get('end_date')))

      self.env.cr.execute(query)
      report = self.env.cr.dictfetchall()
#User error
      print(report, 'report')
      if not report:
         raise UserError(_('No Data Found'))

      state_dict = dict(self.env['manage.event']._fields['state'].selection)

      sheet.merge_range('A1:A3', 'Company :', details)
      sheet.merge_range('B1:B3', data['company_details'], details)
      sheet.merge_range('A5:E5', 'EVENT REPORT', head)
      sheet.set_column(0, 7, 25)
      sheet.set_row(4, 30)
      i = 6
      sheet.write(f'A{i}', 'Event', cell_format)
      sheet.write(f'B{i}', 'Club', cell_format)
      sheet.write(f'C{i}', 'Start Date', cell_format)
      sheet.write(f'D{i}', 'End Date', cell_format)
      sheet.write(f'E{i}', 'Status', cell_format)

      i += 1  # 7
      for rep in report:
         sheet.write(f'A{i}', rep['name'], txt)
         sheet.write(f'B{i}', rep['club'], txt)
         sheet.write(f'C{i}', str(rep['start_date']), txt)
         sheet.write(f'D{i}', str(rep['end_date']), txt)
         sheet.write(f'E{i}', state_dict[rep['state']], txt)
         i += 1

      workbook.close()
      output.seek(0)
      response.stream.write(output.read())
      output.close()
