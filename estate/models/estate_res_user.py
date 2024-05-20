# -*- coding: utf-8 -*-

from odoo import models, fields

class EstateResUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson_id", domain = "[('salesperson_id', '=', active_id)]")

