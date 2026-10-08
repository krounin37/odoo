# -*- coding: utf-8 -*-
import json
import logging
import os
from . import models

_logger = logging.getLogger(__name__)


def _load_vietnam_wards_data(env):
    """
    Tự động nạp bộ dữ liệu Đơn Vị Hành Chính Việt Nam mới (mô hình 2 cấp - Nghị quyết 202/2025/QH15):
    - Cập nhật thông tin 34 tỉnh/thành phố (mã tỉnh, mã viết tắt, trung tâm hành chính).
    - Nạp 3.321 Phường/Xã/Thị trấn mới trực thuộc 34 tỉnh/thành, kèm lịch sử sáp nhập các đơn vị cũ (dvhcvn/34tinhthanh).
    """
    State = env['res.country.state']
    Ward = env['res.ward']
    vn = env.ref('base.vn', raise_if_not_found=False)
    if not vn:
        return

    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    prov_file = os.path.join(data_dir, 'dvhcvn_provinces.json')
    ward_file = os.path.join(data_dir, 'dvhcvn_wards_new.json')

    # 1. Cập nhật 34 tỉnh thành
    state_by_code = {}
    if os.path.exists(prov_file):
        try:
            with open(prov_file, 'r', encoding='utf-8') as f:
                provinces = json.load(f)
            for p in provinces:
                s = State.search([
                    ('country_id', '=', vn.id),
                    '|', ('name', 'ilike', p['short_name']),
                         ('name', 'ilike', p['name'])
                ], limit=1)
                if s:
                    s.write({
                        'vn_province_code': p.get('province_code'),
                        'vn_code_short': p.get('code'),
                        'vn_place_type': 'city' if p.get('place_type') == 'Thành phố Trung Ương' else 'province',
                    })
                    state_by_code[p.get('province_code')] = s.id
        except Exception as e:
            _logger.error("Lỗi cập nhật 34 tỉnh/thành: %s", str(e))

    # 2. Nạp 3.321 Phường / Xã mới (2 cấp)
    if os.path.exists(ward_file):
        try:
            with open(ward_file, 'r', encoding='utf-8') as f:
                wards_list = json.load(f)

            Ward.search([]).unlink()

            vals_list = []
            for item in wards_list:
                p_code = item.get('province_code')
                state_id = state_by_code.get(p_code)
                if not state_id:
                    s = State.search([
                        ('country_id', '=', vn.id),
                        '|', ('name', 'ilike', item.get('province_short_name', '')),
                             ('name', 'ilike', item.get('province_name', ''))
                    ], limit=1)
                    if s:
                        state_id = s.id
                        state_by_code[p_code] = s.id

                if state_id:
                    old_units_str = ', '.join(item.get('old_units', [])) if item.get('old_units') else ''
                    vals_list.append({
                        'name': item.get('ward_name'),
                        'code': item.get('ward_code'),
                        'state_id': state_id,
                        'has_merger': bool(item.get('has_merger')),
                        'old_units': old_units_str,
                        'merger_details': item.get('merger_details') or '',
                        'administrative_center': item.get('administrative_center') or '',
                    })

            batch_size = 1000
            for i in range(0, len(vals_list), batch_size):
                batch = vals_list[i:i + batch_size]
                Ward.create(batch)

            _logger.info("Đã nạp thành công %d Phường/Xã mới (2 cấp) vào Odoo.", len(vals_list))
        except Exception as e:
            _logger.error("Lỗi nạp danh mục Phường/Xã 2 cấp: %s", str(e))

