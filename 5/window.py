import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import time
import numpy as np
from numpy.linalg import eig


def print_hadler():
    os.system("python3 drawer.py")
    start = time.time()
    while not os.path.exists('res.png'):
        time.sleep(0.5)
        if time.time() - start > 5:
            messagebox.showinfo("Aborted (core dumped)", 
                                "double free or corruption (out)")
            return 0
    img = Image.open("res.png").resize((600,233))
    img_shower = tk.Label(image_frm)
    img_tk = ImageTk.PhotoImage(img)
    img_shower.image = img_tk
    img_shower.config(image=img_tk)
    img_shower.grid(row=0, column=0)


def count_handler():
    a11 = round(eval(a11_entry.get()), 3)
    a12 = round(eval(a12_entry.get()), 3)
    a13 = round(eval(a13_entry.get()), 3)
    a21 = round(eval(a21_entry.get()), 3)
    a22 = round(eval(a22_entry.get()), 3)
    a23 = round(eval(a23_entry.get()), 3)
    a31 = round(eval(a31_entry.get()), 3)
    a32 = round(eval(a32_entry.get()), 3)
    a33 = round(eval(a33_entry.get()), 3)
    iternum = int(iter_n_entry.get())
    matr = np.array([[a11, a12, a13], [a21, a22, a23], [a31, a32, a33]])
    # print(matr)
    # print(eig(matr)[0])
    start = time.time()
    os.system(f"./a.out {a11} {a12} {a13} {a21} {a22} {a23} {a31} {a32} {a33} {iternum}")
    while not os.path.exists("info"):
        time.sleep(0.5)
        if time.time() - start > 5:
            messagebox.showinfo("Aborted (core dumped)", 
                                "double free or corruption (out)")
            return 0
    with open('info', 'r') as f:
        cells, eltime, step = f.readline().split()
    time_elapsed_entry.config(state='normal')
    time_elapsed_entry.delete(0, tk.END)
    time_elapsed_entry.insert(tk.END, eltime)
    time_elapsed_entry.config(state='readonly')
    cells_entry.config(state='normal')
    cells_entry.delete(0, tk.END)
    cells_entry.insert(tk.END, cells)
    cells_entry.config(state='readonly')
    step_entry.config(state='normal')
    step_entry.delete(0, tk.END)
    step_entry.insert(tk.END, step)
    step_entry.config(state='readonly')
    eig_value_entry.config(state='normal')
    eig_value_entry.delete(0, tk.END)
    eig_value_entry.insert(tk.END, ', '.join(map(str, 
                                                 map(lambda x: np.round(x, 4), eig(matr)[0]))))
    eig_value_entry.config(state='readonly')


def next_iter():
    n = eval(iter_n_entry.get()) + 1
    iter_n_entry.delete(0, tk.END)
    iter_n_entry.insert(tk.END, n)
    count_handler()


root = tk.Tk()
root.config(bg="#FFFFFF")
root.title("CRM")

hello_txt = tk.Label(root, text="Локализация ЦРМ в проективном пространстве",
                     font=("Arial Bold", 12), bg="#FFFFFF")
hello_txt.pack()

params = tk.Frame(root, bg="#FFFFFF", pady=4)
params.pack()
"""Ввод матрицы"""
matrix_txt = tk.Label(params, text="Матрица А", bg="#FFFFFF")
matrix_txt.grid(row=0, column=0, columnspan=3)

a11_entry = tk.Entry(params, width=5)
a11_entry.insert(tk.END, '0.7')
a11_entry.grid(row=1, column=0)
a12_entry = tk.Entry(params, width=5)
a12_entry.insert(tk.END, '-0.5')
a12_entry.grid(row=1, column=1)
a13_entry = tk.Entry(params, width=5)
a13_entry.insert(tk.END, '0.0')
a13_entry.grid(row=1, column=2)

a21_entry = tk.Entry(params, width=5)
a21_entry.insert(tk.END, '0.5')
a21_entry.grid(row=2, column=0)
a22_entry = tk.Entry(params, width=5)
a22_entry.insert(tk.END, '0.7')
a22_entry.grid(row=2, column=1)
a23_entry = tk.Entry(params, width=5)
a23_entry.insert(tk.END, '0.0')
a23_entry.grid(row=2, column=2)

a31_entry = tk.Entry(params, width=5)
a31_entry.insert(tk.END, '1.0')
a31_entry.grid(row=3, column=0)
a32_entry = tk.Entry(params, width=5)
a32_entry.insert(tk.END, '2.0')
a32_entry.grid(row=3, column=1)
a33_entry = tk.Entry(params, width=5)
a33_entry.insert(tk.END, '5.0')
a33_entry.grid(row=3, column=2)

iters = tk.Frame(root, bg="#FFFFFF", pady=8)
iters.pack()
"""Ввод количества итераций"""
iter_n_txt = tk.Label(iters, text="Количество итераций: ",
                      bg="#FFFFFF")
iter_n_txt.grid(row=0, column=0, sticky=tk.E)
iter_n_entry = tk.Entry(iters, width=4)
iter_n_entry.insert(tk.END, '3')
iter_n_entry.grid(row=0, column=1, sticky=tk.W)

btns = tk.Frame(root, bg="#FFFFFF", pady=8)
btns.pack()

"""Задача кнопок действий"""
print_btn = tk.Button(btns,
                      text="Построить\nизображение",
                      bg="green",
                      command=print_hadler)
print_btn.grid(row=0, column=0, padx=4)
count_btn = tk.Button(btns,
                      text="Запуск\nпрограммы",
                      bg="black",
                      fg="red",
                      command=count_handler)
count_btn.grid(row=0, column=1, padx=4)
next_hop_btn = tk.Button(btns,
                         text="Следующая\nитерация",
                         bg="purple", fg="white",
                         command=next_iter)
next_hop_btn.grid(row=0, column=2, padx=4)

extra_info = tk.Frame(root, bg="#FFFFFF")
extra_info.pack()
"""Затраченное время"""
time_elapsed_txt = tk.Label(extra_info, 
                            text="Затраченное время (s)", 
                            bg="#FFFFFF")
time_elapsed_txt.grid(row=0, 
                      column=0, 
                      sticky=tk.E,
                      padx=4, pady=2)
time_elapsed_entry = tk.Entry(extra_info, width=10, bg="#FFFFFF")
time_elapsed_entry.config(state='readonly')
time_elapsed_entry.grid(row=0,
                        column=1,
                        sticky=tk.W,
                        padx=4, pady=2)

cells_txt = tk.Label(extra_info, text="Количество ячеек", bg="#FFFFFF")
cells_txt.grid(row=1, column=0, sticky=tk.E, padx=4, pady=4)
cells_entry = tk.Entry(extra_info, width=10, bg="#FFFFFF")
cells_entry.config(state='readonly')
cells_entry.grid(row=1,
                 column=1,
                 sticky=tk.W,
                 padx=4, pady=2)

step_txt = tk.Label(extra_info,
                    text="Полученный шаг",
                    bg="#FFFFFF")
step_txt.grid(row=2, column=0, sticky=tk.E,
              padx=4, pady=2)
step_entry = tk.Entry(extra_info, width=10, bg="#FFFFFF")
step_entry.config(state='readonly')
step_entry.grid(row=2,
                 column=1,
                 sticky=tk.W,
                 padx=4, pady=2)

eig_value_txt = tk.Label(extra_info,
                         text="Собственные значения",
                         bg="#FFFFFF")
eig_value_txt.grid(row=3, column=0, sticky=tk.E,
                   padx=4, pady=2)
eig_value_entry = tk.Entry(extra_info, width=15)
eig_value_entry.config(state='readonly')
eig_value_entry.grid(row=3, column=1, sticky=tk.W)

"""Вставка изображения"""
image_frm = tk.Frame(root, bg="#FFFFFF", pady=5)
image_frm.pack(pady=5)

root.mainloop()
for i in range(1,4):
    if os.path.exists(f"{i}buf"):
        os.remove(f"{i}buf")
if os.path.exists("info"):
    os.remove("info")
