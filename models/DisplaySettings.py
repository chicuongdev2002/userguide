from odoo import models, fields, api

class DisplaySettings(models.Model):
    _name = 'display.settings'
    _description = 'Display Settings'

    new_uom_field_1 = fields.Selection([
        ('option1', 'Đúng'),
        ('option2', 'Hổng phải'),
    ], string="Bạn có phải Chí Cường không?", readonly=True)

    @api.model
    def default_get(self, fields):
        res = super(DisplaySettings, self).default_get(fields)
        res['new_uom_field_1'] = self.env['ir.config_parameter'].sudo().get_param('new_uom_field_1')
        return res
