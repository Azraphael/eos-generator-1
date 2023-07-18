from breezypythongui import EasyFrame
from breezypythongui import *
from datetime import datetime
from tkinter import VERTICAL, HORIZONTAL


class MainWindow(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title="End-Of-Shift Reports")

        # Add Components / Row 0/1
        self.addLabel(text="Name:", row=0, column=0)
        self.addLabel(text="Date: ",
                      row=0, column=2)
        self.addLabel(text="Shift:", row=0, column=4)

        self.addTextField(text='', row=1, column=0, columnspan=2, sticky="ew")
        self.addLabel(text=datetime.today().strftime("%m-%d-%Y"), row=1, column=2)  # Date of Report

        self.shiftSelection = self.addRadiobuttonGroup(row=1, column=4, orient=VERTICAL)
        self.shiftSelection.setSelectedButton(self.shiftSelection.addRadiobutton(text="6AM-6PM"))
        self.shiftSelection.addRadiobutton(text="6PM-6AM")

        # Row 2/3
        self.addLabel(text="Breakfast:", row=2, column=0, columnspan=2)
        self.breakfastCount = self.addIntegerField(row=3, column=0, columnspan=2, sticky="ew", value=0)
        self.addLabel(text="Lunch:", row=2, column=2)
        self.lunchCount = self.addIntegerField(row=3, column=2, columnspan=2, value=0, sticky="ew")
        self.addLabel(text="Dinner:", row=2, column=4)
        self.dinnerCount = self.addIntegerField(row=3, column=4, columnspan=2, value=0, sticky="ew")
        # Row 4/5
        self.addButton(text='Add Event', row=4, column=0)
        self.addButton(text='Remove Event', row=4, column=1)
        self.list_events = self.addListbox(row=5, column=0, columnspan=6, rowspan=5)


