from tkinter import *
import datetime
from datetime import datetime
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.messagebox
import sqlite3

#TODO: Edit database to accomodate for DR#
#TODO: If DR is selected, when enter is hit, prompt user for DR#
#TODO: Fix lastentry query (top part main menu) to account for doy
#TODO: Add a timer to check for database changes and update GUI in case partner types entry
#TODO: Entry Validation

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
def update(doesnothing):
        conn = sqlite3.connect('logs.db')
        c = conn.cursor()

        record_id = oid_box.get()
        c.execute("""
            UPDATE logs SET
            doy = :DOYEntry,
            utc = :UTCEntry,
            dss = :DSSEntry,
            sc = :SCEntry,
            enttype = :EntType,
            note = :NoteEntry

            WHERE oid = :oid
        """,
        {
            'DOYEntry': DOYEntry_editor.get(),
            'UTCEntry': UTCEntry_editor.get(),
            'DSSEntry': DSSEntry_editor.get(),
            'SCEntry': SCEntry_editor.get(),
            'EntType': EntType_editor.get(),
            'NoteEntry': NoteEntry_editor.get("1.0", 'end'),

            'oid': record_id
        })

        conn.commit()
        query_label.delete(1.0, END)
        printLogs(c)
        get_last_entries()
        conn.close()

        editor.destroy()

def modify():
    global editor
    editor = Tk()
    editor.title('Edit an entry')

    editor.bind('<Return>', update)

    conn = sqlite3.connect('logs.db')
    c = conn.cursor()

    record_id = oid_box.get()

    # Query the database
    c.execute("SELECT * FROM logs WHERE oid = " + record_id)
    records = c.fetchall()

    # Select record to modify
    
    # Create Global Variables for text box names
    global DOYEntry_editor
    global UTCEntry_editor
    global DSSEntry_editor
    global SCEntry_editor
    global EntType_editor
    global NoteEntry_editor
    
    ##################  Edit GUI   #######################
    # DOY
    DOYLabel_editor = Label(editor, text="DOY")
    DOYEntry_editor = Entry(editor)

    # UTC
    UTCValue_editor = StringVar(editor)
    UTCValue_editor.trace('w', limitSizeUTC)

    UTCLabel_editor = Label(editor, text="UTC")
    UTCEntry_editor = Entry(editor, textvariable=UTCValue)

    #DSS
    DSSValue_editor = StringVar(editor)
    DSSValue_editor.trace('w', limitSizeDSS)

    DSSLabel_editor = Label(editor, text="DSS")
    DSSEntry_editor = Entry(editor, textvariable=DSSValue_editor)

    # SC
    SCValue_editor = StringVar(editor)
    SCValue_editor.trace('w', limitSizeSC)

    SCLabel_editor = Label(editor, text="S/C")
    SCEntry_editor = Entry(editor, textvariable=SCValue_editor)

    # ENTType
    EntType_editor = StringVar(editor)   #FIXME: If DR, FR or Proc is selected, should promt user to enter numeber
    EntTypeLabel_editor = Label(editor, text="EntType")
    EntTypeOptions = [ "Log", "DR", "FR", "Proc" ]
    EntTypeDropdown_editor = OptionMenu(editor, EntType_editor, *EntTypeOptions)
    EntType_editor.set(EntTypeOptions[0]) # default value = Log

    # Note
    NoteLabel_editor = Label(editor, text="Entry")
    NoteEntry_editor = Text(editor, height=5 , width=90)

    

    #############    Placement   ##################
    DOYLabel_editor.grid(row=0, column=0)
    DOYEntry_editor.grid(row=1, column=0)

    UTCLabel_editor.grid(row=0, column=1)
    UTCEntry_editor.grid(row=1, column=1)
    UTCEntry_editor.focus()

    DSSLabel_editor.grid(row=0, column=2)
    DSSEntry_editor.grid(row=1, column=2)

    SCLabel_editor.grid(row=0, column=3)
    SCEntry_editor.grid(row=1, column=3)

    EntTypeLabel_editor.grid(row=0, column=4)
    EntTypeDropdown_editor.grid(row=1, column=4)

    NoteLabel_editor.grid(row=2, columnspan=5)
    NoteEntry_editor.grid(row=3, columnspan=5)

    for record in records:
        DOYEntry_editor.insert(0, record[0])
        UTCEntry_editor.insert(0, record[1])
        DSSEntry_editor.insert(0, record[2])
        SCEntry_editor.insert(0, record[3])
        EntType_editor.set(record[4])
        NoteEntry_editor.insert(1.0, record[5])



def delete():
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()

    # Delete a record
    c.execute("DELETE from logs WHERE oid= " + oid_box.get())
    query_label.delete(1.0, END)
    conn.commit()
    printLogs(c)
    get_last_entries()
    conn.close()


def submit(doesnothing):    #i had to put a dummy parameter because enter was bound to submit... I am not sure why but it is ok
    
    conn = sqlite3.connect('logs.db')
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

    #printLogs(c)
    # Commit changes
    conn.commit()
    get_last_entries()

    # Close Connection
    conn.close()
        


def openRecords():
    recordWindow = Toplevel(root)

    recordWindow.title("Manage Records")
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()


    global query_label
    query_label = tkst.ScrolledText(
        master = recordWindow,
        wrap = tk.WORD,
        width = 70,
        height = 20
    )
                
    printLogs(c)

    # Print Button
    print_btn = Button(recordWindow, text="Print (DOY)", command=printDay)

    # Delete Button
    delete_btn = Button(recordWindow, text="Delete (ID)", command=delete)

    # Modify Button
    modify_btn = Button(recordWindow, text="Modify (ID)", command=modify)
    
    oid_label = Label(recordWindow, text="ID")
    global oid_box
    oid_box = Entry(recordWindow, width=5)

    query_label.pack(padx=10, pady=10, fill=tk.BOTH ,expand=False)
    oid_box.pack(side=RIGHT, padx=10)
    oid_label.pack(side=RIGHT, padx=10, pady=10)
    print_btn.pack(side=RIGHT)
    modify_btn.pack(side=RIGHT)
    delete_btn.pack(side=RIGHT)


    conn.commit()
    conn.close()

def printLogs(c):
    # Query the database
    c.execute("SELECT *, oid FROM logs ORDER BY utc ASC;")
    records = c.fetchall()

    # Loop through results
    print_records =  ''
    for record in reversed(records):
        print_records += "DOY: " + str(record[0]) + "\t\tUTC: " + str(record[1]) + "\t\tDSS: " + str(record[2]) + "\t\tS/C: " + str(record[3]) + "\t\tID: " + str(record[6]) + "\nLog: " + str(record[5]) + "\n\n"
    query_label.insert(tk.INSERT, print_records)


##################  TK GUI   #######################
# DOY
day_of_year = str(datetime.utcnow().timetuple().tm_yday)
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


#############  Last Entry UI ###############
def get_last_entries():
    global LastDOY
    global LastUTC
    global LastDSS
    global LastSC
    global LastEnt
    global LastEntry

    conn = sqlite3.connect('logs.db')
    c = conn.cursor()

    # Query the database
    c.execute("SELECT doy, MAX(utc), dss, sc, enttype, note AS MostRecent FROM logs")
    r = c.fetchall()
    LastDOY = r[0][0]
    LastUTC = r[0][1]
    LastDSS = r[0][2]
    LastSC = r[0][3]
    LastEnt = r[0][4]
    LastEntry = r[0][5]

    LastDOYEntry = Label(root, text=LastDOY, bg="white")
    LastUTCEntry = Label(root, text=LastUTC, bg="white")
    LastDSSEntry = Label(root, text=LastDSS, bg="white")
    LastSCEntry = Label(root, text=LastSC, bg="white")
    LastEntEntry = Label(root, text=LastEnt, bg="white")
    LastEntryEntry = Label(root, text=LastEntry, bg="white", height=5, width=90, justify=LEFT)

    LastDOYEntry.grid(row=1, column=0)
    LastUTCEntry.grid(row=1, column=1)
    LastDSSEntry.grid(row=1, column=2)
    LastSCEntry.grid(row=1, column=3)
    LastEntEntry.grid(row=1, column=4)
    LastEntryEntry.grid(row=3, columnspan=5, pady=(5, 5))

    conn.commit()
    conn.close()

def printDay():

    conn = sqlite3.connect('logs.db')
    c = conn.cursor()

    now = datetime.now()
    record_id = oid_box.get()
    title = "Printlog" + str(now.year) + "_" + record_id

    print(title)
    c.execute("SELECT * FROM logs WHERE doy = " + record_id + " ORDER BY utc DESC")
    records = c.fetchall()
    outF = open(title, "w")
    outF.write("UTC\tDSS\tS/C\tType\tEntry\n")
    
    for record in records:
        outF.write(record[1] + "\t"  +record[2] + "\t"  +record[3] + "\t"  +record[4] + "\t"  +record[5])
    
    outF.close()

    conn.commit()
    conn.close()


get_last_entries()

LastDOYLabel = Label(root, text="DOY")
LastDOYEntry = Label(root, text=LastDOY, bg="white")

LastUTCLabel = Label(root, text="UTC")
LastUTCEntry = Label(root, text=LastUTC, bg="white")

LastDSSLabel = Label(root, text="DSS")
LastDSSEntry = Label(root, text=LastDSS, bg="white")

LastSCLabel = Label(root, text="S/C")
LastSCEntry = Label(root, text=LastSC, bg="white")

LastEntLabel = Label(root, text="Ent")
LastEntEntry = Label(root, text=LastEnt, bg="white")

LastEntryLabel = Label(root, text="Entry")
LastEntryEntry = Label(root, text=LastEntry, bg="white", height=5, width=90, justify=LEFT)

get_last_entries()
# SC
def limitSizeSC(*args):
    value = SCValue.get()
    if len(value) > 3: SCValue.set(value[:3])

SCValue = StringVar(root)
SCValue.trace('w', limitSizeSC)

SCLabel = Label(root, text="S/C")
SCEntry = Entry(root, textvariable=SCValue)

# ENTType
EntType = StringVar(root)   #FIXME: If DR, FR or Proc is selected, should promt user to enter numeber
EntTypeLabel = Label(root, text="EntType")
EntTypeOptions = [ "Log", "DR", "FR", "Proc" ]
EntTypeDropdown = OptionMenu(root, EntType, *EntTypeOptions)
EntType.set(EntTypeOptions[0]) # default value = Log

# Note
NoteLabel = Label(root, text="Entry")
NoteEntry = Text(root, height=5 , width=90)


# view Button
query_btn = Button(root, text="Show Records", command=openRecords)


## Last Entry Gridding
LastDOYLabel.grid(row=0, column=0)
LastDOYEntry.grid(row=1, column=0)

LastUTCLabel.grid(row=0, column=1)
LastUTCEntry.grid(row=1, column=1)

LastDSSLabel.grid(row=0, column=2)
LastDSSEntry.grid(row=1, column=2)

LastSCLabel.grid(row=0, column=3)
LastSCEntry.grid(row=1, column=3)

LastEntLabel.grid(row=0, column=4)
LastEntEntry.grid(row=1, column=4)

LastEntryLabel.grid(row=2, columnspan=5)
LastEntryEntry.grid(row=3, columnspan=5, pady=(5, 5))

## Current Entry Gridding
DOYLabel.grid(row=4, column=0)
DOYEntry.grid(row=5, column=0)

UTCLabel.grid(row=4, column=1)
UTCEntry.grid(row=5, column=1)
UTCEntry.focus()

DSSLabel.grid(row=4, column=2)
DSSEntry.grid(row=5, column=2)

SCLabel.grid(row=4, column=3)
SCEntry.grid(row=5, column=3)

EntTypeLabel.grid(row=4, column=4)
EntTypeDropdown.grid(row=5, column=4)

NoteLabel.grid(row=6, columnspan=5)
NoteEntry.grid(row=7, columnspan=5)

query_btn.grid(row = 8, columnspan=5, pady = (5, 5))


# Binds Enter key to submit Log
root.bind('<Return>', submit)


root.mainloop()