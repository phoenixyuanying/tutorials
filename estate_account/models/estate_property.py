# -*- coding:utf-8 -*-

from odoo import models
from odoo.exceptions import UserError
from datetime import date
from odoo import Command

class InheritedEstateProperty(models.Model):
    _inherit= "estate.property"
    def set_property_sold(self):
        print("Override set_property_sold")
        journal = self.env["account.journal"].search([
            ('type', '=', 'sales'), ('company_id', '=', self.env.company.id)])
        print("self.env.company.name = {}".format(self.env.company.name))
        if not journal:
            journal = self.env["account.journal"].create({
                "code" : str(self.env.company.id) + "_sales_" + str(date.today()),
                "company_id" : self.env.company.id,
                "name" : self.env.company.name + "_sales_journal",
                "type" : "sale",
            })
            # raise UserError("Please define an accounting sales journal for the company")
        print("Creating account move...")
        self.env["account.move"].create({
            "move_type" : "out_invoice",
            "partner_id" : self.buyer_id,
            "journal_id" : journal.id,
            "invoice_line_ids" : [
                Command.create({
                "name" : "Selling fee",
                "quantity" : 1,
                "price_unit" : 0.6 * self.selling_price
                }),
                Command.create({
                "name" : "Administrative fee",
                "quantity" : 1,
                "price_unit" : 100.0
                })
            ],
        })
        return super().set_property_sold()