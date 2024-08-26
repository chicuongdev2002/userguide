{
    # Tên module
    'name': 'User Guide',
    'version': '1.0',

    # Loại module
    'category': 'Guide',

    # Độ ưu tiên module trong list module
    # Số càng nhỏ, độ ưu tiên càng cao
    #### Chấp nhận số âm
    'sequence': 5,

    # Mô tả module
    'summary': 'Module này giúp người dùng có thể xem hướng dẫn sử dụng các chức năng của Odoo',
    'description': '',


    # Module dựa trên các category nào
    # Khi hoạt động, category trong 'depends' phải được install
    ### rồi module này mới đc install
   'depends': ['base_setup', 'product', 'web'],

    # Module có được phép install hay không
    # Nếu bạn thắc mắc nếu tắt thì làm sao để install
    # Bạn có thể dùng 'auto_install'
    'installable': True,
    'auto_install': False,
    'application': True,

    # Import các file cấu hình
    # Những file ảnh hưởng trực tiếp đến giao diện (không phải file để chỉnh sửa giao diện)
    ## hoặc hệ thống (file group, phân quyền)
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
         'views/res_config_settings_views.xml',
          'views/display_settings_views.xml',
          'views/user_menu.xml',
          'views/user_guide_view.xml'
    ],
      'qweb': [
        'static/src/xml/file_viewer_templates.xml',
    ],


    # Import các file cấu hình (chỉ gọi từ folder 'static')
    # Những file liên quan đến
    ## + các class mà hệ thống sử dụng
    ## + các chỉnh sửa giao diện
    ## + t
     'assets': {
        'web.assets_backend': [
            'userguide/static/src/js/custom_menu_user.js',
        ],
        'point_of_sale._assets_pos': [
            'userguide/static/description/*'
        ],
    },
    'license': 'LGPL-3',
}
