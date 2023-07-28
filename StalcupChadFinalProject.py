"""
Author: Chad Stalcup
Date: 07/27/23
Code:  I've altered breezypythongui and other classes to make all this possible.
 Including images, adding image labels etc.
 I still use tkInter but breezypythongui made designing alot easier.  I still use functions and events that tkinter
 requires.  I've done heavy modification of breezypythongui.py to utilize these things.

"""

from breezypythongui import *
from datetime import datetime
from tkinter import VERTICAL, messagebox


def validate_integer(value, widget, previous_value):
    """
    Function to validate integer
    :param value: Value that i would be if it passes
    :param widget: For testing purposes, passed when called
    :param previous_value: For testing purposes, passed when called
    :return: Boolean ( True or False )
    """
    if value.isdigit() or value == '':
        return True
    else:
        return False


class MainWindow(EasyFrame):
    """
    Our main window class! Subclass of EasyFrame
    """

    def close_window(self):
        """
        Close window event: Called when 'X' is clicked or windows is attempting to get destroyed.
        :return: None
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()

    def __init__(self):
        """
        Initialization of our Class
        """
        EasyFrame.__init__(self, title="End-Of-Shift Reports", resizable=False)
        self.icon = tkinter.PhotoImage(file="./images/flag2.png")  # Our Icon for the Application
        self.setIcon(self.icon)  # Sets the Icon

        self.master.protocol("WM_DELETE_WINDOW", self.close_window)  # Register close window event

        validate_integer_command = (self.register(validate_integer), "%P", "%W", "%s")  # Validates Integer Field

        self.wheeler_image = tkinter.PhotoImage(file="./images/wmm.png")  # Wheeler Image Logo

        # Add Components / Row 0/1
        self.addLabel(row=16, column=1, columnspan=6, rowspan=5, image=self.wheeler_image, text='')
        self.addLabel(text="Name:", row=0, column=0)
        self.addLabel(text="Date: ",
                      row=0, column=2)
        self.addLabel(text="Shift:", row=0, column=4)

        self.employee = self.addTextField(text='', row=1, column=0, columnspan=2, sticky="new")  # Employee Name

        self.report_date = self.addLabel(text=datetime.today().strftime("%m-%d-%Y"), row=1, column=2)  # Date of Report

        self.shiftSelection = self.addRadiobuttonGroup(row=1, column=4, orient=VERTICAL)  # Shift Selection

        self.shiftSelection.setSelectedButton(
            self.shiftSelection.addRadiobutton(text="6AM-6PM"))  # Set default to first shift
        self.shiftSelection.addRadiobutton(text="6PM-6AM")

        # Row 2/3

        self.addLabel(text="Breakfast:", row=2, column=0, columnspan=2)
        # Variable containing breakfast count(number only)
        self.breakfastCount = self.addIntegerField(row=3, column=0, columnspan=2, sticky="ew", value=0,
                                                   validationcommand=validate_integer_command, validation='key')

        self.addLabel(text="Lunch:", row=2, column=2)
        # Variable containing the days lunch count
        self.lunchCount = self.addIntegerField(row=3, column=2, columnspan=2, value=0, sticky="ew",
                                               validationcommand=validate_integer_command, validation='key')

        self.addLabel(text="Dinner:", row=2, column=4)
        # Variable containing the days dinner count
        self.dinnerCount = self.addIntegerField(row=3, column=4, columnspan=2, value=0, sticky="ew",
                                                validationcommand=validate_integer_command, validation='key')

        # Row 5-15

        # Listbox containing the shifts events
        self.list_events = self.addListbox(row=5, column=0, columnspan=6, rowspan=10)
        # Add Event Button - Button-1 is bound on command parameter
        self.btn_add_event = self.addButton(text='Add Event', row=15, column=0, command=self.add_event)

        #  Remove Event Button - Button-1 is bound on command parameter
        self.btn_remove_event = self.addButton(text='Remove Event', row=15, column=1, command=self.remove_event)

        #  Export Data Button - Button-1 is bound on command parameter
        self.btn_export = self.addButton(text='Export Data', row=15, column=2, command=self.export_data)

        self.btn_add_event.bind("<3>", self.add_event)  # Add Right Click
        self.btn_remove_event.bind("<3>", self.remove_event)  # Add Right Click
        self.btn_export.bind("<3>", self.export_data)  # Add Right Click

        self.btn_add_event.bind("<2>", self.add_event)  # Add Middle Button
        self.btn_remove_event.bind("<2>", self.remove_event)  # Add Middle Button
        self.btn_export.bind("<2>", self.export_data)  # Add Middle Button

    def export_data(self):
        """
        Exports our data to a txt file
        :return: None
        """
        file = open("./report.txt", "w")  # File to Create(report.txt)

        file.write(self.employee.getText() + "\n")  # Write Employee Name
        file.write(self.report_date["text"] + "\n")  # Write Report Date
        file.write("Date: " + self.shiftSelection.getSelectedButton()["text"] + "\n")  # Write Date
        file.write("Breakfast Count: " + self.breakfastCount.get() + "\n")  # Write Breakfast Count
        file.write("Lunch Count: " + self.lunchCount.get() + "\n")  # Write Lunch Count
        file.write("Dinner Count: " + self.dinnerCount.get() + "\n\n")  # Write Dinner Count
        file.write("Today's Events:\n")
        for events in self.list_events.get(0, END):
            file.write("\t" + events)  # Write each line tabbed over for easier readability
        file.close()
        MessageBox(self, title="Save complete!", message="File saved to report.txt", width=50, height=10)

    def add_event(self, extra=None):
        """
        'Add Event' button click
        :return: None
        """
        EventWindow(self, self.register_event)

    def register_event(self, text):
        """
        Registers event in listbox
        :param text: Text to add to list
        :return: None
        """
        self.list_events.insert(tkinter.END, text)  # Add Event to list

    def remove_event(self, extra=None):
        """
        'Remove Event' button click
        :return:
        """
        index = self.list_events.getSelectedIndex()  # Get Selected Item to remove
        self.list_events.delete(index)  # Delete from list.


class EventWindow(EasyDialog):
    """
    Our eventwindow class to gather event information.  Popup window!
    """

    def __init__(self, parent, event):
        """
        Initial instantiation
        :param parent: parent of the window calling this
        :param event: event to call when hitting ok
        """
        self._event_text = None
        self._add_event = event  # Our callback function to call when hitting 'Ok' or hitting enter.

        self.flag_image = tkinter.PhotoImage(file='./images/flag2.png')  # Fancy flag for this window

        EasyDialog.__init__(self, parent, title='Add Event')   # Master init.

    def body(self, master) -> None:
        """
        Overloaded function, does not require an event returned
        :param master: Master window that was passed as parent.
        :return:
        """
        self.addLabel(master, text='Add Event', row=0, column=0, image=self.flag_image)
        self._event_text = self.addTextArea(master,
                                            text='', row=0, column=2, rowspan=5)  # TextArea with data to put in

        return self._event_text  # Returns Widget to instance

    def buttonbox(self):
        """
        Overloaded to create our own buttons!
        :return: None
        """
        box = tkinter.Frame(self)  # Create Frame on bottom (Ok/Cancel)
        w = tkinter.Button(box, text="Ok", width=10,
                           command=self.okbutton, default=ACTIVE, padx=10)  # Our Ok Button
        e = tkinter.Button(box, text="Cancel", width=10, command=self.cancel, default=ACTIVE, padx=10)  # Our Cancel

        w.bind("<2>", self.okbutton)  # Bind OK Middle Mouse
        e.bind("<2>", self.cancel)  # Bind Cancel Middle Mouse
        w.bind("<3>", self.okbutton)  # Bind OK Right Mouse
        e.bind("<3>", self.cancel)  # Bind Cancel Right Mouse

        w.grid(row=0, column=0)  # Set up the grid layout
        e.grid(row=0, column=2)  # Set up the grid layout
        self.bind("<Return>", self.ok)  # Bind to the Return key  for the entire window
        box.pack()

    def cancel(self, extra=None):
        """
        Gets called when Cancel button is clicked. Destroys this window.
        :return: None
        """
        self.destroy()

    def okbutton(self):
        """
        Calls the function we passed in instantiation. And passes the data in the textarea entry.
        :return: None
        """
        text = self._event_text.getText()
        if text != '':  # Validate that text is not empty
            self._add_event(text)

        self.destroy()

    def ok(self, value):
        """
        Is called when the "enter" button is hit.  Call the function we passed in instantiation and passes the data
        in the textarea entry
        :param value: has no real value
        :return:
        """
        text = self._event_text.getText()  # Get text from event text
        if text != '':
            self._add_event(text)  # IF text is not empty, add it

        self.destroy()  # Destroy window


if __name__ == '__main__':
    MainWindow().mainloop()  # Start the program
