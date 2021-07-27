import tkinter as tk
from tkinter import ttk
from sqlalchemy import and_, or_
from tkcalendar import Calendar
from datetime import date, datetime
import string

from base import session
from application import Application
from employee import Employee
from client import Client
from scrollable_frame import ScrollableFrame


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

        # filter page format differs from the one of main page and data management page
        if isinstance(self.frame, FilterPage):
            self.frame.grid()
        else:
            self.frame.pack()


class StartPage(tk.Frame):
    """inital page, i.e main menu"""

    def __init__(self, master):
        """initialize all main menu widgets"""

        # the page is a frame, inheriting from tkinter Frame
        tk.Frame.__init__(self, master)

        # main label
        label = tk.Label(self, text='Главное меню', font=('Helvetica', 20), pady=10)
        label.pack()

        # data management button
        data_management_button = tk.Button(self, text='Управление служебными данными',
                  command=lambda: master.switch_frame(DataManagementPage), pady=10)
        data_management_button.pack()

        # applications filter button
        applications_filter_button = tk.Button(self, text='Фильтрация заявок',
                  command=lambda: master.switch_frame(FilterPage), pady=10)
        applications_filter_button.pack()


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
    """class representing the page for updating and deleting employees, clients, applications"""

    def __init__(self, master):
        """initialize all widgets"""

        # page inherits from Frame
        tk.Frame.__init__(self, master)

        # main label
        main_label = tk.Label(self, text="Управление служебными данными", font="Arial 18")
        main_label.pack(side="top", fill="x")
        main_label.config(height=5)


        # frame for buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=0)

        # employees button
        tk.Button(button_frame, text='Сотрудники', command=self._call_employees_menu).grid(row=0, column=0, padx=10)
        # applications button
        tk.Button(button_frame, text='Заявки', command=self._call_apps_menu).grid(row=0, column=1, padx=10)
        # client button
        tk.Button(button_frame, text='Клиенты', command=self._call_clients_menu).grid(row=0, column=2, padx=10)

        # return button
        tk.Button(self, text='Назад',
                  command=lambda: master.switch_frame(StartPage)).pack(side="right", fill="x", pady=10)


    """Employees menu functions"""

    def _call_employees_menu(self):
        """employees menu"""

        # initial settings
        self.emp_menu = tk.Toplevel()
        self.emp_menu.title("Сотрудники")
        self.emp_menu.geometry("650x600")
        self.emp_scrollable_frame = None

        # main label
        tk.Label(self.emp_menu, text="Список сотрудников").grid(row=0, column=0, columnspan=3, pady=10)

        # table footer
        emps_footer_frame = tk.LabelFrame(self.emp_menu)
        emps_footer_frame.grid(row=1, column=0)
        tk.Label(emps_footer_frame, text="Имя", width=19).grid(row=0, column=0, sticky="w")
        tk.Label(emps_footer_frame, text="Номер телефона", width=19).grid(row=0, column=1, sticky="w")
        tk.Label(emps_footer_frame, text="ID", width=19).grid(row=0, column=3, sticky="w")

        # output employees
        self._output_employees()

        # add employee label
        tk.Label(self.emp_menu, text="Новый сотрудник", font="Arial 14").grid(row=3, column=0, columnspan=3, pady=10)

        # add employee entries
        add_employee_frame = tk.Frame(self.emp_menu)
        add_employee_frame.grid(row=4, column=0, columnspan=3, pady=10)

        tk.Label(add_employee_frame, text="Имя:").grid(row=0, column=0, sticky="w")
        self.emp_name_entry = tk.Entry(add_employee_frame)
        self.emp_name_entry.grid(row=0, column=1)

        tk.Label(add_employee_frame, text="Номер телефона:").grid(row=1, column=0, sticky="w")
        self.emp_phone_number_entry = tk.Entry(add_employee_frame)
        self.emp_phone_number_entry.grid(row=1, column=1)

        # "add employee" button
        add_emp_button = tk.Button(self.emp_menu, text="Добавить", command=self._add_employee)
        add_emp_button.grid(row=5, column=0, columnspan=3, pady=10)

        # alert label
        self.emp_add_failed = tk.Label(self.emp_menu, text="")
        self.emp_add_failed.grid(row=6, column=0, pady=5)


    def _output_employees(self):
        """create a scrollable frame for employees and output employees, currently in database"""

        # employee list
        emps = session.query(Employee).order_by(Employee.name).all()

        # delete previous frame if exists
        if self.emp_scrollable_frame:
            self.emp_scrollable_frame.destroy()

        # create and configure new scrollable frame
        self.emp_scrollable_frame = ScrollableFrame(self.emp_menu, width=600)
        self.emp_scrollable_frame.grid(row=2, column=0, columnspan=3, pady=10)

        # print employees, each in a different frame
        for index, employee in enumerate(emps):

            # get unique id of record so as to be deleted in the future
            record_id = employee.id

            # frame for attributes and "delete" button
            emp_frame = tk.LabelFrame(self.emp_scrollable_frame.scrollable_frame)
            emp_frame.grid(row=index, column=0, sticky="w")

            # attributes
            attributes = employee.attribute_list()
            col_num = 0
            for value in attributes:
                label = tk.Label(emp_frame, text=str(value))
                label.grid(row=0, column=col_num, sticky='W')
                label.config(width=19)
                col_num += 1

            # delete button
            delete_button = tk.Button(emp_frame, text="Удалить", command=lambda port = record_id: self._delete_employee(port))
            delete_button.grid(row=0, column=col_num + 1, sticky="e")


    def _delete_employee(self, id):
        """deletes the frame of the record and erases record from SQl table"""

        emp_to_delete = session.query(Employee).filter(Employee.id == id).first()
        session.delete(emp_to_delete)
        session.commit()

        self._output_employees()


    def _add_employee(self):
        """add employee to the database and output updated list"""

        # add only if input is valid
        if not self.emp_name_entry.get() or not self.emp_phone_number_entry.get():
            self.emp_add_failed["text"] = "Обязательные поля: имя и номер телефона"
            return None
        else:
            self.emp_add_failed["text"] = ""

        new_emp = Employee(name=self._capitalise_name(self.emp_name_entry.get()), phone_number=self.emp_phone_number_entry.get())
        session.add(new_emp)
        session.commit()
        self.emp_name_entry.delete(0, "end")
        self.emp_phone_number_entry.delete(0, "end")
        self._output_employees()


    """Clients menu functions"""

    def _call_clients_menu(self):
        """clients menu"""

        # initial settings
        self.client_menu = tk.Toplevel()
        self.client_menu.title("Клиенты")
        self.client_menu.geometry("800x600")
        self.client_scrollable_frame = None

        # main label
        tk.Label(self.client_menu, text="Список клиентов").grid(row=0, column=0, columnspan=3, pady=10)

        # table footer
        clients_footer_frame = tk.LabelFrame(self.client_menu)
        clients_footer_frame.grid(row=1, column=0)
        tk.Label(clients_footer_frame, text="Имя", width=18).grid(row=0, column=0, sticky="w")
        tk.Label(clients_footer_frame, text="Номер телефона", width=18).grid(row=0, column=1, sticky="w")
        tk.Label(clients_footer_frame, text="Телеграм", width=18).grid(row=0, column=2, sticky="w")
        tk.Label(clients_footer_frame, text="ID", width=18).grid(row=0, column=3, sticky="w")

        # output clients
        self._output_clients()

        # client label
        tk.Label(self.client_menu, text="Новый клиент", font="Arial 14").grid(row=3, column=0, columnspan=3, pady=10)

        # clients' entries
        add_client_frame = tk.Frame(self.client_menu)
        add_client_frame.grid(row=4, column=0, columnspan=3, pady=10)

        tk.Label(add_client_frame, text="Имя:").grid(row=0, column=0, sticky="w")
        self.client_name_entry = tk.Entry(add_client_frame)
        self.client_name_entry.grid(row=0, column=1)

        tk.Label(add_client_frame, text="Номер телефона:").grid(row=1, column=0, sticky="w")
        self.client_phone_number_entry = tk.Entry(add_client_frame)
        self.client_phone_number_entry.grid(row=1, column=1)

        tk.Label(add_client_frame, text="Телеграм:").grid(row=2, column=0, sticky="w")
        self.client_tg_entry = tk.Entry(add_client_frame)
        self.client_tg_entry.grid(row=2, column=1)

        # "add client" button
        add_client_button = tk.Button(self.client_menu, text="Добавить", command=self._add_client)
        add_client_button.grid(row=5, column=0, columnspan=3, pady=10)

        # alert label
        self.client_add_failed = tk.Label(self.client_menu, text="")
        self.client_add_failed.grid(row=6, column=0, pady=5)


    def _output_clients(self):
        """create a scrollable frame for clients and output clients, currently in database"""

        # clients list
        clients = session.query(Client).order_by(Client.name).all()

        # delete previous frame if exists
        if self.client_scrollable_frame:
            self.client_scrollable_frame.destroy()

        # create new scrollable frame
        self.client_scrollable_frame = ScrollableFrame(self.client_menu, width=750)
        self.client_scrollable_frame.grid(row=2, column=0, columnspan=3, pady=10)

        # print clients, each in a different frame
        for index, client in enumerate(clients):

            # get unique id of record so as to be deleted in the future
            record_id = client.id

            # frame for attributes and "delete" button
            client_frame = tk.LabelFrame(self.client_scrollable_frame.scrollable_frame)
            client_frame.grid(row=index, column=0, sticky="w")

            # attributes
            attributes = client.attribute_list()
            col_num = 0
            for value in attributes:
                label = tk.Label(client_frame, text=str(value))
                label.grid(row=0, column=col_num, sticky='W')
                label.config(width=18)
                col_num += 1

            # delete button
            delete_button = tk.Button(client_frame, text="Удалить", command=lambda port = record_id: self._delete_client(port))
            delete_button.grid(row=0, column=col_num + 1, sticky="e")


    def _delete_client(self, id):
        """deletes the frame of the record and erases record from SQl table"""

        client_to_delete = session.query(Client).filter(Client.id == id).first()
        session.delete(client_to_delete)
        session.commit()

        self._output_clients()


    def _add_client(self):
        """add client to the database and output updated list"""

        # add only if input is valid
        if not self.client_name_entry.get() or not self.client_phone_number_entry.get():
            self.client_add_failed["text"] = "Обязательные поля: имя и номер телефона"
            return None
        else:
            self.client_add_failed["text"] = ""

        # add and output new client record
        new_client = Client(name=self._capitalise_name(self.client_name_entry.get()),
                            phone_number=self.client_phone_number_entry.get(), tg=self.client_tg_entry.get())
        session.add(new_client)
        session.commit()
        self.client_name_entry.delete(0, "end")
        self.client_phone_number_entry.delete(0, "end")
        self.client_tg_entry.delete(0, "end")
        self._output_clients()


    """Applications menu functions"""

    def _call_apps_menu(self):
        """apps menu"""

        # initial settings
        self.app_menu = tk.Toplevel()
        self.app_menu.title("Заявки")
        self.app_menu.geometry("900x700")
        self.app_scrollable_frame = None

        # main label
        tk.Label(self.app_menu, text="Список заявок").grid(row=0, column=0, columnspan=3, pady=10)

        # table footer
        apps_footer_frame = tk.LabelFrame(self.app_menu)
        apps_footer_frame.grid(row=1, column=0)
        tk.Label(apps_footer_frame, text="Дата", width=17).grid(row=0, column=0, sticky="w")
        tk.Label(apps_footer_frame, text="Статус", width=17).grid(row=0, column=1, sticky="w")
        tk.Label(apps_footer_frame, text="Тип", width=17).grid(row=0, column=2, sticky="w")
        tk.Label(apps_footer_frame, text="Клиент", width=17).grid(row=0, column=3, sticky="w")
        tk.Label(apps_footer_frame, text="Сотрудник", width=17).grid(row=0, column=4, sticky="w")

        # output apps
        self._output_apps()

        # app label
        tk.Label(self.app_menu, text="Новая заявка", font="Arial 14").grid(row=3, column=0, columnspan=3, pady=10)

        # apps' entries and respective labels
        add_app_frame = tk.Frame(self.app_menu)
        add_app_frame.grid(row=4, column=0, columnspan=3, pady=10)

        tk.Label(add_app_frame, text="Дата:").grid(row=0, column=0, sticky="w")
        self.app_creation_date_entry = tk.Entry(add_app_frame)
        self.app_creation_date_entry.grid(row=0, column=1)

        tk.Label(add_app_frame, text="Статус:").grid(row=1, column=0, sticky="w")
        self.app_status_combo = ttk.Combobox(add_app_frame, values=["открыта", "в работе", "закрыта"])
        self.app_status_combo.grid(row=1, column=1)

        tk.Label(add_app_frame, text="Тип:").grid(row=2, column=0, sticky="w")
        self.app_type_combo = ttk.Combobox(add_app_frame, values=['Ремонт', 'Обслуживание', 'Консультация'])
        self.app_type_combo.grid(row=2, column=1)

        tk.Label(add_app_frame, text="Клиент:").grid(row=3, column=0, sticky="w")
        clients = [(client.name, client.id) for client in session.query(Client).distinct()]
        self.app_client_combo = ttk.Combobox(add_app_frame, values=[str(client[1]) + ". " + client[0] for client in clients])
        self.app_client_combo.grid(row=3, column=1)

        tk.Label(add_app_frame, text="Сотрудник:").grid(row=4, column=0, sticky="w")
        emps = [(employee.name, employee.id) for employee in session.query(Employee).distinct()]
        self.app_emp_combo = ttk.Combobox(add_app_frame, values=[str(emp[1]) + ". " + emp[0] for emp in emps])
        self.app_emp_combo.grid(row=4, column=1)

        # "add app" button
        add_app_button = tk.Button(self.app_menu, text="Добавить", command=self._add_app)
        add_app_button.grid(row=5, column=0, columnspan=3, pady=10)

        # alert label
        self.app_add_failed = tk.Label(self.app_menu, text="")
        self.app_add_failed.grid(row=6, column=0, pady=5)


    def _output_apps(self):
        """create a scrollable frame for apps and output apps, currently in database"""

        # apps list
        apps = session.query(Application).order_by(Application.creation_date).all()

        # delete previous frame if exists
        if self.app_scrollable_frame:
            self.app_scrollable_frame.destroy()

        # create new scrollable frame
        self.app_scrollable_frame = ScrollableFrame(self.app_menu, width=860)
        self.app_scrollable_frame.grid(row=2, column=0, columnspan=3, pady=10)

        # print apps, each in a different frame
        for index, app in enumerate(apps):

            # get unique id of record so as to be deleted in the future
            record_id = app.id

            # frame for attributes and "delete" button
            app_frame = tk.LabelFrame(self.app_scrollable_frame.scrollable_frame)
            app_frame.grid(row=index, column=0, sticky="w")

            # attributes
            attributes = app.attribute_list()
            col_num = 0
            for value in attributes:
                label = tk.Label(app_frame, text=str(value))
                label.grid(row=0, column=col_num, sticky='W')
                label.config(width=17)
                col_num += 1

            # delete button
            delete_button = tk.Button(app_frame, text="Удалить", command=lambda port = record_id: self._delete_app(port))
            delete_button.grid(row=0, column=col_num + 1, sticky="e")


    def _delete_app(self, id):
        """deletes the frame of the record and erases record from SQl table"""

        app_to_delete = session.query(Application).filter(Application.id == id).first()
        session.delete(app_to_delete)
        session.commit()

        self._output_apps()


    def _add_app(self):
        """add app to the database and output updated list"""

        # add only if input is not empty
        if not self.app_creation_date_entry.get() or not self.app_status_combo.get() or \
                    not self.app_type_combo.get() or not self.app_client_combo.get() or \
                    not self.app_emp_combo.get():
            self.app_add_failed["text"] = "Все поля обязательны для заполнения"
            return None
        else:
            self.app_add_failed["text"] = ""

        # try to add and output new app record if date format is valid
        try:
            new_app = Application(creation_date=datetime.strptime(self.app_creation_date_entry.get(), '%d.%m.%Y'),
                                  status=self.app_status_combo.get(), type=self.app_type_combo.get(),
                                  client_id=int(self.app_client_combo.get().split('.')[0]),
                                  employee_id=int(self.app_emp_combo.get().split('.')[0]))
            self.app_add_failed["text"] = ""
        except ValueError:
            self.app_add_failed["text"] = "Неправильно введена дата. Введите дату в формате дд.мм.гггг"
            return None

        session.add(new_app)
        session.commit()
        self.app_creation_date_entry.delete(0, "end")
        self.app_status_combo.delete(0, "end")
        self.app_type_combo.delete(0, "end")
        self.app_client_combo.delete(0, "end")
        self.app_emp_combo.delete(0, "end")
        self._output_apps()


    """common functions"""
    def _capitalise_name(self, name):
        """makes first letter of name and surname capital and erases redundant spaces"""

        # capitalise names
        name = ' ' + name
        for index in range(len(name) - 2):
            if name[index] == ' ' and name[index+1] != ' ':
                if name[index+1].islower():
                    name = name[:index+1] + name[index+1].upper() + name[index+2:]

        # delete redundant spaces
        name = " ".join(name.split())

        return name

