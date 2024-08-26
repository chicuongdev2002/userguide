from odoo import models, fields,api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    new_uom_field_1 = fields.Selection(
        [('option1', 'Đúng'), ('option2', 'Hổng phải')],
        string="Bạn có phải Chí Cường không?",
        default='option1',
    )
    new_uom_field_2 = fields.Selection(
        [('option1', 'Option 1'), ('option2', 'Option 2')],
        string="Câu hỏi 2",
        default='option1',
    )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('new_uom_field_1', self.new_uom_field_1)

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            new_uom_field_1=self.env['ir.config_parameter'].sudo().get_param('new_uom_field_1'),
        )
        return res
    # @api.model
    # def get_values(self):
    #     res = super(ResConfigSettings, self).get_values()
    #     res.update(
    #         new_uom_field_1=self.env['ir.config_parameter'].sudo().get_param('new_uom_field_1', default='option1')
    #     )
    #     return res