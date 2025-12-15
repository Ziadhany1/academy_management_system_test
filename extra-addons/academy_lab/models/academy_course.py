from odoo import fields, models, api
from odoo.exceptions import ValidationError

class AcademyCourse(models.Model):
    _name = 'academy.course'
    _description = 'Course'
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    name = fields.Char(required=True, tracking=True) 
    code = fields.Char(required=True, index=True) 
    description = fields.Text() 
    instructor_id = fields.Many2one('res.partner', string='Instructor') 
    category_id = fields.Many2one('academy.course.category', string='Category') 
    duration_hours = fields.Float(string='Duration (Hours)') 
    max_students = fields.Integer(default=20) 
    
    state = fields.Selection([ 
        ('draft', 'Draft'), 
        ('published', 'Published'), 
        ('in_progress', 'In Progress'), 
        ('done', 'Done'), 
        ('cancelled', 'Cancelled')
    ], default='draft', tracking=True)
    
    start_date = fields.Date(tracking=True) 
    end_date = fields.Date(tracking=True) #
    
    enrollment_ids = fields.One2many('academy.enrollment', 'course_id', string='Enrollments') 
    instructor_name = fields.Char(related='instructor_id.name', store=True, string='Instructor Name')

    enrolled_count = fields.Integer(
        string='Enrolled Students', 
        compute='_compute_enrollment_stats', 
        store=True
    )
    available_seats = fields.Integer(
        string='Available Seats', 
        compute='_compute_enrollment_stats', 
        store=True
    ) 
    is_full = fields.Boolean(
        string='Is Full', 
        compute='_compute_enrollment_stats', 
        store=True
    ) 

    @api.depends('enrollment_ids.state', 'max_students')
    def _compute_enrollment_stats(self):
        for course in self:
           
            confirmed_enrollments = len(course.enrollment_ids.filtered(lambda e: e.state == 'confirmed'))
            course.enrolled_count = confirmed_enrollments
            course.available_seats = course.max_students - confirmed_enrollments 
            course.is_full = course.available_seats <= 0 

   
    @api.onchange('code')
    def _onchange_code(self):
        if self.code:
            self.code = self.code.upper() 

    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for course in self:
            if course.start_date and course.end_date and course.start_date > course.end_date:
                raise ValidationError("The course end date cannot be before the start date.")

    @api.constrains('max_students')
    def _check_max_students(self):
        for course in self:
            if course.max_students <= 0:
                raise ValidationError("Maximum students must be greater than zero.")

    _sql_constraints = [
        ('code_unique', 
         'UNIQUE(code)', 
         'The course code must be unique.')
    ]

    def action_publish(self):
        self.state = 'published'
        
    def action_start(self):
        self.state = 'in_progress'

    def action_complete(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancelled'