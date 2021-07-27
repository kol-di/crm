# crm
Tkinter based CRM prototype

For russian README version scroll down

Required Python version: **3.8.2**.
Some string methods might not function for python < 3.5

Requirements are specified in requirements.txt

To run the program, run **crm.py**


**User guide**:

CRM provides functionality of managing clients, employees and applications and filtering the applications in order to 
find the appropriate. 
From the starter page you can navigate either to the page for _managing data_ or to the _filter page_.

**Data management page**:

From this page you can access a window for managing your employee, window for managing your clients and window for 
managing your applications. To insert new record type the information in the corresponding field and press the button.
If your inputs don't correspond to the format, the program will let you know. To delete the record from the database,
press the delete button next to it.For the applications management window, you must create a client record and an 
employee record in the corresponding windows first, and than you would be able to choose them as an option when adding 
an application record.

_Important!_ Even though it is possible to open the windows for employee, client and application management at once, if
you add new record, for example, in the clients window, the drop-down list in applications window would not be updated
unless you reopen the window.

_Also:_ the numbers before the clients and employees in drop-down lists represent their unique id, given by the system 
and used to not mix up people with the same names.

**Filter page**:

This page provides a bunch of instruments for filtering the applications, which are currently in the database.

1. To choose the date interval, press on the date in the calendar, than press the button to/from. If some of the borders is insignificant,
don't do anything and leave the field blank.
2. To choose the statuses, mark the ones, which you need in the checkbox.
3. To choose the type, select it from the drop-down list. Select "All" option, if you wish to select all of them.
4. After your filters are set up, press the "Apply" button.

_Important!_ No applications would be present on the filter page unless you add some through the applications management 
menu

Требуемая версия Python: **3.8.2**. Некоторые методы работы со строками могут не функционировать для версий < 3.5

Требования приведены в файле requirements.txt

Для запсука программы, запустите **crm.py**

**Инструкция по использованию:**

CRM предоставляет функционал добавления/удаления записей о сотрудниках/клиентах/заявках и механизм фильтрации заявок. Со
стартовой страницы вы можете попасть или на страницу управления служебными данными, или на страницу фильтрации заявок.

**Управление служебными данными:**

С этой страницы вы можете получить доступ к окну управления сторудниками, клиентами, заявками. Чтобы добавить новую 
запись, введите необходимую информацию в соответствующие поля и нажмите кнопку "Добавить". Если введенные данные не 
соответствуют формату, вы увидите предупреждение. Для удаления записи, нажмите кнопку "Удалить" возле соответствующей записи. 
Что касается окна управления заявками, вы должеы создать запись о 
клиенте и о сотруднике прежде, чем сможете выбрать их в выпадающем списке при создании новой заявки.

_Важно!_  Несмотря на то что у вас есть возможность открыть сразу несколько окон для управления клиентами/сотрудниками/заявками,
при добавлении новой записи о клиенте/сотруднике, необходимо перезагрузить окно управления заявками чтобы иметь возможность выбрать
этого сотрудника/клиента в выпадающем списке.

_Также:_числа перед именами клиентов/сотрудников в выпадающих списках соответствуют их уникальным номерам, которые присваиваются
системой во избежание путаницы между людьми с одинаковыми именами.

**Фильтрация заявок:**

Эта страница предоставляет набор инструментов для удобного поиска необходимых заявок, в данный момент находящихся в базе.

1. Чтобы выбрать временной интервал, выберите необходимую дату в календаре и нажмите кнопку от/до. Если какая-то из границ не важна, 
оставьте поле пустым.
2. Чтобы выбрать нужные статусы, отметьте их галочкой в соответствующем поле.
3. Чтобы выбрать статус, выберите его из выпадающего списка.
4. После настройки фильтров, нажмите кнопку "Применить" чтобы увидеть результат.

_Важно!_ Пока вы не добавите заявки на странице управления заявками, на странице фильтрации заявок будет пусто.
