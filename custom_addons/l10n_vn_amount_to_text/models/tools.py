# -*- coding: utf-8 -*-

DIGITS = ['không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín']
UNITS = ['', 'nghìn', 'triệu', 'tỷ', 'nghìn tỷ', 'triệu tỷ', 'tỷ tỷ']


def _read_three_digits(number, read_zero_hundred=False):
    """Đọc một cụm 3 chữ số: trăm, chục, đơn vị"""
    hundred = number // 100
    remainder = number % 100
    ten = remainder // 10
    unit = remainder % 10

    words = []
    if hundred > 0 or read_zero_hundred:
        words.append(DIGITS[hundred] + ' trăm')

    if ten > 1:
        words.append(DIGITS[ten] + ' mươi')
        if unit == 1:
            words.append('mốt')
        elif unit == 4:
            words.append('tư')
        elif unit == 5:
            words.append('lăm')
        elif unit > 0:
            words.append(DIGITS[unit])
    elif ten == 1:
        words.append('mười')
        if unit == 5:
            words.append('lăm')
        elif unit > 0:
            words.append(DIGITS[unit])
    elif ten == 0:
        if (hundred > 0 or read_zero_hundred) and unit > 0:
            words.append('linh')
            words.append(DIGITS[unit])
        elif unit > 0:
            words.append(DIGITS[unit])

    return ' '.join(words)


def amount_to_vietnamese_words(amount, currency_name='VND'):
    """Chuyển đổi số tiền thành chuỗi chữ Tiếng Việt hoàn chỉnh"""
    if amount is None:
        return ''

    is_negative = amount < 0
    amount = abs(amount)

    integer_part = int(amount)
    fractional_part = int(round((amount - integer_part) * 100))

    if integer_part == 0:
        res = 'Không'
    else:
        groups = []
        temp = integer_part
        while temp > 0:
            groups.append(temp % 1000)
            temp //= 1000

        group_words = []
        for i, group in enumerate(groups):
            if group > 0:
                read_zero_hundred = (i < len(groups) - 1)
                text = _read_three_digits(group, read_zero_hundred=read_zero_hundred)
                unit = UNITS[i] if i < len(UNITS) else ''
                if unit:
                    group_words.append(f"{text} {unit}")
                else:
                    group_words.append(text)

        group_words.reverse()
        res = ' '.join(group_words).strip()

    # Thêm tiền tệ
    currency_upper = (currency_name or 'VND').upper()
    if currency_upper in ['VND', 'VNĐ']:
        currency_label = 'đồng'
    elif currency_upper == 'USD':
        currency_label = 'đô la Mỹ'
    elif currency_upper == 'EUR':
        currency_label = 'euro'
    else:
        currency_label = currency_name.lower()

    if fractional_part > 0 and currency_upper != 'VND':
        frac_text = _read_three_digits(fractional_part, read_zero_hundred=False)
        full_text = f"{res} {currency_label} và {frac_text} xu."
    else:
        full_text = f"{res} {currency_label} chẵn."

    if is_negative:
        full_text = "Âm " + full_text

    # Viết hoa chữ cái đầu tiên
    return full_text[0].upper() + full_text[1:]
