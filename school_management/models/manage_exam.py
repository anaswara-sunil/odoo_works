# -*- coding: utf-8 -*-
from odoo import models, fields, Command, api



class ManageExam(models.Model):
    """Manage Exam"""
    _name = "manage.exam"
    _description = "Manage Exam"
    _inherit = 'mail.thread'

    name = fields.Char('Name', required=True)
    class_id = fields.Many2one('manage.class')
    color = fields.Integer()
    subject_ids = fields.Many2many('manage.subject', string="Sub name")
    student_ids = fields.Many2many('student.reg', string="Students")
    total_mark = fields.Float(compute='_compute_total_mark',store=True)
    start_date = fields.Date(default=fields.Datetime.now, copy=False, string="Start Date")
    end_date = fields.Date(default=fields.Datetime.now, copy=False, string="End Date")

    def action_assign_exam_to_students(self):
        """Button action for assigning exam to students"""
        for record in self:
            students = self.env['student.reg'].search([('current_class_id', '=', record.class_id.id)])  #  fetching all students in this class
            # record.student_ids = [(6, 0, students.ids)]
            record.write({'student_ids': [Command.set(students.ids)]})

    @api.depends('subject_ids')
    def _compute_total_mark(self):
        """Total Mark of the Exam"""
        for rec in self:
            rec.total_mark = sum(rec.subject_ids.mapped('max_mark'))
            print(rec.subject_ids.mapped('max_mark'))

