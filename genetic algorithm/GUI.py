from __future__ import annotations

import genetic
import tkinter as tr
from tkinter import ttk

class Window():
    def __init__(self, g:genetic.Gen) -> None:
        self.gen = g

        self.wind = tr.Tk()
        self.wind.title("genetic")
        self.wind.geometry("625x350")

        self.frame1 = ttk.LabelFrame(self.wind,text="Управление:")
        self.frame1.grid(column=0,row=0,sticky="we")
        self.frame2 = ttk.LabelFrame(self.wind,text="Вывод")
        self.frame2.grid(column=0,row=2,sticky="we")
        self.frame3 = ttk.LabelFrame(self.wind,text="Таблица")
        self.frame3.grid(column=1,row=0,rowspan=3)
        self.frame4 = ttk.LabelFrame(self.wind,text="Параметры")
        self.frame4.grid(column=0,row=1,sticky="we")


        self.textvar = tr.StringVar(value=f"Значение функции:\n{str(self.gen.getmin())}\nГен:\n{str(self.gen.getpoint())}")
        self.text_out = tr.Label(self.frame2, height=4, textvariable=self.textvar)
        self.text_out.grid()

        
    
    def start(self):
        self.__control()
        self.__fparams()
        self.__tablebuild()
        self.wind.mainloop()

    def __fpupulation(self) -> None:
        self.__updatepar()
        self.gen.rpopulation()
        self.__table_ins()
        self.__set_textvar1()

    def __numpupolation(self) -> None:
        self.__updatepar()
        for i in range(int(self.inp.get())):
            self.gen.npopulation()
        self.__set_textvar1()
        self.__table_ins()

    def __tablebuild(self):
        self.table = ttk.Treeview(self.frame3,columns=("num","func","population x","population y"),show="headings",height=15)
        self.table.heading("num",text="Номер")
        self.table.heading("func",text="Значение целевой функции")
        self.table.heading("population x",text="Ген 1")
        self.table.heading("population y",text="Ген 2")
        self.table.column("num",width=50)
        self.table.column("func",width=100)
        self.table.column("population x",width=100)
        self.table.column("population y",width=100)
        scrollbar = ttk.Scrollbar(self.frame3,orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.table.grid(row=0,column=0)

    def __set_textvar1(self):
        self.textvar.set(f"Значение функции:\n{str(self.gen.getmin())}\nГен:\n{str(self.gen.getpoint())}")

    def __table_ins(self):
        self.table.delete(*self.table.get_children())
        for i in range(len(self.gen.vpopulation)):
            self.table.insert("","end",values=[i+1,self.gen.vpopulation[i][0],self.gen.vpopulation[i][-1][0],self.gen.vpopulation[i][-1][-1]])

    def __control(self):
        bt1 = tr.Button(self.frame1, text="first random generation", command= self.__fpupulation)
        bt1.grid(column=0,row=0)
        self.inp = tr.Spinbox(self.frame1, from_=0, to=1000, width=5)
        self.inp.grid(column=1,row=1,sticky="e")
        bt2 = tr.Button(self.frame1, text="make population", command= self.__numpupolation)
        bt2.grid(column=0,row=1)

        self.mode = tr.IntVar()
        self.mode.set(0)
        t = tr.Label(self.frame1,text="Метод:")
        t.grid(column=0,row=2,sticky='w')
        rb1 = tr.Radiobutton(self.frame1, text="Дискретный",value=0, variable=self.mode)
        rb2 = tr.Radiobutton(self.frame1, text="Вещественный",value=1, variable=self.mode)
        rb1.grid(column=0,row=3)
        rb2.grid(column=1,row=3)

    def __fparams(self):
        tx1 = tr.Label(self.frame4,text="min значение гена")
        self.in1 = tr.Entry(self.frame4)
        self.in1.insert(0,"0")
        tx2 = tr.Label(self.frame4,text="max значение гена")
        self.in2 = tr.Entry(self.frame4)
        self.in2.insert(0,"10")
        tx3 = tr.Label(self.frame4,text="количество хромосом")
        self.in3 = tr.Entry(self.frame4)
        self.in3.insert(0,"100")
        tx4 = tr.Label(self.frame4,text="шанс мутации")
        self.in4 = tr.Entry(self.frame4)
        self.in4.insert(0,"0.4")
        tx1.grid(column=0,row=0)
        tx2.grid(column=0,row=1)
        tx3.grid(column=0,row=2)
        tx4.grid(column=0,row=3)
        self.in1.grid(column=1,row=0)
        self.in2.grid(column=1,row=1)
        self.in3.grid(column=1,row=2)
        self.in4.grid(column=1,row=3)

    def __updatepar(self):
        if self.mode.get() == 0:
            self.gen.setmode(1)
        else:
            self.gen.setmode(2)
        self.gen.setbounds([int(self.in1.get()),int(self.in2.get())])
        self.gen.setpsize(int(self.in3.get()))
        self.gen.setmchance(float(self.in4.get()))
