# -*- coding: utf-8 -*-
import base64
import logging
import re
import socket
import unicodedata
from urllib.parse import quote, urlparse
import requests

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

SKIP_DOMAINS = [
    'bing.com', 'microsoft.com', 'wikipedia.org', 'facebook.com', 'youtube.com',
    'masothue.com', 'thongtindoanhnghiep.co', 'hosocongty.vn', 'trangvangvietnam.com',
    'dichvucong.gov.vn', 'gdt.gov.vn', 'vietqr.io', 'cas.so', 'google.com', 'linkedin.com',
    'timkiemdoanhnghiep.com', 'mst.vn', 'opendata.gov.vn', 'dangkykinhdoanh.gov.vn',
    'topcv.vn', 'vietnamworks.com', 'careerbuilder.vn', 'shopee.vn', 'lazada.vn', 'tiki.vn'
]


def _remove_accents(input_str):
    if not input_str:
        return ''
    s = str(input_str).replace('đ', 'd').replace('Đ', 'D')
    nfkd = unicodedata.normalize('NFKD', s)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)]).lower()


def _is_domain_active(domain):
    """Kiểm tra domain có resolve được IP không"""
    try:
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False


def _clean_brand_keyword(name):
    if not name:
        return ''
    clean = re.sub(r'^(công ty|tập đoàn|tổng công ty|tnhh|cổ phần|cp|doanh nghiệp tư nhân)\s+', '', name, flags=re.IGNORECASE)
    clean = re.sub(r'\s+(cổ phần|tnhh|jsc|corp|corporation|group|ltd|việt nam|viet nam|vn)\b', '', clean, flags=re.IGNORECASE)
    return clean.strip()


def _find_website_for_company(company_name, short_name=None, international_name=None):
    """
    Thuật toán đa tầng tìm website chính thức của công ty:
    Tầng 1: Domain Heuristics dựa trên tên viết tắt (shortName) & thương hiệu lõi (.vn, .com.vn, .com)
    Tầng 2: Tra cứu Wikipedia API (trích xuất thuộc tính homepage / website / trang_web từ infobox)
    Tầng 3: Tra cứu Wikidata P856 (Official Website)
    Tầng 4: Tìm kiếm Bing Web search kèm giải mã liên kết đích
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'vi,en;q=0.9',
    }

    # Tầng 1: Domain Heuristics dựa trên brand/shortName
    brand_candidates = []
    if short_name:
        clean_s = re.sub(r'\b(jsc|corp|corporation|group|ltd|vietnam|vn)\b', '', short_name, flags=re.IGNORECASE).strip()
        if clean_s:
            brand_candidates.append(clean_s)

    brand_from_name = _clean_brand_keyword(company_name)
    if brand_from_name:
        brand_candidates.append(brand_from_name)

    for b in brand_candidates:
        clean_slug = re.sub(r'[^a-zA-Z0-9]', '', _remove_accents(b)).lower()
        if len(clean_slug) >= 3:
            for tld in ['.vn', '.com.vn', '.com']:
                domain = clean_slug + tld
                if _is_domain_active(domain):
                    return f"https://{domain}"

    # Tầng 2: Tra cứu Wikipedia tiếng Việt
    try:
        w_url = f"https://vi.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote(company_name)}&format=json"
        w_res = requests.get(w_url, headers=headers, timeout=4).json()
        items = w_res.get('query', {}).get('search', [])
        if items:
            title = items[0]['title']
            page_url = f"https://vi.wikipedia.org/w/api.php?action=parse&page={quote(title)}&prop=wikitext&format=json"
            p_data = requests.get(page_url, headers=headers, timeout=4).json()
            wikitext = p_data.get('parse', {}).get('wikitext', {}).get('*', '')
            m = re.search(r'\|\s*(?:homepage|website|trang_web)\s*=\s*(?:\{\{url\|)?([^\s\}\|]+)', wikitext, re.IGNORECASE)
            if m:
                raw_u = m.group(1).strip().replace('[', '').replace(']', '')
                if not raw_u.startswith('http'):
                    raw_u = 'https://' + raw_u
                return raw_u.rstrip('/')
    except Exception:
        pass

    # Tầng 3: Tra cứu Wikidata
    try:
        search_kw = short_name or brand_from_name
        wiki_url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={quote(search_kw[:30])}&language=vi&format=json"
        w_resp = requests.get(wiki_url, headers=headers, timeout=4)
        if w_resp.status_code == 200:
            w_data = w_resp.json().get('search', [])
            if w_data:
                qid = w_data[0].get('id')
                ent_url = f"https://www.wikidata.org/w/api.php?action=wbgetclaims&entity={qid}&property=P856&format=json"
                ent_resp = requests.get(ent_url, headers=headers, timeout=4)
                if ent_resp.status_code == 200:
                    claims = ent_resp.json().get('claims', {}).get('P856', [])
                    if claims:
                        web_val = claims[0].get('mainsnak', {}).get('datavalue', {}).get('value')
                        if web_val and isinstance(web_val, str) and web_val.startswith('http'):
                            return web_val.rstrip('/')
    except Exception:
        pass

    # Tầng 4: Bing Web search và giải mã link đích
    try:
        query = f'"{company_name}" website'
        bing_url = f"https://www.bing.com/search?q={quote(query)}"
        r = requests.get(bing_url, headers=headers, timeout=5)
        if r.status_code == 200:
            matches = re.findall(r'u=(a1[a-zA-Z0-9_-]+)', r.text)
            for m in matches:
                try:
                    b64_str = m[2:].replace('-', '+').replace('_', '/')
                    b64_str += '=' * (-len(b64_str) % 4)
                    target_url = base64.b64decode(b64_str).decode('utf-8', errors='ignore')
                    netloc = urlparse(target_url).netloc.lower()
                    clean_netloc = netloc[4:] if netloc.startswith('www.') else netloc
                    if any(skip in clean_netloc for skip in SKIP_DOMAINS):
                        continue
                    return f"https://{netloc}".rstrip('/')
                except Exception:
                    continue
    except Exception:
        pass

    return False


class ResPartner(models.Model):
    _inherit = 'res.partner'

    vn_tax_status = fields.Char(
        string='Trạng thái thuế',
        readonly=True,
        copy=False,
        help='Trạng thái hoạt động của Người Nộp Thuế từ cơ quan thuế'
    )
    vn_international_name = fields.Char(
        string='Tên giao dịch quốc tế',
        copy=False,
        help='Tên tiếng Anh / quốc tế của doanh nghiệp'
    )
    vn_short_name = fields.Char(
        string='Tên viết tắt',
        copy=False
    )

    def _parse_and_match_address_vn(self, full_address):
        """Tự động phân tích chuỗi địa chỉ để xác định Country, State, District, Ward"""
        if not full_address:
            return {}

        vals = {}
        vn_country = self.env.ref('base.vn', raise_if_not_found=False)
        if vn_country:
            vals['country_id'] = vn_country.id

        norm_addr = _remove_accents(full_address)

        # 1. Khớp Tỉnh / Thành phố (res.country.state)
        matched_state = None
        if vn_country:
            states = self.env['res.country.state'].search([('country_id', '=', vn_country.id)])
            for s in states:
                norm_state = _remove_accents(s.name)
                clean_state = re.sub(r'^(tp|tinh)\s+', '', norm_state).strip()
                if clean_state and clean_state in norm_addr:
                    matched_state = s
                    break

        if matched_state:
            vals['state_id'] = matched_state.id

            # 2. Khớp Quận / Huyện (res.district nếu có)
            if 'district_id' in self._fields and 'res.district' in self.env:
                districts = self.env['res.district'].search([('state_id', '=', matched_state.id)])
                matched_district = None
                for d in districts:
                    clean_d = re.sub(r'^(quan|huyen|thi xa|thanh pho|tp)\s+', '', _remove_accents(d.name)).strip()
                    if clean_d and clean_d in norm_addr:
                        matched_district = d
                        break

                if matched_district:
                    vals['district_id'] = matched_district.id

                    # 3. Khớp Phường / Xã (res.ward nếu có)
                    if 'ward_id' in self._fields and 'res.ward' in self.env:
                        wards = self.env['res.ward'].search([('district_id', '=', matched_district.id)])
                        for w in wards:
                            clean_w = re.sub(r'^(phuong|xa|thi tran)\s+', '', _remove_accents(w.name)).strip()
                            if clean_w and clean_w in norm_addr:
                                vals['ward_id'] = w.id
                                break

        return vals

    def action_lookup_tax_info(self):
        """Gọi API tra cứu thông tin doanh nghiệp, tự điền tên, địa chỉ chi tiết và website"""
        self.ensure_one()
        if not self.vat:
            raise UserError(_("Vui lòng nhập Mã số thuế (Mã số DN) trước khi thực hiện tra cứu."))

        clean_vat = re.sub(r'[^0-9\-]', '', self.vat.strip())
        if not clean_vat:
            raise UserError(_("Mã số thuế không hợp lệ."))

        url = f"https://api.vietqr.io/v2/business/{clean_vat}"
        try:
            response = requests.get(url, timeout=8)
            res_json = response.json()
        except requests.exceptions.Timeout:
            raise UserError(_("Không thể kết nối đến máy chủ tra cứu mã số thuế (Quá thời gian chờ)."))
        except Exception as e:
            raise UserError(_("Đã xảy ra lỗi khi tra cứu mã số thuế: %s") % str(e))

        if res_json.get('code') != '00' or not res_json.get('data'):
            desc = res_json.get('desc', _('Không tìm thấy thông tin người nộp thuế.'))\
                if isinstance(res_json, dict) else _('Không tìm thấy thông tin.')
            raise UserError(_("Tra cứu thất bại: %s") % desc)

        data = res_json['data']
        company_name = data.get('name') or ''
        company_address = data.get('address') or ''
        status = data.get('status') or ''
        international_name = data.get('internationalName') or ''
        short_name = data.get('shortName') or ''

        vals = {
            'is_company': True,
            'vn_tax_status': status,
        }

        if company_name:
            vals['name'] = company_name
        if company_address:
            vals['street'] = company_address
            # Tự động bóc tách Tỉnh/Thành phố, Quận/Huyện, Phường/Xã
            address_vals = self._parse_and_match_address_vn(company_address)
            vals.update(address_vals)

        if international_name:
            vals['vn_international_name'] = international_name
        if short_name:
            vals['vn_short_name'] = short_name

        # Tự động tìm kiếm trang web của doanh nghiệp nếu đối tác chưa có website
        found_website = None
        if not self.website:
            try:
                found_website = _find_website_for_company(company_name, short_name=short_name)
                if found_website:
                    vals['website'] = found_website
            except Exception as e:
                _logger.info("Không thể tìm website tự động: %s", str(e))

        self.write(vals)

        details = []
        details.append(f"Tên: {company_name}")
        if vals.get('state_id'):
            state_rec = self.env['res.country.state'].browse(vals['state_id'])
            details.append(f"Tỉnh/Thành: {state_rec.name}")
        if vals.get('district_id') and self.env.get('res.district'):
            dist_rec = self.env['res.district'].browse(vals['district_id'])
            details.append(f"Quận/Huyện: {dist_rec.name}")
        if found_website:
            details.append(f"Website: {found_website}")
        details.append(f"Trạng thái: {status or 'Đang hoạt động'}")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Tra cứu & Cập nhật thành công!'),
                'message': '\n • '.join(details),
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
