from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AcademyCourse(models.Model):
    _name = 'academy.course'
    _description = 'Academy Course'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, tracking=True)
    code = fields.Char(required=True, index=True)
    description = fields.Text()
    product_id = fields.Many2one('product.product', string='Related Product', readonly=True)

    instructor_id = fields.Many2one(
        'res.partner',
        string='Instructor'
    )
    product_id = fields.Many2one(
        'product.product',
        string='Related Product',
        readonly=True)


    instructor_name = fields.Char(
        related='instructor_id.name',
        store=True
    )

    category_id = fields.Many2one(
        'academy.course.category',
        string='Category'
    )

    duration_hours = fields.Float()
    max_students = fields.Integer(default=20)

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('published', 'Published'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft',
        tracking=True
    )

    start_date = fields.Date(tracking=True)
    end_date = fields.Date(tracking=True)

    enrollment_ids = fields.One2many('academy.enrollment','course_id')

    enrolled_count = fields.Integer(compute='_compute_enrolled_count',store=True)

    available_seats = fields.Integer(compute='_compute_available_seats',store=True)

    is_full = fields.Boolean(compute='_compute_is_full',store=True)

    _sql_constraints = [('code_unique', 'unique(code)', 'Course code must be unique.')]

    def action_generate_product(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Generate Product",
            "res_model": "academy.product.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_name": self.name,
            },
        }
    def action_view_sales(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Sales Orders",
            "res_model": "sale.order",
            "view_mode": "list,form",
            "domain": [
                ("order_line.product_id", "=", self.product_id.id)
            ],
    }

    @api.depends('enrollment_ids.state')
    def _compute_enrolled_count(self):
        for rec in self:
            rec.enrolled_count = len(
                rec.enrollment_ids.filtered(lambda e: e.state == 'confirmed')
            )

    @api.depends('max_students', 'enrolled_count')
    def _compute_available_seats(self):
        for rec in self:
            rec.available_seats = rec.max_students - rec.enrolled_count

    @api.depends('available_seats')
    def _compute_is_full(self):
        for rec in self:
            rec.is_full = rec.available_seats <= 0

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date < rec.start_date:
                raise ValidationError('End date must be after start date.')

    @api.constrains('max_students')
    def _check_max_students(self):
        for rec in self:
            if rec.max_students <= 0:
                raise ValidationError('Max students must be greater than zero.')

    @api.onchange('code')
    def _onchange_code(self):
        if self.code:
            self.code = self.code.upper()

    def action_publish(self):
        self.write({'state': 'published'})

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_complete(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})
