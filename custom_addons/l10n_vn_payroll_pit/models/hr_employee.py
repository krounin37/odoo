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

    @api.depends('vn_salary_gross', 'vn_insurance_salary', 'vn_dependent_count', 'vn_self_deduction', 'vn_dependent_deduction')
    def _compute_vn_payroll(self):
        for emp in self:
            ins_sal = max(0.0, emp.vn_insurance_salary or 0.0)
            gross = max(0.0, emp.vn_salary_gross or 0.0)

            # Người lao động: 8% + 1.5% + 1% = 10.5%
            ee_bhxh = round(ins_sal * 0.08)
            ee_bhyt = round(ins_sal * 0.015)
            ee_bhtn = round(ins_sal * 0.01)
            ee_total_ins = ee_bhxh + ee_bhyt + ee_bhtn

            # Doanh nghiệp: 17.5% + 3% + 1% + 2% = 23.5%
            er_bhxh = round(ins_sal * 0.175)
            er_bhyt = round(ins_sal * 0.03)
            er_bhtn = round(ins_sal * 0.01)
            er_kpcd = round(ins_sal * 0.02)
            er_total_ins = er_bhxh + er_bhyt + er_bhtn + er_kpcd

            # Giảm trừ gia cảnh
            self_ded = emp.vn_self_deduction or 11000000.0
            dep_ded = (emp.vn_dependent_count or 0) * (emp.vn_dependent_deduction or 4400000.0)
            total_ded = self_ded + dep_ded

            # Thu nhập tính thuế = Gross - Bảo hiểm NLĐ - Giảm trừ gia cảnh
            taxable_income = max(0.0, gross - ee_total_ins - total_ded)

            # Thuế TNCN
            pit = round(_calculate_pit_progressive(taxable_income))

            # Lương Net = Gross - Bảo hiểm NLĐ - Thuế TNCN
            net = max(0.0, gross - ee_total_ins - pit)

            emp.vn_ee_bhxh = ee_bhxh
            emp.vn_ee_bhyt = ee_bhyt
            emp.vn_ee_bhtn = ee_bhtn
            emp.vn_ee_total_insurance = ee_total_ins

            emp.vn_er_bhxh = er_bhxh
            emp.vn_er_bhyt = er_bhyt
            emp.vn_er_bhtn = er_bhtn
            emp.vn_er_kpcd = er_kpcd
            emp.vn_er_total_insurance = er_total_ins

            emp.vn_total_deduction = total_ded
            emp.vn_taxable_income = taxable_income
            emp.vn_pit_tax = pit
            emp.vn_salary_net = net
