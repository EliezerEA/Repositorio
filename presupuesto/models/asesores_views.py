# -*- coding: utf-8 -*-
import logging
from random import randint

from odoo import models, fields, api
from odoo.addons.base.models.res_partner import PartnerCategory
from odoo.exceptions import ValidationError


class ruta(models.Model):
    _description = 'Vista de Asesores'
    _name = 'presupuesto.asesor'

    name = fields.Char(string='Nombre del Acesor', required=True)
    email = fields.Char(string='Correo Electronico', required=True)
    telefono = fields.Char(string='Telefono', required=True)
    active = fields.Boolean(default=True, help="El campo activo le permite ocultar la categoría sin eliminarla.")


class Partner(models.Model):
    # _description = 'Contact'
    _inherit = 'sale.order'
    _name = 'sale.order'
    asesor_partner = fields.Many2one('presupuesto.asesor', string='Asesor de ventas')
    asesor_partner_phone = fields.Char(related='asesor_partner.telefono', string="Telefono", readonly=True)
    asesor_partner_email = fields.Char(related='asesor_partner.email', string="Correo", readonly=True)
       