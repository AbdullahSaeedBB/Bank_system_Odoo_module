from odoo import api, fields, models
from odoo.exceptions import ValidationError
import datetime


class VipCheck(models.TransientModel):
    _name = 'vip.check'
    _description = 'Check of consumer can upgrade his account to VIP'

    consumer = fields.Many2one('consumers.bank')
    # money_history = fields.One2many('money.history.bank', 'bank_money_history', string="Money history")
    can_upgrade = fields.Boolean(default=True)

    char1 = fields.Boolean(default=True)
    char2 = fields.Boolean(default=True)
    char3 = fields.Boolean(default=True)

    def upgrade_to_vip(self):
        print(self.consumer.id)
        self.env['consumers.bank'].browse(self.consumer.id).write({'isVIP': True})

    @api.model
    def default_get(self, fields):
        rec = super(VipCheck, self).default_get(fields)

        print(rec)
        if rec != {'char2': True, 'char1': True, 'char3': True}:
            rec.update({
                'char1': True,
                'char2': True,
                'char3': True})
            print(rec)

            upgrade = True

            # Had more than 100,000
            if self.env['consumers.bank'].browse(rec['consumer']).account < 100000:
                upgrade = False
                rec.update({'char1': False})
                print("Not Pass 1")

            # Had add 50,000
            money_history = self.env['consumers.bank'].browse(rec['consumer']).money_history
            for func in money_history:
                i_check = False
                if func.money_service == 'add' and func.money_count >= 50000:
                    i_check = True
            if not i_check:
                upgrade = False
                rec.update({'char2': False})
                print("Not Pass 2")

            # Had made his account than 1 year
            if datetime.date.today().year - self.env['consumers.bank'].browse(rec['consumer']).date_registered.year < 1:
                upgrade = False
                rec.update({'char3': False})
                print("Not Pass 3")

            rec.update({'can_upgrade': upgrade})

            return rec
        else:
            return rec
