# -*- coding: utf-8 -*-

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    
    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False, default = fields.Date.today() + relativedelta(months = 3))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Float(default = 2)
    living_area = fields.Float()
    facades = fields.Float()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float()
    garden_orientation = fields.Selection(
        string = 'Orientation',
        selection = [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help = "The orientation of the garden."
    )
    active = fields.Boolean(default = True)
    state = fields.Selection(
        string = 'State',
        selection = [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        required = True,
        copy = False,
        default = 'new'
    )
    property_type_id = fields.Many2one('estate.property.type', string = 'Property Type')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string = 'Buyer', copy = False)
    tag_ids = fields.Many2many('estate.property.tag', string = 'Property Tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    total_area = fields.Float(compute = '_compute_total_area')

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(compute = '_compute_best_price')

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'),default = 0) 

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden is True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        elif self.garden is False:
            self.garden_area = False
            self.garden_orientation = False

    def set_property_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold properties cannot be canceled.')
            else: record.state = 'canceled'
        return True

    def set_property_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('Canceled properties cannot be sold.')
            else: record.state = 'sold'
        return True

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price >= 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'The selling price must be strictly positive.'),
        ('check_bedrooms_positive', 'Check(bedrooms >= 0)', 'The bedrooms must be strictly positive.')
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            goodPrice = 1
            if not record.selling_price == False:
                goodPrice = float_compare(record.selling_price, record.expected_price * 0.9, 2, )
            if goodPrice < 0:
                raise UserError('The selling price cannot be accepted if less than 90 percent of the expected price.')
    
    # Check the state prevent from delete the property which state is not New or Canceled        
    def unlink(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError('cannot delete property which status is New or Canceled')
        return super().unlink()
    
    