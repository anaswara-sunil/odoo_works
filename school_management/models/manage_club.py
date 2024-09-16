# -*- coding: utf-8 -*-
from odoo import models, fields
# from odoo.exceptions import ValidationError



class ManageClub(models.Model):
    """Manage Clubs"""
    _name = "manage.club"
    _description = "Manage Clubs"
    _inherit = 'mail.thread'


    name = fields.Char('Club Name')
    color = fields.Integer()
    student_ids = fields.Many2many('student.reg', string="Student name")
    event_count = fields.Integer(string="Events", compute='_compute_event_count', default=0)
    school_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)


    def _compute_event_count(self):
        """Computing the event count"""
        for record in self:
            record.event_count = self.env['manage.event'].search_count([('club_ids', '=', self.ids)])
            print(record.event_count)

    def action_get_events_record(self):
        """Event records """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Events',
            'view_mode': 'tree',
            'res_model': 'manage.event',
            'domain': [('club_ids', '=', self.ids)],
            'context': {'create': False}
        }















    # @api.model
    # def create(self, vals):
    #     if 'student_ids' in vals:
    #         student_ids = vals['student_ids'][0][2]
    #         for student_id in student_ids:
    #             if not self.env['school.student'].browse(student_id).exists():
    #                 raise ValidationError("Cannot create a new student from the class model.")
    #     return super(ManageClub, self).create(vals)
    #
    # def write(self, vals):
    #     if 'student_ids' in vals:
    #         student_ids = vals['student_ids'][0][2]
    #         for student_id in student_ids:
    #             if not self.env['school.student'].browse(student_id).exists():
    #                 raise ValidationError("Cannot create a new student from the class model.")
    #     return super(ManageClub, self).write(vals)


