from odoo import fields, models, api
from odoo.exceptions import ValidationError

class AcademyEnrollment(models.Model):
    _name = 'academy.enrollment'
    _description = 'Course Enrollment'
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    student_id = fields.Many2one('res.partner', string='Student', required=True) 
    course_id = fields.Many2one('academy.course', string='Course', required=True) 
    enrollment_date = fields.Date(default=fields.Date.today) 
    state = fields.Selection([ 
        ('draft', 'Draft'), 
        ('confirmed', 'Confirmed'), 
        ('cancelled', 'Cancelled'), 
        ('completed', 'Completed')
    ], default='draft', tracking=True)
    
    grade = fields.Float(string='Grade (0-100)') 
    attendance_percentage = fields.Float(string='Attendance (%)') 
    notes = fields.Text() 

 
    student_name = fields.Char(related='student_id.name', string='Student Name', store=True) 
    course_name = fields.Char(related='course_id.name', string='Course Name', store=True) 

   
    passed = fields.Boolean(
        string='Passed Course', 
        compute='_compute_passed', 
        store=True
    )

 
    @api.depends('grade', 'attendance_percentage')
    def _compute_passed(self):
        for enrollment in self:
           
            enrollment.passed = enrollment.grade >= 60 and enrollment.attendance_percentage >= 75 

    _sql_constraints = [
        ('student_course_unique',
         'UNIQUE(student_id, course_id)',
         'A student can only be enrolled in a course once.')
    ]

    def action_confirm(self):
        for enrollment in self:
           
            if enrollment.course_id.available_seats <= 0:
                raise ValidationError("Cannot confirm enrollment. The course is full.")
            enrollment.state = 'confirmed'
        
    def action_cancel(self):
        self.state = 'cancelled'

    def action_complete(self):
        self.state = 'completed'