# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PosConfig(models.Model):
    _inherit = 'pos.config'

    branch_address = fields.Many2one('res.partner',compute='_get_branch_address')
    branch_address_street = fields.Char('res.partner',compute='_get_branch_address')
    company_address_street = fields.Char('res.partner',compute='_get_branch_address')

    @api.multi
    def _get_branch_address(self):
        for rec in self:
            rec.company_address_street = '%(street)s %(street2)s %(city)s' % {
                'street': rec.company_id.street or '',
                'street2': rec.company_id.street2 or '',
                'city': (rec.company_id.city_id.name if rec.company_id.city_id else rec.company_id.city) or ''
            }

            if rec.stock_location_id:
                if rec.stock_location_id.parent_left == 0 or rec.stock_location_id.parent_right == 0:
                    rec.stock_location_id._parent_store_compute()
                warehouse = rec.stock_location_id.get_warehouse()
                if warehouse:
                    rec.branch_address = warehouse.partner_id

            if rec.branch_address:
                rec.branch_address_street = '%(street)s %(street2)s %(city)s' % {
                    'street': rec.branch_address.street or '',
                    'street2': rec.branch_address.street2 or '',
                    'city': (rec.branch_address.city_id.name if rec.branch_address.city_id else rec.branch_address.city) or ''
                }
            else:
                rec.branch_address = rec.company_id.partner_id
                rec.branch_address_street = rec.company_address_street
|