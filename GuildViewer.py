"""Copyright 2013 ealdorj@gmail.com"""

"""This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>."""

from tkinter import Button, Frame, Tk, BOTTOM, BOTH, TOP, Scrollbar, VERTICAL, Listbox, RIDGE, LEFT, Y, END, RIGHT, Label, FLAT
from tkinter.font import Font

import re
import os

#construimos un diccionario en base a lo que hay guardado en options: Nombre:linea, Nombre:linea, ...
try:
    options = open('options.txt', 'r')
except (FileNotFoundError, IOError) as error:
    options = open('options.txt', 'w')

optionsDictionary = {}

options = open('options.txt', 'r')
for line in options:
    optionsMatch = re.match('(.*):(.*)', line)
    if optionsMatch != None:
        optionsDictionary[optionsMatch.group(1)] = optionsMatch.group(2)

#print('Antes:', optionsDictionary)

#analizar que logs hay en el directorio donde estamos. Si el nombre del log no esta en el diccionario lo añadimos y le ponemos linea 0
for (root, subs, files) in os.walk('..'):
    for name in files:
        if name.startswith('eqlog_'):
            matchLog = re.match('.*_(.*)_.*', name)
            if matchLog != None:
                if optionsDictionary.get(matchLog.group(1)) == None:
                    optionsDictionary[matchLog.group(1)] = 0
    
#print('Despues:', optionsDictionary)

class Example(Frame): 
    def __init__(self, parent):
        Frame.__init__(self, parent, background='#8080FF')   
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        self.parent.title("EQ GuildViewer 0.1")

        fontb = Font(size=12, weight='bold')

        #inicializo variables
        self.ant = None
        self.lastLine = 0
        self.name = ''

        #frame padre
        area = Frame(self)
        area.pack(side=BOTTOM, fill=BOTH, expand=1)

        areab = Frame(self)
        areab.pack(side=TOP, fill=BOTH, expand=1)

        #scroll players
        self.scrollbar2 = Scrollbar(areab, orient=VERTICAL)

        #construimos un menu con todos los nombres del diccionario y un boton
        self.refreshButton = Button(areab, text= """PARSEA!""", command=self.onRefresh, bd=2, relief="groove")
        self.listboxLogs = Listbox(areab, width=50, activestyle="none", highlightthickness=0, yscrollcommand=self.scrollbar2.set, relief=RIDGE)
        self.listboxLogs.pack(side=LEFT, fill=Y)
        self.scrollbar2.pack(side=LEFT, fill=Y)
        self.refreshButton.pack(side=LEFT, fill=BOTH, expand=1)

        for player in optionsDictionary:
            self.listboxLogs.insert(END, player)

        #scroll
        self.scrollbar = Scrollbar(area, orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        #area1
        area1 = Frame(area)
        area1.pack(side=LEFT, fill=Y)
        
        lbl = Label(area1, text='Name')
        self.listbox = Listbox(area1, yscrollcommand=self.scrollbar.set, font=fontb, relief=FLAT, highlightthickness=0, activestyle='none')
        lbl.pack(side=TOP)
        self.listbox.pack(side=BOTTOM, fill=Y, expand=1)

        #area2
        area2 = Frame(area)
        area2.pack(side=LEFT, fill=Y)
        
        lbl2 = Label(area2, text='Level')
        self.listbox2 = Listbox(area2, yscrollcommand=self.scrollbar.set, font=fontb, relief=FLAT, highlightthickness=0, activestyle='none')
        lbl2.pack(side=TOP)
        self.listbox2.pack(side=BOTTOM, fill=Y, expand=1)

        #area3
        area3 = Frame(area)
        area3.pack(side=LEFT, fill=Y)
        
        lbl3 = Label(area3, text='Class')
        self.listbox3 = Listbox(area3, yscrollcommand=self.scrollbar.set, font=fontb, relief=FLAT, highlightthickness=0, activestyle='none')
        lbl3.pack(side=TOP)
        self.listbox3.pack(side=BOTTOM, fill=Y, expand=1)

        #area4
        area4 = Frame(area)
        area4.pack(side=LEFT, fill=Y)
        
        lbl4 = Label(area4, text='Race')
        self.listbox4 = Listbox(area4, yscrollcommand=self.scrollbar.set, font=fontb, relief=FLAT, highlightthickness=0, activestyle='none')
        lbl4.pack(side=TOP)
        self.listbox4.pack(side=BOTTOM, fill=Y, expand=1)

        #area3
        area5 = Frame(area)
        area5.pack(side=LEFT, fill=Y)
        
        lbl5 = Label(area5, text='Zone')
        self.listbox5 = Listbox(area5, yscrollcommand=self.scrollbar.set, font=fontb, relief=FLAT, highlightthickness=0, activestyle='none')
        lbl5.pack(side=TOP)
        self.listbox5.pack(side=BOTTOM, fill=Y, expand=1)

        self.pack(fill=BOTH, expand=1)

        #config-scrollbar
        self.scrollbar.config(command=self.yview)
        self.scrollbar2['command'] = self.listboxLogs.yview

        #bindeos de acciones
        self.listbox.bind("<<ListboxSelect>>", self.onSelect)
        self.listbox.bind("<MouseWheel>", self.onTest)
        self.listbox2.bind("<<ListboxSelect>>", self.onSelect)
        self.listbox2.bind("<MouseWheel>", self.onTest)
        self.listbox3.bind("<<ListboxSelect>>", self.onSelect)
        self.listbox3.bind("<MouseWheel>", self.onTest)
        self.listbox4.bind("<<ListboxSelect>>", self.onSelect)
        self.listbox4.bind("<MouseWheel>", self.onTest)
        self.listbox5.bind("<<ListboxSelect>>", self.onSelect)
        self.listbox5.bind("<MouseWheel>", self.onTest)
        self.listboxLogs.bind("<<ListboxSelect>>", self.onSelectPlayer)

    #mostrar la barra de scroll
    def yview(self, *args):
        self.listbox.yview(*args)
        self.listbox2.yview(*args)
        self.listbox3.yview(*args)
        self.listbox4.yview(*args)
        self.listbox5.yview(*args)

    #accion de la rueda del raton
    def onTest(self, val):
        return "break"

    #seleccionar un elementos de una listbox
    def onSelect(self, val):
        try:
            if self.ant != None:
                self.listbox.itemconfig(self.ant, background='#FFFFFF')
                self.listbox2.itemconfig(self.ant, background='#FFFFFF')
                self.listbox3.itemconfig(self.ant, background='#FFFFFF')
                self.listbox4.itemconfig(self.ant, background='#FFFFFF')
                self.listbox5.itemconfig(self.ant, background='#FFFFFF')
            self.listbox.itemconfig(val.widget.curselection(), background='#C0C0C0')
            self.listbox2.itemconfig(val.widget.curselection(), background='#C0C0C0')
            self.listbox3.itemconfig(val.widget.curselection(), background='#C0C0C0')
            self.listbox4.itemconfig(val.widget.curselection(), background='#C0C0C0')
            self.listbox5.itemconfig(val.widget.curselection(), background='#C0C0C0')

            self.ant=val.widget.curselection()
        except:
            None
            #print('No hay valores')

    #dependiendo de que nombre se elija en el menu cargamos en lastLine la linea de ese nombre del diccionario
    def onSelectPlayer(self, val):
        try:
            self.name = val.widget.get(val.widget.curselection())
            self.lastLine = optionsDictionary[self.name]
            #print(self.name, ' ', self.lastLine)
        except:
            None
            #print('No hay valores')

    #recorremos el fichero log al clickar sobre el boton 'Refresh!'
    def onRefresh(self):
        if self.name != '':
            yes = False
            count = 0
            dictionary = {}
            dictionaryAuxiliar = {}

            stringLog = '../eqlog_'+str(self.name)+'_project1999.txt' 
            with open(stringLog, 'r') as log:
                for i in range(int(self.lastLine)):
                    next(log)
                    count = count + 1
                for line in log:
                    match = re.match('\[.*\] \[(.*) (.*)\] (.*) \((.*)\) <.*> ZONE: (.*)', line)
                    matchRole = re.match('\[.*\] \[(.*)\] (.*) <.*>', line)
                    matchToken = re.match('\[.*\] You say, \'t0000\'', line)
                    matchTokenI = re.match('\[.*\] You say, \'t0001\'', line)

                    if matchTokenI != None:
                        yes = True
                    elif match != None and yes:
                        dictionaryAuxiliar[match.group(3)] = (match.group(1), match.group(2), match.group(4), match.group(5))
                    elif matchRole != None and yes:
                        dictionaryAuxiliar[matchRole.group(2)] = [(matchRole.group(1))]
                    elif matchToken != None and yes:
                        dictionary = dictionaryAuxiliar.copy()
                        dictionaryAuxiliar.clear()
                        yes = False
                    count = count + 1

            #bucle para sacar datos, primero eliminamos todo lo que haya
            self.listbox.delete(0, self.listbox.size())
            self.listbox2.delete(0, self.listbox2.size())
            self.listbox3.delete(0, self.listbox3.size())
            self.listbox4.delete(0, self.listbox4.size())
            self.listbox5.delete(0, self.listbox5.size())
            for member in dictionary:
                self.listbox.insert(END, member)
                self.listbox2.insert(END, dictionary[member][0])
                try:
                    self.listbox3.insert(END, dictionary[member][1])
                    self.listbox4.insert(END, dictionary[member][2])
                    self.listbox5.insert(END, dictionary[member][3])
                except IndexError as error:
                    self.listbox3.insert(END, '-')
                    self.listbox5.insert(END, '-')
                    self.listbox4.insert(END, '-')
            
            #print(dictionary)
            #print('Longitud', len(dictionary))

            #guardamos la linea ultima leida en el diccionario
            #self.lastLine = count
            #optionsDictionary[self.name] = count
            #print('Despues:', optionsDictionary)

            #guardamos el diccionario en el archivo options
            options = open('options.txt', 'w')
            for player in optionsDictionary:
                options.write(str(player)+':'+str(optionsDictionary[player]))
            options.close()

def main():
  
    root = Tk()
    root.geometry("927x550+50+50")
    root.resizable(width=False, height=False)
    app = Example(root)
    root.mainloop()  

if __name__ == '__main__':
    main() 
