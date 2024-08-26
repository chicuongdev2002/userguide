from odoo import models, fields, api
from odoo.exceptions import UserError
from lxml import etree

class UserGuide(models.Model):
    _name = 'user.guide'
    _description = 'User Guide'

    ###############################THUỘC TÍNH##################################
    name = fields.Char(string='Name', required=True)
    #Mô tả
    summary = fields.Text(string='Summary')
    #Nội dung
    content = fields.Html(string='Content')
    #Thuộc gr nào
    user_group_ids = fields.Many2many('res.groups', 'user_guide_res_groups_rel', 'user_guide_id', 'group_id', 'User Groups')
    #File
    file_ids = fields.Many2many('ir.attachment', 'user_guide_file_rel', 'user_guide_id', 'file_id', 'Files')
    #Danh mục
    category_id = fields.Many2one('product.category', string='Category', required=True)
    #Trạng thái
    status = fields.Selection([
        ('draft', 'Bản nháp'),
        ('pending_review', 'Chờ duyệt'),
        ('approved', 'Đã phê duyệt'),
        ('edit', 'Đã chỉnh sửa'),
        ('archived', 'Đã lưu trữ'),
        ('cancelled', 'Đã hủy')
    ], string='Status', default='draft', track_visibility='onchange')
    #Thời gian cập nhật cuối cùng
    last_edited_time = fields.Datetime(string='Last Edited Time', readonly=True)
    #Hình ảnh
    image = fields.Binary("Icon", attachment=True)
    #############################PHƯƠNG THỨC######################################
    #Phương thức mở form
    def action_open_form(self):
        if self.status == 'cancelled':
            raise UserError(_("You cannot open a cancelled document."))
        return {
            'type': 'ir.actions.act_window',
            'name': 'User Guide',
            'res_model': 'user.guide',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }
    #Phương thức mở 
    def action_open(self):
        if self.status == 'cancelled':
            raise UserError("Tài liệu này đã bị hủy và không thể xem chi tiết.")
        return {
            'type': 'ir.actions.act_window',
            'name': 'User Guide',
            'res_model': 'user.guide',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }

    # Ghi đề phương thức create
    @api.model
    def create(self, vals):
        if vals.get('status') == 'cancelled':
            raise UserError("Lỗi! Không thể tạo tài liệu với trạng thái đã hủy")
        record = super(UserGuide, self).create(vals)
        record._update_status()
        return record
    # Ghi đè phương thức write
    def write(self, vals):
        #Kiểm tra có phải admin không?
        is_admin = self.env.user.has_group('base.group_system')
         #Cảnh báo người dùng khi chuyển trạng thái thành 'cancelled'
        if not is_admin and 'status' in vals and vals['status'] == 'cancelled':
         raise Warning("Bạn đang chuyển trạng thái tài liệu thành 'đã hủy'. Hãy chắc chắn rằng bạn muốn thực hiện điều này.")
         #Kiểm tra nếu trạng thái đã hủy thì không cho chỉnh sửa
        if 'status' in vals and vals['status'] == 'cancelled':
            vals['last_edited_time'] = fields.Datetime.now()
            return super(UserGuide, self).write(vals)
        #Nếu không phải admin và tài liệu đã bị hủy thì hiển thị lỗi
        if not is_admin and self.status == 'cancelled':
            raise UserError("Lỗi! Bạn không có quyền chỉnh sửa tài liệu đã hủy. Hãy liên hệ admin")
        # Nếu không có trạng thái và trạng thái không phải là 'edit' thì chuyển trạng thái sang 'edit'
        if 'status' not in vals and self.status != 'edit':
            vals['status'] = 'edit'
        vals['last_edited_time'] = fields.Datetime.now()
         # Kiểm tra nếu file không rỗng thì chuyển trạng thái sang 'approved', trừ khi trạng thái là 'cancelled'
        if 'file' in vals and vals['file'] and self.status != 'cancelled':
            vals['status'] = 'approved'
        return super(UserGuide, self).write(vals)

    # Ghi đè phương thức unlink
    def unlink(self):
        for record in self:
            if record.status == 'cancelled':
                raise UserError("Tài liệu này đã bị hủy và không thể xóa.")
        return super(UserGuide, self).unlink()

    # Thay đổi status thành edit ngoài aprroved
    def _update_status(self):
        if self.status != 'approved':
            self.status = 'edit'
