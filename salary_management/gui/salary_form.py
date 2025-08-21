"""
Salary calculation form for Employee Salary Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import DatabaseManager
from database.models import SalaryRecord
from .styles import COLORS, FONTS, PADDING, BUTTON_STYLES, ENTRY_STYLE

class SalaryForm:
    """Salary calculation form class"""
    
    def __init__(self, parent: tk.Frame, db_manager: DatabaseManager, refresh_callback=None):
        self.parent = parent
        self.db_manager = db_manager
        self.refresh_callback = refresh_callback
        
        self.employees = []
        self.areas = []
        self.selected_employee_id = None
        self.selected_area_id = None
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Create and arrange widgets"""
        main_frame = tk.Frame(self.parent, bg=COLORS['white'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="حساب المرتبات",
            font=FONTS['title'],
            bg=COLORS['white'],
            fg=COLORS['dark']
        )
        title_label.pack(pady=(0, PADDING['large']))
        
        # Create form frame
        form_frame = tk.Frame(main_frame, bg=COLORS['white'])
        form_frame.pack(fill=tk.X, pady=(0, PADDING['large']))
        
        # Employee selection
        employee_label = tk.Label(
            form_frame,
            text="اختر الموظف:",
            font=FONTS['default'],
            bg=COLORS['white']
        )
        employee_label.pack(anchor=tk.E, pady=(0, PADDING['small']))
        
        self.employee_var = tk.StringVar()
        self.employee_combo = ttk.Combobox(
            form_frame,
            textvariable=self.employee_var,
            font=FONTS['arabic'],
            state='readonly',
            width=40
        )
        self.employee_combo.pack(fill=tk.X, pady=(0, PADDING['medium']))
        self.employee_combo.bind('<<ComboboxSelected>>', self.on_employee_select)
        
        # Area selection
        area_label = tk.Label(
            form_frame,
            text="اختر المنطقة:",
            font=FONTS['default'],
            bg=COLORS['white']
        )
        area_label.pack(anchor=tk.E, pady=(0, PADDING['small']))
        
        self.area_var = tk.StringVar()
        self.area_combo = ttk.Combobox(
            form_frame,
            textvariable=self.area_var,
            font=FONTS['arabic'],
            state='readonly',
            width=40
        )
        self.area_combo.pack(fill=tk.X, pady=(0, PADDING['medium']))
        self.area_combo.bind('<<ComboboxSelected>>', self.on_area_select)
        
        # Base salary display
        base_salary_label = tk.Label(
            form_frame,
            text="المرتب الأساسي:",
            font=FONTS['default'],
            bg=COLORS['white']
        )
        base_salary_label.pack(anchor=tk.E, pady=(0, PADDING['small']))
        
        self.base_salary_var = tk.StringVar(value="0.00")
        base_salary_entry = tk.Entry(
            form_frame,
            textvariable=self.base_salary_var,
            font=FONTS['default'],
            **ENTRY_STYLE,
            state='readonly',
            width=40
        )
        base_salary_entry.pack(fill=tk.X, pady=(0, PADDING['medium']))
        
        # Transportation allowance input
        allowance_label = tk.Label(
            form_frame,
            text="بدل الانتقالات:",
            font=FONTS['default'],
            bg=COLORS['white']
        )
        allowance_label.pack(anchor=tk.E, pady=(0, PADDING['small']))
        
        self.allowance_var = tk.StringVar(value="0.00")
        self.allowance_entry = tk.Entry(
            form_frame,
            textvariable=self.allowance_var,
            font=FONTS['default'],
            **ENTRY_STYLE,
            width=40
        )
        self.allowance_entry.pack(fill=tk.X, pady=(0, PADDING['medium']))
        self.allowance_entry.bind('<KeyRelease>', self.calculate_total)
        
        # Total display
        total_label = tk.Label(
            form_frame,
            text="إجمالي المرتب:",
            font=FONTS['heading'],
            bg=COLORS['white'],
            fg=COLORS['primary']
        )
        total_label.pack(anchor=tk.E, pady=(0, PADDING['small']))
        
        self.total_var = tk.StringVar(value="0.00")
        total_entry = tk.Entry(
            form_frame,
            textvariable=self.total_var,
            font=FONTS['heading'],
            **ENTRY_STYLE,
            state='readonly',
            width=40
        )
        total_entry.pack(fill=tk.X, pady=(0, PADDING['large']))
        
        # Buttons frame
        buttons_frame = tk.Frame(form_frame, bg=COLORS['white'])
        buttons_frame.pack(fill=tk.X, pady=PADDING['medium'])
        
        # Save button
        save_btn = tk.Button(
            buttons_frame,
            text="حفظ السجل",
            command=self.save_record,
            **BUTTON_STYLES['success'],
            width=15,
            height=2
        )
        save_btn.pack(side=tk.LEFT, padx=(0, PADDING['small']))
        
        # Clear button
        clear_btn = tk.Button(
            buttons_frame,
            text="مسح البيانات",
            command=self.clear_form,
            **BUTTON_STYLES['secondary'],
            width=15,
            height=2
        )
        clear_btn.pack(side=tk.LEFT, padx=PADDING['small'])
        
        # Rates management button
        rates_btn = tk.Button(
            buttons_frame,
            text="إدارة الأسعار",
            command=self.open_rates_management,
            **BUTTON_STYLES['primary'],
            width=15,
            height=2
        )
        rates_btn.pack(side=tk.LEFT, padx=PADDING['small'])
        
        # Recent records frame
        records_frame = tk.Frame(main_frame, bg=COLORS['white'])
        records_frame.pack(fill=tk.BOTH, expand=True, pady=(PADDING['large'], 0))
        
        # Records label
        records_label = tk.Label(
            records_frame,
            text="السجلات الحديثة:",
            font=FONTS['heading'],
            bg=COLORS['white']
        )
        records_label.pack(anchor=tk.E, pady=(0, PADDING['small']))
        
        # Create treeview for recent records
        columns = ('Employee', 'Area', 'Base', 'Allowance', 'Total', 'Date')
        self.records_tree = ttk.Treeview(records_frame, columns=columns, show='headings', height=10)
        
        # Define headings
        self.records_tree.heading('Employee', text='الموظف')
        self.records_tree.heading('Area', text='المنطقة')
        self.records_tree.heading('Base', text='المرتب الأساسي')
        self.records_tree.heading('Allowance', text='البدل')
        self.records_tree.heading('Total', text='الإجمالي')
        self.records_tree.heading('Date', text='التاريخ')
        
        # Configure columns
        self.records_tree.column('Employee', width=150, anchor=tk.E)
        self.records_tree.column('Area', width=120, anchor=tk.E)
        self.records_tree.column('Base', width=100, anchor=tk.CENTER)
        self.records_tree.column('Allowance', width=100, anchor=tk.CENTER)
        self.records_tree.column('Total', width=100, anchor=tk.CENTER)
        self.records_tree.column('Date', width=120, anchor=tk.CENTER)
        
        # Add scrollbar
        records_scrollbar = ttk.Scrollbar(records_frame, orient=tk.VERTICAL, command=self.records_tree.yview)
        self.records_tree.configure(yscrollcommand=records_scrollbar.set)
        
        # Pack treeview and scrollbar
        self.records_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        records_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load recent records
        self.load_recent_records()
    
    def load_data(self):
        """Load employees and areas data"""
        try:
            # Load employees
            self.employees = self.db_manager.get_all_employees()
            employee_names = [emp.name for emp in self.employees]
            self.employee_combo['values'] = employee_names
            
            # Load areas
            self.areas = self.db_manager.get_all_areas()
            area_names = [area.name for area in self.areas]
            self.area_combo['values'] = area_names
            
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في تحميل البيانات: {str(e)}")
    
    def on_employee_select(self, event):
        """Handle employee selection"""
        selected_name = self.employee_var.get()
        self.selected_employee_id = None
        
        for emp in self.employees:
            if emp.name == selected_name:
                self.selected_employee_id = emp.id
                break
        
        self.update_base_salary()
    
    def on_area_select(self, event):
        """Handle area selection"""
        selected_name = self.area_var.get()
        self.selected_area_id = None
        
        for area in self.areas:
            if area.name == selected_name:
                self.selected_area_id = area.id
                break
        
        self.update_base_salary()
    
    def update_base_salary(self):
        """Update base salary based on selected employee and area"""
        if self.selected_employee_id and self.selected_area_id:
            try:
                base_salary = self.db_manager.get_employee_area_rate(
                    self.selected_employee_id, 
                    self.selected_area_id
                )
                
                if base_salary is not None:
                    self.base_salary_var.set(f"{base_salary:.2f}")
                else:
                    self.base_salary_var.set("0.00")
                    messagebox.showwarning(
                        "تحذير", 
                        "لم يتم تحديد سعر لهذا الموظف في هذه المنطقة.\nيرجى إدارة الأسعار أولاً."
                    )
                
                self.calculate_total()
                
            except Exception as e:
                messagebox.showerror("خطأ", f"خطأ في جلب المرتب الأساسي: {str(e)}")
        else:
            self.base_salary_var.set("0.00")
            self.calculate_total()
    
    def calculate_total(self, event=None):
        """Calculate total salary"""
        try:
            base_salary = float(self.base_salary_var.get())
            allowance = float(self.allowance_var.get() or "0")
            total = base_salary + allowance
            self.total_var.set(f"{total:.2f}")
        except ValueError:
            self.total_var.set("0.00")
    
    def save_record(self):
        """Save salary record"""
        if not self.selected_employee_id:
            messagebox.showerror("خطأ", "يرجى اختيار موظف")
            return
        
        if not self.selected_area_id:
            messagebox.showerror("خطأ", "يرجى اختيار منطقة")
            return
        
        try:
            base_salary = float(self.base_salary_var.get())
            allowance = float(self.allowance_var.get() or "0")
            
            if base_salary <= 0:
                messagebox.showerror("خطأ", "المرتب الأساسي يجب أن يكون أكبر من صفر")
                return
            
            record = SalaryRecord(
                employee_id=self.selected_employee_id,
                area_id=self.selected_area_id,
                base_salary=base_salary,
                allowance=allowance
            )
            
            self.db_manager.add_salary_record(record)
            messagebox.showinfo("نجح", "تم حفظ السجل بنجاح")
            
            self.clear_form()
            self.load_recent_records()
            
            if self.refresh_callback:
                self.refresh_callback()
                
        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال قيم صحيحة للمبالغ")
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في حفظ السجل: {str(e)}")
    
    def clear_form(self):
        """Clear the form"""
        self.employee_var.set("")
        self.area_var.set("")
        self.base_salary_var.set("0.00")
        self.allowance_var.set("0.00")
        self.total_var.set("0.00")
        self.selected_employee_id = None
        self.selected_area_id = None
    
    def load_recent_records(self):
        """Load recent salary records"""
        # Clear existing items
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        
        try:
            records = self.db_manager.get_all_salary_records()
            # Show only the last 20 records
            recent_records = records[:20]
            
            for record in recent_records:
                date_str = record.date_created.strftime('%Y-%m-%d') if record.date_created else ''
                self.records_tree.insert('', tk.END, values=(
                    record.employee_name,
                    record.area_name,
                    f"{record.base_salary:.2f}",
                    f"{record.allowance:.2f}",
                    f"{record.total:.2f}",
                    date_str
                ))
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في تحميل السجلات: {str(e)}")
    
    def open_rates_management(self):
        """Open rates management window"""
        try:
            rates_window = tk.Toplevel(self.parent)
            RatesManagementForm(rates_window, self.db_manager, self.load_data)
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في فتح إدارة الأسعار: {str(e)}")


class RatesManagementForm:
    """Rates management form for setting employee rates per area"""
    
    def __init__(self, parent: tk.Toplevel, db_manager: DatabaseManager, refresh_callback=None):
        self.parent = parent
        self.db_manager = db_manager
        self.refresh_callback = refresh_callback
        
        self.setup_window()
        self.create_widgets()
        self.load_rates()
    
    def setup_window(self):
        """Set up the window properties"""
        self.parent.title("إدارة أسعار الموظفين")
        self.parent.geometry("1000x700")
        self.parent.configure(bg=COLORS['white'])
        self.parent.resizable(True, True)
        
        # Make window modal
        self.parent.transient()
        self.parent.grab_set()
        
        # Center the window
        self.parent.update_idletasks()
        x = (self.parent.winfo_screenwidth() // 2) - (self.parent.winfo_width() // 2)
        y = (self.parent.winfo_screenheight() // 2) - (self.parent.winfo_height() // 2)
        self.parent.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        """Create and arrange widgets"""
        main_frame = tk.Frame(self.parent, bg=COLORS['white'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING['large'], pady=PADDING['large'])
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="إدارة أسعار الموظفين حسب المناطق",
            font=FONTS['title'],
            bg=COLORS['white'],
            fg=COLORS['dark']
        )
        title_label.pack(pady=(0, PADDING['large']))
        
        # Rates table frame
        table_frame = tk.Frame(main_frame, bg=COLORS['white'])
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview for rates
        columns = ('Employee', 'Area', 'Rate')
        self.rates_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        # Define headings
        self.rates_tree.heading('Employee', text='الموظف')
        self.rates_tree.heading('Area', text='المنطقة')
        self.rates_tree.heading('Rate', text='المرتب الأساسي')
        
        # Configure columns
        self.rates_tree.column('Employee', width=300, anchor=tk.E)
        self.rates_tree.column('Area', width=200, anchor=tk.E)
        self.rates_tree.column('Rate', width=150, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.rates_tree.yview)
        self.rates_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.rates_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Close button
        close_frame = tk.Frame(main_frame, bg=COLORS['white'])
        close_frame.pack(fill=tk.X, pady=(PADDING['large'], 0))
        
        close_btn = tk.Button(
            close_frame,
            text="إغلاق",
            command=self.close_window,
            **BUTTON_STYLES['secondary'],
            width=15
        )
        close_btn.pack(side=tk.RIGHT)
        
        # Note label
        note_label = tk.Label(
            close_frame,
            text="ملاحظة: لتعديل الأسعار، يرجى استخدام قاعدة البيانات مباشرة أو إضافة واجهة تعديل",
            font=FONTS['small'],
            bg=COLORS['white'],
            fg=COLORS['secondary']
        )
        note_label.pack(side=tk.LEFT)
    
    def load_rates(self):
        """Load rates into the treeview"""
        # Clear existing items
        for item in self.rates_tree.get_children():
            self.rates_tree.delete(item)
        
        try:
            rates = self.db_manager.get_all_employee_area_rates()
            for employee_name, area_name, rate in rates:
                self.rates_tree.insert('', tk.END, values=(
                    employee_name,
                    area_name,
                    f"{rate:.2f}"
                ))
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في تحميل الأسعار: {str(e)}")
    
    def close_window(self):
        """Close the window and refresh parent if needed"""
        if self.refresh_callback:
            self.refresh_callback()
        self.parent.destroy()
