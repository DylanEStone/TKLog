from tkinter import *
from datetime import datetime
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.messagebox
import sqlite3

#TODO: Print by day Functionality
#TODO: Add modify functionality to records page
#TODO: Adjust DOY value change days at the correct UTC time
#TODO: Edit database to accomodate for DR#
#TODO: If DR is selected, when enter is hit, prompt user for DR#

root = Tk()
root.title("TK LOG")


#################    Database    ###################

# create a database or connect to one
conn = sqlite3.connect('logs.db')
# create cursor
c = conn.cursor()

# Create table (Primary key auto genereated by sqlite3)
c.execute("""
CREATE TABLE IF NOT EXISTS logs (
    doy text,
    utc text,
    dss text,
    sc text,
    enttype text,
    note text
)
""")

# TODO: On submit, copy submitted fields to last comment field (Like SFOCLOG DOES)
# Create Submit function for database
def submit(doesnothing):
    # create a database or connect to one
    conn = sqlite3.connect('logs.db')
    # create cursor
    c = conn.cursor()

    
    # Insert into table
    c.execute("INSERT INTO logs VALUES (:doyentry, :utcentry, :dssentry, :scentry, :enttype, :note)",
            {
                'doyentry': DOYEntry.get(),
                'utcentry': UTCEntry.get(),
                'dssentry': DSSEntry.get(),
                'scentry': SCEntry.get(),
                'enttype': EntType.get(),
                'note': NoteEntry.get("1.0", 'end')
            })

    # Clear the text Boxes
    DOYEntry.delete(0, END)
    DOYEntry.insert(0, day_of_year)
    UTCEntry.delete(0, END)
    DSSEntry.delete(0, END)
    SCEntry.delete(0, END)
    NoteEntry.delete(1.0, END)
    UTCEntry.focus()

    # Commit changes
    conn.commit()

    # Close Connection
    conn.close()


def openRecords():


    
    def delete():
        conn = sqlite3.connect('logs.db')
        c = conn.cursor()

        # Delete a record
        c.execute("DELETE from logs WHERE oid= " + oid_box.get())
        #TODO: Provide some confrimation that the delete worked
        conn.commit()
        conn.close()

    recordWindow = Toplevel(root)

    recordWindow.title("Manage Records")
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()

    # Query the database
    c.execute("SELECT *, oid FROM logs")
    records = c.fetchall()
    print(records)

    # Loop through results
    print_records =  ''
    for record in records:
        print_records += "DOY: " + str(record[0]) + "\t\tUTC: " + str(record[1]) + "\t\tDSS: " + str(record[2]) + "\t\tS/C: " + str(record[3]) + "\t\tID: " + str(record[6]) + "\nLog: " + str(record[5]) + "\n\n"

    query_label = tkst.ScrolledText(
        master = recordWindow,
        wrap = tk.WORD,
        width = 70,
        height = 20
    )

    # Delete Button
    delete_btn = Button(recordWindow, text="Delete", command=delete)

    # Modify Button
    modify_btn = Button(recordWindow, text="Modify", command=delete)
    
    oid_label = Label(recordWindow, text="ID")
    oid_box = Entry(recordWindow, width=5)

    query_label.pack(padx=10, pady=10, fill=tk.BOTH ,expand=False)
    oid_box.pack(side=RIGHT, padx=10)
    oid_label.pack(side=RIGHT, padx=10, pady=10)
    modify_btn.pack(side=RIGHT)
    delete_btn.pack(side=RIGHT)

    query_label.insert(tk.INSERT, print_records)

    conn.commit()
    conn.close()


    




##################  TK GUI   #######################
# DOY
day_of_year = str(datetime.now().timetuple().tm_yday)
DOYLabel = Label(root, text="DOY")
DOYEntry = Entry(root)
DOYEntry.insert(0, day_of_year)

# UTC
def limitSizeUTC(*args):    #All of these limit functions just make sure that the amount of characters per field are correct
    value = UTCValue.get()  #TODO: Better data validation, make sure there are no empty fields when submitting note
    if len(value) > 4: UTCValue.set(value[:4])

UTCValue = StringVar(root)
UTCValue.trace('w', limitSizeUTC)

UTCLabel = Label(root, text="UTC")
UTCEntry = Entry(root, textvariable=UTCValue)

#DSS
def limitSizeDSS(*args):
    value = DSSValue.get()
    if len(value) > 3: DSSValue.set(value[:3])

DSSValue = StringVar(root)
DSSValue.trace('w', limitSizeDSS)

DSSLabel = Label(root, text="DSS")
DSSEntry = Entry(root, textvariable=DSSValue)

# SC
def limitSizeSC(*args):
    value = SCValue.get()
    if len(value) > 3: SCValue.set(value[:3])

SCValue = StringVar(root)
SCValue.trace('w', limitSizeSC)

SCLabel = Label(root, text="S/C")
SCEntry = Entry(root, textvariable=SCValue)

# ENTType
EntType = StringVar(root)
EntTypeLabel = Label(root, text="EntType")
EntTypeOptions = [ "Log", "DR", "FR", "Proc" ]
EntTypeDropdown = OptionMenu(root, EntType, *EntTypeOptions)
EntType.set(EntTypeOptions[0]) # default value = Log

# Note
NoteLabel = Label(root, text="Entry")
NoteEntry = Text(root, height=5 , width=90)


# view Button
query_btn = Button(root, text="Show Records", command=openRecords)




DOYLabel.grid(row=0, column=0)
DOYEntry.grid(row=1, column=0)

UTCLabel.grid(row=0, column=1)
UTCEntry.grid(row=1, column=1)
UTCEntry.focus()

DSSLabel.grid(row=0, column=2)
DSSEntry.grid(row=1, column=2)

SCLabel.grid(row=0, column=3)
SCEntry.grid(row=1, column=3)

EntTypeLabel.grid(row=0, column=4)
EntTypeDropdown.grid(row=1, column=4)

NoteLabel.grid(row=2, columnspan=5)
NoteEntry.grid(row=3, columnspan=5)

query_btn.grid(row = 4, columnspan=5, pady = (5, 5))


# Binds Enter key to submit Log
root.bind('<Return>', submit)


root.mainloop()