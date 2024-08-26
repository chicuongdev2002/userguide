from odoo import models, fields, api
from odoo.exceptions import AccessError

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def check(self, mode, values=None):
        """Override check method to add custom access rights check for user guides"""
        super(IrAttachment, self).check(mode, values)
        
        if mode == 'read' and self.env.context.get('bypass_user_guide_check'):
            return

        if self.env.is_superuser():
            return

        if self.env.user.has_group('userguide.group_user_guide_manager'):
            return

        if values and values.get('res_model') == 'user.guide':
            user_guide = self.env['user.guide'].browse(values.get('res_id'))
            if not user_guide.exists() or not user_guide.user_group_ids & self.env.user.groups_id:
                raise AccessError("Bạn không có quyền truy cập tài liệu này")
        
        elif self.res_model == 'user.guide':
            user_guide = self.env['user.guide'].browse(self.res_id)
            if not user_guide.exists() or not user_guide.user_group_ids & self.env.user.groups_id:
                raise AccessError("You don't have access to this User Guide attachment.")

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        # Add a context key to bypass the check in the read method
        return super(IrAttachment, self.with_context(bypass_user_guide_check=True)).search_read(
            domain=domain, fields=fields, offset=offset, limit=limit, order=order)

    def read(self, fields=None, load='_classic_read'):
        # If we're bypassing the check, just call super directly
        if self.env.context.get('bypass_user_guide_check'):
            return super(IrAttachment, self).read(fields=fields, load=load)
        
        # Otherwise, check each record individually
        result = []
        for record in self:
            try:
                record.check('read')
                result.extend(super(IrAttachment, record).read(fields=fields, load=load))
            except AccessError:
                # If access is denied, we skip this record
                continue
        return result