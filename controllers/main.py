# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import json
from urllib.parse import urlparse, parse_qs

import requests
from werkzeug import urls
from werkzeug.exceptions import Forbidden
from werkzeug.utils import redirect

from odoo import _, http
from odoo.exceptions import ValidationError
from odoo.tools import html_escape

_logger = logging.getLogger(__name__)


class MainController(http.Controller):

    @http.route('/courses', type='http', auth="user", website=True)
    def get_courses(self):
        records = http.request.env['course.odoo'].search([])

        return http.request.render(
            # Tên templae (Khởi tạo trong views folder)
            "hello_world.course_list_template",

            # Object render
            ## Biến đầu tên là tên biến sẽ gọi trong template
            ## Biến thứ 2   là biến đã query ở trên
            {"courses": records},
        )
    
    #######################################
    # Hàm này chỉ demo KHÔNG CHẠY
    # báo lỗi đó
    @http.route('/courses/demo')
    def get_courses(self):

        # Lấy params từ get request
        url = http.request.httprequest.url

        parsed_url = urlparse(url)

        params = {'hihi': parse_qs(parsed_url.query)['vnp_TxnRef'][0]}
        try:
            # Gọi một method từ model
            http.request.env['payment.stack_payment'].isExistsOrder('')

            # Get dữ liệu từ model
            # Get tất cả
            http.request.env['course.odoo'].search([])
            # Get có điều kiện
            http.request.env['course.odoo'].search(['id', '=', 1])

            return redirect('/courses')
        except:
            return redirect('/courses')
