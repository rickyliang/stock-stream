import sys
import platform
import threading
import PySide
from time import sleep
from PySide import QtGui, QtCore, QtSql
from config import __version__, SQLALCHEMY_DATABASE_NAME
from models import Stock
from datetime import datetime

import process, windowSettable



app = QtGui.QApplication(sys.argv)



class MainWindow(QtGui.QMainWindow, windowSettable.WindowSettable):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.db_model = None
        self.streamer = process.Streamer()
        self.initUI()
        
    def initUI(self):
        # Load previous window attributes (position, size).
        self._readAndApplyWindowAttributeSettings()
        
        # Initialize status bar.
        self.statusBar().showMessage('Ready')
        
        # Set up menu actions.
        exit_action = QtGui.QAction(QtGui.QIcon('exit24.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)
        about_action = QtGui.QAction(QtGui.QIcon('bin/resources/about.png'), '&About', self)
        about_action.setStatusTip('About this program')
        about_action.triggered.connect(self.show_about_box)
        license_action = QtGui.QAction('&License', self)
        license_action.setStatusTip('Show the GPL v3 license')
        license_action.triggered.connect(self.show_license_box)
        
        # Menu bar.
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(exit_action)
        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction(about_action)
        help_menu.addAction(license_action)
        
        # Set up toolbar actions.
        add_stock_action = QtGui.QAction(QtGui.QIcon('bin/plusminus/plus.png'), '&Add', self)
        add_stock_action.setShortcut('Ctrl+N')
        add_stock_action.setStatusTip('Add a new stock')
        add_stock_action.triggered.connect(self.show_add_stock_dialog)
        remove_stock_action = QtGui.QAction(QtGui.QIcon('bin/plusminus/minus.png'), '&Remove', self)
        remove_stock_action.setShortcut('Ctrl+D')
        remove_stock_action.setStatusTip('Remove a stock')
        remove_stock_action.triggered.connect(self.show_remove_stock_dialog)
        
        # Toolbar.
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.addAction(add_stock_action)
        self.toolbar.addAction(remove_stock_action)
        # Necessary for saving window state.
        # From http://qt-project.org/doc/note_revisions/312/514/view
        self.toolbar.setObjectName('Toolbar')
        
        # Set up central stocks widget.
        stocks_db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        stocks_db.setDatabaseName("db/{}.db".format(SQLALCHEMY_DATABASE_NAME))
        stocks_db.open()
        self.db_model = QtSql.QSqlTableModel(db=stocks_db)
        self.db_model.setTable(Stock.__tablename__)
        self.db_model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.db_model.select()
        self.db_model.removeColumn(0)
        self.db_model.setHeaderData(0, QtCore.Qt.Horizontal, 'Symbol')
        self.db_model.setHeaderData(1, QtCore.Qt.Horizontal, 'Last Price')
        self.db_model.setHeaderData(2, QtCore.Qt.Horizontal, 'Change')
        stocks_view = QtGui.QTableView()
        stocks_view.setModel(self.db_model)
        #stocks_view.verticalHeader().setResizeMode(QtGui.QHeaderView.Interactive)
        #stocks_view.setFont(QtGui.QFont('SansSerif', 8))
        scroll_area = QtGui.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(stocks_view)
        self.setCentralWidget(scroll_area)
        
        # Set window size and position.
        self.setGeometry(300, 300, 800, 250)
        self.setWindowTitle('Stock Stream')
        
        # Initiate other threads.
        refresh_thread = threading.Thread(target=self.refresh)
        refresh_thread.daemon = True
        self.streamer.threads.append(refresh_thread)
        
        # Initiate the stream and show the GUI.
        refresh_thread.start()
        self.streamer.run()
        self.show()
        
    def refresh(self):
        """
        Retrieves data (hopefully updated) every 100 ms from the
        database. Used to refresh the view with updated information.
        Run on a separate thread.
        """
        while True:
            self.db_model.select()
            sleep(0.1)
            
    def closeEvent(self, event):
        # Save current window attributes (position, size).
        self._writeWindowAttributeSettings()
            ############### QUARANTINE ################
          ###                                         ###
        ###  super(MainWindow, self).closeEvent(event)  ###
          ###                                         ###
            ############### QUARANTINE ################
        
    def show_add_stock_dialog(self):
        """
        Creates a dialog box to prompt the user for a stock to insert
        into the stream.
        """
        stock_qstring, ok = QtGui.QInputDialog.getText(self, 'Add a stock', 'Stock:')
        stock_string = str(stock_qstring)
        if ok:
            self.streamer.add(stock_string)
            
    def show_remove_stock_dialog(self):
        """
        Creates a dialog box to prompt the user for a stock to remove
        from the stream.
        """
        stock_qstring, ok = QtGui.QInputDialog.getText(self, 'Remove a stock', 'Stock: ')
        stock_string = str(stock_qstring)
        if ok:
            self.streamer.remove(stock_string)
            
    def show_license_box(self):
        """
        Read and display the GPL v3 license.
        """
        QtGui.QMessageBox.about(self, "License",
            open("LICENSE.txt").read())
        
    def show_about_box(self):
        """
        Display information about StockStream.
        """
        QtGui.QMessageBox.about(self, "About StockStream",
            """<b>StockStream</b> ver. %s
            <p>StockStream draws live stock data from Yahoo!
            servers and updates it on a visual platform.</p>
            <p>Copyright 2014 Richard Liang. All rights
            reserved in accordance with GPL v3.</p>
            <p>Python %s - PySide %s - Qt %s on %s""" % \
            (__version__, platform.python_version(), \
            PySide.__version__, PySide.QtCore.__version__, \
            platform.system()))



class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setGeometry(300, 200, 800, 200)
        self.setWindowTitle('Stock Stream')
        #self.setWindowIcon(QtGui.QIcon('web.png'))
        
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 8))
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        centerButton = QtGui.QPushButton('Center this window', self)
        centerButton.clicked.connect(self.centerWindow)
        centerButton.resize(centerButton.sizeHint())
        centerButton.move(5, 5)
        
        quitButton = QtGui.QPushButton('Quit', self)
        quitButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        quitButton.setToolTip('This is a <b>QPushButton</b> widget')
        quitButton.resize(quitButton.sizeHint())
        quitButtonOffset = centerButton.frameGeometry().size().width() + 5
        quitButton.move(quitButtonOffset, 5)
        
    def centerWindow(self):
        appSize = self.frameGeometry()
        screenSize = QtGui.QDesktopWidget().availableGeometry().center()
        appSize.moveCenter(screenSize)
        self.move(appSize.topLeft())
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            'Remember to save your changes! Quit now?', QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    

class Table(QtSql.QSqlTableModel):
    
    def __init__(self, db):
        super(Table, self).__init__()

