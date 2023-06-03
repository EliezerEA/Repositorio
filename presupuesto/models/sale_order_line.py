# modulo para heredar sale.order.line y agregar campos
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
# api para garantia


class SaleOrder(models.Model):
    _inherit = ['sale.order.line', 'image.mixin']
    _name = "sale.order.line"

    product_image = fields.Binary(related='product_id.image_1920', string="Imagen del producto", readonly=True)
    product_image_medium = fields.Binary(related='product_id.image_1920', string="Imagen del producto", readonly=True)
    product_garantia = fields.Many2one('sale.order.garantia', string="Garantia", required=False, store=True, readonly=False)

    delivery_date_presupuesto = fields.Date(string='Fecha de entrega', required=False, store=True, readonly=False)


class ProductTemplate(models.Model):
    _inherit = "product.product"

    product_garantia = fields.Char(
        string="Garantia del producto", required=False)
    