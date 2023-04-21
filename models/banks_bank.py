from odoo import api, fields, models


class BanksBank(models.Model):
    _name = 'banks.bank'
    _description = 'Bank bank'

    # Location
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    city = fields.Char('City')
    country_id = fields.Many2one('res.country', string='Country')

    # Connect
    phone = fields.Char('Phone')
    email = fields.Char('Email')

    # Options
    IsAdd = fields.Boolean(string='Can deposit', default=True)
    type = fields.Selection([
        ('bank', 'Bank'),
        ('atm', 'ATM')
    ])

    def name_get(self):
        names = []
        for rec in self:
            names.append((rec.id, f"[{rec.type}] St: {rec.street}"))
        return names
