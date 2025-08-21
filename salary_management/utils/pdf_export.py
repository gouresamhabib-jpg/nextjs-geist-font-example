"""
PDF export utilities for Employee Salary Management System
"""

import os
from datetime import datetime
from typing import List
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from database.models import SalaryRecordView

def setup_arabic_font():
    """Setup Arabic font for PDF generation"""
    try:
        # Try to register Arabic font (you may need to download and place the font file)
        # For now, we'll use default fonts
        pass
    except:
        pass

def export_salary_records_to_pdf(records: List[SalaryRecordView], filename: str = None) -> str:
    """
    Export salary records to PDF file
    
    Args:
        records: List of salary records to export
        filename: Optional filename, if not provided, auto-generated
    
    Returns:
        str: Path to the generated PDF file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"salary_report_{timestamp}.pdf"
    
    # Ensure the filename has .pdf extension
    if not filename.endswith('.pdf'):
        filename += '.pdf'
    
    # Create reports directory if it doesn't exist
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    filepath = os.path.join(reports_dir, filename)
    
    # Setup Arabic font
    setup_arabic_font()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.darkblue
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=20,
        alignment=1  # Center alignment
    )
    
    # Add title
    title = Paragraph("تقرير مرتبات العمال", title_style)
    elements.append(title)
    
    # Add report info
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    report_info = Paragraph(f"تاريخ التقرير: {current_date}", header_style)
    elements.append(report_info)
    
    elements.append(Spacer(1, 20))
    
    if not records:
        no_data = Paragraph("لا توجد بيانات للعرض", header_style)
        elements.append(no_data)
    else:
        # Create table data
        table_data = [
            ['التاريخ', 'الإجمالي', 'البدل', 'المرتب الأساسي', 'المنطقة', 'الموظف']
        ]
        
        total_sum = 0
        for record in records:
            date_str = record.date_created.strftime('%Y-%m-%d') if record.date_created else ''
            table_data.append([
                date_str,
                f"{record.total:.2f}",
                f"{record.allowance:.2f}",
                f"{record.base_salary:.2f}",
                record.area_name,
                record.employee_name
            ])
            total_sum += record.total
        
        # Add total row
        table_data.append([
            'الإجمالي العام',
            f"{total_sum:.2f}",
            '',
            '',
            '',
            ''
        ])
        
        # Create table
        table = Table(table_data, colWidths=[1.2*inch, 1*inch, 1*inch, 1.2*inch, 1.5*inch, 2*inch])
        
        # Add table style
        table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.beige, colors.white]),
            
            # Total row
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightblue),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
        
        # Add summary
        elements.append(Spacer(1, 30))
        
        summary_style = ParagraphStyle(
            'Summary',
            parent=styles['Normal'],
            fontSize=14,
            alignment=1,
            textColor=colors.darkblue
        )
        
        summary_text = f"عدد السجلات: {len(records)}<br/>الإجمالي العام: {total_sum:.2f} جنيه"
        summary = Paragraph(summary_text, summary_style)
        elements.append(summary)
    
    # Add footer
    elements.append(Spacer(1, 50))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1,
        textColor=colors.grey
    )
    
    footer = Paragraph("نظام إدارة مرتبات العمال", footer_style)
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    return filepath

def export_employee_summary_to_pdf(db_manager, filename: str = None) -> str:
    """
    Export employee summary report to PDF
    
    Args:
        db_manager: Database manager instance
        filename: Optional filename
    
    Returns:
        str: Path to the generated PDF file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"employee_summary_{timestamp}.pdf"
    
    if not filename.endswith('.pdf'):
        filename += '.pdf'
    
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    filepath = os.path.join(reports_dir, filename)
    
    # Get data
    employees = db_manager.get_all_employees()
    areas = db_manager.get_all_areas()
    rates = db_manager.get_all_employee_area_rates()
    
    # Create PDF document
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,
        textColor=colors.darkblue
    )
    
    title = Paragraph("تقرير ملخص الموظفين والأسعار", title_style)
    elements.append(title)
    
    # Current date
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    date_para = Paragraph(f"تاريخ التقرير: {current_date}", styles['Normal'])
    elements.append(date_para)
    elements.append(Spacer(1, 20))
    
    # Employees section
    emp_title = Paragraph("قائمة الموظفين", styles['Heading2'])
    elements.append(emp_title)
    
    emp_data = [['الرقم', 'اسم الموظف']]
    for emp in employees:
        emp_data.append([str(emp.id), emp.name])
    
    emp_table = Table(emp_data, colWidths=[1*inch, 4*inch])
    emp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(emp_table)
    elements.append(Spacer(1, 20))
    
    # Areas section
    area_title = Paragraph("قائمة المناطق", styles['Heading2'])
    elements.append(area_title)
    
    area_data = [['الرقم', 'اسم المنطقة']]
    for area in areas:
        area_data.append([str(area.id), area.name])
    
    area_table = Table(area_data, colWidths=[1*inch, 4*inch])
    area_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(area_table)
    elements.append(Spacer(1, 20))
    
    # Rates section
    rates_title = Paragraph("أسعار الموظفين حسب المناطق", styles['Heading2'])
    elements.append(rates_title)
    
    rates_data = [['الموظف', 'المنطقة', 'المرتب الأساسي']]
    for emp_name, area_name, rate in rates:
        rates_data.append([emp_name, area_name, f"{rate:.2f}"])
    
    rates_table = Table(rates_data, colWidths=[2*inch, 2*inch, 1.5*inch])
    rates_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.white]),
    ]))
    
    elements.append(rates_table)
    
    # Build PDF
    doc.build(elements)
    
    return filepath
