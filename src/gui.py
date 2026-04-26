"""
GUI界面模块
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
from typing import Optional, Dict
from .processor import BulkDataProcessor
from .utils import ConfigManager


class BulkProcessorGUI:
    """亚马逊广告数据处理器GUI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("亚马逊广告数据处理器")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        
        self.folder_path = tk.StringVar()
        self.old_file = tk.StringVar()
        self.new_file = tk.StringVar()
        
        self.is_processing = False
        self.processor = None
        
        self._create_widgets()
        self._auto_search_files()
    
    def _create_widgets(self):
        """创建所有UI组件"""
        self._create_file_selection_frame()
        self._create_config_frame()
        self._create_progress_frame()
        self._create_result_frame()
        self._create_buttons()
    
    def _create_file_selection_frame(self):
        """创建文件选择区域"""
        frame = ttk.LabelFrame(self.root, text="📁 数据文件夹", padding="10")
        frame.pack(fill="x", padx=10, pady=5)
        
        path_frame = ttk.Frame(frame)
        path_frame.pack(fill="x")
        
        ttk.Entry(path_frame, textvariable=self.folder_path, width=50).pack(side="left", fill="x", expand=True)
        ttk.Button(path_frame, text="选择文件夹", command=self._select_folder).pack(side="right", padx=(5, 0))
        
        files_frame = ttk.LabelFrame(frame, text="📄 识别到的文件", padding="5")
        files_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Label(files_frame, textvariable=self.old_file, foreground="green").pack(anchor="w")
        ttk.Label(files_frame, textvariable=self.new_file, foreground="green").pack(anchor="w")
    
    def _create_config_frame(self):
        """创建配置区域"""
        frame = ttk.LabelFrame(self.root, text="⚙️ 处理参数", padding="10")
        frame.pack(fill="x", padx=10, pady=5)
        
        config_text = f"曝光量阈值: {self.config['thresholds']['impressions']}  " \
                     f"点击率阈值: {self.config['thresholds']['ctr']*100:.2f}%  " \
                     f"转化率阈值: {self.config['thresholds']['cvr']*100:.0f}%  " \
                     f"ACOS阈值: {self.config['thresholds']['acos']*100:.0f}%"
        
        ttk.Label(frame, text=config_text).pack(side="left")
        ttk.Button(frame, text="配置参数", command=self._show_config_dialog).pack(side="right")
    
    def _create_progress_frame(self):
        """创建进度显示区域"""
        frame = ttk.LabelFrame(self.root, text="📊 处理进度", padding="10")
        frame.pack(fill="x", padx=10, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x")
        
        self.progress_label = ttk.Label(frame, text="等待开始...")
        self.progress_label.pack(anchor="w", pady=(5, 0))
    
    def _create_result_frame(self):
        """创建结果显示区域"""
        frame = ttk.LabelFrame(self.root, text="✅ 处理结果", padding="10")
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.result_text = tk.Text(frame, height=10, width=70, state="disabled")
        self.result_text.pack(fill="both", expand=True)
    
    def _create_buttons(self):
        """创建按钮"""
        frame = ttk.Frame(self.root)
        frame.pack(fill="x", padx=10, pady=10)
        
        self.start_button = ttk.Button(frame, text="开始处理", command=self._start_processing)
        self.start_button.pack(side="left", padx=5)
        
        ttk.Button(frame, text="打开输出文件夹", command=self._open_output_folder).pack(side="left", padx=5)
        ttk.Button(frame, text="关闭", command=self.root.quit).pack(side="right", padx=5)
    
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
            
            self.old_file.set(f"✅ 旧表: {Path(old_file).name}")
            self.new_file.set(f"✅ 新表: {Path(new_file).name}")
        except Exception as e:
            self.old_file.set("")
            self.new_file.set("")
            messagebox.showerror("错误", str(e))
    
    def _show_config_dialog(self):
        """显示配置对话框"""
        dialog = ConfigDialog(self.root, self.config, self.config_manager)
        self.root.wait_window(dialog)
        
        if dialog.result:
            self.config = dialog.result
            self._update_config_display()
    
    def _update_config_display(self):
        """更新配置显示"""
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.LabelFrame) and widget.cget("text") == "⚙️ 处理参数":
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label):
                        config_text = f"曝光量阈值: {self.config['thresholds']['impressions']}  " \
                                     f"点击率阈值: {self.config['thresholds']['ctr']*100:.2f}%  " \
                                     f"转化率阈值: {self.config['thresholds']['cvr']*100:.0f}%  " \
                                     f"ACOS阈值: {self.config['thresholds']['acos']*100:.0f}%"
                        child.config(text=config_text)
    
    def _start_processing(self):
        """开始处理"""
        if self.is_processing:
            return
        
        if not self.folder_path.get():
            messagebox.showwarning("警告", "请先选择文件夹")
            return
        
        self.is_processing = True
        self.start_button.config(state="disabled")
        self.progress_var.set(0)
        self.progress_label.config(text="正在处理...")
        
        thread = threading.Thread(target=self._process_data)
        thread.start()
    
    def _process_data(self):
        """处理数据"""
        try:
            self.processor = BulkDataProcessor(self.folder_path.get(), self.config)
            
            results = self.processor.process(progress_callback=self._update_progress)
            
            self._show_results(results)
            
            self.root.after(0, lambda: messagebox.showinfo("成功", "数据处理完成!"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"处理失败: {str(e)}"))
        finally:
            self.is_processing = False
            self.root.after(0, lambda: self.start_button.config(state="normal"))
    
    def _update_progress(self, message: str):
        """更新进度"""
        self.root.after(0, lambda: self.progress_label.config(text=message))
    
    def _show_results(self, results: Dict):
        """显示结果"""
        self.root.after(0, lambda: self._update_result_text(results))
    
    def _update_result_text(self, results: Dict):
        """更新结果文本"""
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        
        total_rows = sum(len(df) for df in results.values())
        
        text = f"处理文件: 2 个\n"
        text += f"总数据行: {total_rows:,} 行\n"
        text += f"输出文件: {len(results)} 个\n"
        text += f"📁 {self.folder_path.get()}\n"
        
        for ad_type in results:
            text += f"  - bulk_{ad_type}_数据源表格.csv\n"
        
        self.result_text.insert(1.0, text)
        self.result_text.config(state="disabled")
    
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
        self.geometry("300x250")
        self.resizable(False, False)
        
        self.config = config.copy()
        self.config_manager = config_manager
        self.result = None
        
        self._create_widgets()
        
        self.transient(parent)
        self.grab_set()
    
    def _create_widgets(self):
        """创建组件"""
        frame = ttk.Frame(self, padding="10")
        frame.pack(fill="both", expand=True)
        
        thresholds = self.config['thresholds']
        
        ttk.Label(frame, text="曝光量阈值:").grid(row=0, column=0, sticky="w", pady=5)
        self.impressions_var = tk.StringVar(value=str(thresholds['impressions']))
        ttk.Entry(frame, textvariable=self.impressions_var, width=15).grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="点击率阈值:").grid(row=1, column=0, sticky="w", pady=5)
        self.ctr_var = tk.StringVar(value=str(thresholds['ctr']))
        ttk.Entry(frame, textvariable=self.ctr_var, width=15).grid(row=1, column=1, pady=5)
        ttk.Label(frame, text=f"({float(thresholds['ctr'])*100:.2f}%)").grid(row=1, column=2, pady=5)
        
        ttk.Label(frame, text="转化率阈值:").grid(row=2, column=0, sticky="w", pady=5)
        self.cvr_var = tk.StringVar(value=str(thresholds['cvr']))
        ttk.Entry(frame, textvariable=self.cvr_var, width=15).grid(row=2, column=1, pady=5)
        ttk.Label(frame, text=f"({float(thresholds['cvr'])*100:.0f}%)").grid(row=2, column=2, pady=5)
        
        ttk.Label(frame, text="ACOS阈值:").grid(row=3, column=0, sticky="w", pady=5)
        self.acos_var = tk.StringVar(value=str(thresholds['acos']))
        ttk.Entry(frame, textvariable=self.acos_var, width=15).grid(row=3, column=1, pady=5)
        ttk.Label(frame, text=f"({float(thresholds['acos'])*100:.0f}%)").grid(row=3, column=2, pady=5)
        
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="恢复默认", command=self._reset_config).pack(side="left", padx=5)
        ttk.Button(button_frame, text="取消", command=self._cancel).pack(side="left", padx=5)
        ttk.Button(button_frame, text="确定", command=self._save_config).pack(side="left", padx=5)
    
    def _reset_config(self):
        """重置配置"""
        default_config = self.config_manager.reset_config()
        self.impressions_var.set(str(default_config['thresholds']['impressions']))
        self.ctr_var.set(str(default_config['thresholds']['ctr']))
        self.cvr_var.set(str(default_config['thresholds']['cvr']))
        self.acos_var.set(str(default_config['thresholds']['acos']))
    
    def _save_config(self):
        """保存配置"""
        try:
            self.config['thresholds']['impressions'] = int(self.impressions_var.get())
            self.config['thresholds']['ctr'] = float(self.ctr_var.get())
            self.config['thresholds']['cvr'] = float(self.cvr_var.get())
            self.config['thresholds']['acos'] = float(self.acos_var.get())
            
            self.config_manager.save_config(self.config)
            self.result = self.config
            self.destroy()
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数值")
    
    def _cancel(self):
        """取消"""
        self.result = None
        self.destroy()
