# -*- coding: utf-8 -*-
from odoo import models, fields, api


def _calculate_pit_progressive(taxable_income):
    """Tính thuế TNCN theo biểu thuế lũy tiến từng phần 7 bậc (Thông tư 111/2013/TT-BTC)"""
    if taxable_income <= 0:
        return 0.0
    if taxable_income <= 5000000:
        return taxable_income * 0.05
    elif taxable_income <= 10000000:
        return taxable_income * 0.10 - 250000
    elif taxable_income <= 18000000:
        return taxable_income * 0.15 - 750000
    elif taxable_income <= 32000000:
        return taxable_income * 0.20 - 1650000
    elif taxable_income <= 52000000:
        return taxable_income * 0.25 - 3250000
    elif taxable_income <= 80000000:
        return taxable_income * 0.30 - 5850000
    else:
        return taxable_income * 0.35 - 9850000


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    vn_citizen_id = fields.Char(
        string='Số CCCD / CMND',
        copy=False,
        help='Số Căn cước công dân hoặc Chứng minh nhân dân'
    )
    vn_tax_code = fields.Char(
        string='Mã số thuế cá nhân (TNCN)',
        copy=False
    )
    vn_social_insurance_no = fields.Char(
        string='Mã số sổ BHXH',
        copy=False
    )
    vn_dependent_count = fields.Integer(
        string='Số người phụ thuộc',
        default=0,
        help='Số người phụ thuộc đăng ký giảm trừ gia cảnh'
    )

    vn_currency_id = fields.Many2one(
        'res.currency',
        string='Tiền tệ',
        default=lambda self: self.env.ref('base.VND', raise_if_not_found=False) or self.env.company.currency_id
    )

    vn_salary_gross = fields.Monetary(
        string='Lương Gross hàng tháng',
        currency_field='vn_currency_id',
        default=15000000.0,
        help='Mức lương thỏa thuận trước khi trích bảo hiểm và thuế'
    )
    vn_insurance_salary = fields.Monetary(
        string='Mức lương đóng BHXH',
        currency_field='vn_currency_id',
        default=5000000.0,
        help='Mức lương làm căn cứ trích đóng bảo hiểm (áp dụng trần 20 lần mức lương cơ sở)'
    )
    vn_self_deduction = fields.Monetary(
        string='Giảm trừ bản thân',
        currency_field='vn_currency_id',
        default=11000000.0
    )
    vn_dependent_deduction = fields.Monetary(
        string='Giảm trừ 1 người phụ thuộc',
        currency_field='vn_currency_id',
        default=4400000.0
    )

    # Cấu hình Công Đoàn
    vn_has_union = fields.Boolean(
        string='Tham gia Công Đoàn',
        default=True,
        help='Bỏ tích chọn nếu người lao động không tham gia công đoàn hoặc công ty không trích kinh phí công đoàn 2%'
    )
    vn_has_union_fee = fields.Boolean(
        string='Trích Đoàn Phí NLĐ (1%)',
        default=False,
        help='Tích chọn nếu người lao động trích nộp đoàn phí công đoàn 1% từ tiền lương'
    )
    vn_ee_union_fee = fields.Monetary(
        string='Đoàn phí công đoàn NLĐ (1%)',
        compute='_compute_vn_payroll',
        currency_field='vn_currency_id'
    )

    # Cấu hình & Biến Động Thuế TNCN
    vn_pit_calc_method = fields.Selection(
        selection=[
            ('progressive', 'Lũy tiến 7 bậc (HĐLĐ từ 3 tháng trở lên)'),
            ('flat_10', 'Khấu trừ 10% tại nguồn (HĐLĐ dưới 3 tháng / Vãng lai / Thử việc)'),
            ('flat_20', 'Khấu trừ 20% tại nguồn (Cá nhân không cư trú)'),
            ('commitment', 'Cam kết mẫu 08/CK-TNCN (Miễn khấu trừ - Thuế 0%)'),
            ('custom', 'Nhập số tiền thuế thủ công'),
        ],
        string='Phương pháp tính Thuế TNCN',
        default='progressive',
        required=True,
        help='Chọn phương pháp tính thuế phù hợp với loại hợp đồng và tình trạng cư trú'
    )
    vn_non_taxable_income = fields.Monetary(
        string='Thu nhập miễn thuế / Phụ cấp không chịu thuế',
        currency_field='vn_currency_id',
        default=0.0,
        help='Các khoản phụ cấp ăn trưa, điện thoại, trang phục, công tác phí khoán chi không tính vào thu nhập chịu thuế'
    )
    vn_other_deductions = fields.Monetary(
        string='Các khoản giảm trừ khác',
        currency_field='vn_currency_id',
        default=0.0,
        help='Các khoản đóng góp từ thiện, nhân đạo, quỹ hưu trí tự nguyện được giảm trừ'
    )
    vn_custom_pit_tax = fields.Monetary(
        string='Thuế TNCN nhập thủ công',
        currency_field='vn_currency_id',
        default=0.0,
        help='Áp dụng khi chọn phương pháp tính thuế là Nhập số tiền thuế thủ công'
    )
    vn_tax_adjustment = fields.Monetary(
        string='Điều chỉnh thuế trong kỳ (+/-)',
        currency_field='vn_currency_id',
        default=0.0,
        help='Số tiền điều chỉnh tăng (truy thu) hoặc giảm (hoàn thuế / khấu trừ thừa kỳ trước)'
    )

    # Các khoản bảo hiểm Người lao động đóng (10.5%)
    vn_ee_bhxh = fields.Monetary(
        string='BHXH NLĐ (8%)',
        compute='_compute_vn_payroll',
        currency_field='vn_currency_id'
    )
    vn_ee_bhyt = fields.Monetary(
        string='BHYT NLĐ (1.5%)',
        compute='_compute_vn_payroll',
        currency_field='vn_currency_id'
    )
    vn_ee_bhtn = fields.Monetary(
        string='BHTN NLĐ (1%)',
        compute='_compute_vn_payroll',
        currency_field='vn_currency_id'
    )
    vn_ee_total_insurance = fields.Monetary(
        string='Tổng BH NLĐ nộp (10.5%)',
        compute='_compute_vn_payroll',
        currency_field='vn_currency_id'
    )

    # Các khoản bảo hiểm Doanh nghiệp đóng (23.5%)
    vn_er_bhxh = fields.Monetary(
        string='BHXH Công ty (17.5%)',
        compute='_compute_vn_payroll',
        currency_field='vn_currency_id'
    )
    vn_er_bhyt = fields.Monetary(
        string='BHYT Công ty (3%)',
        compute='_compute_vn_payroll',
        currency_field='vn_currency_id'
    )
    vn_er_bhtn = fields.Monetary(
        string='BHTN Công ty (1%)',
        compute='_compute_vn_payroll',
        currency_field='vn_currency_id'
    )
    vn_er_kpcd = fields.Monetary(
        string='Kinh phí công đoàn (2%)',
        compute='_compute_vn_payroll',
        currency_field='vn_currency_id'
    )
    vn_er_total_insurance = fields.Monetary(
        string='Tổng BH Công ty nộp (23.5%)',
        compute='_compute_vn_payroll',
        currency_field='vn_currency_id'
    )

    # Thuế TNCN & Lương Net
    vn_total_deduction = fields.Monetary(
        string='Tổng giảm trừ gia cảnh',
        compute='_compute_vn_payroll',
        currency_field='vn_currency_id'
    )
    vn_taxable_income = fields.Monetary(
        string='Thu nhập tính thuế TNCN',
        compute='_compute_vn_payroll',
        currency_field='vn_currency_id'
    )
    vn_pit_tax = fields.Monetary(
        string='Thuế TNCN phải nộp',
        compute='_compute_vn_payroll',
        currency_field='vn_currency_id'
    )
    vn_salary_net = fields.Monetary(
        string='Lương thực nhận (Net)',
        compute='_compute_vn_payroll',
        currency_field='vn_currency_id'
    )

    @api.depends(
        'vn_salary_gross', 'vn_insurance_salary', 'vn_dependent_count',
        'vn_self_deduction', 'vn_dependent_deduction', 'vn_has_union', 'vn_has_union_fee',
        'vn_pit_calc_method', 'vn_non_taxable_income', 'vn_other_deductions',
        'vn_custom_pit_tax', 'vn_tax_adjustment'
    )
    def _compute_vn_payroll(self):
        for emp in self:
            ins_sal = max(0.0, emp.vn_insurance_salary or 0.0)
            gross = max(0.0, emp.vn_salary_gross or 0.0)

            # Người lao động: 8% + 1.5% + 1% = 10.5%
            ee_bhxh = round(ins_sal * 0.08)
            ee_bhyt = round(ins_sal * 0.015)
            ee_bhtn = round(ins_sal * 0.01)
            ee_total_ins = ee_bhxh + ee_bhyt + ee_bhtn

            # Đoàn phí công đoàn NLĐ (1% lương nếu có tham gia & trích nộp)
            ee_union_fee = 0.0
            if emp.vn_has_union and emp.vn_has_union_fee:
                ee_union_fee = round(ins_sal * 0.01)

            # Doanh nghiệp: BHXH 17.5% + BHYT 3% + BHTN 1% = 21.5% + KPCĐ 2% (nếu có tham gia công đoàn)
            er_bhxh = round(ins_sal * 0.175)
            er_bhyt = round(ins_sal * 0.03)
            er_bhtn = round(ins_sal * 0.01)
            er_kpcd = round(ins_sal * 0.02) if emp.vn_has_union else 0.0
            er_total_ins = er_bhxh + er_bhyt + er_bhtn + er_kpcd

            # Thu nhập chịu thuế sau khi trừ các khoản phụ cấp miễn thuế
            non_taxable = max(0.0, emp.vn_non_taxable_income or 0.0)
            gross_taxable = max(0.0, gross - non_taxable)

            # Giảm trừ gia cảnh & các khoản giảm trừ khác (từ thiện, nhân đạo...)
            self_ded = emp.vn_self_deduction or 11000000.0
            dep_ded = (emp.vn_dependent_count or 0) * (emp.vn_dependent_deduction or 4400000.0)
            other_ded = max(0.0, emp.vn_other_deductions or 0.0)
            total_ded = self_ded + dep_ded + other_ded

            # Thu nhập tính thuế = Thu nhập chịu thuế - Bảo hiểm NLĐ - Giảm trừ
            taxable_income = max(0.0, gross_taxable - ee_total_ins - total_ded)

            # Tính thuế TNCN theo phương pháp được chọn
            method = emp.vn_pit_calc_method or 'progressive'
            if method == 'commitment':
                pit = 0.0
            elif method == 'flat_10':
                pit = round(gross_taxable * 0.10)
            elif method == 'flat_20':
                pit = round(gross_taxable * 0.20)
            elif method == 'custom':
                pit = max(0.0, round(emp.vn_custom_pit_tax or 0.0))
            else:
                pit = round(_calculate_pit_progressive(taxable_income))

            # Điều chỉnh biến động thuế (+/-) trong kỳ (hoàn thuế / truy thu)
            adjustment = emp.vn_tax_adjustment or 0.0
            final_pit = max(0.0, pit + adjustment)

            # Lương Net = Gross - Bảo hiểm NLĐ - Đoàn phí NLĐ - Thuế TNCN
            net = max(0.0, gross - ee_total_ins - ee_union_fee - final_pit)

            emp.vn_ee_bhxh = ee_bhxh
            emp.vn_ee_bhyt = ee_bhyt
            emp.vn_ee_bhtn = ee_bhtn
            emp.vn_ee_total_insurance = ee_total_ins
            emp.vn_ee_union_fee = ee_union_fee

            emp.vn_er_bhxh = er_bhxh
            emp.vn_er_bhyt = er_bhyt
            emp.vn_er_bhtn = er_bhtn
            emp.vn_er_kpcd = er_kpcd
            emp.vn_er_total_insurance = er_total_ins

            emp.vn_total_deduction = total_ded
            emp.vn_taxable_income = taxable_income
            emp.vn_pit_tax = final_pit
            emp.vn_salary_net = net
