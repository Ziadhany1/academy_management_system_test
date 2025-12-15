from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = 'res.partner' 
    is_student = fields.Boolean(string='Is Student') 
    is_instructor = fields.Boolean(string='Is Instructor') 

    student_enrollment_ids = fields.One2many(
        'academy.enrollment', 
        'student_id', 
        string='Student Enrollments'
    ) 

    instructor_course_ids = fields.One2many(
        'academy.course', 
        'instructor_id', 
        string='Courses Taught'
    ) 
    total_courses_enrolled = fields.Integer(
        string='Total Courses Enrolled', 
        compute='_compute_total_courses', 
        store=True
    )

    total_courses_teaching = fields.Integer(
        string='Total Courses Teaching', 
        compute='_compute_total_courses', 
        store=True
    )

    @api.depends('student_enrollment_ids', 'instructor_course_ids')
    def _compute_total_courses(self):
        for partner in self:
            partner.total_courses_enrolled = len(partner.student_enrollment_ids)
            partner.total_courses_teaching = len(partner.instructor_course_ids)