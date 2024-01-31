import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import chainy_recursion as crm
from PIL import Image, ImageTk
import os, time


def insert_info_into_entry(entr:Entry, info:str):
    entr.config(state='normal')
    entr.delete(0, END)
    entr.insert(END, info)
    entr.config(state='readonly')


# def julian_koef():
#     a_param_ctch.delete(0, END)
#     b_param_ctch.delete(0, END)
#     b_param_ctch.insert(END, '-0.6')

# def henon_koef():
#     a_param_ctch.delete(0, END)
#     b_param_ctch.delete(0, END)
#     a_param_ctch.insert(END, '1.4')
#     b_param_ctch.insert(END, '0.3')

# xx0, xx1, yy0, yy1, iterrr,

# def insert_txt(lbl:Label, txt:str):
#     lbl.config(state=NORMAL)
#     lbl.delete(0, END)
#     lbl.insert(END, txt)
#     lbl.config(state=DISABLED)


def start_handler():
    try:
        start = time.time()
        a = eval(a_param_ctch.get())
        b = eval(b_param_ctch.get())
        x_l = eval(x0_ctch.get())
        x_r = eval(x1_ctch.get())
        y_t = eval(y1_ctch.get())
        y_l = eval(y0_ctch.get())
        h = eval(step_ctch.get())
        iter_num = int(combo.get())
        # repres = int(selected.get())
        # insert_txt(n_cells_input, f"{int(abs(x_r - x_l) / h * abs(y_t - y_l) / h)}")
        crm.main(x_l, x_r, y_l, y_t, h, iter_num, a, b)
        elapsed = time.time() - start
        insert_info_into_entry(time_elapsed_entry, int(elapsed * 1000))
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
    is_grid = chk_state.get()
    x_l = eval(x0_ctch.get())
    x_r = eval(x1_ctch.get())
    y_t = eval(y1_ctch.get())
    y_l = eval(y0_ctch.get())
    crm.draw(x_l, x_r, y_l, y_t, is_grid)


def iteration_handler():
    a = eval(a_param_ctch.get())
    b = eval(b_param_ctch.get())
    x_l = eval(x0_ctch.get())
    x_r = eval(x1_ctch.get())
    y_t = eval(y1_ctch.get())
    y_l = eval(y0_ctch.get())
    # h = eval(step_ctch.get())
    iterc = int(combo.get()) + 1
    combo.delete(0, END)
    combo.insert(END, str(iterc))
    crm.new_iterat(x_l, x_r, y_l, y_t, a,b, iterc)


root = Tk()
root.config(bg="#FFFFFF")
# root.geometry("600x450")
root.title("Symbolic Shape Julya")
for i in range(12):
    root.columnconfigure(i, pad=20)
    root.rowconfigure(i, pad=20)

"""Отображение оглавления"""
hello_words = Label(root,
                    text="Программа для построения цепно-реккурентного множества\nотображения Жулия",
                    font=("Arial Bold", 12),
                    bg="#FFFFFF")
hello_words.grid(row=0,
                 column=0,
                 columnspan=4)

"""Картинка отображения"""
img_otobrazh_shower = Label(root, bg="#FFFFFF")
img_otobr = Image.open("otobrzhenie.png").resize((149, 51))
img_otobr_tk = ImageTk.PhotoImage(img_otobr)
img_otobrazh_shower.config(image=img_otobr_tk)
img_otobrazh_shower.grid(row=1, column=0, columnspan=6)

"""Ввод параметра A"""
a_param_txt = Label(root,
                    text="A = ",
                    bg="#FFFFFF")
a_param_txt.grid(row=2,
                 column=0,
                 sticky=E)
a_param_ctch = Entry(root,
                     width=9)
a_param_ctch.insert(END, '0.0')
a_param_ctch.grid(row=2,
                  column=1,
                  sticky=W)

"""Ввод параметра B"""
b_param_txt = Label(root,
                    text="B = ",
                    bg="#FFFFFF")
b_param_txt.grid(row=2,
                 column=2,
                 sticky=E)
b_param_ctch = Entry(root,
                     width=9)
b_param_ctch.insert(END, '-0.6')
b_param_ctch.grid(row=2,
                  column=3,
                  sticky=W)

"""Текст координат"""
coord_words = Label(root,
                    text="Координаты изначальной области",
                    font=("Arial Bold", 10),
                    bg="#FFFFFF")
coord_words.grid(row=3,
                 column=0,
                 columnspan=4)

"""Ввод координат"""
# x coords
x0_text = Label(root,
                text="x0 ",
                bg="#FFFFFF")
x0_text.grid(row=4,
             column=0,
             sticky=E)  

x0_ctch = Entry(root,
                width=9)
x0_ctch.insert(END, '-1.5')
x0_ctch.grid(row=4,
             column=1,
             sticky=W)

x1_text = Label(root,
                text="x1 ",
                bg="#FFFFFF")
x1_text.grid(row=4,
             column=2,
             sticky=E)  

x1_ctch = Entry(root,
                width=9)
x1_ctch.insert(END, '1.5')
x1_ctch.grid(row=4,
             column=3,
             sticky=W)
# y coords
y0_text = Label(root,
                text="y0 ",
                bg="#FFFFFF")
y0_text.grid(row=5,
             column=0,
             sticky=E)  

y0_ctch = Entry(root,
                width=9)
y0_ctch.insert(END, '-1.5')
y0_ctch.grid(row=5,
             column=1,
             sticky=W)

y1_text = Label(root,
                text="y0 ",
                bg="#FFFFFF")
y1_text.grid(row=5,
             column=2,
             sticky=E)  

y1_ctch = Entry(root,
                width=9)
y1_ctch.insert(END, '1.5')
y1_ctch.grid(row=5,
             column=3,
             sticky=W)

"""Ввод шага"""
step_txt = Label(root,
                 text="Шаг (h): ",
                 bg="#FFFFFF")
step_txt.grid(row=6,
              column=0,
              columnspan=2,
              sticky=E)
step_ctch = Entry(root, width=9)
step_ctch.insert(END, '0.5')
step_ctch.grid(row=6,
               column=2,
               columnspan=2,
               sticky=W)

"""Ввод количества точек внутри области"""
pnt_sqr_txt = Label(root,
                    text="Корень кол-ва точек внутри области: ",
                    bg="#FFFFFF"
                    )
pnt_sqr_txt.grid(row=7,
                 column=0,
                 columnspan=2,
                 sticky=E)

pnt_sqr_ctch = Entry(root, width=9)
pnt_sqr_ctch.insert(END, "6")
pnt_sqr_ctch.grid(row=7,
                 column=2,
                 columnspan=2,
                 sticky=W)

"""Выбор количества итераций"""
iter_num_txt = Label(root,
                        text="Количество итераций",
                        bg="#FFFFFF")
iter_num_txt.grid(row=8,
                  column=0,
                  columnspan=2,
                  sticky=E)

combo = Combobox(root)
combo['values'] = list(range(1,11))
combo.current(5)
combo.grid(row=8,
           column=2,
           columnspan=2,
           sticky=W)

# """Выбор предпочитаемого отображения"""
# rad_txt = Label(root,
#                 text="Выберите отображение",
#                 bg="#FFFFFF")
# rad_txt.grid(row=8,
#              column=0,
#              columnspan=4)

# selected = IntVar()
# # rad1 = Radiobutton(root, text='Хенона', value=0, variable=selected, command=henon_koef)  
# rad2 = Radiobutton(root, text='Жюлия', value=1, variable=selected, command=julian_koef)
# # rad1.grid(row=9,
# #           column=0,
# #           columnspan=2)
# rad2.grid(row=9,
#           column=0,
#           columnspan=4)

"""Выбор вывода сетки на координатной плоскости"""
chk_state = BooleanVar()
chk_state.set(False)  # задайте проверку состояния чекбокса  
chk = Checkbutton(root,
                  text='Показывать координатную сетку',
                  var=chk_state,
                  bg="#FFFFFF")
chk.grid(row=9,
         column=0,
         sticky=W,
         columnspan=2)

"""Задание кнопки запуска"""
btn = Button(root,
             text="Запуск программы",
             bg="black",
             fg="red",
             command=start_handler)
# btn.pack()
btn.grid(row=10,
         column=1,
         columnspan=2,
         pady=16)

draw_btn = Button(root,
             text="Построить решение",
             bg="green",
             fg="black",
             command=draw_handler)
draw_btn.grid(row=10,
         column=0,
        #  columnspan=4,
         pady=16)

iter_btn = Button(root,
             text="Следующая итерация",
             bg="purple",
             fg="blue",
             command=iteration_handler)
iter_btn.grid(row=10,
         column=3,
        #  columnspan=4,
         pady=16)

# n_cells_txt = Label(root,
#                 text="Количество ячеек: ",
#                 bg="#FFFFFF")
# n_cells_txt.grid(row=12,
#              column=0,
#              columnspan=2,
#              pady=10,
#              sticky=E)

# n_cells_input = Entry(root,
#                       width=16)
# n_cells_input.config(state=DISABLED)
# n_cells_input.grid(row=12,
#                    column=2,
#                    columnspan=2,
#                    pady=10,
#                    sticky=W)


"""Затраченное время"""
time_elapsed_txt = Label(root, 
                            text="Затраченное время (ms)", 
                            bg="#FFFFFF")
time_elapsed_txt.grid(row=11, 
                      column=0, 
                      sticky=E, 
                      columnspan=2,
                      padx=4, pady=4)
time_elapsed_entry = Entry(root, width=8, bg="#FFFFFF")
time_elapsed_entry.config(state='readonly')
time_elapsed_entry.grid(row=11,
                        column=2, 
                        columnspan=2, 
                        sticky=W, 
                        padx=4, pady=4)

root.mainloop()

try:
    if not (os.path.exists('buf') or os.path.exists('buf')):
        raise FileExistsError
    os.remove("buf")
    os.remove('tmpgraph')
except FileExistsError:
    pass
except:
    messagebox.showinfo('Temp deletion error',
                            "Try to delete temp files finished unsuccessfully. Exiting...")
    # print("Try to delete temp files finished unsuccessfully. Exiting...")
