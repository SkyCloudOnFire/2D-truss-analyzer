"""
Multi-language localization system for 2D Truss Analysis.
Supports English and Persian with internal dictionary-based translation.
"""

from typing import Dict, Literal

Language = Literal['en', 'fa']

class Localization:
    """Manages all user-facing text translations."""
    
    def __init__(self, language: Language = 'en'):
        self.language = language
        self._load_translations()
    
    def _load_translations(self):
        """Load translation dictionaries."""
        
        self.translations: Dict[str, Dict[str, str]] = {
            'en': {
                # App title and headers
                'app_title': '2D Truss Analysis System',
                'app_subtitle': 'Structural Analysis Engine',
                
                # Navigation
                'tab_nodes': 'Nodes',
                'tab_members': 'Members',
                'tab_supports': 'Supports',
                'tab_loads': 'Loads',
                
                # Node input
                'node_name': 'Node Name',
                'node_x': 'X Coordinate',
                'node_y': 'Y Coordinate',
                'add_node': 'Add Node',
                'node_name_placeholder': 'e.g., A, N1',
                
                # Member input
                'member_start': 'Start Node',
                'member_end': 'End Node',
                'add_member': 'Add Member',
                'select_node': 'Select node...',
                
                # Support input
                'support_node': 'Node',
                'support_type': 'Support Type',
                'support_angle': 'Orientation Angle (°)',
                'add_support': 'Add Support',
                'pinned': 'Pinned',
                'roller': 'Roller',
                'fixed': 'Fixed',
                
                # Load input
                'load_name': 'Load Name',
                'load_node': 'Node',
                'load_magnitude': 'Magnitude',
                'load_angle': 'Angle (°)',
                'add_load': 'Add Load',
                'load_name_placeholder': 'e.g., F1, P1',
                
                # Buttons
                'analyze': 'Analyze Structure',
                'reset': 'Reset Project',
                'edit': 'Edit',
                'delete': 'Delete',
                'confirm': 'Confirm',
                'cancel': 'Cancel',
                
                # Unit system
                'unit_system': 'Unit System',
                'unit_n': 'N (Newtons)',
                'unit_kn': 'kN (Kilonewtons)',
                'unit_lbf': 'lbf (Pound-force)',
                
                # Theme
                'theme_light': 'Light',
                'theme_dark': 'Dark',
                'theme_system': 'System',
                
                # Language
                'language': 'Language',
                'lang_en': 'English',
                'lang_fa': 'فارسی',
                
                # Results
                'reaction_forces': 'Reaction Forces',
                'member_forces': 'Member Forces',
                'support': 'Support',
                'member': 'Member',
                'force_fx': 'Fx',
                'force_fy': 'Fy',
                'resultant': 'Resultant',
                'angle': 'Angle',
                'tension': 'TENSION',
                'compression': 'COMPRESSION',
                'force_value': 'Force',
                'type': 'Type',
                
                # Export
                'export_pdf': 'Export PDF Report',
                
                # Status messages
                'analysis_complete': 'Analysis completed successfully',
                'analysis_failed': 'Analysis failed',
                'structure_unstable': 'Structure is unstable or has mechanisms',
                'no_nodes': 'No nodes defined',
                'no_members': 'No members defined',
                'no_supports': 'No supports defined',
                
                # Errors
                'error_duplicate_node': 'Duplicate node name',
                'error_missing_nodes': 'Specified node does not exist',
                'error_invalid_member': 'Invalid member connection',
                'error_zero_length': 'Zero-length member detected',
                'error_missing_support': 'Structure requires at least one support',
                'error_missing_load': 'No loads applied to structure',
                'error_unstable': 'Structure is unstable or has mechanisms',
                'error_invalid_input': 'Invalid numeric input',
                'error_load_on_member': 'Loads must be applied at nodes. Consider adding an intermediate node.',
                
                # Table headers
                'table_nodes': 'Nodes',
                'table_members': 'Members',
                'table_supports': 'Supports',
                'table_loads': 'Loads',
                
                # Preview
                'live_preview': 'Live Preview',
                'no_structure': 'Add nodes and members to see preview',
                
                # Confirmations
                'confirm_delete': 'Are you sure you want to delete this item?',
                'confirm_reset': 'Are you sure you want to reset the entire project?',
            },
            'fa': {
                # App title and headers
                'app_title': 'سیستم تحلیل خرپای دوبعدی',
                'app_subtitle': 'موتور تحلیل سازه‌ای',
                
                # Navigation
                'tab_nodes': 'گره‌ها',
                'tab_members': 'اعضا',
                'tab_supports': 'تکیه‌گاه‌ها',
                'tab_loads': 'بارها',
                
                # Node input
                'node_name': 'نام گره',
                'node_x': 'مختصات X',
                'node_y': 'مختصات Y',
                'add_node': 'افزودن گره',
                'node_name_placeholder': 'مثال: A, N1',
                
                # Member input
                'member_start': 'گره ابتدا',
                'member_end': 'گره انتها',
                'add_member': 'افزودن عضو',
                'select_node': 'انتخاب گره...',
                
                # Support input
                'support_node': 'گره',
                'support_type': 'نوع تکیه‌گاه',
                'support_angle': 'زاویه جهت‌گیری (°)',
                'add_support': 'افزودن تکیه‌گاه',
                'pinned': 'مفصلی',
                'roller': 'غلتکی',
                'fixed': 'گیردار',
                
                # Load input
                'load_name': 'نام بار',
                'load_node': 'گره',
                'load_magnitude': 'بزرگی',
                'load_angle': 'زاویه (°)',
                'add_load': 'افزودن بار',
                'load_name_placeholder': 'مثال: F1, P1',
                
                # Buttons
                'analyze': 'تحلیل سازه',
                'reset': 'بازنشانی پروژه',
                'edit': 'ویرایش',
                'delete': 'حذف',
                'confirm': 'تایید',
                'cancel': 'انصراف',
                
                # Unit system
                'unit_system': 'سیستم واحد',
                'unit_n': 'نیوتن (N)',
                'unit_kn': 'کیلونیوتن (kN)',
                'unit_lbf': 'پوند-نیرو (lbf)',
                
                # Theme
                'theme_light': 'روشن',
                'theme_dark': 'تاریک',
                'theme_system': 'سیستم',
                
                # Language
                'language': 'زبان',
                'lang_en': 'English',
                'lang_fa': 'فارسی',
                
                # Results
                'reaction_forces': 'نیروهای تکیه‌گاهی',
                'member_forces': 'نیروهای اعضا',
                'support': 'تکیه‌گاه',
                'member': 'عضو',
                'force_fx': 'Fx',
                'force_fy': 'Fy',
                'resultant': 'برآیند',
                'angle': 'زاویه',
                'tension': 'کششی',
                'compression': 'فشاری',
                'force_value': 'نیرو',
                'type': 'نوع',
                
                # Export
                'export_pdf': 'خروجی گزارش PDF',
                
                # Status messages
                'analysis_complete': 'تحلیل با موفقیت انجام شد',
                'analysis_failed': 'تحلیل ناموفق بود',
                'structure_unstable': 'سازه ناپایدار است یا مکانیزم دارد',
                'no_nodes': 'گرهی تعریف نشده است',
                'no_members': 'عضوی تعریف نشده است',
                'no_supports': 'تکیه‌گاهی تعریف نشده است',
                
                # Errors
                'error_duplicate_node': 'نام گره تکراری است',
                'error_missing_nodes': 'گره مشخص شده وجود ندارد',
                'error_invalid_member': 'اتصال عضو نامعتبر است',
                'error_zero_length': 'عضوی با طول صفر تشخیص داده شد',
                'error_missing_support': 'سازه حداقل به یک تکیه‌گاه نیاز دارد',
                'error_missing_load': 'هیچ باری به سازه اعمال نشده است',
                'error_unstable': 'سازه ناپایدار است یا مکانیزم دارد',
                'error_invalid_input': 'ورودی عددی نامعتبر',
                'error_load_on_member': 'بارها باید در گره‌ها اعمال شوند. ایجاد یک گره میانی توصیه می‌شود.',
                
                # Table headers
                'table_nodes': 'گره‌ها',
                'table_members': 'اعضا',
                'table_supports': 'تکیه‌گاه‌ها',
                'table_loads': 'بارها',
                
                # Preview
                'live_preview': 'پیش‌نمایش زنده',
                'no_structure': 'برای مشاهده پیش‌نمایش، گره‌ها و اعضا را اضافه کنید',
                
                # Confirmations
                'confirm_delete': 'آیا از حذف این آیتم اطمینان دارید؟',
                'confirm_reset': 'آیا از بازنشانی کل پروژه اطمینان دارید؟',
            }
        }
    
    def get(self, key: str) -> str:
        """Get translated text for a key."""
        return self.translations.get(self.language, self.translations['en']).get(key, key)
    
    def __call__(self, key: str) -> str:
        """Allow calling the instance directly to get translations."""
        return self.get(key)