
from tkinter import Tk, Label, StringVar, Button, Entry, OptionMenu

import tkinter as tk

import numpy as np

import fractions
np.set_printoptions(formatter={'all':lambda x: str(fractions.Fraction(x).limit_denominator())})
import pandas as pd

text_var = []
entries = []
basic=['Z']
non_basic=[]

def op_bf():
    global A
    op_sol=np.zeros((1,cols-1))   
    for i in range(0,cols-1):
        if ("X"+str(i)) in non_basic:
            A[:,i]=0
        for j in range(0,rows):
            if A[j,i]!=0:
                A[j,-1]=A[j,-1]/A[j,i]
                A[j,i]=A[j,i]/A[j,i]
                op_sol[0,0]=A[0,-1]
      
    output=("The optimization solution is Z = "+str(op_sol[0,0]))
    return output

def standard_cal():
    global A
    newWindow3 = tk.Toplevel(root)
    newWindow3.title("Standard Form")
    newWindow3.geometry("800x800")
    counter1=0
    y1=25
    df_cols_index=["Z"]
    for i in range(1,cols-1):
        df_cols_index.append("X"+str(i))
    df_cols_index.append("RHS")
    for i in range(1,cols-1):
        if i>=cols-rows:
            basic.append('X'+str(i))
        else:
            non_basic.append('X'+str(i))
    A = np.zeros((rows,cols))
    for i in range(rows):
        for j in range(cols):
            A[i,j]=float(text_var[i][j].get())
    df1 = pd.DataFrame(data = A, 
                  index = basic, 
                  columns = df_cols_index)
    Label(newWindow3,text="Tabular Form", font=('arial', 10, 'bold'), bg='LightSkyBlue1').place(x=20,y=y1)
    Label(newWindow3,text=df1, font=('arial', 10, 'bold'), bg='LightSkyBlue2').place(x=20,y=y1+25)
    #Label(newWindow3,text="Basic Variables: "+str(basic), font=('arial', 10, 'bold'), bg='LightSkyBlue3').place(x=20,y=rows*20+50)
    while True:
        counter1+=1
        

        ratio={}
        if A[0,0]>0:
            piv_col=min(list(A[0,1:(cols-1)]))
        elif A[0,0]<0:
            piv_col=max(list(A[0,1:(cols-1)]))
        col_index =list(A[0,1:(cols-1)]).index(piv_col)+1
        for i in range(1,rows):
            if A[i,col_index]==0:
                continue
            else:
                ratio[abs(A[i,(cols-1)]/A[i,col_index])]=i
        piv_row=min(list(ratio.keys()))
        row_index=ratio[piv_row]
        pivot_no=A[row_index,col_index]
        A_=np.copy(A)
        A=np.zeros((rows,cols))
        A[row_index]=A_[row_index]/A_[row_index,col_index]
        for j in range(0,rows):
            if j==row_index:
                continue
            else:                                                                           
                A[j]=A_[j]-(A_[j,col_index]/A[row_index,col_index])*A[row_index]          #25 50 130;y25 155; y180 180 205 285, 310; y335 335 360 440
 
        if counter1==1:  
            Label(newWindow3,text=" pivot row : "+ str(row_index+1) + " pivot column : "+ str(col_index+1) + " pivot: "+ str(pivot_no), font=('arial', 10, 'bold'), bg='LightSkyBlue3' ).place(x=20,y=75+rows*20)
        else:
            Label(newWindow3,text=" pivot row : "+ str(row_index+1) + " pivot column : "+ str(col_index+1) + " pivot: "+ str(pivot_no), font=('arial', 10, 'bold'), bg='LightSkyBlue3' ).place(x=20,y=y1+50+rows*20)
        y1+=rows*20+75
        non_basic[list(non_basic).index('X'+str(col_index))]=basic[row_index]
        basic[row_index]='X'+str(col_index)
        df1 =pd.DataFrame(data = A, 
                  index = basic, 
                  columns = df_cols_index)
        Label(newWindow3,text="Iteration "+str(counter1), font=('arial', 10, 'bold'), bg='LightSkyBlue1').place(x=20,y=y1)
        Label(newWindow3,text=df1, font=('arial', 10, 'bold'), bg='LightSkyBlue2').place(x=20,y=y1+25)
        #Label(newWindow3,text="Basic Variables: "+str(basic), font=('arial', 10, 'bold'), bg='LightSkyBlue3').place(x=20,y=y1+25+rows*20)
        
        if A[0,0]>0:
            if min(list(A[0,1:(cols-1)]))<0:
                print(row_index)
                continue
            else:
                Label(newWindow3,text=op_bf(), font=('arial', 10, 'bold'), bg='LightSkyBlue4').place(x=20,y=y1+50+rows*20)
                break
        elif A[0,0]<0:
            if max(list(A[0,1:(cols-1)]))>0:
                print(row_index)
                continue
            else:
                Label(newWindow3,text=op_bf(), font=('arial', 10, 'bold'), bg='LightSkyBlue4').place(x=20,y=y1+50+rows*20)
                break

def standard():
    global rows, cols
    newWindow1 = tk.Toplevel(root)
    newWindow1.title("Standard Form")
    newWindow1.geometry("400x400")
    Label(newWindow1,text="Enter matrix :", font=('arial', 10, 'bold'), bg="bisque2").place(x=20, y=20)
    x2 = 0
    y2 = 0
    d_v=int(E1.get())
    n_c=int(E2.get())

    rows, cols = (n_c+1,n_c+d_v+2)
    for i in range(rows):
    # append an empty list to your two arrays
    # so you can append to those later
        text_var.append([])
        entries.append([])
        for j in range(cols):
        # append your StringVar and Entry
            text_var[i].append(StringVar())
            entries[i].append(Entry(newWindow1, textvariable=text_var[i][j],width=3))
            entries[i][j].place(x=60 + x2, y=50 + y2)
            x2 += 30


        y2 += 30
        x2 = 0
    button= Button(newWindow1,text="Submit", bg='bisque3', width=15, command=standard_cal)
    button.place(x=x2+60,y=y2+50)
    

# root window
root = tk.Tk()
root.geometry('900x600')
root.resizable(False, False)
root.title('simplex')

B = tk.Button(text ="Standard Form", command =standard)
#C = tk.Button(text ="Non-standard Form", command =non_standard )

L1 = tk.Label(root, text="The number of the decision variable")
E1 = tk.Entry(root, bd =5)

L2 = tk.Label(root, text="The number of the functional constraints")
E2 = tk.Entry(root, bd =5)

L1.pack()
E1.pack()
L2.pack()
E2.pack()
B.pack()
#C.pack()

root.mainloop()








