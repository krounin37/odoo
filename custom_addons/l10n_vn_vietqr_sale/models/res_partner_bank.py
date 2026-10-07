# -*- coding: utf-8 -*-
from odoo import models, fields, api

BANK_BIC_MAP = {
    'BFTVVNVX': 'VCB',   # Vietcombank
    'ICBVVNVX': 'CTG',   # VietinBank
    'BIDVVNVX': 'BIDV',  # BIDV
    'VTCBVNVX': 'TCB',   # Techcombank
    'MBBEVNVX': 'MB',    # MBBank
    'ASCBVNVX': 'ACB',   # ACB
    'VPBNVNVX': 'VPB',   # VPBank
    'TPBNVNVX': 'TPB',   # TPBank
    'STBBVNVX': 'STB',   # Sacombank
    'HDBKVNVX': 'HDB',   # HDBank
    'VIBNVNVX': 'VIB',   # VIB
    'MSBVVNVX': 'MSB',   # MSB
    'OCBVVNVX': 'OCB',   # OCB
    'SHBVVNVX': 'SHB',   # SHB
    'SEABVNVX': 'SEAB',  # SeABank
    'LPBVVNVX': 'LPB',   # LPBank
    'EBBKVNVX': 'EIB',   # Eximbank
}


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    vietqr_bank_code = fields.Char(
        string='Mã VietQR (BIN/Short Name)',
        help='Mã viết tắt ngân hàng theo VietQR (như VCB, MB, TCB, CTG, ACB, VPB, TPB,...) hoặc mã BIN 6 số.'
    )

    def get_vietqr_bank_code(self):
        self.ensure_one()
        if self.vietqr_bank_code:
            return self.vietqr_bank_code.strip()

        # Tự động suy ra từ BIC
        bic = (self.bank_bic or (self.bank_id and self.bank_id.bic) or '').strip().upper()
        if bic in BANK_BIC_MAP:
            return BANK_BIC_MAP[bic]

        # Tự động suy ra từ tên ngân hàng nếu có
        bank_name = (self.bank_id and self.bank_id.name or '').upper()
        for k, v in BANK_BIC_MAP.items():
            if v in bank_name:
                return v

        return (self.bank_bic or '').strip()
