from odoo import models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super().action_confirm()

        Enrollment = self.env["academy.enrollment"]

        for order in self:
            for line in order.order_line:
                course = line.product_id.course_id
                if course:
                    exists = Enrollment.search([
                        ("student_id", "=", order.partner_id.id),
                        ("course_id", "=", course.id),
                    ], limit=1)

                    if not exists:
                        Enrollment.create({
                            "student_id": order.partner_id.id,
                            "course_id": course.id,
                            "state": "draft",
                        })

        return res
