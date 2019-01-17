# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PosConfig(models.Model):
    _inherit = 'pos.config'

    branch_address = fields.Many2one('res.partner',compute='_get_branch_address')
    branch_address_street = fields.Char('res.partner',compute='_get_branch_address')
    company_address_street = fields.Char('res.partner',compute='_get_branch_address')

    @api.multi
    def _get_branch_address(self):

        self.company_address_street = '%(street)s %(street2)s %(city)s' % {
            'street': self.company_id.street or '',
            'street2': self.company_id.street2 or '',
            'city': (self.company_id.city_id.name if self.company_id.city_id else self.company_id.city) or ''
        }

        if self.stock_location_id:
            if self.stock_location_id.parent_left == 0 or self.stock_location_id.parent_right == 0:
                self.stock_location_id._parent_store_compute()
            warehouse = self.stock_location_id.get_warehouse()
            if warehouse:
                self.branch_address = warehouse.partner_id

        if self.branch_address:
            self.branch_address_street = '%(street)s %(street2)s %(city)s' % {
                'street': self.branch_address.street or '',
                'street2': self.branch_address.street2 or '',
                'city': (self.branch_address.city_id.name if self.branch_address.city_id else self.branch_address.city) or ''
            }
        else:
            self.branch_address = self.company_id.partner_id
            self.branch_address_street = self.company_address_street
