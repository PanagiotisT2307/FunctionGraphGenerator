import tkinter as tk
from tkinter import *
from math import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import messagebox
from PIL import Image, ImageTk


class Application:
    def __init__(self, root):
        self.window = root
        self.window.title("Function Graph Generator")
        self.window.minsize(500, 450)

        self.programTitle = tk.Label(self.window, text="Function Graph Generator", font=20, pady=10).pack()
        
        self.graphInputs = tk.Frame(self.window, pady=30, padx=40)
        self.graphInputs.pack()
        
        self.funcLabel = tk.Label(self.graphInputs, text="*f(x)=", pady=5, font=10).grid(row=0, column=0)
        self.funcInput = tk.Entry(self.graphInputs)
        self.funcInput.grid(row=0, column=1)

        self.startLabel = tk.Label(self.graphInputs, text="*Start:", pady=5, font=10).grid(row=1, column=0)
        self.startInput = tk.Entry(self.graphInputs)
        self.startInput.grid(row=1, column=1)

        self.finishLabel = tk.Label(self.graphInputs, text="*Finish:", pady=5, font=10).grid(row=2, column=0)
        self.finishInput = tk.Entry(self.graphInputs)
        self.finishInput.grid(row=2, column=1)

        self.stepLabel = tk.Label(self.graphInputs, text="Step:", pady=5, font=10).grid(row=3, column=0)
        self.stepInput = tk.Entry(self.graphInputs)
        self.stepInput.grid(row=3, column=1)

        self.xAxisLabel = tk.Label(self.graphInputs, text="X-Axis Label:", pady=5, font=10).grid(row=4, column=0)
        self.xAxisInput = tk.Entry(self.graphInputs)
        self.xAxisInput.grid(row=4, column=1)

        self.yAxisLabel = tk.Label(self.graphInputs, text="Y-Axis Label:", pady=5, font=10).grid(row=5, column=0)
        self.yAxisInput = tk.Entry(self.graphInputs)
        self.yAxisInput.grid(row=5, column=1)

        self.showgrid = IntVar()
        self.showGridLabel = tk.Label(self.graphInputs, text="Show Grid: ", pady=5, font=10).grid(row=6, column=0)
        self.showGridInput = tk.Checkbutton(self.graphInputs, text="Enable", font=10, variable=self.showgrid)
        self.showGridInput.grid(row=6, column=1)

        self.important = tk.Label(self.window, text="Everything that have * is important", fg="red", font=10).pack()

        self.operations = tk.Button(
                                    self.window,
                                    text="Show Operations",
                                    bg="blue",
                                    fg="white",
                                    font=30,
                                    command=lambda: self.showOperations()
                                )
        self.operations.pack(side="bottom", fill="x")
        
        self.showGraph = tk.Button(
                                    self.window,
                                    text="Generate Graph",
                                    bg="green",
                                    fg="white",
                                    font=30,
                                    command=lambda: self.generateGraph()
                                )
        self.showGraph.pack(side="bottom", fill="x")

    def showOperations(self):
        operations = open("operations.txt", "r")
        opWindow = tk.Toplevel(self.window)
        
        operationsText = tk.Text(opWindow)
        
        scrollbar = tk.Scrollbar(opWindow, command=operationsText.yview)
        scrollbar.pack(side='right', fill='y')
        scrollbar.config(command=operationsText.yview)
        
        operationsText.config(yscrollcommand=scrollbar.set)
        operationsText.pack(side="left")
        
        for opText in operations:
            operationsText.insert(tk.END, opText)
            
        operationsText.config(state='disabled')
        operations.close()

    def generateGraph(self):
        function = self.funcInput.get()
        start = self.startInput.get()
        finish = self.finishInput.get()
        if function == "" or start == "" or finish == "":
            messagebox.showwarning("Error", "Please fill the important fields!")
        else:
            self.calculateAndPlot(function, start, finish)

    def calculateAndPlot(self, funcTitle, start, finish):
        function = []
        for ch in funcTitle:
            if ch == "^":
                function.append("**")
            else:
                function.append(ch)

        try:
            x = 1
            function = "".join(function)
            eval(function)
            correctFunc = True
        except:
            correctFunc = False
        try:
            start = int(start)
            finish = int(finish)
            correctStartFinish = True
        except:
            correctStartFinish = False
        try:
            step = int(self.stepInput.get())
        except:
            step = 1
        xAxisLabel = self.xAxisInput.get()
        yAxisLabel = self.yAxisInput.get()

        xValues = []
        yValues = []

        if not(correctFunc) and correctStartFinish:
            messagebox.showerror("Error", "Function is not valid!")
        elif correctFunc and not(correctStartFinish):
            messagebox.showerror("Error", "Start and/or finish values are not valid!")
        elif not(correctFunc) and not(correctStartFinish):
            messagebox.showerror("Error", "All important fields are not valid!")
        else:
            for x in range(start, (finish+1), step):
                xValues.append(eval(function))
                yValues.append(x)

            

            plt.plot(yValues, xValues)
            print(self.showgrid.get())
            if self.showgrid.get() == 1:
                plt.grid(True)
            else:
                plt.grid(False)
            plt.title(funcTitle)
            plt.xlabel(xAxisLabel)
            plt.ylabel(yAxisLabel)
            plt.show()

        
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
