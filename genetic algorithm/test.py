import tkinter as tk
from tkinter import ttk
from math import sqrt

class GraphGUI(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Graph")
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack()
        self.nodes = []
        self.canvas.bind("<Button-1>", self.add_node)
        self.threshold_dist = 10

    def add_node(self, event):
        x, y = event.x, event.y
        merged_node = self.try_merge_nodes(x, y)
        if merged_node:
            x, y = merged_node
        else:
            self.nodes.append((x, y))
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='black')
        self.connect_nodes(x, y)

    def connect_nodes(self, x, y):
        if self.nodes:
            p1 = self.nodes[-1]
            self.canvas.create_line(p1[0], p1[1], x, y, fill='black')

    def try_merge_nodes(self, x, y):
        for node_x, node_y in self.nodes:
            if self.distance((x, y), (node_x, node_y)) <= self.threshold_dist:
                return node_x, node_y
        return None

    def distance(self, p1, p2):
        return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.graph = GraphGUI(self)
        self.graph.pack(expand=True, fill="both")

def main():
    root = tk.Tk()
    app = MainFrame(root)
    app.pack(expand=True, fill="both")
    root.mainloop()

if __name__ == "__main__":
    main()
