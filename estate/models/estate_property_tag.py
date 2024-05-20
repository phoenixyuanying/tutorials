# -*- coding: utf-8 -*-

from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = "name"

    name = fields.Char(required = True)
    color = fields.Integer()

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'A tag with the same name already exists.')
    ]