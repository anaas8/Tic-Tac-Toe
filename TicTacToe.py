from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from copy import deepcopy

winStates = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
player1 = True
player2 = False

class node :
    def __init__(self, statex, stateo, empty, newstep):
        self.xstate = statex
        self.ostate = stateo
        self.empty = empty
        self.newstep = newstep
        self.Children = []
        self.similar_states = []
        self.Huristic = self.getHuristic(self.newstep)

    def Equal(self,node):
        if set(self.xstate) == set(node.xstate)and set(self.ostate) == set(node.ostate):
              return True
        return False

    def getHuristic(self,newstep):
        H = 0
        global winStates
        if not len(self.empty) % 2 == 0:
            xlist = self.xstate
            olist = self.ostate
        else:
            olist = self.xstate
            xlist = self.ostate
        if len(self.empty) <= 5:
            for L in winStates:
                if L[0] in olist and (L[1] in olist) and (L[2] in olist):
                    H = 999
                    return H

            for L in winStates:
                if ((L[0] in xlist) and (L[1] in xlist)) and (L[2] ==  newstep):
                    H = 99
                    return H
                elif ((L[0] in xlist) and (L[2]in xlist)) and (L[1] == newstep):
                    H = 99
                    return H
                elif ((L[1] in xlist) and (L[2] in xlist)) and (L[0] == newstep):
                    H = 99
                    return H

        for L in winStates:
            if (L[0] in olist) or (L[1] in olist) or (L[2] in olist):
                 if (L[0] not in xlist) and (L[1] not in xlist)and (L[2] not in xlist):
                      H = H+1
        return H

    def Build(self):

            if len(self.empty) % 2 == 0:
                for o in self.empty:
                    E = list(self.empty)
                    oS = list(self.ostate)
                    E.pop(E.index(o))
                    oS.append(o)
                    child = node(self.xstate, oS, E, o)
                    self.add_child(child)

            else:
                 for x in self.empty:
                    E = list(self.empty)
                    xS = list(self.xstate)
                    E.pop(E.index(x))
                    xS.append(x)
                    child = node(xS, self.ostate, E, x)
                    child.newstep = x
                    self.add_child(child)

    def add_child(self, Child):
        if not len(self.Children):
            self.Children.append(Child)
        else:
            if not self.chick_repeatation(Child):
                self.Children.append(Child)

    def chick_repeatation(self, Child):
        Child1 = deepcopy(Child)
        for x in range(len(self.Children)):
                if Child1.Equal(self.Children[x]):
                    print("right")
                    self.Children[x].similar_states.append(Child)
                    return True
                else:
                    s = True
                    while s:
                        if Child1.Equal(self.Children[x]) or Child1.reflect().Equal(self.Children[x]) :
                            self.Children[x].similar_states.append(Child)
                            return True
                        Child1 = Child1.rotate()
                        if Child1.Equal(Child):
                            s = False

        return False

    def reflect(self):
        self1 = deepcopy(self)
        reflection_right_list = [3, 2, 1, 6, 5, 4, 9, 8, 7]
        for x in range(len(self1.xstate)):
            self1.xstate[x] = reflection_right_list[self1.xstate[x]-1]
        for O in range(len(self1.ostate)):
            self1.ostate[O] = reflection_right_list[self1.ostate[O]-1]
        for e in range(len(self1.empty)):
            self1.empty[e] = reflection_right_list[self1.empty[e]-1]
        return self1

    def rotate(self):
        copy = deepcopy(self)
        rotatelist = [7, 4, 1, 8, 5, 2, 9, 6, 3]
        for x in range(len(copy.xstate)):
            copy.xstate[x] = rotatelist[copy.xstate[x]-1]
        for O in range(len(copy.ostate)):
            copy.ostate[O] = rotatelist[copy.ostate[O]-1]
        for e in range(len(copy.empty)):
            copy.empty[e] = rotatelist[copy.empty[e]-1]
        return copy

    def play(self):
        if len(self.Children):
            max = deepcopy(self.Children[0])
            for x in range(len(self.Children)):
                if max.Huristic <= self.Children[x].Huristic:
                    max = deepcopy(self.Children[x])
        return list([max.newstep, max])

xlist = []
olist = []
empty = [1, 2, 3, 4, 5, 6, 7, 8, 9]
CurrentGUIState = node(xlist, olist, empty, 0)
root = Tk()
root.title("TicTacToy")
style = ttk.Style()
style.theme_use('classic')


def ChickWinning(State):
    if player1:
        for l in winStates:
            if (l[0] in State.xstate) and (l[1] in State.xstate) and (l[2] in State.xstate):
                return True
    elif player2:
        for l in winStates:
            if (l[0] in State.ostate) and(l[1] in State.ostate) and (l[2] in State.ostate):
                return True
    return False

def switchstate():
    global player1
    global player2
    k = player1
    player1 = player2
    player2 = k

def X_O(location, value):
    if location == 1:
         but1.config(text=value, state="disabled")
    elif location == 2:
         but2.config(text=value, state="disabled")
    elif location == 3:
         but3.config(text=value, state="disabled")
    elif location == 4:
         but4.config(text=value, state="disabled")
    elif location == 5:
         but5.config(text=value, state="disabled")
    elif location == 6:
         but6.config(text=value, state="disabled")
    elif location == 7:
         but7.config(text=value, state="disabled")
    elif location == 8:
         but8.config(text=value, state="disabled")
    else:
         but9.config(text=value, state="disabled")

def let_player2_play():
    global CurrentGUIState
    laststate = deepcopy(CurrentGUIState)
    c = CurrentGUIState.play()
    newlocation = c[0]
    CurrentGUIState = c[1]
    X_O(newlocation, "O")
    if not ChickWinning(CurrentGUIState):
        switchstate()
    else:
        messagebox.showinfo(title="congratulations", message="you Lose")
        for i in CurrentGUIState.empty:
             X_O(i, " ")

def onclick(location):
    CurrentGUIState.xstate.append(CurrentGUIState.empty.pop(CurrentGUIState.empty.index(location)))
    CurrentGUIState.Build()
    if player1:
        X_O(location, "X")
        if not ChickWinning(CurrentGUIState):
            if len(CurrentGUIState.empty):
                switchstate()
                let_player2_play()
            else:
                messagebox.showinfo(title="VOid", message="there is No Winner")
        else:
            messagebox.showinfo(title="congratulations", message="winner winner")
            for i in CurrentGUIState.empty:
                X_O(i, " ")

but1 = ttk.Button(root, text=' ', command=lambda: onclick(1))
but1.grid(row=0, column=0, sticky='snew', ipadx=40, ipady=40)
but2 = ttk.Button(root, text=' ', command=lambda: onclick(2))
but2.grid(row=0, column=1, sticky='snew', ipadx=40, ipady=40)
but3 = ttk.Button(root, text=' ', command=lambda: onclick(3))
but3.grid(row=0, column=2, sticky='snew', ipadx=40, ipady=40)

but4 = ttk.Button(root, text=' ', command=lambda: onclick(4))
but4.grid(row=1, column=0, sticky='snew', ipadx=40, ipady=40)
but5 = ttk.Button(root, text=' ', command=lambda: onclick(5))
but5.grid(row=1, column=1, sticky='snew', ipadx=40, ipady=40)
but6 = ttk.Button(root, text=' ', command=lambda: onclick(6))
but6.grid(row=1, column=2, sticky='snew', ipadx=40, ipady=40)

but7 = ttk.Button(root, text=' ', command=lambda: onclick(7))
but7.grid(row=2, column=0, sticky='snew', ipadx=40, ipady=40)
but8 = ttk.Button(root, text=' ', command=lambda: onclick(8))
but8.grid(row=2, column=1, sticky='snew', ipadx=40, ipady=40)
but9 = ttk.Button(root, text=' ', command=lambda: onclick(9))
but9.grid(row=2, column=2, sticky='snew', ipadx=40, ipady=40)

root.mainloop()
