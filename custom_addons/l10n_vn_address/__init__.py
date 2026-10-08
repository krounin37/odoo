# -*- coding: utf-8 -*-
import json
import logging
import os
from . import models

_logger = logging.getLogger(__name__)


def _load_vietnam_wards_data(env):
    """Tự động nạp toàn bộ danh mục hơn 10.000 Phường / Xã / Thị trấn Việt Nam vào database khi cài đặt module"""
    Ward = env['res.ward']
    if Ward.search_count([]) > 0:
        return

    json_path = os.path.join(os.path.dirname(__file__), 'data', 'vietnam_wards.json')
    if not os.path.exists(json_path):
        _logger.warning("Không tìm thấy file data/vietnam_wards.json")
        return

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            wards_data = json.load(f)

        District = env['res.district']
        all_districts = District.search([])
        dist_by_code = {d.code: d.id for d in all_districts if d.code}
        dist_by_name = {d.name.lower(): d.id for d in all_districts}

        vals_list = []
        for item in wards_data:
            dist_id = dist_by_code.get(item['district_code']) or dist_by_name.get(item.get('district_name', '').lower())
            if dist_id:
                vals_list.append({
                    'name': item['name'],
                    'code': item.get('code', ''),
                    'district_id': dist_id,
                })

        batch_size = 2000
        for i in range(0, len(vals_list), batch_size):
            batch = vals_list[i:i + batch_size]
            Ward.create(batch)

        _logger.info("Đã nạp thành công %d Phường / Xã / Thị trấn vào cơ sở dữ liệu Odoo.", len(vals_list))
    except Exception as e:
        _logger.error("Lỗi khi nạp dữ liệu Phường/Xã: %s", str(e))

