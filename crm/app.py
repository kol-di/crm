import tkinter as tk
from tkinter import ttk
from sqlalchemy import inspect, select, and_, or_
from tkcalendar import Calendar, DateEntry
from datetime import date

from base import session
from application import Application


class App(tk.Tk):
    """class containing all pages and general settings"""

    def __init__(self):
        """initialize general settings"""
        tk.Tk.__init__(self)
        self.frame = None
        self.switch_frame(StartPage)
        self.title('CRM')
        self.geometry('800x800')

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one"""
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.grid()


class StartPage(tk.Frame):
    """inital page, i.e main menu"""

    def __init__(self, master):
        """initialize all main menu widgets"""

        # the page is a frame, inheriting from tkinter Frame
        tk.Frame.__init__(self, master)

        # main label
        label = tk.Label(self, text='Главное меню', font=('Helvetica', 16))
        label.grid(row=0, column=0, columnspan=2, padx=30, pady=10)

        # data management button
        data_management_button = tk.Button(self, text='Управление служебными данными',
                  command=lambda: master.switch_frame(DataManagementPage))
        data_management_button.grid(row=1, column=0, padx=10, pady=10)

        # applications filter button
        applications_filter_button = tk.Button(self, text='Фильтрация заявок',
                  command=lambda: master.switch_frame(FilterPage))
        applications_filter_button.grid(row=1, column=1)

class FilterPage(tk.Frame):
    """page for filtering applications"""

    def __init__(self, master):
        """initialize all filter page widgets"""

        #initial settings
        self.from_date = date.min
        self.to_date = date.max
        self.applications_list = None

        # main label
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page filter", font="Arial 18").grid(row=0, column=0, padx=100, pady=20)

        """applications list"""
        # query all appliactions
        applications = session.query(Application).order_by(Application.creation_date).all()

        # create the list
        self.applications_list = self._create_applications_list(applications)

        """filters"""
        # type filter
        self.combo_type = ttk.Combobox(self, values=['Все', 'Ремонт', 'Обслуживание', 'Консультация'])
        self.combo_type.grid(row=2, column=3, sticky='NW', padx=10, pady=10)
        self.combo_type.set('Все')

        # calendar for date choice
        cal = Calendar(self, font="Arial 14", selectmode='day', locale='en_US',
                       foreground="black", selectforeground="blue", year=2021, month=7, day=25)
        cal.grid(row=2, column=0, columnspan=2, pady=10)

        # from/till dates
        from_till_frame = tk.LabelFrame(self)
        from_till_frame.grid(row=3, column=0)
        self.from_label = tk.Label(from_till_frame, text='-')
        self.from_label.grid(row=0, column=0, sticky='W')
        self.to_label = tk.Label(from_till_frame, text='-')
        self.to_label.grid(row=0, column=1, sticky='E')

        # from/till buttons
        tk.Button(from_till_frame, text='От',
                  command=lambda: self._change_from_label(cal.selection_get())).grid(row=1, column=0, sticky='W')
        tk.Button(from_till_frame, text='До',
                 command=lambda: self._change_to_label(cal.selection_get())).grid(row=1, column=1, sticky='E')

        # status checkboxes located in their own frame
        checkbox_frame = tk.LabelFrame(self)
        checkbox_frame.grid(row=2, column=2, sticky='NW', padx=10, pady=10)
        self.chkValue1 = tk.BooleanVar()
        self.chkValue1.set(True)
        self.chkValue2 = tk.BooleanVar()
        self.chkValue2.set(True)
        self.chkValue3 = tk.BooleanVar()
        self.chkValue3.set(True)
        cb1 = tk.Checkbutton(checkbox_frame, text='открыта', var=self.chkValue1)
        cb2 = tk.Checkbutton(checkbox_frame, text='в работе', var=self.chkValue2)
        cb3 = tk.Checkbutton(checkbox_frame, text='закрыта', var=self.chkValue3)
        cb1.grid(row=0, column=0)
        cb2.grid(row=1, column=0)
        cb3.grid(row=2, column=0)

        """other widgets"""
        # error label
        self.error_label = tk.Label(self, text='')
        self.error_label.grid(row=4, column = 0)

        # apply filter button
        apply_button_frame = tk.Frame(self)
        apply_button_frame.grid(row=5, column=0, columnspan=5, pady=30)
        tk.Button(apply_button_frame, text='Применить', command=lambda: self._apply_filter()).pack()

        # return button
        tk.Button(self, text='Назад',
                  command=lambda: master.switch_frame(StartPage)).grid(row=6, column=4, pady=50)


    def _change_from_label(self, date):
        self.from_label['text'] = str(date)
        self.from_date = date

    def _change_to_label(self, date):
        self.to_label['text'] = str(date)
        self.to_date = date

    def _apply_filter(self):
        """apply all filters to all records and print a new applications list"""

        # check if chosen date interval is valid
        if self.from_date > self.to_date:
            self.error_label['text'] = 'Неправильно выбрана дата!'
            return None
        else:
            self.error_label['text'] = ''

        # checkbuttons' conditions
        conditions = [and_(Application.status == 'открыта', self.chkValue1.get()),
                      and_(Application.status == 'в работе', self.chkValue2.get()),
                      and_(Application.status == 'закрыта', self.chkValue3.get())]

        # two different queries: for all types and for a particular type
        if self.combo_type.get() == 'Все':
            final_query = session.query(Application).filter(and_(Application.creation_date >= self.from_date,
                                                                 Application.creation_date <= self.to_date)).filter(
                                                                 or_(*conditions))
        else:
            final_query = session.query(Application).filter(and_(Application.creation_date >= self.from_date,
                                                                 Application.creation_date <= self.to_date)).filter(
                                                                 Application.type == self.combo_type.get()).filter(
                                                                 or_(*conditions))

        # create new applications list and assign it
        self.applications_list = self._create_applications_list(final_query)

    def _create_applications_list(self, applications):
        """creates a frame with a list of applications"""

        # delete previous applications list if exists
        if self.applications_list:
            self.applications_list.destroy()

        # frame for applications
        applications_frame = tk.LabelFrame(self)
        applications_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10)

        # footer
        label = tk.Label(applications_frame, text='Дата')
        label.grid(row=0, column=0, columnspan=2, sticky='W')
        label = tk.Label(applications_frame, text='Статус')
        label.grid(row=0, column=2, sticky='W')
        label = tk.Label(applications_frame, text='Тип')
        label.grid(row=0, column=3, sticky='W')

        # list all applications ordered by date
        for index, application in enumerate(applications):
            attributes = application.attribute_list()
            col_num = 0
            for value in attributes:
                label = tk.Label(applications_frame, text=str(value))
                label.grid(row=index + 1, column=col_num, sticky='W')
                col_num += 1

        return applications_frame


class DataManagementPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page dataManagement").pack(side="top", fill="x", pady=10)
        tk.Button(self, text='Назад',
                  command=lambda: master.switch_frame(StartPage)).pack(side="right", pady=10)
