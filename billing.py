from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import time
class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed By Shailja")
        self.root.config(bg="white")
        self.root.focus_force()
        self.cart_list=[]
        
        #===title=====
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)
        
        #====btn logout======
        btn_logout=Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)
        
        #=======clock============
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD-MM-YY\t\t Time: HH:MM:SS",font=("times new roman",15,),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        
        #=======Product Frame=====
        self.var_search=StringVar()
        product_frame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        product_frame1.place(x=10,y=110,width=450,height=620)
        
        pTitle=Label(product_frame1,text="All Products",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
        
        product_frame2=Frame(product_frame1,bd=2,relief=RIDGE,bg="white")
        product_frame2.place(x=2,y=42,width=400,height=100)
        
        lbl_search=Label(product_frame2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        
        lbl_name=Label(product_frame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=5,y=45)
        txt_search=Entry(product_frame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=130,y=48,width=150,height=22)
        btn_search=Button(product_frame2,text="Search",command=self.search,font=("goudy old style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=285,y=45,width=100,height=25)
        btn_show_all=Button(product_frame2,text="Show All",command=self.show,font=("goudy old style",15,"bold"),bg="#083531",fg="white",cursor="hand2").place(x=285,y=15,width=100,height=25)

        #======Product Details======
        product_frame3=Frame(product_frame1,bd=3,relief=RIDGE)
        product_frame3.place(x=2,y=140,width=400,height=450)

        scrolly=Scrollbar(product_frame3,orient=VERTICAL)
        scrollx=Scrollbar(product_frame3,orient=HORIZONTAL)
        
        self.product_table=ttk.Treeview(product_frame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)
        
        self.product_table.heading("pid",text="PID")
        self.product_table.heading("name",text="Name")
        self.product_table.heading("price",text="Price")
        self.product_table.heading("qty",text="Quantity")
        self.product_table.heading("status",text="Status")
        self.product_table["show"]="headings"
        
        self.product_table.column("pid",width=40)
        self.product_table.column("name",width=100)
        self.product_table.column("price",width=100)
        self.product_table.column("qty",width=40)
        self.product_table.column("status",width=80)
        self.product_table.pack(fill=BOTH,expand=1)
        self.product_table.bind("<ButtonRelease-1>",self.get_data)
        
        lbl_note=Label(product_frame1,text="Note: 'Enter 0 Quantity to remove product from Cart'",font=("goudy old style",12),bg="white",fg="red").pack(side=BOTTOM,fill=X)

        #======Customer Frame=====
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=500,y=110,width=550,height=80)
        
        cTitle=Label(CustomerFrame,text="Customer Details",font=("goudy old style",15,"bold"),bg="lightgrey",fg="black").pack(side=TOP,fill=X)
        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15,"bold"),bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="lightyellow").place(x=80,y=38,width=180)
        
        lbl_contact=Label(CustomerFrame,text="Contact No.",font=("times new roman",15,"bold"),bg="white").place(x=270,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="lightyellow").place(x=380,y=38,width=140)
        
        #===============Cal_Cart Frame======
        Cal_cart_Frame=Frame(self.root,bd=5,relief=RIDGE,bg="white")
        Cal_cart_Frame.place(x=500,y=190,width=550,height=450)
        
        #=====================Calculator Frame================
        self.var_cal_input=StringVar()
        
        Cal_Frame=Frame(Cal_cart_Frame,bd=9,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=10,width=268,height=400)
        
        txt_cal_input=Entry(Cal_Frame,font=("arial",15,"bold"),width=21,bd=10,relief=GROOVE,state='readonly',textvariable=self.var_cal_input,justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4)
        
        btn_7=Button(Cal_Frame,text="7",font=("arial",15,"bold"),width=4,bd=5,pady=17,cursor="hand2",command=lambda:self.get_input(7),bg="lightgrey",fg="black").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text="8",font=("arial",15,"bold"),width=4,bd=5,pady=17,cursor="hand2",command=lambda:self.get_input(8),bg="lightgrey",fg="black").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text="9",font=("arial",15,"bold"),width=4,bd=5,pady=17,cursor="hand2",command=lambda:self.get_input(9),bg="lightgrey",fg="black").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text="+",font=("arial",15,"bold"),width=4,bd=5,pady=17,cursor="hand2",command=lambda:self.get_input("+"),bg="lightgrey",fg="black").grid(row=1,column=3)
        btn_4=Button(Cal_Frame,text="4",font=("arial",15,"bold"),width=4,bd=5,pady=17,cursor="hand2",command=lambda:self.get_input(4),bg="lightgrey",fg="black").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text="5",font=("arial",15,"bold"),width=4,bd=5,pady=17,cursor="hand2",command=lambda:self.get_input(5),bg="lightgrey",fg="black").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text="6",font=("arial",15,"bold"),width=4,bd=5,pady=17,cursor="hand2",command=lambda:self.get_input(6),bg="lightgrey",fg="black").grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text="-",font=("arial",15,"bold"),width=4,bd=5,pady=17,cursor="hand2",command=lambda:self.get_input("-"),bg="lightgrey",fg="black").grid(row=2,column=3)
        btn_1=Button(Cal_Frame,text="1",font=("arial",15,"bold"),width=4,bd=5,pady=17,cursor="hand2",command=lambda:self.get_input(1),bg="lightgrey",fg="black").grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text="2",font=("arial",15,"bold"),width=4,bd=5,pady=17,cursor="hand2",command=lambda:self.get_input(2),bg="lightgrey",fg="black").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text="3",font=("arial",15,"bold"),width=4,bd=5,pady=17,cursor="hand2",command=lambda:self.get_input(3),bg="lightgrey",fg="black").grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text="*",font=("arial",15,"bold"),width=4,bd=5,pady=17,cursor="hand2",command=lambda:self.get_input("*"),bg="lightgrey",fg="black").grid(row=3,column=3)
        btn_0=Button(Cal_Frame,text="0",font=("arial",15,"bold"),width=4,bd=5,pady=20,cursor="hand2",command=lambda:self.get_input(0),bg="lightgrey",fg="black").grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text="C",font=("arial",15,"bold"),width=4,bd=5,pady=20,cursor="hand2",command=self.clear_cal,bg="lightgrey",fg="black").grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text="=",font=("arial",15,"bold"),width=4,bd=5,pady=20,cursor="hand2",command=self.perform_cal,bg="lightgrey",fg="black").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text="/",font=("arial",15,"bold"),width=4,bd=5,pady=20,cursor="hand2",command=lambda:self.get_input("/"),bg="lightgrey",fg="black").grid(row=4,column=3)
        
        
        
        #=====================Cart Frame================
        cart_Frame=Frame(Cal_cart_Frame,bd=3,relief=RIDGE)
        cart_Frame.place(x=280,y=8,width=245,height=400)
        self.cartTitle=Label(cart_Frame,text="Cart \t Total Product: [0]",font=("goudy old style",15),bg="lightgrey",fg="black")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(cart_Frame,orient=HORIZONTAL)
        
        self.CartTable=ttk.Treeview(cart_Frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        
        self.CartTable.heading("pid",text="PID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="Quantity")
        self.CartTable["show"]="headings"
        
        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=90)
        self.CartTable.column("price",width=90)
        self.CartTable.column("qty",width=40)
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)
        
        #=============Add Cart Widgets Frame================
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        
        Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWidgetsFrame.place(x=500,y=610,width=550,height=120)
        
        lbl_p_name=Label(Add_CartWidgetsFrame,text="Product Name",font=("times new roman",13,"bold"),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("times new roman",13),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)
        
        lbl_price=Label(Add_CartWidgetsFrame,text="Price Per Qty",font=("times new roman",13,"bold"),bg="white").place(x=210,y=5)
        txt_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("times new roman",13),bg="lightyellow",state='readonly').place(x=210,y=35,width=150,height=22)
        
        lbl_qty=Label(Add_CartWidgetsFrame,text="Quantity",font=("times new roman",13,"bold"),bg="white").place(x=380,y=5)
        txt_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("times new roman",13),bg="lightyellow").place(x=380,y=35,width=140,height=22)
        
        self.lbl_instock=Label(Add_CartWidgetsFrame,text="In Stock[]",font=("times new roman",15),bg="white")
        self.lbl_instock.place(x=10,y=80)
        
        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman",13,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=80,width=150,height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",13,"bold"),bg="orange",cursor="hand2").place(x=340,y=80,width=150,height=30)
        
        #==================billing area================================
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=1085,y=110,width=440,height=450)

        billTitle=Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="black",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        
        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)
        
        #=====================billing buttons========================
        btn_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=1085,y=560,width=440,height=170)
        
        self.lbl_amnt=Label(btn_frame,text="Bill Amount \n[0]",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=0,y=2,width=140,height=72)
        
        self.lbl_discount=Label(btn_frame,text="Discount \n[5%]",font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white")
        self.lbl_discount.place(x=142,y=2,width=140,height=72)

        self.lbl_net_pay=Label(btn_frame,text="Net Pay \n[0]",font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=286,y=2,width=160,height=72)
        
        btn_print=Button(btn_frame,text="Print",font=("goudy old style",13,"bold"),bg="lightgreen",cursor="hand2")
        btn_print.place(x=0,y=85,width=140,height=60)
        
        btn_clear_all=Button(btn_frame,text="Clear All",command=self.clear_all,font=("goudy old style",13,"bold"),bg="gray",cursor="hand2")
        btn_clear_all.place(x=142,y=85,width=140,height=60)
        
        btn_generate=Button(btn_frame,text="Generate/Save Bill",command=self.generate_bill,font=("goudy old style",13,"bold"),bg="orange",cursor="hand2")
        btn_generate.place(x=286,y=85,width=160,height=60)
        
        #================Footer====================
        footer=Label(self.root,text="Inventory Management System | Developed By Shailja Jha\nFor any Technical Issue Contact: 798xxxxx39",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        self.show()
        self.bill_top()
        self.update_date_time()
        
        #==================All Functions=======================
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)
    
    def clear_cal(self):
        self.var_cal_input.set("")
        
    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))
        
    def show(self):
            con=sqlite3.connect(database=r'ims.db')
            cur=con.cursor()
            try:
                cur.execute("select pid,name,price,qty,status from product where Status='Active'")
                rows=cur.fetchall()
                self.product_table.delete(*self.product_table.get_children())
                for row in rows:
                    self.product_table.insert('',END,values=row)
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
                
    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=='':
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%' and satus='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No Record Found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
    def get_data(self,ev):
        f=self.product_table.focus()
        content=(self.product_table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')
    
    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
        
        
        
    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror("Error","Please Select Product from the list",parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror("Error","Quantity is Required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror("Error","Invalid Quantity",parent=self.root)
        else:
            #price_cal=int(self.var_qty.get())*float(self.var_price.get())
            #price_cal=float(price_cal)
            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            #=================update_cart=================
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno("Confirm","Product already present\nDo you want to Update| Remove from the Cart List",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal
                        self.cart_list[index_][3]=self.var_qty.get()
            else:
                self.cart_list.append(cart_data)
                    
            self.show_cart()
            self.bill_updates()
            
    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
            
        self.discount=(self.bill_amnt*5)/100   
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f'Bill Amount\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Net Pay\n{str(self.net_pay)}')
        self.cartTitle.config(text=f'Cart \t Total Product: ({str(len(self.cart_list))})')
        
            
                        
                    
            
    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error",f"Customer Details are Required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please Add Product to the Cart",parent=self.root)
        else:
            #Bill Top
            self.bill_top()
            #Bill Middle
            self.bill_middle()
            #Bill Bottom
            self.bill_bottom()
            
            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo("Saved",f"Bill Generated Successfully\nBill No. {str(self.invoice)}",parent=self.root)
            
            
           
    
    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tXYZ-Inventory
\t Phone No. 79802*****   Kolkata-700053
{str("="*47)}
 Customer Name: {self.var_cname.get()}
 Ph no. : {self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
 Product Name\t\t\tQty\tPrice
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)
    
    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*47)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)
        
    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'
                    
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                #========update quantity in product table==========================
                cur.execute('Update Product set qty=?,status=? where pid=?',(
                    qty,
                    status,
                    pid 
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_instock.config(text=f"In Stock")
        self.var_stock.set('')
    
    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()
        self.bill_updates()
        
    def update_date_time(self):
        time_=time.strftime("%H:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\tDate: {str(date_)}\t\tTime: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)
        
        
       
        
               
        
if __name__=="__main__":
    root=Tk()
    obj=BillClass(root)
    root.mainloop()
        