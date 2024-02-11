import genetic
import GUI

def f(x1:int, x2:int) -> int:
    return 2*pow(x1,3) + 4*x1*pow(x2,3) - 10*x1*x2 + pow(x2,2)

if __name__ == '__main__':
    g = genetic.Gen(f,[-50,100],10)
    gui = GUI.Window(g)
    gui.start()