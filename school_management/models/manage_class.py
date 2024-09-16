# -*- coding: utf-8 -*-
from operator import countOf

from odoo import models, fields,api
from odoo.tools.populate import compute


class ManageClass(models.Model):
    """Manage Class"""
    _name = "manage.class"
    _description = "Manage Class"
    _inherit = 'mail.thread'

    name = fields.Char('Name', required=True)
    school_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

    department_id = fields.Many2one('manage.department', string="Department", required=True)
    # head_of_department = fields.Many2one('res.partner', string="HOD", readonly="1", force_save="0")

    # to show the hod field in ui without saving it in the db
    head_of_department_id = fields.Many2one(related='department_id.hod_id')
    # student_ids = fields.Many2many('student.reg')
    class_student_ids = fields.One2many('student.reg',inverse_name='current_class_id')
    student_count = fields.Integer(compute="_compute_student_count",store=True)


    @api.depends("class_student_ids")
    def _compute_student_count(self):
        """Computing the students count"""
        for rec in self:
            rec.student_count = len(rec.class_student_ids.ids)
            # print(rec.student_count)



# using onchange method
    # @api.onchange('department_id')
    # def _onchange_department_id(self):
    #     self.write({
    #         'head_of_department': self.department_id.hod_id
    #     })


# using computed field method
    # head_dept = fields.Many2one('res.partner', 'hod', compute='_compute_head_dept')

    # @api.depends("department_id")
    # def _compute_head_dept(self):
    #     for record in self:
    #         record.write({
    #             'head_dept': record.department_id.hod_id.id
    #         })





