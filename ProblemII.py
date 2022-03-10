import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
from matplotlib.figure import Figure
from tkinter import *
import matplotlib.patches as patches
import matplotlib
matplotlib.use("TkAgg")
#from matplotlib.figure import Figureb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Drunk():
    def __init__(self, d, h, mu, v):
        self.x = 0
        self.y = 0
        self.xpos = []
        self.ypos = []
        self.d = d
        self.h = h
        self.mu = mu
        self.v = v
        self.t = 0
        self.cars_l = []
        self.cars_r = []
        self.dt = 1

    def move_x(self, a, x0=0):
        y = np.random.normal(0, 1) * np.sqrt(self.h)
        u = np.random.uniform(0, 1)
        m = (y + np.sqrt(y ** 2 - 2 * self.h * np.log(u))) / 2
        x = max(m - y, x0 + self.mu * self.h - y) + self.v * self.dt
        if x < a:
            x = a + abs(x - a)
        return x

    def move_y(self, a, b, x0=0):
        y = np.random.normal(0, 1) * np.sqrt(self.h)
        u = np.random.uniform(0, 1)
        m = (y + np.sqrt(y ** 2 - 2 * self.h * np.log(u))) / 2
        x = max(m - y, x0 + self.mu * self.h - y)
        if x < a:
            x = a + abs(x - a)
        elif x > b:
            x = b - abs(x - b)
        return x


    def car_time(self, N, t=0):
        u = np.random.uniform(0, 1)
        t = t - 1 / N * np.log(u)
        return t

    def speed_check(self, v):
        for car in self.cars_l + self.cars_r:
            if car.v <= v:
                v = car.v
        return v

    def cars_coming(self):
        dead = False
        N = np.random.exponential(3)
        M = np.random.exponential(3)
        left_t = self.car_time(N, self.t)
        right_t = self.car_time(M, self.t)
        while self.x < 1000 and not dead:
            self.x = self.move_x(0, self.x)
            self.y = self.move_y(0, 50, self.y)
            self.t += self.dt
            self.xpos.append(self.x)
            self.ypos.append(self.y)
            v = np.random.uniform(20, 30)
            v = self.speed_check(v)
            if left_t <= self.t:
                self.cars_l.append(CarLeft(self.d, self.t, v))
                left_t = self.car_time(N, left_t)
            if right_t <= self.t:
                self.cars_r.append(CarRight(self.d, self.t, v))
                right_t = self.car_time(M, right_t)
            dead = self.call_gravedigger()
            if dead:
                v = 1
            else:
                v = 0
        #return v
        return self.xpos, self.ypos, self.cars_l, self.cars_r, dead

    def call_gravedigger(self):
        for car in self.cars_l:
            car.update(self.t)
            if car.x1 <= self.x <= car.x2 and car.y1 <= self.y <= car.y2:
                return True
        for car in self.cars_r:
            car.update(self.t)
            if car.x1 <= self.x <= car.x2 and car.y1 <= self.y <= car.y2:
                return True
        return False


class CarLeft():
    def __init__(self, d, t, v):
        self.x1 = 0
        self.x2 = 10
        self.y1 = (25 + d / 2) - 2.5
        self.y2 = (25 + d / 2) + 2.5
        self.t = t
        self.v = v
        self.pos = []
        self.start = t

    def update(self, t):
        self.pos.append(self.x1)
        t = t - self.t
        self.t = t
        self.x1 = self.x1 + self.v * t
        self.x2 = self.x1 + 10


class CarRight():
    def __init__(self, d, t, v):
        self.x1 = 1000 - 10
        self.x2 = 1000
        self.y1 = (25 - d / 2) - 2.5
        self.y2 = (25 - d / 2) + 2.5
        self.t = t
        self.v = v
        self.pos = []
        self.start = t

    def update(self, t):
        self.pos.append(self.x1)
        t = t - self.t
        self.t = t
        self.x1 = self.x1 - self.v * t
        self.x2 = self.x1 + 10


class FunctionPlt(Frame):  # klasa dziedzicząca metody klasy Frame
    """Klasa do rysowania wykresów podanej przez użytkownika funkcji"""

    # funkcja potrzebna do przycisku quit
    def quit(self):
        """Funkcja kończąca działanie programu"""
        import sys;
        sys.exit()

    # tworzenie okienka
    def __init__(self, master):
        """Funkcja, w której tworzone jest okno z potrzebnymi przyciskami, polami oraz płótnem na wykres"""
        master.title("Drunk man")
        master.geometry('1300x600+40+40')

        self.v = DoubleVar()
        self.d = DoubleVar()
        self.save = IntVar()

        # wprowadzanie parametrów
        Label(master, text='Speed (0.5 < v < 2):').grid(row=3, column=0)
        v = Entry(master, width=10, textvariable=self.v)
        v.grid(row=3, column=1)

        Label(master, text='Parameter d (5 <= d <= 15):').grid(row=4, column=0)
        d = Entry(master, width=10, textvariable=self.d)
        d.grid(row=4, column=1)

        # zapisanie animacji
        c = Checkbutton(master, text='save animation', variable=self.save, onvalue=1, offvalue=0)
        c.grid(row=9, column=0, pady=10)

        # płótno na wykres
        self.figure = Figure(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master)
        self.canvas.get_tk_widget().grid(row=1, column=8, columnspan=14, rowspan=14)

        # przycisk uruchamiający rysowanie i przycisk kończący program
        draw_button = Button(master, text="Create simulation", width=30, height=2, command=lambda: self.plot())
        draw_button.grid(row=9, column=1, columnspan=3)

        quit_button = Button(master, text='Quit', width=30, height=2, command=lambda: self.quit())
        quit_button.grid(row=10, column=1, columnspan=3)

        # miejsce na ewentualne błędy
        self.text = StringVar()
        Label(master, textvariable=self.text).grid(row=11, column=0, columnspan=5, rowspan=2)

    # def get_param(self):
    #     """Funkcja zwracająca zakresy osi"""
    #     v = self.v.get()
    #     d = self.d.get()
    #     return v, d
    def check_d(self, n, N):
        ds = np.linspace(5, 15, n)
        xs = list(ds)
        for i in range(len(ds)):
            c = 0
            for j in range(N):
                p = Drunk(ds[i], 1, -1, 1)
                dead = p.cars_coming()[4]
                print(dead)
                if str(dead) == 'True':
                    c += 1
            xs[i] = 1 - c/N
        plt.plot(ds, xs)
        plt.title('Wykres zależności od d')
        plt.xlabel('d')
        plt.ylabel('P')
        plt.savefig('pijak_d.png')

    def plot(self):
        self.figure.clear()
        try:
            pijak = Drunk(self.d.get(), 1, 0, self.v.get())
            xs, ys, cars_l, cars_r, dead = pijak.cars_coming()
            #self.check_d(20, 30)
            print(dead)
            cars = cars_l + cars_r
            ax = self.figure.add_subplot(111)
            ax.set_xlim(0, 1000)
            ax.set_ylim(0, 50)
            x_data = []
            y_data = []

            line = ax.plot(1000, 50)
            rect = [patches.Rectangle((0, 0), 0, 0, fc='y') for _ in range(len(cars))]
            patches1 = line + rect

            def init():
                # for l in line:
                #     l.set_data([], [])
                for r in rect:
                    ax.add_patch(r)
                return patches1

            def animation_frame(i):
                for k in range(len(rect)):
                    r = rect[k]
                    c = cars[k]
                    c_pos = c.pos
                    c_pos = [i for i in c_pos if i <= 1000]
                    zeros = [0 for _ in range(len(xs) - len(c_pos))]
                    c_pos = c_pos + zeros
                    if cars[k].start <= i/100:
                        r.set_width(10)
                        r.set_height(5)
                        r.set_xy([c_pos[i-int(cars[k].start*100)], c.y1])
                #patch._angle = -np.rad2deg(yaw[i])
                for l in line:
                    x_data.append(xs[i])
                    y_data.append(ys[i])
                    l.set_xdata(x_data)
                    l.set_ydata(y_data)

                return patches1

            self.figure = FuncAnimation(self.figure, func=animation_frame, init_func=init, frames=len(xs), interval=5)
            self.canvas.draw()
            print(xs)
            print(ys)
            for car in cars_l + cars_r:
                print(car.pos)
                print(car.t)
            self.text.set(dead)
            if self.save.get() == 1:
                f = r"C:\Users\User\Desktop\semestr_4\symulacje\pijak\animation.gif"
                writergif = PillowWriter(fps=30)
                self.figure.save('animation.gif', writer=writergif)
        except Exception as e:
            self.text.set(e)

if __name__ == '__main__':
    root = Tk()
    apl = FunctionPlt(root)
    root.mainloop()