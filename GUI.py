import time
import tkinter as tk


class TrafficLights:

    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Traffic Light")

        frame = tk.Frame(self.window)
        frame.pack()

        self.color = tk.StringVar()
        radio_red = tk.Radiobutton(frame, text="Red", bg="red", variable=self.color, value="R", command=self.radiobutton_resettime)
        radio_red.grid(row=1, column=1)

        radio_yellow = tk.Radiobutton(frame, text="Yellow", bg="yellow", variable=self.color, value="Y", command=self.radiobutton_resettime)               
        radio_yellow.grid(row = 1, column = 2)

        radio_green = tk.Radiobutton(frame, text="Green", bg="green", variable=self.color, value="G", command=self.radiobutton_resettime)
        radio_green.grid(row = 1, column = 3)

        self.canvas = tk.Canvas(self.window, width=450, height=250, bg="skyblue")
        self.canvas.pack()
        self.titele=self.canvas.create_text(220, 50, text="Pedestrain signal",font=('Times',15),fill='red')
        self.oval_red = self.canvas.create_oval(60, 90, 160, 190, fill="white" ,width=2)
        self.oval_yellow = self.canvas.create_oval(170, 90, 270, 190, fill="white",width=2)
        self.oval_green = self.canvas.create_oval(280, 90, 380, 190, fill="white",width=2)

        self.color.set('G')
        self.canvas.itemconfig(self.oval_green, fill="green")
        self.counter = 8
        self.raidocounter = 8
        self.film_signal= "FALSE"
        self.addgseconds="FALSE"
        self.click_radiobutton="FALSE"
        self.button_label = tk.StringVar()
        self.button_label.set(self.counter)
        clockbutton=tk.Button(self.window, textvariable=self.button_label,  height = 5, 
        width = 10,).pack(padx=50, pady=10, side= tk.LEFT)
        #clockbutton.grid(row=0, column=0)
        alertbutton=tk.Button(self.window, text="alert",command=self.up_Gseconds, height = 5, 
        width = 10).pack(padx=50, pady=10, side= tk.RIGHT)
        #alertbutton.grid(row=0, column=1)
        self.button_countdown(self.counter, self.button_label) #一開始直接倒數
        
        #  mainloop，是一個要電腦在使用者關閉視窗之前持續偵測視窗並處理事件的語法。
        self.window.mainloop()

    def on_RadioChange(self):
        color = self.color.get()

        if color == 'R':
            self.canvas.itemconfig(self.oval_red, fill="red")
            self.canvas.itemconfig(self.oval_yellow, fill="white")
            self.canvas.itemconfig(self.oval_green, fill="white")    
        elif color == 'Y':
            self.canvas.itemconfig(self.oval_red, fill="white")
            self.canvas.itemconfig(self.oval_yellow, fill="yellow")
            self.canvas.itemconfig(self.oval_green, fill="white")
        elif color == 'G':
            self.canvas.itemconfig(self.oval_red, fill="white")
            self.canvas.itemconfig(self.oval_yellow, fill="white")
            self.canvas.itemconfig(self.oval_green, fill="green")
    #倒數時間
    def button_countdown(self,i, label):
        
        if i >= 0:
            
            with open('film.txt', 'r')as f:
                signal=f.readlines() 
                if signal[0]=='YES' and self.film_signal=="FALSE": 
                    self.film_signal="TRUE"
                    print(signal)
                    self.up_Gseconds()
			#$with open('film.txt', 'w')as f:
				#	if self.film_signal=="TRUE":
				#		f.wirte("NO")
                

            label.set(i)
            if self.click_radiobutton=="TRUE":
                self.click_radiobutton="FALSE"
                self.button_countdown(self.raidocounter, self.button_label)    
            elif self.addgseconds=="TRUE":
               # label.set(i+5)
                self.addgseconds="FALSE"
                self.button_countdown(i+5, label)
            else:
                self.window.after(1000, lambda: self.button_countdown(i, label))
            i -= 1
        else:
            self.restart()

    #更換燈號重新倒數

    def restart(self):
        #light=['R','Y','G']
        if self.color.get()=="R":
            self.counter=8
            selctcolor="G"
        elif self.color.get()=="G":
            self.counter=1
            selctcolor="Y" 
        elif self.color.get()=="Y":
            self.counter=2
            selctcolor="R"     
        #selctcolor=choice(light)
        self.color.set(selctcolor)
        self.on_RadioChange()
        self.button_countdown(self.counter, self.button_label)
   #馬路上有老人,綠燈剩餘時間也剩5秒以下,增加綠燈秒數
    def up_Gseconds(self):
        if self.color.get()=="G":
            self.addgseconds="TRUE"
    #reset到各自燈號的秒數
    def radiobutton_resettime(self):
         self.click_radiobutton="TRUE"
         if self.color.get()=="G":
            self.raidocounter=8          
         if self.color.get()=="Y":
            self.raidocounter=1           
         if self.color.get()=="R":
            self.raidocounter=2           
         self.on_RadioChange()
    # invoke()	相当于按动按钮
    
   
TrafficLights()
