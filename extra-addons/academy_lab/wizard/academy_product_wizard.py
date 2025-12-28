from odoo import models, fields, api

class AcademyProductWizard(models.TransientModel):
    _name = "academy.product.wizard"
    _description = "Generate Product from Course"

    name = fields.Char(string="Product Name", required=True)
    price = fields.Float(string="Price", required=True)

    def action_create_product(self):
        self.ensure_one()

        course = self.env["academy.course"].browse(
            self.env.context.get("active_id")
        )

        product = self.env["product.product"].create({
            "name": self.name,
            "list_price": self.price,
            "type": "service",
            "course_id": course.id,
        })

        course.product_id = product.id

        return {"type": "ir.actions.act_window_close"}
