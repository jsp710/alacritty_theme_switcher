#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import ttk, messagebox

# 配置文件路径
THEMES_DIR = os.path.expanduser("~/.config/alacritty/themes/themes/")
ALACRITTY_CONF = os.path.expanduser("~/.config/alacritty/alacritty.toml")

def scan_themes():
    """扫描主题目录并返回主题列表（无后缀）"""
    themes = []
    try:
        for f in os.listdir(THEMES_DIR):
            if f.endswith(".toml"):
                themes.append(f[:-5])  # 去掉 .toml 后缀
    except FileNotFoundError:
        messagebox.showerror("错误", f"主题目录不存在: {THEMES_DIR}")
    return sorted(themes)

def apply_theme(theme_name):
    """应用指定主题"""
    try:
        # 读取原配置
        with open(ALACRITTY_CONF, "r") as f:
            lines = f.readlines()
        
        # 修改第11行（索引从0开始是第10行）
        if len(lines) >= 11:
            lines[10] = f'    "~/.config/alacritty/themes/themes/{theme_name}.toml"\n'
        else:
            messagebox.showerror("错误", "配置文件格式不符合预期")
            return
            
        # 写入新配置
        with open(ALACRITTY_CONF, "w") as f:
            f.writelines(lines)
            
        messagebox.showinfo("成功", f"已切换至主题: {theme_name}")
        
    except Exception as e:
        messagebox.showerror("错误", f"应用主题失败: {str(e)}")

class ThemeSwitcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Alacritty 主题切换器")
        self.geometry("300x400")
        
        # 主题列表
        self.theme_list = ttk.Treeview(self, columns=(), show="tree", selectmode="browse")
        self.theme_list.heading("#0", text="可用主题")
        self.theme_list.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # 双击应用主题
        self.theme_list.bind("<Double-1>", self.on_double_click)
        
        # 刷新按钮
        ttk.Button(self, text="刷新列表", command=self.update_list).pack(pady=5)
        
        self.update_list()
        
    def update_list(self):
        """刷新主题列表"""
        self.theme_list.delete(*self.theme_list.get_children())
        for theme in scan_themes():
            self.theme_list.insert("", "end", text=theme)
            
    def on_double_click(self, event):
        """双击事件处理"""
        item = self.theme_list.selection()[0]
        theme_name = self.theme_list.item(item, "text")
        apply_theme(theme_name)

if __name__ == "__main__":
    # 检查依赖
    try:
        import tkinter
    except ImportError:
        print("请先安装 tkinter：sudo pacman -S tk")
        exit(1)
        
    app = ThemeSwitcher()
    app.mainloop()