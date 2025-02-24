#!/usr/bin/env python3


import os
import tkinter as tk
from tkinter import messagebox
import toml

# 主题文件夹路径
THEME_DIR = '/home/skubla/.config/alacritty/themes/themes'
ALACRITTY_CONFIG_PATH = '/home/skubla/.config/alacritty/alacritty.toml'

# 获取主题文件名列表
def get_themes():
    try:
        # 扫描目录并提取所有 toml 配置文件的名称（去掉后缀）
        theme_files = [f[:-5] for f in os.listdir(THEME_DIR) if f.endswith('.toml')]
        return theme_files
    except FileNotFoundError:
        messagebox.showerror("错误", "主题目录未找到！")
        return []

# 更新 Alacritty 配置文件
def update_alacritty_config(selected_theme):
    try:
        # 读取当前 alacritty.toml 配置文件
        with open(ALACRITTY_CONFIG_PATH, 'r') as file:
            lines = file.readlines()

        # 修改第11行的主题路径
        lines[10] = f'"{THEME_DIR}/{selected_theme}.toml"]\n'

        # 将修改后的内容写回配置文件
        with open(ALACRITTY_CONFIG_PATH, 'w') as file:
            file.writelines(lines)
        messagebox.showinfo("成功", f"已切换主题到 {selected_theme}！")
    except Exception as e:
        messagebox.showerror("错误", f"更新配置文件失败: {str(e)}")

# 创建并显示 GUI
def create_gui():
    root = tk.Tk()
    root.title("Alacritty 主题切换器")
    
    # 设置合适的窗口大小
    root.geometry("900x1200")
    
    # 获取所有主题
    themes = get_themes()
    
    if not themes:
        return

    # 创建主题选择的下拉菜单
    theme_var = tk.StringVar(root)
    theme_var.set(themes[0])  # 默认选择第一个主题

    # 创建布局：使用 grid 布局管理器并设置行间距
    theme_label = tk.Label(root, text="选择主题:")
    theme_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')  # 添加适当的 padding
    
    theme_menu = tk.OptionMenu(root, theme_var, *themes)
    theme_menu.grid(row=1, column=0, padx=10, pady=10, sticky='ew')  # 使用 grid 设置行距
    
    # 创建切换按钮
    switch_button = tk.Button(root, text="切换主题", command=lambda: update_alacritty_config(theme_var.get()))
    switch_button.grid(row=2, column=0, padx=10, pady=20, sticky='ew')  # 添加适当的 padding

    # 配置 grid 的列和行的权重，以便组件适应窗口大小
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # 运行 GUI
    root.mainloop()

if __name__ == "__main__":
    create_gui()
