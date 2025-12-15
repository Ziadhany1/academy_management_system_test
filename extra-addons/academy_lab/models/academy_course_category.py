from odoo import fields, models, api

class AcademyCourseCategory(models.Model):
    _name = 'academy.course.category'
    _description = 'Course Category'

    name = fields.Char(required=True)
    description = fields.Text() 
    course_ids = fields.One2many('academy.course', 'category_id', string='Courses')
    
    course_count = fields.Integer(
        string='Number of Courses',
        compute='_compute_course_count',
        store=True,
    )


    @api.depends('course_ids')
    def _compute_course_count(self):
        for category in self:
            category.course_count = len(category.course_ids)