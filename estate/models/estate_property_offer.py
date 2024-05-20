# -*- coding: utf-8 -*-

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name='estate.property.offer'
    _description='Estate Property Offer'
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string = 'Status',
        selection = [('accepted', 'Accepted'), ('refused', 'Refused')],
        copy = False,
    )
    partner_id = fields.Many2one('res.partner', required = True)
    property_id = fields.Many2one('estate.property', required = True)
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute = '_compute_date_deadline', inverse = '_set_date_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date is False:
                record.date_deadline = date.today() + timedelta(record.validity)
            else:    
                record.date_deadline = record.create_date + timedelta(record.validity)

    @api.depends("validity")
    def _set_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(record.validity)

    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'
        return True
    
    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            record.property_id.selling_price = False
            record.property_id.buyer_id = False
            record.property_id.state = 'new'
        return True
    
    _sql_constraints = {
        ('check_price_positive', 'CHECK(price >= 0)', 'The price must be strictly positive.')
    }

    @api.model
    def create(self, vals):
        property_id = self.env['estate.property'].browse(vals['property_id'])
        if vals.get('price') < property_id.best_price:
            raise UserError('Price cannot be lower than current best price.')
        property_id.state = 'offer_received'
        return super().create(vals)