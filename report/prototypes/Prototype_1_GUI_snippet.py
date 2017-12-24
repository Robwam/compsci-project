class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.inputData = [] # Rows, each contains sub array for columns
        self.project = None

        # NOTE debuggin prepopulate with test data
        if DEBUG:
          self.inputData = TEST_DATA

        self.initUI()


    def initUI(self):
        self.main_widget = QWidget(self)
        add_event_button = QPushButton("Add event")
        add_event_button.clicked.connect(self.get_event_input)

        schedule_button = QPushButton("Schedule")
        schedule_button.clicked.connect(self.create_schedule_project)

        #self.le = QLineEdit(self)
        #self.le.move(130, 22)

        self.event_name_textbox = QLineEdit(self)
        self.event_duration_textbox = QLineEdit(self)
        self.event_dependencies_textbox = QLineEdit(self)

        self.tableWidget = QTableWidget()
        self.tableWidget.move(100,100)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Name', 'Duration', 'Dependencies'])

        self.updateTable()

        # Left virticle box
        labelsVbox = QVBoxLayout()
        inputsVbox = QVBoxLayout()
        labelsVbox.addWidget(QLabel("Name:"))
        inputsVbox.addWidget(self.event_name_textbox)
        labelsVbox.addWidget(QLabel("Duration:"))
        inputsVbox.addWidget(self.event_duration_textbox)
        labelsVbox.addWidget(QLabel("Dependencies:")) # TODO this should be a dropdown list (checkbox list) of Dependencies
        inputsVbox.addWidget(self.event_dependencies_textbox)

        leftVboxHbox = QHBoxLayout()
        leftVboxHbox.addLayout(labelsVbox)
        leftVboxHbox.addLayout(inputsVbox)


        leftVbox = QVBoxLayout()
        leftVbox.addLayout(leftVboxHbox)
        leftVbox.addWidget(add_event_button)
        leftVbox.addWidget(schedule_button)

        # TODO setup correct graph
        graph = MyMplCanvas(self.main_widget, width=5, height=4, dpi=100)

        # Right virticle box
        rightVbox = QVBoxLayout()
        rightVbox.addWidget(self.tableWidget)
        rightVbox.addWidget(graph)

        hbox = QHBoxLayout()
        hbox.addLayout(leftVbox)
        hbox.addLayout(rightVbox)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.show()
