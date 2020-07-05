********************************************************************************************
************************       __   __   .__                      **************************
************************     _/  |_|  | _|  |   ____   ____       **************************
************************     \   __\  |/ /  |  /  _ \ / ___\      **************************
************************      |  | |    <|  |_(  <_> ) /_/  >     **************************
************************      |__| |__|_ \____/\____/\___  /      **************************
************************                \/          /_____/       **************************
********************************************************************************************

TKlog aims to be functionally identical to tklist. It features some minor changes that I
believe improve the quality of life for the user. This app was developed using Python 3.8.3
with dependencies including tkinter, datetime, and sqlite3. I realized after I began 
development that we have Python 2.7.5 installed on smc3 at the moment, but hopefully we can
upgrade, otherwise I can tweak the application to work on smc3's version.

After executing the script you should be greeted with a screen that looks similar to 
sfoclog. Fields are navigated by tabbing over, or by clicking/highlighting previous boxes.
Once an entry is added to the database, the entry with the latest time should be displayed
on the top half onece at least one entry is submitted. Entries are submitted by hitting 
return.

The show records at the bottom brings up the manage records screen. This screen has a text
box that contains every record currently in the database. Underneath the text box are three
buttons that correspond to the Delete, Modify, and Print Functions.

To delete, the user should pick the ID of the entry they want to delete and type/paste it in
the text box, and click the delete button. The entry should then clear itself from the text
box.

To modify an entry, you should pick the ID of the entry they want to delete and type/paste it
in the text box, and click the modify button. A window should then pop up with text boxes
filled with the entry they selected that can be used to modify the entry. Hit return to
accept changes, or the x button to cancel.

To print, the user should type the Day of year in the text box, and hit the print button.
This will generate a file titled PrintLogYYYY_DOY in the directory that tklog is in.

There is still some polishing that needs to be done, near future plans have been noted in my
todos in the top of the file,  but I felt that this was a good place to get some input, let 
me know what you think.