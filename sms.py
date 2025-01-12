from tkinter import *
import time
import ttkthemes
from tkinter import  ttk, messagebox,filedialog
import pymysql
import pandas
#functionality Part
def iexit():
    result=messagebox.askyesno('Confirm','3Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass

def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    #getting all the rows of the table
    indexing=studentTable.get_children()
    #an empty list to store the data of each row in the table.
    newlist=[]
    #This loop iterates over each row in the studentTable.
    for index in indexing:
        #For each row, this line gets the item (row) details from the studentTable.
        content=studentTable.item(index)
        # extracts the values (columns) of the row and stores them in datalist
        datalist=content['values']
        #each row is added to this new list variable. newlist is list of lists.
        newlist.append(datalist)
    print(newlist)

    #Here, the newlist is converted into a DataFrame using the Pandas library.
    table=pandas.DataFrame(newlist,columns=['Id','Name','Mobile','Email','Gender','Address','DOB','Added Date','Added Time'])
    #converting the table into a csv file, eliminating the row indexes
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved successfully')




def update_student():

    def update_data():

        #updating in mysql
        query='update student set name=%s, mobile=%s, email=%s, address=%s, gender=%s,dob=%s,date=%s, time=%s where id=%s'
        mycursor.execute(query,(nameEntry.get(), phoneEntry.get(), emailEntry.get(),addressEntry.get(), genderEntry.get(),dobEntry.get(),date,currenttime,idEntry.get()))
        con.commit()
        messagebox.showinfo('Success',f'Id{idEntry.get()} is modified successfully',parent=update_window)
        update_window.destroy()

        #updating data in tree view
        show_student()




    update_window = Toplevel()
    update_window.grab_set()
    update_window.title('Update Student')
    update_window.resizable(False, False)
    idLabel = Label(update_window, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=20, pady=15, sticky=W)
    idEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(update_window, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=20, pady=15, sticky=W)
    nameEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(update_window, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=20, pady=15, sticky=W)
    phoneEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(update_window, text='email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=20, pady=15, sticky=W)
    emailEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(update_window, text='address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=20, pady=15, sticky=W)
    addressEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(update_window, text='gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=20, pady=15, sticky=W)
    genderEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(update_window, text='dob', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=20, pady=15, sticky=W)
    dobEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    update_student_button = ttk.Button(update_window, text='UPDATE',command=update_data)
    update_student_button.grid(row=7, columnspan=2, pady=15)

    indexing=studentTable.focus()
    content=studentTable.item(indexing)
    listdata=content['values']
    idEntry.insert(0,listdata[0])
    nameEntry.insert(0,listdata[1])
    phoneEntry.insert(0,listdata[2])
    emailEntry.insert(0,listdata[3])
    addressEntry.insert(0,listdata[4])
    genderEntry.insert(0,listdata[5])
    dobEntry.insert(0,listdata[6])


def show_student():
    #fetches all the rows
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    #deleting the previous old data
    studentTable.delete(*studentTable.get_children())
    #inserting updated/new data if updated
    for data in fetched_data:
        studentTable.insert('', END, values=data)

def delete_student():
    #retrieves the index of the currently selected item in the studentTable
    indexing = studentTable.focus()
    #gets the details of the selected item (row) from the studentTable
    content = studentTable.item(indexing)
    #extracts the value of Id, which is the primary key
    content_id = content['values'][0]
    #SQL query to delete a record from the 'student' table based on the Id.
    query = 'DELETE FROM student WHERE id=%s'
    #executes the SQL query, deleting the record with the specified Id.
    mycursor.execute(query, content_id)
    #committing the changes
    con.commit()
    #a pop-up message indicating that the record with the specified ID has been successfully deleted.
    messagebox.showinfo('Deleted', f'Id {content_id} is deleted successfully')

    #The above section of the code, was for deleting in mysql server.

    #The below section is for deleting in my treeview(front end) and reflecting the changes immedietely.

    #fetches all the records and deletes them
    query='select * from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())

    #inserting the updated data from the db after the deletion is done.
    for data in fetched_data:
        studentTable.insert('',END,values=data)


def search_student():
    def search_data():
        #creates an SQL query to search for records in the 'student' table
        query='select * from student where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s'

        #executes the SQL query using the values entered by the user in the search fields, to retrieve the values entered by the user in the respective Entry fields.
        mycursor.execute(query,(idEntry.get(),nameEntry.get(),emailEntry.get(),phoneEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get()))
        #clears existing rows from the studentTable.
        studentTable.delete(*studentTable.get_children())
        #retrieves all the records that match the search criteria from the database.
        fetched_data=mycursor.fetchall()
        #updated data
        for data in fetched_data:
            studentTable.insert('',END,values=data)#new row should be inserted at the end of the table



    search_window = Toplevel()
    search_window.grab_set()
    search_window.title('Search Student' )
    search_window.resizable(False, False)
    idLabel = Label(search_window, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=20, pady=15, sticky=W)
    idEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(search_window, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=20, pady=15, sticky=W)
    nameEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(search_window, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=20, pady=15, sticky=W)
    phoneEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(search_window, text='email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=20, pady=15, sticky=W)
    emailEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(search_window, text='address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=20, pady=15, sticky=W)
    addressEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(search_window, text='gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=20, pady=15, sticky=W)
    genderEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(search_window, text='dob', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=20, pady=15, sticky=W)
    dobEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    search_student_button = ttk.Button(search_window, text='SEARCH STUDENT', command=search_data)
    search_student_button.grid(row=7, columnspan=2, pady=15)


def add_student():
    def add_data():

        #Adding in DB
        if idEntry.get()=='' or nameEntry.get()=='' or phoneEntry.get()=='' or emailEntry.get()=='' or addressEntry.get()=='' or genderEntry.get()==''or dobEntry.get()=='':
            messagebox.showerror('Error','All Fields are required', parent= add_window)
        else:
            currentdate = time.strftime('%d/%m/%Y')
            currenttime = time.strftime('%H:%M:%S')
            try:

                query='insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                mycursor.execute(query,(idEntry.get(),nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get(),date,currenttime))
                con.commit()
                result=messagebox.askyesno('Confirm','Data added successfully. Do you want to clean the form?',parent=add_window)
                if result:
                    idEntry.delete(0,END)
                    nameEntry.delete(0,END)
                    phoneEntry.delete(0,END)
                    emailEntry.delete(0,END)
                    addressEntry.delete(0,END)
                    genderEntry.delete(0,END)
                    dobEntry.delete(0,END)
                else:
                    pass
            except:
                messagebox.showerror('Error','Id cannot be repeated',parent=add_window)
                return

            #Adding in Treeview(Frontend)
            query='select *from student'
            mycursor.execute(query)
            fetched_data=mycursor.fetchall()
            studentTable.delete(*studentTable.get_children())
            for data in fetched_data:

                studentTable.insert('',END,values=data)


    add_window=Toplevel()
    add_window.grab_set()
    add_window.resizable(False,False)
    idLabel=Label(add_window,text='Id',font=('times new roman',20,'bold'))
    idLabel.grid(row=0,column=0,padx=20,pady=15,sticky=W)
    idEntry=Entry(add_window,font=('roman',15,'bold'),width=24)
    idEntry.grid(row=0,column=1,pady=15,padx=10)

    nameLabel = Label(add_window, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=20, pady=15,sticky=W)
    nameEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(add_window, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=20, pady=15,sticky=W)
    phoneEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(add_window, text='email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=20, pady=15,sticky=W)
    emailEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(add_window, text='address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=20, pady=15,sticky=W)
    addressEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(add_window, text='gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=20, pady=15,sticky=W)
    genderEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(add_window, text='dob', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=20, pady=15,sticky=W)
    dobEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    add_student_button=ttk.Button(add_window,text='ADD STUDENT',command=add_data)
    add_student_button.grid(row=7,columnspan=2,pady=15)


def connect_database():
    global hostEntry, usernameEntry, passwordEntry
    def connect():
        global mycursor,con
        try:
            con=pymysql.connect(host=hostEntry.get(),user=usernameEntry.get(),password=passwordEntry.get())
            mycursor=con.cursor()
            #messagebox.showinfo('Success', 'Database Connection is successfull',parent=connectWindow)
        except:
            messagebox.showerror('Error', 'Invalid Details',parent=connectWindow)
            return

        try:
            query='create database studentmanagementsystem'
            mycursor.execute(query)
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
            query='create table student(id int not null primary key,' \
              'name varchar(30), mobile varchar(10), email varchar(30),' \
              'address varchar(100), gender varchar(10), DOB varchar(20),' \
              'date varchar(50), time varchar(50))'

            mycursor.execute(query)

        except:
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
        messagebox.showinfo('Success', 'Database Connection is successfull', parent=connectWindow)
        connectWindow.destroy()
        addstudentButton.config(state=NORMAL)
        searchstudentButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportstudentButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)


    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0,0)

    hostnameLabel=Label(connectWindow,text='Host Name', font=('arial',20,'bold'))
    hostnameLabel.grid(row=0,column=0,padx=20)

    hostEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=40,pady=20)

    usernameLabel = Label(connectWindow, text='Username', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton=ttk.Button(connectWindow,text='CONNECT', command=connect)
    connectButton.grid(row=3,columnspan=2)


count=0
text=''
def slider():
    global text,count
    if count==len(s):
        count=0
        text=''
    text=text+s[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(300,slider)


def clock():
    global date,currenttime
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000,clock)




#GUI Part
root =ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')

root.geometry('1174x680+0+0')
root.resizable(0,0)
root.title('Student Management System') #s[count]=S when count is 0

datetimeLabel=Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5,y=5)
clock()

s='Student Management System'
sliderLabel=Label(root,text=s, font=('arial', 28, 'italic bold'),width=30)
sliderLabel.place(x=200,y=0)
slider()

connectButton=ttk.Button(root,text='Connect Database',command=connect_database)
connectButton.place(x=980,y=0)

leftFrame=Frame(root)
leftFrame.place(x=50,y=80, width=300, height=600)

logo_image=PhotoImage(file='student1.png')
logo_Label=Label(leftFrame, image=logo_image)
logo_Label.grid(row=0,column=0)

addstudentButton=ttk.Button(leftFrame,text='Add Student',width=25, command=add_student)
addstudentButton.grid(row=1,column=0, pady=20)

searchstudentButton=ttk.Button(leftFrame,text='Search Student',width=25,command=search_student)
searchstudentButton.grid(row=2,column=0, pady=20)

deletestudentButton=ttk.Button(leftFrame,text='Delete Student',width=25,command=delete_student)
deletestudentButton.grid(row=3,column=0, pady=20)

updatestudentButton=ttk.Button(leftFrame,text='Update Student',width=25, command=update_student)
updatestudentButton.grid(row=4,column=0, pady=20)

showstudentButton=ttk.Button(leftFrame,text='Show Student',width=25,command=show_student)
showstudentButton.grid(row=5,column=0, pady=20)

exportstudentButton=ttk.Button(leftFrame,text='Export Data',width=25, command=export_data)
exportstudentButton.grid(row=6,column=0, pady=20)

exitButton=ttk.Button(leftFrame,text='Exit',width=25,command=iexit)
exitButton.grid(row=7,column=0, pady=20)


rightFrame=Frame(root)
rightFrame.place(x=350,y=80, width=820, height=600)

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)


studentTable=ttk.Treeview(rightFrame,columns=('Id','Name','Mobile No','Email','Address','Gender','D.O.B',
                                 'Added Date','Added Time')
                          , xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)
scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

studentTable.pack(fill=BOTH,expand=1)

studentTable.heading('Id',text='Id')
studentTable.heading('Name',text='Name')
studentTable.heading('Mobile No',text='Mobile No')
studentTable.heading('Email',text='Email')
studentTable.heading('Address',text='Address')
studentTable.heading('Gender',text='Gender')
studentTable.heading('D.O.B',text='D.O.B')
studentTable.heading('Added Date',text='Added Date')
studentTable.heading('Added Time',text='Added Time')

studentTable.column('Id',width=50, anchor=CENTER)
studentTable.column('Name',width=300, anchor=CENTER)
studentTable.column('Email',width=400, anchor=CENTER)
studentTable.column('Mobile No',width=200, anchor=CENTER)
studentTable.column('Address',width=400, anchor=CENTER)
studentTable.column('Gender',width=100, anchor=CENTER)
studentTable.column('D.O.B',width=200, anchor=CENTER)
studentTable.column('Added Date',width=200, anchor=CENTER)

style=ttk.Style()

style.configure('Treeview',rowheight=40, font=('arial',12,'bold'),background='white', fieldbackground='white')
style.configure('Treeview.Heading',font=('arial',12,'bold'))

studentTable.config(show='headings')
root.mainloop()