from odoo import api, fields, models
from odoo.exceptions import ValidationError
import datetime
from dateutil.relativedelta import relativedelta


class Consumers(models.Model):
    _name = 'consumers.bank'
    _description = 'Consumers of the bank'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Info
    name = fields.Char(string="Name")
    birthday = fields.Date(string="Birthday")
    age = fields.Integer(string="Age", compute="_AgeCalculate", inverse="_InverseAgeCalculate")
    seq = fields.Char(string="Seq", readonly=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender')
    image = fields.Image(string="Image")

    # Account
    password = fields.Char(string="PIN")
    isVIP = fields.Boolean(string='VIP', tracking=True)
    state = fields.Selection([
        ('stop', 'Stop'),
        ('secure', 'Secure'),
        ('freeze', 'Freeze'),
    ], string='State', default='secure', tracking=True)
    money_history = fields.One2many('money.history.bank', 'bank_money_history', string="Money history")
    account = fields.Integer(string="Account", default=0, tracking=True)
    date_registered = fields.Date(string="Date registered")

    # Connect
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='email', tracking=True)

    @api.depends('money_history')
    def Account(self):
        print(self.money_history)

    @api.depends('birthday')
    def _AgeCalculate(self):
        time = datetime.date.today().year
        for rec in self:
            if rec.birthday:
                rec.age = time - rec.birthday.year
            else:
                rec.age = 0

    @api.depends('age')
    def _InverseAgeCalculate(self):
        today = datetime.date.today()
        for rec in self:
            if rec.age:
                rec.birthday = today - relativedelta(years=rec.age)

    @api.model
    def create(self, vals):
        print('Create method -',vals)

        if vals['age'] < 18:
            raise ValidationError('The age should be above 18')
        vals['seq'] = self.env['ir.sequence'].next_by_code('consumer.seq')

        ref = super(Consumers, self).create(vals)
        return ref

    def write(self, vals):
        res = super(Consumers, self).write(vals)
        print('Write method -',vals)

        for rec in self:
            age = datetime.date.today().year - rec.birthday.year
        if age < 18:
            raise ValidationError('The age should be above 18')
        return res

    def stop(self):
        self.state = 'stop'

    def secure(self):
        self.state = 'secure'

    def freeze(self):
        self.state = 'freeze'


class MoneyHistory(models.Model):
    _name = "money.history.bank"
    _description = "Money history bank"

    money_service = fields.Selection([
        ('add', 'Add'),
        ('pull', 'Pull'),
    ], string="MS", required=True)
    money_count = fields.Float(string="Money count")
    bank_place = fields.Many2one('banks.bank')
    datetime = fields.Datetime(string="When", default=datetime.datetime.now())

    bank_money_history = fields.Many2one('consumers.bank')

    @api.onchange('money_service')
    def on_change_money_service(self):
        for rec in self:
            if self.money_service == 'add':
                return {'domain': {'bank_place': [('IsAdd', '=', True)]}}
            else:
                return {'domain': []}

    def create(self, vals):
        id_bank = self.env['consumers.bank'].browse(vals[-1]['bank_money_history'])

        print(vals)
        count = 0
        for v in vals:
            if v['money_service'] == 'add':
                count += v['money_count']
            else:
                count -= v['money_count']
        print(count)

        id_bank.write({
            'account': id_bank.account + count
        })
        return super(MoneyHistory, self).create(vals)
