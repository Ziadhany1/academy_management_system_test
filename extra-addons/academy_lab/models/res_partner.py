from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_student = fields.Boolean()
    is_instructor = fields.Boolean()

    student_enrollment_ids = fields.One2many(
        'academy.enrollment',
        'student_id'
    )

    instructor_course_ids = fields.One2many(
        'academy.course',
        'instructor_id'
    )

    total_courses_enrolled = fields.Integer(
        compute='_compute_total_courses_enrolled'
    )

    total_courses_teaching = fields.Integer(
        compute='_compute_total_courses_teaching'
    )

    def _compute_total_courses_enrolled(self):
        for rec in self:
            rec.total_courses_enrolled = len(rec.student_enrollment_ids)

    def _compute_total_courses_teaching(self):
        for rec in self:
            rec.total_courses_teaching = len(rec.instructor_course_ids)
