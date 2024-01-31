from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import CRM_drawer as crm
import os, time

if os.getcwd().endswith("my_osip"):
    os.chdir("9")


DELETE_FLAG = True      # Flag of deleting images and result file after program working 

def timer(k:int):
    start = time.time()
    if time.time() - start > k:
        raise TimeoutError


def add_new_line(x: str, n_line:int = 30):
    with open("main.cpp") as fd:
        file = fd.readlines()
    if ';' in x:
        x.replace(';', '')
    x = f"{x};\n"
    if file[n_line].strip() != x.strip():
        del file[n_line]
        file.insert(n_line, x)
        with open("main.cpp", "w") as fd:
            fd.writelines(file)


def insert_info_into_entry(entr:Entry, info:str):
    entr.config(state='normal')
    entr.delete(0, END)
    entr.insert(END, info)
    entr.config(state='readonly')


def start_handler():
    try:
        a = eval(a_param_ctch.get())
        b = eval(b_param_ctch.get())
        x_l = eval(x0_ctch.get())
        x_r = eval(x1_ctch.get())
        y_t = eval(y1_ctch.get())
        y_l = eval(y0_ctch.get())
        L = abs(x_r - x_l)
        H = abs(y_t - y_l)
        iter_num = int(combo.get())
        myfunc = opt_func.get()
        add_new_line(f"    return {myfunc}")
        print("Compiling: ")
        os.system("g++ main.cpp")
        print("Starting: ")
        os.system(f"./a.out {x_l} {y_t} {L} {H} {a} {b} {iter_num}")
        res = []
        with open("res.txt", "r") as fd:
            for line in fd:
                if line.startswith("comp"):
                    res.append(line)
            h, ctr, num_cells, comps, elapsed = map(float, line.split())
        component_txt = Text(image_frame, height=12, width=37)
        component_txt.insert(END, "".join(res))
        component_txt.grid(row=1, column=0)
        insert_info_into_entry(h_entry, str(h))
        insert_info_into_entry(time_elapsed_entry, str(elapsed))
        insert_info_into_entry(cells_entry, f"{int(ctr)}/{int(num_cells)}")
        insert_info_into_entry(comps_entry, str(int(comps)))

    except SyntaxError:
        messagebox.showinfo('Ошибка SyntaxError',
                            "Вы не ввели необходимые параметры или передали их неверно.")
    except ValueError:
        messagebox.showinfo('Ошибка ValueError',
                            "Вы ввели необходимые параметры неверно.")


def draw_handler():
    a = eval(a_param_ctch.get())
    b = eval(b_param_ctch.get())
    x_l = eval(x0_ctch.get())
    x_r = eval(x1_ctch.get())
    y_t = eval(y1_ctch.get())
    y_l = eval(y0_ctch.get())
    iterc = int(combo.get())
    try:
        h = eval(h_entry.get())
    except SyntaxError:
        messagebox.showinfo('Ошибка SyntaxError',
                            "Не найдено значение размера ячейки, запустите программу перед построением ЦРМ")
    crm.main(x_l, x_r, y_l, y_t, h, iterc, a, b)
    img = Image.open(f"CRM{iterc}.png").resize((350, 350))
    img_shower = Label(image_frame)
    img_tk = ImageTk.PhotoImage(img)
    img_shower.image = img_tk
    img_shower.config(image=img_tk)
    img_shower.grid(row=0, column=0)
    if DELETE_FLAG:
        os.remove(f"CRM{iterc}.png")


def iteration_handler():
    iter_num = int(combo.get()) + 1
    combo.delete(0, END)
    combo.insert(END, str(iter_num))
    start_handler()
    draw_handler()


root = Tk()
root.config(bg="#FFFFFF")
# root.geometry("600x450")
root.title("Вычислительная задача 9")
for i in range(12):
    root.columnconfigure(i, pad=20)
    root.rowconfigure(i, pad=20)

"""Отображение оглавления"""
Label(root,
      text="Вычисление спектра усреднения функции\nдля отображения Жюлия.",
      font=("Arial Bold", 12), bg="#FFFFFF").grid(row=0, column=0, columnspan=2)

"""Картинка отображения"""
img_otobrazh_shower = Label(root, bg="#FFFFFF")
img_otobr = Image.open("icons/otobrzhenie.png").resize((158, 55))
img_otobr_tk = ImageTk.PhotoImage(img_otobr)
img_otobrazh_shower.config(image=img_otobr_tk)
img_otobrazh_shower.grid(row=1, column=0, columnspan=2)

parameters_frame = Frame(root, bg="#FFFFFF")
parameters_frame.grid(row=2, column=0)
"""Ввод параметра A"""
Label(parameters_frame, text="a = ", bg="#FFFFFF").grid(row=0,
                                                        column=0,
                                                        sticky=E)
a_param_ctch = Entry(parameters_frame, width=7)
a_param_ctch.insert(END, '0.0')
a_param_ctch.grid(row=0, column=1, sticky=W)

"""Ввод параметра B"""
Label(parameters_frame, text="b = ", bg="#FFFFFF").grid(row=0,
                                                        column=2,
                                                        sticky=E)
b_param_ctch = Entry(parameters_frame, width=7)
b_param_ctch.insert(END, '-0.6')
b_param_ctch.grid(row=0,
                  column=3,
                  sticky=W)

"""Текст координат"""
Label(parameters_frame, text="Координаты изначальной области",
      font=("Arial Bold", 10), bg="#FFFFFF").grid(row=1, column=0, 
                                                  columnspan=4, pady=8)

"""Ввод координат"""
# x coords
Label(parameters_frame, text="x0 ", bg="#FFFFFF").grid(row=2,
                                                       column=0,
                                                       sticky=E)
x0_ctch = Entry(parameters_frame, width=7)
x0_ctch.insert(END, '-2')
x0_ctch.grid(row=2, column=1, sticky=W)

Label(parameters_frame, text="x1 ", bg="#FFFFFF").grid(row=2,
                                                       column=2,
                                                       sticky=E)
x1_ctch = Entry(parameters_frame, width=7)
x1_ctch.insert(END, '2')
x1_ctch.grid(row=2, column=3, sticky=W)

# y coords
Label(parameters_frame, text="y0 ", bg="#FFFFFF").grid(row=3,
                                                       column=0,
                                                       sticky=E)  
y0_ctch = Entry(parameters_frame, width=7)
y0_ctch.insert(END, '-2')
y0_ctch.grid(row=3,
             column=1,
             sticky=W)

Label(parameters_frame, text="y0 ", bg="#FFFFFF").grid(row=3,
                                                       column=2,
                                                       sticky=E)
y1_ctch = Entry(parameters_frame, width=7)
y1_ctch.insert(END, '2')
y1_ctch.grid(row=3, column=3, sticky=W)

"""Выбор количества итераций"""
Label(parameters_frame, text="Количество итераций:", 
      bg="#FFFFFF").grid(row=4, column=0,
                         columnspan=2, 
                         padx=2, pady=10,
                         sticky=E)

combo = Combobox(parameters_frame, width=8)
combo['values'] = list(range(5, 13))
combo.current(2)
combo.grid(row=4, column=2, columnspan=2,
           padx=2, pady=10, sticky=W)

"""Ввод функции"""
function_frame = Frame(root)
function_frame.grid(row=3, column=0)
Label(function_frame, text="Функция оснащения").grid(row=0,
                                                     column=0,
                                                     sticky=E)
label_font = font.Font(slant="italic")
Label(function_frame, text="С(x,y):", font=label_font).grid(row=0,
                                                            column=1,
                                                            sticky=W)

opt_func = Entry(function_frame, width=25, justify="center")
opt_func.insert(END, "x*x + y*y")
opt_func.grid(row=1, column=0, columnspan=2)


btn_frame = Frame(root, bg="#FFFFFF")
btn_frame.grid(row=4, column=0)
"""Задание кнопки запуска"""
Button(btn_frame, text="Построить ЦРМ\nотображения",
       bg="green", fg="black",
       command=draw_handler).grid(row=0,
                                  column=0,
                                  pady=8, padx=3)

Button(btn_frame, text="Запуск\nпрограммы",
       bg="black", fg="red",
       command=start_handler).grid(row=0,
                                   column=1,
                                   columnspan=2,
                                   pady=8, padx=3)

Button(btn_frame, text="Следующая\nитерация",
       bg="gray", fg="blue",
       command=iteration_handler).grid(row=0,
                                       column=3,
                                       pady=8, padx=3)


info_frame = Frame(root, bg="#FFFFFF")
info_frame.grid(row=5, column=0)
"""Полученный шаг"""
Label(info_frame, text="Диаметр ячейки",
      bg="#FFFFFF").grid(row=0, column=0,
                         sticky=E,
                         columnspan=2,
                         padx=4, pady=1)
h_entry = Entry(info_frame, width=10, bg="#FFFFFF")
h_entry.config(state='readonly')
h_entry.grid(row=0, column=2,
             columnspan=2, sticky=W,
             padx=4, pady=1)

"""Затраченное время"""
Label(info_frame, text="Затраченное время (s)",
      bg="#FFFFFF").grid(row=1, column=0,
                         sticky=E,
                         columnspan=2,
                         padx=4, pady=1)
time_elapsed_entry = Entry(info_frame, width=10, bg="#FFFFFF")
time_elapsed_entry.config(state='readonly')
time_elapsed_entry.grid(row=1, column=2, 
                        columnspan=2, 
                        sticky=W, 
                        padx=4, pady=1)

"""Количество ячеек"""
Label(info_frame, text="Количество ячеек",
      bg="#FFFFFF").grid(row=2, column=0,
                         sticky=E,
                         columnspan=2,
                         padx=4, pady=1)
cells_entry = Entry(info_frame, width=20, bg="#FFFFFF")
cells_entry.config(state='readonly')
cells_entry.grid(row=2, column=2,
                 sticky=W,
                 columnspan=2,
                 padx=4, pady=1)

"""Компонент сильной связности"""
Label(info_frame, text="Компонент сильной связности",
      bg="#FFFFFF").grid(row=3,
                         column=0,
                         sticky=E,
                         columnspan=2,
                         padx=4, pady=1)
comps_entry = Entry(info_frame, width=10, bg="#FFFFFF")
comps_entry.config(state='readonly')
comps_entry.grid(row=3, column=2,
                 columnspan=2,
                 sticky=W,
                 padx=4, pady=1)

"""Вставка текста с компонентами и картинки ЦРМ"""
image_frame = Frame(root, bg="#FFFFFF")
image_frame.grid(row=2, column=1, rowspan=4)


root.mainloop()
if DELETE_FLAG:
    if os.path.exists("res.txt"):
        os.remove("res.txt")
    if os.path.exists("a.out"):
        os.remove("a.out")
