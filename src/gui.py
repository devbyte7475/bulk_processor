"""
GUI界面模块 - 极简商务风格设计
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
from typing import Optional, Dict, List
from .processor import BulkDataProcessor
from .utils import ConfigManager


class ThemeColors:
    """主题配色方案 - 极简商务风"""
    BG_PRIMARY = "#FFFFFF"
    BG_SECONDARY = "#F5F5F7"
    BG_CARD = "#FAFAFA"
    
    TEXT_PRIMARY = "#1D1D1F"
    TEXT_SECONDARY = "#86868B"
    TEXT_TERTIARY = "#AEAEB2"
    
    ACCENT = "#007AFF"
    ACCENT_HOVER = "#0051D5"
    ACCENT_LIGHT = "#E5F1FF"
    
    BORDER = "#D2D2D7"
    BORDER_LIGHT = "#E5E5EA"
    
    SUCCESS = "#34C759"
    WARNING = "#FF9500"
    ERROR = "#FF3B30"
    
    SHADOW = "#000000"
    SHADOW_OPACITY = 0.05


class ModernStyle:
    """现代化样式管理器"""
    
    @staticmethod
    def configure_styles():
        """配置全局样式"""
        style = ttk.Style()
        
        style.theme_use('clam')
        
        style.configure('TFrame', background=ThemeColors.BG_PRIMARY)
        style.configure('Card.TFrame', background=ThemeColors.BG_CARD)
        
        style.configure('Title.TLabel',
                       background=ThemeColors.BG_PRIMARY,
                       foreground=ThemeColors.TEXT_PRIMARY,
                       font=('SF Pro Display', 24, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       background=ThemeColors.BG_PRIMARY,
                       foreground=ThemeColors.TEXT_SECONDARY,
                       font=('SF Pro Text', 13))
        
        style.configure('Body.TLabel',
                       background=ThemeColors.BG_PRIMARY,
                       foreground=ThemeColors.TEXT_PRIMARY,
                       font=('SF Pro Text', 11))
        
        style.configure('Secondary.TLabel',
                       background=ThemeColors.BG_PRIMARY,
                       foreground=ThemeColors.TEXT_SECONDARY,
                       font=('SF Pro Text', 10))
        
        style.configure('BigNumber.TLabel',
                       background=ThemeColors.BG_PRIMARY,
                       foreground=ThemeColors.ACCENT,
                       font=('SF Pro Display', 48, 'bold'))
        
        style.configure('Progress.TLabel',
                       background=ThemeColors.BG_PRIMARY,
                       foreground=ThemeColors.TEXT_PRIMARY,
                       font=('SF Pro Text', 12))
        
        style.configure('Primary.TButton',
                       background=ThemeColors.ACCENT,
                       foreground=ThemeColors.BG_PRIMARY,
                       font=('SF Pro Text', 11, 'bold'),
                       padding=(24, 12))
        
        style.map('Primary.TButton',
                 background=[('active', ThemeColors.ACCENT_HOVER),
                           ('disabled', ThemeColors.TEXT_TERTIARY)])
        
        style.configure('Secondary.TButton',
                       background=ThemeColors.BG_SECONDARY,
                       foreground=ThemeColors.TEXT_PRIMARY,
                       font=('SF Pro Text', 11),
                       padding=(16, 10))
        
        style.map('Secondary.TButton',
                 background=[('active', ThemeColors.BORDER_LIGHT)])
        
        style.configure('Card.TLabelframe',
                       background=ThemeColors.BG_CARD,
                       bordercolor=ThemeColors.BORDER_LIGHT,
                       relief='flat')
        
        style.configure('Card.TLabelframe.Label',
                       background=ThemeColors.BG_CARD,
                       foreground=ThemeColors.TEXT_PRIMARY,
                       font=('SF Pro Text', 12, 'bold'))
        
        style.configure('Custom.Horizontal.TProgressbar',
                       background=ThemeColors.ACCENT,
                       troughcolor=ThemeColors.BG_SECONDARY,
                       bordercolor=ThemeColors.BG_PRIMARY,
                       lightcolor=ThemeColors.ACCENT,
                       darkcolor=ThemeColors.ACCENT)
        
        style.configure('Custom.TEntry',
                       fieldbackground=ThemeColors.BG_PRIMARY,
                       bordercolor=ThemeColors.BORDER,
                       lightcolor=ThemeColors.ACCENT,
                       darkcolor=ThemeColors.ACCENT)


class AnimatedProgressIndicator:
    """动画进度指示器"""
    
    def __init__(self, parent, size=120):
        self.parent = parent
        self.size = size
        self.angle = 0
        self.is_animating = False
        
        self.canvas = tk.Canvas(
            parent,
            width=size,
            height=size,
            bg=ThemeColors.BG_PRIMARY,
            highlightthickness=0
        )
        
        self.center = size // 2
        self.radius = size // 2 - 10
        
    def start_animation(self):
        """开始旋转动画"""
        self.is_animating = True
        self._animate()
    
    def stop_animation(self):
        """停止动画"""
        self.is_animating = False
    
    def _animate(self):
        """执行动画帧"""
        if not self.is_animating:
            return
        
        self.canvas.delete("all")
        
        for i in range(12):
            angle = self.angle + i * 30
            opacity = 1 - (i / 12)
            
            x1 = self.center + self.radius * 0.7 * self._cos(angle)
            y1 = self.center + self.radius * 0.7 * self._sin(angle)
            x2 = self.center + self.radius * 0.9 * self._cos(angle)
            y2 = self.center + self.radius * 0.9 * self._sin(angle)
            
            color = self._interpolate_color(
                ThemeColors.BG_SECONDARY,
                ThemeColors.ACCENT,
                opacity
            )
            
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=color,
                width=3,
                capstyle=tk.ROUND
            )
        
        self.angle = (self.angle + 10) % 360
        
        self.parent.after(50, self._animate)
    
    def _cos(self, angle):
        import math
        return math.cos(math.radians(angle))
    
    def _sin(self, angle):
        import math
        return math.sin(math.radians(angle))
    
    def _interpolate_color(self, color1, color2, factor):
        """颜色插值"""
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        
        return f"#{r:02x}{g:02x}{b:02x}"


class StepIndicator:
    """步骤指示器组件"""
    
    def __init__(self, parent, steps: List[str]):
        self.parent = parent
        self.steps = steps
        self.current_step = 0
        
        self.frame = ttk.Frame(parent, style='Card.TFrame')
        
        self.step_labels = []
        self.status_indicators = []
        
        self._create_widgets()
    
    def _create_widgets(self):
        """创建步骤指示器组件"""
        for i, step in enumerate(self.steps):
            step_frame = ttk.Frame(self.frame, style='Card.TFrame')
            step_frame.pack(fill='x', pady=4)
            
            indicator = tk.Canvas(
                step_frame,
                width=20,
                height=20,
                bg=ThemeColors.BG_CARD,
                highlightthickness=0
            )
            indicator.pack(side='left', padx=(0, 10))
            
            label = ttk.Label(
                step_frame,
                text=step,
                style='Secondary.TLabel'
            )
            label.pack(side='left')
            
            self.step_labels.append(label)
            self.status_indicators.append(indicator)
        
        self._update_indicators()
    
    def set_current_step(self, step_index: int):
        """设置当前步骤"""
        self.current_step = step_index
        self._update_indicators()
    
    def _update_indicators(self):
        """更新指示器状态"""
        for i, indicator in enumerate(self.status_indicators):
            indicator.delete("all")
            
            if i < self.current_step:
                color = ThemeColors.SUCCESS
                self._draw_checkmark(indicator, color)
                self.step_labels[i].configure(foreground=ThemeColors.TEXT_PRIMARY)
            elif i == self.current_step:
                color = ThemeColors.ACCENT
                self._draw_progress_circle(indicator, color)
                self.step_labels[i].configure(foreground=ThemeColors.ACCENT)
            else:
                color = ThemeColors.TEXT_TERTIARY
                self._draw_empty_circle(indicator, color)
                self.step_labels[i].configure(foreground=ThemeColors.TEXT_TERTIARY)
    
    def _draw_checkmark(self, canvas, color):
        """绘制对勾"""
        canvas.create_oval(2, 2, 18, 18, fill=color, outline=color)
        canvas.create_line(6, 10, 9, 13, fill='white', width=2)
        canvas.create_line(9, 13, 14, 7, fill='white', width=2)
    
    def _draw_progress_circle(self, canvas, color):
        """绘制进行中圆圈"""
        canvas.create_oval(2, 2, 18, 18, outline=color, width=2)
        canvas.create_oval(6, 6, 14, 14, fill=color, outline=color)
    
    def _draw_empty_circle(self, canvas, color):
        """绘制空圆圈"""
        canvas.create_oval(2, 2, 18, 18, outline=color, width=2)


class RealTimeLogViewer:
    """实时日志查看器"""
    
    def __init__(self, parent, height=8):
        self.parent = parent
        
        self.frame = ttk.Frame(parent, style='Card.TFrame')
        
        self.text_widget = tk.Text(
            self.frame,
            height=height,
            wrap='word',
            font=('SF Mono', 9),
            bg=ThemeColors.BG_SECONDARY,
            fg=ThemeColors.TEXT_PRIMARY,
            relief='flat',
            padx=12,
            pady=8,
            state='disabled'
        )
        
        scrollbar = ttk.Scrollbar(
            self.frame,
            orient='vertical',
            command=self.text_widget.yview
        )
        
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side='right', fill='y')
        self.text_widget.pack(side='left', fill='both', expand=True)
        
        self._configure_tags()
    
    def _configure_tags(self):
        """配置文本标签样式"""
        self.text_widget.tag_configure(
            'timestamp',
            foreground=ThemeColors.TEXT_TERTIARY
        )
        self.text_widget.tag_configure(
            'info',
            foreground=ThemeColors.TEXT_PRIMARY
        )
        self.text_widget.tag_configure(
            'success',
            foreground=ThemeColors.SUCCESS
        )
        self.text_widget.tag_configure(
            'warning',
            foreground=ThemeColors.WARNING
        )
        self.text_widget.tag_configure(
            'error',
            foreground=ThemeColors.ERROR
        )
    
    def add_log(self, message: str, level: str = 'info'):
        """添加日志条目"""
        from datetime import datetime
        
        self.text_widget.configure(state='normal')
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.text_widget.insert('end', f"[{timestamp}] ", 'timestamp')
        self.text_widget.insert('end', f"{message}\n", level)
        
        self.text_widget.see('end')
        self.text_widget.configure(state='disabled')


class DataPreviewCard:
    """数据预览卡片"""
    
    def __init__(self, parent, title: str):
        self.parent = parent
        
        self.frame = ttk.Frame(parent, style='Card.TFrame')
        
        title_label = ttk.Label(
            self.frame,
            text=title,
            style='Body.TLabel'
        )
        title_label.pack(anchor='w', pady=(0, 8))
        
        self.value_label = ttk.Label(
            self.frame,
            text="--",
            style='BigNumber.TLabel'
        )
        self.value_label.pack(anchor='w')
        
        self.subtitle_label = ttk.Label(
            self.frame,
            text="",
            style='Secondary.TLabel'
        )
        self.subtitle_label.pack(anchor='w')
    
    def update_value(self, value: str, subtitle: str = ""):
        """更新显示值"""
        self.value_label.configure(text=value)
        self.subtitle_label.configure(text=subtitle)


class BulkProcessorGUI:
    """亚马逊广告数据处理器GUI - 极简商务风格"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("亚马逊广告数据处理器")
        self.root.geometry("900x850")
        self.root.configure(bg=ThemeColors.BG_PRIMARY)
        self.root.resizable(True, True)
        
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        
        self.folder_path = tk.StringVar()
        self.old_file = tk.StringVar()
        self.new_file = tk.StringVar()
        
        self.is_processing = False
        self.processor = None
        self.processing_steps = [
            "识别文件",
            "读取旧表数据",
            "读取新表数据",
            "处理 SP 数据",
            "处理 SB 数据",
            "处理 SD 数据",
            "导出结果"
        ]
        
        ModernStyle.configure_styles()
        self._create_widgets()
        self._auto_search_files()
    
    def _create_widgets(self):
        """创建所有UI组件"""
        main_container = ttk.Frame(self.root, style='TFrame')
        main_container.pack(fill='both', expand=True, padx=40, pady=40)
        
        self._create_header(main_container)
        
        self._create_file_selection_card(main_container)
        
        self._create_config_card(main_container)
        
        self._create_progress_section(main_container)
        
        self._create_results_section(main_container)
        
        self._create_action_buttons(main_container)
    
    def _create_header(self, parent):
        """创建顶部标题区域"""
        header_frame = ttk.Frame(parent, style='TFrame')
        header_frame.pack(fill='x', pady=(0, 30))
        
        title = ttk.Label(
            header_frame,
            text="广告数据处理",
            style='Title.TLabel'
        )
        title.pack(anchor='w')
        
        subtitle = ttk.Label(
            header_frame,
            text="快速处理亚马逊广告 Bulk 文件，生成优化策略表格",
            style='Subtitle.TLabel'
        )
        subtitle.pack(anchor='w', pady=(8, 0))
    
    def _create_file_selection_card(self, parent):
        """创建文件选择卡片"""
        card_frame = ttk.LabelFrame(
            parent,
            text="  数据源  ",
            style='Card.TLabelframe',
            padding=20
        )
        card_frame.pack(fill='x', pady=(0, 20))
        
        path_frame = ttk.Frame(card_frame, style='Card.TFrame')
        path_frame.pack(fill='x', pady=(0, 15))
        
        path_entry = ttk.Entry(
            path_frame,
            textvariable=self.folder_path,
            font=('SF Pro Text', 11),
            state='readonly'
        )
        path_entry.pack(side='left', fill='x', expand=True, padx=(0, 12))
        
        browse_btn = ttk.Button(
            path_frame,
            text="选择文件夹",
            style='Secondary.TButton',
            command=self._select_folder
        )
        browse_btn.pack(side='right')
        
        files_info_frame = ttk.Frame(card_frame, style='Card.TFrame')
        files_info_frame.pack(fill='x')
        
        old_file_label = ttk.Label(
            files_info_frame,
            textvariable=self.old_file,
            style='Secondary.TLabel'
        )
        old_file_label.pack(anchor='w', pady=2)
        
        new_file_label = ttk.Label(
            files_info_frame,
            textvariable=self.new_file,
            style='Secondary.TLabel'
        )
        new_file_label.pack(anchor='w', pady=2)
    
    def _create_config_card(self, parent):
        """创建配置参数卡片"""
        card_frame = ttk.LabelFrame(
            parent,
            text="  处理参数  ",
            style='Card.TLabelframe',
            padding=20
        )
        card_frame.pack(fill='x', pady=(0, 20))
        
        config_frame = ttk.Frame(card_frame, style='Card.TFrame')
        config_frame.pack(fill='x')
        
        params = [
            ("曝光量阈值", f"{self.config['thresholds']['impressions']:,}"),
            ("点击率阈值", f"{self.config['thresholds']['ctr']*100:.2f}%"),
            ("转化率阈值", f"{self.config['thresholds']['cvr']*100:.0f}%"),
            ("ACOS阈值", f"{self.config['thresholds']['acos']*100:.0f}%")
        ]
        
        for i, (label, value) in enumerate(params):
            param_frame = ttk.Frame(config_frame, style='Card.TFrame')
            param_frame.pack(side='left', padx=(0 if i == 0 else 30, 0))
            
            ttk.Label(
                param_frame,
                text=label,
                style='Secondary.TLabel'
            ).pack(anchor='w')
            
            ttk.Label(
                param_frame,
                text=value,
                style='Body.TLabel'
            ).pack(anchor='w', pady=(4, 0))
        
        config_btn = ttk.Button(
            config_frame,
            text="配置",
            style='Secondary.TButton',
            command=self._show_config_dialog
        )
        config_btn.pack(side='right')
    
    def _create_progress_section(self, parent):
        """创建进度可视化区域"""
        progress_frame = ttk.LabelFrame(
            parent,
            text="  处理进度  ",
            style='Card.TLabelframe',
            padding=20
        )
        progress_frame.pack(fill='x', pady=(0, 20))
        
        progress_visual_frame = ttk.Frame(progress_frame, style='Card.TFrame')
        progress_visual_frame.pack(fill='x', pady=(0, 20))
        
        left_section = ttk.Frame(progress_visual_frame, style='Card.TFrame')
        left_section.pack(side='left', fill='both', expand=True)
        
        self.progress_indicator = AnimatedProgressIndicator(left_section, size=100)
        self.progress_indicator.canvas.pack(side='left', padx=(0, 20))
        
        progress_text_frame = ttk.Frame(left_section, style='Card.TFrame')
        progress_text_frame.pack(side='left', fill='y', expand=True)
        
        self.progress_percentage_label = ttk.Label(
            progress_text_frame,
            text="0%",
            style='BigNumber.TLabel'
        )
        self.progress_percentage_label.pack(anchor='w')
        
        self.progress_status_label = ttk.Label(
            progress_text_frame,
            text="等待开始...",
            style='Progress.TLabel'
        )
        self.progress_status_label.pack(anchor='w', pady=(8, 0))
        
        self.step_indicator = StepIndicator(progress_visual_frame, self.processing_steps)
        self.step_indicator.frame.pack(side='right', padx=(30, 0))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            style='Custom.Horizontal.TProgressbar',
            mode='determinate',
            length=100
        )
        self.progress_bar.pack(fill='x', pady=(0, 15))
        
        log_label = ttk.Label(
            progress_frame,
            text="实时处理日志",
            style='Body.TLabel'
        )
        log_label.pack(anchor='w', pady=(0, 8))
        
        self.log_viewer = RealTimeLogViewer(progress_frame, height=12)
        self.log_viewer.frame.pack(fill='both', expand=True)
    
    def _create_results_section(self, parent):
        """创建结果预览区域"""
        results_frame = ttk.LabelFrame(
            parent,
            text="  处理结果  ",
            style='Card.TLabelframe',
            padding=20
        )
        results_frame.pack(fill='x', pady=(0, 20))
        
        cards_frame = ttk.Frame(results_frame, style='Card.TFrame')
        cards_frame.pack(fill='x', pady=(0, 15))
        
        self.files_card = DataPreviewCard(cards_frame, "处理文件")
        self.files_card.frame.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        self.rows_card = DataPreviewCard(cards_frame, "总数据行")
        self.rows_card.frame.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        self.output_card = DataPreviewCard(cards_frame, "输出文件")
        self.output_card.frame.pack(side='left', fill='x', expand=True)
        
        self.result_text = tk.Text(
            results_frame,
            height=4,
            wrap='word',
            font=('SF Mono', 9),
            bg=ThemeColors.BG_SECONDARY,
            fg=ThemeColors.TEXT_PRIMARY,
            relief='flat',
            padx=12,
            pady=8,
            state='disabled'
        )
        self.result_text.pack(fill='x')
    
    def _create_action_buttons(self, parent):
        """创建操作按钮"""
        buttons_frame = ttk.Frame(parent, style='TFrame')
        buttons_frame.pack(fill='x', pady=(20, 0))
        
        self.start_button = tk.Button(
            buttons_frame,
            text="▶  开始处理数据",
            font=('SF Pro Display', 16, 'bold'),
            bg=ThemeColors.ACCENT,
            fg='white',
            activebackground=ThemeColors.ACCENT_HOVER,
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=50,
            pady=18,
            command=self._start_processing
        )
        self.start_button.pack(fill='x', pady=(0, 15))
        
        secondary_frame = ttk.Frame(buttons_frame, style='TFrame')
        secondary_frame.pack(fill='x')
        
        ttk.Button(
            secondary_frame,
            text="打开输出文件夹",
            style='Secondary.TButton',
            command=self._open_output_folder
        ).pack(side='left', padx=(0, 12))
        
        ttk.Button(
            secondary_frame,
            text="关闭",
            style='Secondary.TButton',
            command=self.root.quit
        ).pack(side='left')
    
    def _select_folder(self):
        """选择文件夹"""
        folder = filedialog.askdirectory(title="选择包含bulk文件的文件夹")
        if folder:
            self.folder_path.set(folder)
            self._identify_files()
    
    def _auto_search_files(self):
        """自动搜索文件"""
        search_paths = [
            Path.cwd(),
            Path.home() / "Downloads",
            Path.home() / "Desktop",
        ]
        
        for search_path in search_paths:
            if not search_path.exists():
                continue
            
            files = list(search_path.glob("bulk-*.xlsx"))
            if len(files) == 2:
                self.folder_path.set(str(search_path))
                self._identify_files()
                break
    
    def _identify_files(self):
        """识别文件"""
        try:
            folder = Path(self.folder_path.get())
            processor = BulkDataProcessor(str(folder))
            old_file, new_file = processor.find_excel_files()
            
            self.old_file.set(f"✓ 旧表: {Path(old_file).name}")
            self.new_file.set(f"✓ 新表: {Path(new_file).name}")
            
            self.log_viewer.add_log(f"识别到文件: {Path(old_file).name}", 'success')
            self.log_viewer.add_log(f"识别到文件: {Path(new_file).name}", 'success')
        except Exception as e:
            self.old_file.set("")
            self.new_file.set("")
            self.log_viewer.add_log(f"文件识别失败: {str(e)}", 'error')
    
    def _show_config_dialog(self):
        """显示配置对话框"""
        dialog = ConfigDialog(self.root, self.config, self.config_manager)
        self.root.wait_window(dialog)
        
        if dialog.result:
            self.config = dialog.result
            self._update_config_display()
    
    def _update_config_display(self):
        """更新配置显示"""
        pass
    
    def _start_processing(self):
        """开始处理"""
        if self.is_processing:
            return
        
        if not self.folder_path.get():
            messagebox.showwarning("警告", "请先选择文件夹")
            return
        
        self.is_processing = True
        self.start_button.config(state='disabled', bg=ThemeColors.TEXT_TERTIARY)
        
        self.progress_indicator.start_animation()
        
        self.log_viewer.add_log("开始数据处理流程", 'info')
        
        thread = threading.Thread(target=self._process_data)
        thread.start()
    
    def _process_data(self):
        """处理数据"""
        try:
            self.processor = BulkDataProcessor(self.folder_path.get(), self.config)
            
            step_messages = {
                "正在识别文件...": 0,
                "正在读取旧表数据...": 1,
                "正在读取新表数据...": 2,
                "正在处理 SP 数据...": 3,
                "正在处理 SB 数据...": 4,
                "正在处理 SD 数据...": 5,
                "正在导出结果...": 6,
                "处理完成!": 7
            }
            
            def progress_callback(message: str):
                self.root.after(0, lambda: self._update_progress(message))
                
                if message in step_messages:
                    step_index = step_messages[message]
                    self.root.after(0, lambda idx=step_index: self.step_indicator.set_current_step(idx))
                    
                    if "处理完成" in message:
                        self.root.after(0, lambda: self.log_viewer.add_log(message, 'success'))
                    elif "加载" in message:
                        self.root.after(0, lambda: self.log_viewer.add_log(message, 'info'))
                    else:
                        self.root.after(0, lambda: self.log_viewer.add_log(message, 'info'))
                else:
                    self.root.after(0, lambda: self.log_viewer.add_log(message, 'info'))
            
            results = self.processor.process(progress_callback=progress_callback)
            
            self._show_results(results)
            
            self.root.after(0, lambda: self.log_viewer.add_log("=" * 50, 'info'))
            self.root.after(0, lambda: self.log_viewer.add_log("✓ 数据处理完成！", 'success'))
            self.root.after(0, lambda: messagebox.showinfo("成功", "数据处理完成!"))
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            self.root.after(0, lambda: messagebox.showerror("错误", f"处理失败: {str(e)}"))
            self.root.after(0, lambda: self.log_viewer.add_log("=" * 50, 'error'))
            self.root.after(0, lambda: self.log_viewer.add_log(f"✗ 处理失败: {str(e)}", 'error'))
            self.root.after(0, lambda: self.log_viewer.add_log(error_detail, 'error'))
        finally:
            self.is_processing = False
            self.root.after(0, lambda: self.start_button.config(state='normal', bg=ThemeColors.ACCENT))
            self.root.after(0, lambda: self.progress_indicator.stop_animation())
    
    def _update_progress(self, message: str):
        """更新进度"""
        self.progress_status_label.configure(text=message)
        
        if "SP" in message:
            progress = 60
        elif "SB" in message:
            progress = 75
        elif "SD" in message:
            progress = 90
        elif "导出" in message:
            progress = 95
        elif "完成" in message:
            progress = 100
        else:
            progress = 20
        
        self.progress_bar['value'] = progress
        self.progress_percentage_label.configure(text=f"{progress}%")
    
    def _show_results(self, results: Dict):
        """显示结果"""
        self.root.after(0, lambda: self._update_result_text(results))
    
    def _update_result_text(self, results: Dict):
        """更新结果文本"""
        total_rows = sum(len(df) for df in results.values())
        
        self.files_card.update_value("2", "个文件")
        self.rows_card.update_value(f"{total_rows:,}", "行数据")
        self.output_card.update_value(f"{len(results)}", "个输出文件")
        
        self.result_text.configure(state='normal')
        self.result_text.delete(1.0, tk.END)
        
        text = f"处理文件: 2 个\n"
        text += f"总数据行: {total_rows:,} 行\n"
        text += f"输出文件: {len(results)} 个\n"
        text += f"📁 {self.folder_path.get()}\n"
        
        for ad_type in results:
            text += f"  - bulk_{ad_type}_数据源表格.csv\n"
        
        self.result_text.insert(1.0, text)
        self.result_text.configure(state='disabled')
    
    def _open_output_folder(self):
        """打开输出文件夹"""
        if self.folder_path.get():
            import subprocess
            import platform
            
            folder = Path(self.folder_path.get())
            
            if platform.system() == "Windows":
                subprocess.run(["explorer", str(folder)])
            elif platform.system() == "Darwin":
                subprocess.run(["open", str(folder)])
            else:
                subprocess.run(["xdg-open", str(folder)])
    
    def run(self):
        """运行应用"""
        self.root.mainloop()


class ConfigDialog(tk.Toplevel):
    """配置对话框"""
    
    def __init__(self, parent, config: Dict, config_manager: ConfigManager):
        super().__init__(parent)
        self.title("参数配置")
        self.geometry("400x300")
        self.configure(bg=ThemeColors.BG_PRIMARY)
        self.resizable(False, False)
        
        self.config = config.copy()
        self.config_manager = config_manager
        self.result = None
        
        self._create_widgets()
        
        self.transient(parent)
        self.grab_set()
    
    def _create_widgets(self):
        """创建组件"""
        main_frame = ttk.Frame(self, style='TFrame', padding=30)
        main_frame.pack(fill='both', expand=True)
        
        title_label = ttk.Label(
            main_frame,
            text="参数配置",
            style='Title.TLabel'
        )
        title_label.pack(anchor='w', pady=(0, 20))
        
        thresholds = self.config['thresholds']
        
        params_frame = ttk.Frame(main_frame, style='TFrame')
        params_frame.pack(fill='x', pady=(0, 20))
        
        params = [
            ("曝光量阈值", 'impressions', str(thresholds['impressions'])),
            ("点击率阈值", 'ctr', str(thresholds['ctr'])),
            ("转化率阈值", 'cvr', str(thresholds['cvr'])),
            ("ACOS阈值", 'acos', str(thresholds['acos']))
        ]
        
        self.param_vars = {}
        
        for i, (label, key, value) in enumerate(params):
            param_frame = ttk.Frame(params_frame, style='TFrame')
            param_frame.pack(fill='x', pady=8)
            
            ttk.Label(
                param_frame,
                text=label,
                style='Body.TLabel'
            ).pack(side='left')
            
            var = tk.StringVar(value=value)
            self.param_vars[key] = var
            
            entry = ttk.Entry(
                param_frame,
                textvariable=var,
                font=('SF Pro Text', 11),
                width=15
            )
            entry.pack(side='right')
        
        button_frame = ttk.Frame(main_frame, style='TFrame')
        button_frame.pack(fill='x')
        
        ttk.Button(
            button_frame,
            text="恢复默认",
            style='Secondary.TButton',
            command=self._reset_config
        ).pack(side='left')
        
        ttk.Button(
            button_frame,
            text="取消",
            style='Secondary.TButton',
            command=self._cancel
        ).pack(side='right', padx=(12, 0))
        
        ttk.Button(
            button_frame,
            text="确定",
            style='Primary.TButton',
            command=self._save_config
        ).pack(side='right', padx=(12, 0))
    
    def _reset_config(self):
        """重置配置"""
        default_config = self.config_manager.reset_config()
        for key, var in self.param_vars.items():
            var.set(str(default_config['thresholds'][key]))
    
    def _save_config(self):
        """保存配置"""
        try:
            self.config['thresholds']['impressions'] = int(self.param_vars['impressions'].get())
            self.config['thresholds']['ctr'] = float(self.param_vars['ctr'].get())
            self.config['thresholds']['cvr'] = float(self.param_vars['cvr'].get())
            self.config['thresholds']['acos'] = float(self.param_vars['acos'].get())
            
            self.config_manager.save_config(self.config)
            self.result = self.config
            self.destroy()
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数值")
    
    def _cancel(self):
        """取消"""
        self.result = None
        self.destroy()
