import rcd30
from rcd30 import ImageSession
from PySide import QtGui, QtCore

class Dialog(QtGui.QDialog):

    # Constructor function
    def __init__(self):
        super(Dialog, self).__init__()

        self.createMenu()
        self.createHorizontalGroupBox()
        self.createGridGroupBox()

        self.sessList = QtGui.QListView()
        self.sessModel = QtGui.QStandardItemModel(self.sessList)

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setMenuBar(self.menuBar)
        mainLayout.addWidget(self.gridGroupBox)
        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(self.sessList)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Frame Pro Processing")

    def createMenu(self):
        self.menuBar = QtGui.QMenuBar()

        self.fileMenu = QtGui.QMenu("&File", self)
        self.exitAction = self.fileMenu.addAction("E&xit")
        self.menuBar.addMenu(self.fileMenu)

        self.exitAction.triggered.connect(self.accept)

    def createGridGroupBox(self):
        self.gridGroupBox = QtGui.QGroupBox("Input Parameters")
        layout = QtGui.QGridLayout()

        self.rawDirLabel = QtGui.QLabel("Browse Raw Location")
        self.dwDirLabel = QtGui.QLabel("Download Location")
        self.dsDirLabel = QtGui.QLabel("Dataset Location")

        self.rawDirLineEdit = QtGui.QLineEdit()
        self.dwDirLineEdit = QtGui.QLineEdit()
        self.dsDirLineEdit = QtGui.QLineEdit()

        self.rawDirButton = QtGui.QPushButton('Browse', self)
        self.rawDirButton.clicked.connect(self.rawDirDialog)
        self.dwDirButton = QtGui.QPushButton('Browse', self)
        self.dwDirButton.clicked.connect(self.dwDirDialog)
        self.dsDirButton = QtGui.QPushButton('Browse', self)
        self.dsDirButton.clicked.connect(self.dsDirDialog)

        layout.addWidget(self.rawDirLabel,0,0)
        layout.addWidget(self.rawDirLineEdit,0,1)
        layout.addWidget(self.rawDirButton,0,2)
        layout.addWidget(self.dwDirLabel,1,0)
        layout.addWidget(self.dwDirLineEdit,1,1)
        layout.addWidget(self.dwDirButton,1,2)
        layout.addWidget(self.dsDirLabel,2,0)
        layout.addWidget(self.dsDirLineEdit,2,1)
        layout.addWidget(self.dsDirButton,2,2)

        self.gridGroupBox.setLayout(layout)

    def createHorizontalGroupBox(self):
        self.horizontalGroupBox = QtGui.QGroupBox("Read In Sessions")
        layout = QtGui.QHBoxLayout()
        button = QtGui.QPushButton("Read Sessions")
        layout.addWidget(button)
        self.horizontalGroupBox.setLayout(layout)
        button.clicked.connect(self.returnSess)

    def rawDirDialog(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        fileDialog = QtGui.QFileDialog.getExistingDirectory(self,
                "Flight Date Raw Folder",
                self.rawDirLabel.text(), options)
        self.rawDirLineEdit.setText(str(fileDialog))
        self.Dir = str(self.rawDirLineEdit.text())
        print self.Dir

    def dwDirDialog(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        fileDialog = QtGui.QFileDialog.getExistingDirectory(self,
                "Download Folder",
                self.dwDirLabel.text(), options)
        self.dwDirLineEdit.setText(str(fileDialog))
        self.Dir = str(self.dwDirLineEdit.text())
        print self.Dir

    def dsDirDialog(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        fileDialog = QtGui.QFileDialog.getExistingDirectory(self,
                "Main Dataset Folder",
                self.dsDirLabel.text(), options)
        self.dsDirLineEdit.setText(str(fileDialog))
        self.Dir = str(self.dsDirLineEdit.text())
        print self.Dir

    def returnSess(self):
        rawDir = self.rawDirLineEdit.text()
        sessIDs = rcd30.getSessionIDs(rawDir)
        print sessIDs
        for sessions in sessIDs:
            # Create an item/session from the session ID list
            self.item = QtGui.QStandardItem(sessions)

            # add a checkbox because we may only want to process only a few sessions
            self.item.setCheckable(True)

            # Add the item to our session list model
            self.sessModel.appendRow(self.item)

        # Apply our  model to the list view
        self.sessList.setModel(self.sessModel)
        self.sessModel.itemChanged.connect(self.on_item_changed)

        #return sessIDs

    def on_item_changed(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            print item.text() + " is checked, will process this Session"
        else:
            item.checkState() == QtCore.Qt.Unchecked
            print item.text() + " this Session was unchecked and will not be processed"
            return


