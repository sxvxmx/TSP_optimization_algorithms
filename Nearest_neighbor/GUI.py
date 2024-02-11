import tkinter as tk
import tkinter.ttk as ttk
import networkx as nx
import random

class Window():
    def __init__(self, method, start_point:int = 0,) -> None:
        self.graph = nx.Graph()
        self.startp = start_point
        self.method = method
        self.root = tk.Tk()
        self.way = None
        self.root.title("Near_neighbor")
        self.__active_node = None
        self.waylen = -1
    
    def create_input_graph(self):
        window = self.root
        label = tk.LabelFrame(window,text="graph input")
        self.gicanvas = tk.Canvas(label, width=500, height=500)
        self.gicanvas.pack()
        self.gicanvas.bind("<Button-1>", self.__onclick)
        label.grid(column=1,row=0,rowspan=5)
    
    def create_output_graph(self):
        window = self.root
        label = tk.LabelFrame(window,text="graph output")
        self.gocanvas = tk.Canvas(label, width=500, height=500)
        self.gocanvas.pack()
        label.grid(column=2,row=0,rowspan=5)
    
    def __draw_edge(self,canvas, point1:tuple, point2:tuple):
        canvas.create_line(point1[0],point1[1],point2[0],point2[1],width=2)

    def __onclick(self,event):
        x = event.x
        y = event.y
        node = self.__merge_point(x,y)
        if node == None:
            self.__create_node(x,y,len(self.graph.nodes()))
            for node in self.graph.nodes():
                if node != self.__active_node:
                    self.graph.add_weighted_edges_from([(self.__active_node, node, random.randint(1,10))])
                    self.__draw_edge(self.gicanvas,self.__active_node, node)
                self.gicanvas.create_oval(node[0]-10, node[1]-10, node[0]+10, node[1]+10, fill="white")
                self.gicanvas.create_text(node[0], node[1], text=str(node[2]))
            self.__table_ins()
            if len(self.graph.nodes()) > 2:
                self.__draw_way_graph()
        # else:
        #     self.__draw_edge(self.__active_node, node, 1)
        #     self.graph.add_weighted_edges_from([(self.__active_node, node, random.randint(1,10))])

    def __draw_way_graph(self):
        self.gocanvas.delete("all")
        if type(self.startp) != type(list(self.graph.nodes())[0]):
            self.startp = list(self.graph.nodes())[self.startp]
        way, self.waylen = self.method(self.graph)
        self.way = way
        point = list(way)[0]
        for cnode in way:
            if cnode != point:
                self.__draw_edge(self.gocanvas,point,cnode)
                # self.waylen += self.graph[cnode][point]["weight"]
                point = cnode
        for node in way:
            self.gocanvas.create_oval(node[0]-10, node[1]-10, node[0]+10, node[1]+10, fill="white")
            self.gocanvas.create_text(node[0], node[1], text=str(node[2]))
        self.textvar.set(f"{list(map(lambda q: q[2],way))} \nдлина {self.waylen}")     


    def __merge_point(self, x, y):
        for point in list(self.graph.nodes()):
            if abs(point[0] - x) <= 10 and abs(point[1] - y) <= 10:
                return point
        return None
    
    def __create_node(self, x, y ,num):
            self.graph.add_node((x, y ,num))
            self.__active_node = (x, y ,num)
            self.gicanvas.create_oval(x-10, y-10, x+10, y+10, fill="white")
            self.gicanvas.create_text(x, y, text=str(num))

    def __tablebuild(self):
        frame3 = ttk.LabelFrame(self.root,text="Таблица")
        frame3.grid(column=3,row=0,rowspan=3)
        self.table = ttk.Treeview(frame3,columns=("node1","node2","weight"),show="headings",height=20)
        self.table.heading("node1",text="вершина1")
        self.table.heading("node2",text="вершина2")
        self.table.heading("weight",text="вес")
        self.table.column("node1",width=50)
        self.table.column("node2",width=100)
        self.table.column("weight",width=100)
        scrollbar = ttk.Scrollbar(frame3,orient="vertical", command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.table.grid(row=0,column=0) 
    
    def __table_ins(self):
        self.table.delete(*self.table.get_children())
        for node in self.graph.nodes():
            for con in self.graph[node]:
                self.table.insert("","end",values=[node[2], con[2] ,self.graph[node][con]["weight"]])

    def __draw_param(self):
        frame = ttk.LabelFrame(self.root,text="Управление:",height=7)
        self.in1 = tk.Entry(frame,width=5)
        self.in2 = tk.Entry(frame,width=5)
        self.in3 = tk.Entry(frame,width=5)
        self.in1.grid(column=0,row=0)
        self.in2.grid(column=1,row=0)
        self.in3.grid(column=2,row=0)

        bt = tk.Button(frame, text="update weight", command= self.__set_weight)
        bt.grid(column=0,row=1,columnspan=3)
        frame.grid(column=0,row=0,sticky="n")

    def __set_weight(self):
        n1 = list(self.graph.nodes())[int(self.in1.get())]
        n2 = list(self.graph.nodes())[int(self.in2.get())]
        self.graph[n1][n2]["weight"] = int(self.in3.get())
        self.__table_ins()
        self.__draw_way_graph()
    
    def __draw_output(self):
        frame = ttk.LabelFrame(self.root,text="Вывод:")
        frame.grid(column=0,row=1,sticky="we")
        self.textvar = tk.StringVar(value=f"{self.way} \nдлина {self.waylen}")
        text_out = tk.Label(frame, height=4, textvariable=self.textvar)
        text_out.grid()
        

    def run(self):
        self.create_input_graph()
        self.create_output_graph()
        self.__draw_param()
        self.__draw_output()
        self.__tablebuild()
        tk.mainloop()