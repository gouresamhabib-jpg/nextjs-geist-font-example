"""
Input validation utilities for Employee Salary Management System
"""

import re
from typing import Optional, Tuple

def validate_name(name: str) -> Tuple[bool, str]:
    """
    Validate employee or area name
    
    Args:
        name: Name to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, "الاسم مطلوب"
    
    name = name.strip()
    
    if len(name) < 2:
        return False, "الاسم يجب أن يكون أكثر من حرف واحد"
    
    if len(name) > 100:
        return False, "الاسم طويل جداً (أكثر من 100 حرف)"
    
    # Check for invalid characters (allow Arabic, English, spaces, and common punctuation)
    if not re.match(r'^[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFFa-zA-Z\s\.\-\']+$', name):
        return False, "الاسم يحتوي على أحرف غير مسموحة"
    
    return True, ""

def validate_salary(salary: str) -> Tuple[bool, str, float]:
    """
    Validate salary amount
    
    Args:
        salary: Salary string to validate
    
    Returns:
        Tuple of (is_valid, error_message, parsed_value)
    """
    if not salary or not salary.strip():
        return False, "المرتب مطلوب", 0.0
    
    try:
        value = float(salary.strip())
        
        if value < 0:
            return False, "المرتب لا يمكن أن يكون سالباً", 0.0
        
        if value > 1000000:  # Maximum salary limit
            return False, "المرتب كبير جداً (أكثر من مليون)", 0.0
        
        # Round to 2 decimal places
        value = round(value, 2)
        
        return True, "", value
        
    except ValueError:
        return False, "يرجى إدخال رقم صحيح للمرتب", 0.0

def validate_allowance(allowance: str) -> Tuple[bool, str, float]:
    """
    Validate allowance amount
    
    Args:
        allowance: Allowance string to validate
    
    Returns:
        Tuple of (is_valid, error_message, parsed_value)
    """
    if not allowance or not allowance.strip():
        return True, "", 0.0  # Allowance is optional
    
    try:
        value = float(allowance.strip())
        
        if value < 0:
            return False, "البدل لا يمكن أن يكون سالباً", 0.0
        
        if value > 100000:  # Maximum allowance limit
            return False, "البدل كبير جداً (أكثر من 100 ألف)", 0.0
        
        # Round to 2 decimal places
        value = round(value, 2)
        
        return True, "", value
        
    except ValueError:
        return False, "يرجى إدخال رقم صحيح للبدل", 0.0

def validate_employee_selection(employee_id: Optional[int], employee_name: str) -> Tuple[bool, str]:
    """
    Validate employee selection
    
    Args:
        employee_id: Selected employee ID
        employee_name: Selected employee name
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not employee_id or not employee_name:
        return False, "يرجى اختيار موظف"
    
    return True, ""

def validate_area_selection(area_id: Optional[int], area_name: str) -> Tuple[bool, str]:
    """
    Validate area selection
    
    Args:
        area_id: Selected area ID
        area_name: Selected area name
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not area_id or not area_name:
        return False, "يرجى اختيار منطقة"
    
    return True, ""

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file operations
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    if not filename:
        return "untitled"
    
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    
    # Ensure it's not empty after sanitization
    if not filename:
        filename = "untitled"
    
    return filename

def validate_pdf_filename(filename: str) -> Tuple[bool, str, str]:
    """
    Validate and sanitize PDF filename
    
    Args:
        filename: Proposed filename
    
    Returns:
        Tuple of (is_valid, error_message, sanitized_filename)
    """
    if not filename or not filename.strip():
        return False, "اسم الملف مطلوب", ""
    
    sanitized = sanitize_filename(filename.strip())
    
    # Ensure .pdf extension
    if not sanitized.lower().endswith('.pdf'):
        sanitized += '.pdf'
    
    return True, "", sanitized

def format_currency(amount: float, currency: str = "جنيه") -> str:
    """
    Format currency amount for display
    
    Args:
        amount: Amount to format
        currency: Currency symbol/name
    
    Returns:
        Formatted currency string
    """
    return f"{amount:,.2f} {currency}"

def parse_currency_input(input_str: str) -> Optional[float]:
    """
    Parse currency input string to float
    
    Args:
        input_str: Input string that may contain currency symbols
    
    Returns:
        Parsed float value or None if invalid
    """
    if not input_str:
        return None
    
    # Remove common currency symbols and text
    cleaned = re.sub(r'[^\d\.\-]', '', input_str.strip())
    
    try:
        return float(cleaned)
    except ValueError:
        return None

def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
    """
    Validate date range for reports
    
    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    from datetime import datetime
    
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start > end:
            return False, "تاريخ البداية يجب أن يكون قبل تاريخ النهاية"
        
        # Check if date range is reasonable (not more than 5 years)
        if (end - start).days > 1825:  # 5 years
            return False, "نطاق التاريخ كبير جداً (أكثر من 5 سنوات)"
        
        return True, ""
        
    except ValueError:
        return False, "تنسيق التاريخ غير صحيح (يجب أن يكون YYYY-MM-DD)"

def is_valid_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid email format
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone_number(phone: str) -> Tuple[bool, str]:
    """
    Validate phone number (Egyptian format)
    
    Args:
        phone: Phone number to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not phone or not phone.strip():
        return True, ""  # Phone is optional
    
    # Remove spaces, dashes, and parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', phone.strip())
    
    # Check Egyptian phone number patterns
    patterns = [
        r'^01[0125][0-9]{8}$',  # Mobile numbers
        r'^02[0-9]{8}$',        # Cairo landline
        r'^03[0-9]{7}$',        # Alexandria landline
        r'^0[4-9][0-9]{7,8}$',  # Other governorates
        r'^\+2[0-9]{10,11}$'    # International format
    ]
    
    for pattern in patterns:
        if re.match(pattern, cleaned):
            return True, ""
    
    return False, "رقم الهاتف غير صحيح"
