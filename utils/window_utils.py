import tkinter as tk

def add_drag_functionality(root, widget):
    def start_move(event):
        root._x = event.x
        root._y = event.y

    def do_move(event):
        x = root.winfo_x() + event.x - root._x
        y = root.winfo_y() + event.y - root._y
        root.geometry(f"+{x}+{y}")

    widget.bind('<ButtonPress-1>', start_move)
    widget.bind('<B1-Motion>', do_move)

def add_resize_handles(root):
    # # 左上角
    # nw_resize = tk.Frame(root, cursor='size_nw_se', bg='gray', width=10, height=10)
    # nw_resize.place(x=0, y=0)
    # nw_resize.bind("<B1-Motion>", lambda event: resize_nw(event, root))
    #
    # # 右上角
    # ne_resize = tk.Frame(root, cursor='size_ne_sw', bg='gray', width=10, height=10)
    # ne_resize.place(relx=1.0, y=0, anchor=tk.NE)
    # ne_resize.bind("<B1-Motion>", lambda event: resize_ne(event, root))

    # 左下角
    sw_resize = tk.Frame(root, cursor='size_ne_sw', bg='gray', width=7, height=7)
    sw_resize.place(x=0, rely=1.0, anchor=tk.SW)
    sw_resize.bind("<B1-Motion>", lambda event: resize_sw(event, root))

    # 右下角
    se_resize = tk.Frame(root, cursor='size_nw_se', bg='gray', width=7, height=7)
    se_resize.place(relx=1.0, rely=1.0, anchor=tk.SE)
    se_resize.bind("<B1-Motion>", lambda event: resize_se(event, root))

    # 上边
    n_resize = tk.Frame(root, cursor='size_ns', bg='gray', height=5)
    n_resize.place(relx=0.5, rely=0, anchor=tk.N)
    n_resize.bind("<B1-Motion>", lambda event: resize_n(event, root))

    # 下边
    s_resize = tk.Frame(root, cursor='size_ns', bg='gray', height=5)
    s_resize.place(relx=0.5, rely=1.0, anchor=tk.S)
    s_resize.bind("<B1-Motion>", lambda event: resize_s(event, root))

    # 左边
    w_resize = tk.Frame(root, cursor='size_we', bg='gray', width=5)
    w_resize.place(rely=0.5, x=0, anchor=tk.W)
    w_resize.bind("<B1-Motion>", lambda event: resize_w(event, root))

    # 右边
    e_resize = tk.Frame(root, cursor='size_we', bg='gray', width=5)
    e_resize.place(relx=1.0, rely=0.5, anchor=tk.E)
    e_resize.bind("<B1-Motion>", lambda event: resize_e(event, root))

def resize_nw(event, root):
    x = root.winfo_x() + event.x
    y = root.winfo_y() + event.y
    width = root.winfo_width() - event.x
    height = root.winfo_height() - event.y
    root.geometry(f"{width}x{height}+{x}+{y}")

def resize_ne(event, root):
    y = root.winfo_y() + event.y
    width = root.winfo_width() + event.x
    height = root.winfo_height() - event.y
    root.geometry(f"{width}x{height}+{root.winfo_x()}+{y}")

def resize_sw(event, root):
    x = root.winfo_x() + event.x
    width = root.winfo_width() - event.x
    height = root.winfo_height() + event.y
    root.geometry(f"{width}x{height}+{x}+{root.winfo_y()}")

def resize_se(event, root):
    width = root.winfo_width() + event.x
    height = root.winfo_height() + event.y
    root.geometry(f"{width}x{height}+{root.winfo_x()}+{root.winfo_y()}")

def resize_n(event, root):
    y = root.winfo_y() + event.y
    height = root.winfo_height() - event.y
    root.geometry(f"{root.winfo_width()}x{height}+{root.winfo_x()}+{y}")

def resize_s(event, root):
    height = root.winfo_height() + event.y
    root.geometry(f"{root.winfo_width()}x{height}+{root.winfo_x()}+{root.winfo_y()}")

def resize_w(event, root):
    x = root.winfo_x() + event.x
    width = root.winfo_width() - event.x
    root.geometry(f"{width}x{root.winfo_height()}+{x}+{root.winfo_y()}")

def resize_e(event, root):
    width = root.winfo_width() + event.x
    root.geometry(f"{width}x{root.winfo_height()}+{root.winfo_x()}+{root.winfo_y()}")