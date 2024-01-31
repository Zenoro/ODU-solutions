import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import os
import time
import old_main as om

if os.getcwd().endswith("my_osip"):
    os.chdir("6")

# def on_closing():
#     if messagebox.askokcancel("Выход", "Вы хотите выйти?"):
#         root.destroy()

def insert_info_into_entry(entr:tk.Entry, info:str):
    entr.config(state='normal')
    entr.delete(0, tk.END)
    entr.insert(tk.END, info)
    entr.config(state='readonly')


# def insert_txt(lbl:tk.Label, txt:str):
#     lbl.config(state=tk.NORMAL)
#     lbl.delete(0, tk.END)
#     lbl.insert(tk.END, txt)
#     lbl.config(state=tk.DISABLED)


def start_handler():
    try:
        alpha = eval(alpha_param_ctch.get())
        beta = eval(beta_param_ctch.get())
        omega = eval(omega_param_ctch.get())
        B = eval(b_param_ctch.get())
        k = eval(k_param_ctch.get())
        x_l = eval(x0_ctch.get())
        x_r = eval(x1_ctch.get())
        y_t = eval(y1_ctch.get())
        y_l = eval(y0_ctch.get())
        h = eval(step_ctch.get())
        iter_num = int(combo.get())
        points_num = int(pnt_sqr_ctch.get())
        om.main(x_l, x_r, y_l, y_t, h, points_num, iter_num, alpha, beta, omega, k, B)
        while not os.path.exists('time.out'):
            time.sleep(1)
        with open('time.out', 'r') as fd:
            elapsed_time = round(float(fd.readline()), 3)
        insert_info_into_entry(time_elapsed_entry, str(elapsed_time))
    except SyntaxError:
        messagebox.showinfo('Ошибка SyntaxError',
                            "Вы не ввели необходимые параметры или передали их неверно.")
    except ValueError:
        messagebox.showinfo('Ошибка ValueError',
                            "Вы ввели необходимые параметры неверно.")
    # except NameError:
    #     messagebox.showinfo('Ошибка ValueError',
    #                         "Параметр количества точек должен быть целым числом.")


def draw_handler():
    x_l = eval(x0_ctch.get())
    x_r = eval(x1_ctch.get())
    y_t = eval(y1_ctch.get())
    y_l = eval(y0_ctch.get())
    iter_num = int(combo.get())
    om.draw(x_l, x_r, y_l, y_t, 0)
    while not os.path.exists(f"res{int(iter_num)}.png"):
        time.sleep(0.5)
    img = Image.open(f"res{int(iter_num)}.png").resize((600,400))
    img_shower = tk.Label(image_frm)
    img_tk = ImageTk.PhotoImage(img)
    img_shower.image = img_tk
    img_shower.config(image=img_tk)
    img_shower.grid(row=0, column=0)
    with open('sys.out', 'r') as fd:
        cellnum = float(fd.readline())
    insert_info_into_entry(cell_count_entry, str(int(cellnum)))


def iteration_handler():
    alpha = eval(alpha_param_ctch.get())
    beta = eval(beta_param_ctch.get())
    omega = eval(omega_param_ctch.get())
    B = eval(b_param_ctch.get())
    k = eval(k_param_ctch.get())
    x_l = eval(x0_ctch.get())
    x_r = eval(x1_ctch.get())
    y_t = eval(y1_ctch.get())
    y_l = eval(y0_ctch.get())
    h = eval(step_ctch.get())
    iterc = int(combo.get()) + 1
    combo.delete(0, tk.END)
    combo.insert(tk.END, str(iterc))
    om.new_iterat(x_l, x_r, y_l, y_t, iterc, alpha, beta, omega, k, B)
    # os.system(f"./a.out {x_l} {x_r} {y_l} {y_t} {h} {iterc} {alpha} {beta} {omega} {k} {B}")
    while not os.path.exists('sys.out'):
        time.sleep(0.5)
    with open('time.out', 'r') as fd:
        elapsed_time = round(float(fd.readline()), 3)
    # insert_info_into_entry(cell_count_entry, str(cells))
    insert_info_into_entry(time_elapsed_entry, str(elapsed_time))

    # crm.new_iterat(x_l, x_r, y_l, y_t, iterc, alpha, beta, omega, k, B)


def draw_area_handler():
    alpha = eval(alpha_param_ctch.get())
    beta = eval(beta_param_ctch.get())
    omega = eval(omega_param_ctch.get())
    B = eval(b_param_ctch.get())
    k = eval(k_param_ctch.get())
    x_l = eval(x0_ctch.get())
    x_r = eval(x1_ctch.get())
    y_t = eval(y1_ctch.get())
    y_l = eval(y0_ctch.get())
    h = eval(step_ctch.get())
    iter_num = int(combo.get())
    points_num = int(pnt_sqr_ctch.get())
    om.main_for_place(x_l, x_r, y_l, y_t, h, points_num, iter_num, alpha, beta, omega, k, B)
    while not os.path.exists(f'area{iter_num}.png'):
        time.sleep(0.5)
    img = Image.open(f"area{iter_num}.png").resize((600,400))
    img_tk = ImageTk.PhotoImage(img)
    area_shower = tk.Label(image_frm)
    area_shower.image = img_tk
    area_shower.config(image=img_tk)
    area_shower.grid(row=0, column=1)


root = tk.Tk()
root.config(bg="#FFFFFF")
# root.geometry("600x450")
root.title("Вычислительная работа 6")
# root.protocol("WM_DELETE_WINDOW", on_closing)


"""Отображение оглавления"""
tk.Label(root, text="Построение аттрактора и фильтрации \nотображения Дуффинга",
         font=("Arial Bold", 12), bg="#FFFFFF").pack()
# hello_words.grid(row=0, column=0, columnspan=4)

img_otobrazh_shower = tk.Label(root, bg="#FFFFFF")
img_otobr = Image.open("otobrzhenie.png").resize((240, 82))
img_otobr_tk = ImageTk.PhotoImage(img_otobr)
img_otobrazh_shower.config(image=img_otobr_tk)
img_otobrazh_shower.pack()

params = tk.Frame(root, bg="#FFFFFF")
params.pack(pady=5)

"""Ввод параметра k"""
tk.Label(params, text="k = ",bg="#FFFFFF").grid(row=0,
                                                column=0,
                                                sticky=tk.E)
k_param_ctch = tk.Entry(params,
                     width=9)
k_param_ctch.insert(tk.END, '0.25')
k_param_ctch.grid(row=0,
                  column=1,
                  sticky=tk.W)

"""Ввод параметра alpha"""
tk.Label(params, text="α = ", bg="#FFFFFF").grid(row=0,
                                                 column=2,
                                                 sticky=tk.E)
alpha_param_ctch = tk.Entry(params,
                     width=9)
alpha_param_ctch.insert(tk.END, '1')
alpha_param_ctch.grid(row=0,
                  column=3,
                  sticky=tk.W)

"""Ввод параметра B"""
tk.Label(params, text="B = ", bg="#FFFFFF").grid(row=1,
                                                 column=0,
                                                 sticky=tk.E)
b_param_ctch = tk.Entry(params,
                     width=9)
b_param_ctch.insert(tk.END, '0')
b_param_ctch.grid(row=1,
                  column=1,
                  sticky=tk.W)

"""Ввод параметра beta"""
tk.Label(params, text="β = ", bg="#FFFFFF").grid(row=1,
                                                 column=2,
                                                 sticky=tk.E)
beta_param_ctch = tk.Entry(params,
                     width=9)
beta_param_ctch.insert(tk.END, '-1')
beta_param_ctch.grid(row=1,
                  column=3,
                  sticky=tk.W)

"""Ввод параметра omega"""
tk.Label(params, text="ω = ", bg="#FFFFFF").grid(row=2,
                                                 column=0,
                                                 columnspan=2,
                                                 sticky=tk.E)
omega_param_ctch = tk.Entry(params,
                     width=9)
omega_param_ctch.insert(tk.END, '1')
omega_param_ctch.grid(row=2,
                  column=2,
                  columnspan=2,
                  sticky=tk.W)

coord = tk.Frame(root, bg="#FFFFFF")
coord.pack(pady=5)
"""Текст координат"""
tk.Label(coord, text="Координаты изначальной области",
         font=("Arial Bold", 10), bg="#FFFFFF").grid(row=0,
                                                     column=0,
                                                     columnspan=4)

"""Ввод координат"""
# x coords
tk.Label(coord, text="x0 ", bg="#FFFFFF").grid(row=1,
                                               column=0,
                                               sticky=tk.E)
x0_ctch = tk.Entry(coord, width=9)
x0_ctch.insert(tk.END, '-2')
x0_ctch.grid(row=1, column=1, sticky=tk.W)

tk.Label(coord, text="x1 ", bg="#FFFFFF").grid(row=1,
                                               column=2,
                                               sticky=tk.E)
x1_ctch = tk.Entry(coord,
                width=9)
x1_ctch.insert(tk.END, '2')
x1_ctch.grid(row=1, column=3, sticky=tk.W)

# y coords
tk.Label(coord, text="y0 ", bg="#FFFFFF").grid(row=2,
                                               column=0,
                                               sticky=tk.E)  
y0_ctch = tk.Entry(coord, width=9)
y0_ctch.insert(tk.END, '-2')
y0_ctch.grid(row=2, column=1, sticky=tk.W)

tk.Label(coord, text="y1 ", bg="#FFFFFF").grid(row=2,
                                               column=2,
                                               sticky=tk.E)
y1_ctch = tk.Entry(coord, width=9)
y1_ctch.insert(tk.END, '2')
y1_ctch.grid(row=2, column=3, sticky=tk.W)

other_params = tk.Frame(root, bg="#FFFFFF")
other_params.pack(pady=5)

"""Ввод шага"""
tk.Label(other_params, text="Шаг (h): ", bg="#FFFFFF").grid(row=0,
                                                            column=0,
                                                            columnspan=2,
                                                            sticky=tk.E)
step_ctch = tk.Entry(other_params, width=9)
step_ctch.insert(tk.END, '0.5')
step_ctch.grid(row=0, column=2, columnspan=2, sticky=tk.W)

"""Ввод количества точек внутри области"""
tk.Label(other_params, text="Корень кол-ва точек внутри области: ", bg="#FFFFFF").grid(row=1,
                                                                                       column=0,
                                                                                       columnspan=2,
                                                                                       sticky=tk.E)
pnt_sqr_ctch = tk.Entry(other_params, width=9)
pnt_sqr_ctch.insert(tk.END, "5")
pnt_sqr_ctch.grid(row=1, column=2, columnspan=2, sticky=tk.W)

"""Выбор количества итераций"""
tk.Label(other_params, text="Количество итераций", bg="#FFFFFF").grid(row=2,
                                                                      column=0,
                                                                      columnspan=2,
                                                                      sticky=tk.E)
combo = Combobox(other_params)
combo['values'] = list(range(1,11))
combo.current(3)
combo.grid(row=2, column=2, columnspan=2, sticky=tk.W)

"""Выбор вывода сетки на координатной плоскости"""
# chk_state = tk.BooleanVar()
# chk_state.set(False)  # задайте проверку состояния чекбокса  
# chk = tk.Checkbutton(root,
#                   text='Показывать координатную сетку',
#                   var=chk_state,
#                   bg="#FFFFFF")
# chk.grid(row=10,
#          column=0,
#          sticky=tk.W,
#          columnspan=2)

buttons_frm = tk.Frame(root, bg="#FFFFFF")
buttons_frm.pack(pady=5)
"""Задание кнопок запуска"""
tk.Button(buttons_frm, text="Запуск программы", bg="black",
             fg="red",
             command=start_handler).grid(row=1,
                                         column=1,
                                         pady=16, padx=5)

tk.Button(buttons_frm, text="Построить решение", bg="green",
          fg="black", command=draw_handler).grid(row=1,
                                                 column=0,
                                                 pady=16, padx=5)

tk.Button(buttons_frm, text="Следующая итерация", bg="purple",
          fg="blue", command=iteration_handler).grid(row=1,
                                                     column=2,
                                                     pady=16, padx=5)

tk.Button(buttons_frm, text="Построить область притяжения", bg="gray",
          fg="blue", command=draw_area_handler).grid(row=2,
                                                     column=0, columnspan=3,
                                                     pady=16, padx=5)


info_frm = tk.Frame(root, bg="#FFFFFF")
info_frm.pack(pady=5)
"""Количество ячеек"""
tk.Label(info_frm, text="Количество ячеек на рисунке", bg="#FFFFFF").grid(row=0,
                                                                          column=0,
                                                                          sticky=tk.E,
                                                                          columnspan=2,
                                                                          padx=4, pady=4)
cell_count_entry = tk.Entry(info_frm, width=15, bg="#FFFFFF")
cell_count_entry.config(state='readonly')
cell_count_entry.grid(row=0, column=2,
                      sticky=tk.W,
                      columnspan=2,
                      padx=4, pady=4)

"""Затраченное время"""
tk.Label(info_frm, text="Затраченное время (s)", bg="#FFFFFF").grid(row=1,
                                                                    column=0,
                                                                    sticky=tk.E,
                                                                    columnspan=2,
                                                                    padx=4, pady=4)
time_elapsed_entry = tk.Entry(info_frm, width=15, bg="#FFFFFF")
time_elapsed_entry.config(state='readonly')
time_elapsed_entry.grid(row=1,
                        column=2,
                        columnspan=2,
                        sticky=tk.W,
                        padx=4, pady=4)

image_frm = tk.Frame(root, bg="#FFFFFF")
image_frm.pack(pady=5)

root.mainloop()

if os.path.exists('sys.out'):
    os.remove('sys.out')
if os.path.exists('tmpgraph'):
    os.remove('tmpgraph')
if os.path.exists('time.out'):
    os.remove('time.out')
if os.path.exists('buf'):
    os.remove('buf')
    # messagebox.showinfo('Temp deletion error',
                            # "Try of deletion temp files finished unsuccessfully. Exiting...")
    # print("Try to delete temp files finished unsuccessfully. Exiting...")
