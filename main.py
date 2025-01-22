from PyQt6 import QtCore, QtGui
from mainWindow import Ui_MainWindow
from addDialog import Ui_dialogAdd
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog ,QFileDialog
import sqlite3
import sys
import os


con = sqlite3.connect("items.db")
cur = con.cursor()
cur.execute("CREATE TABLE if not exists projects(fname PRIMARY KEY, fpath)")
class  Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_search.clicked.connect(self.clickHandler)
        self.listWidget.itemDoubleClicked.connect(self.clickItem)
        self.btn_addItem.clicked.connect(self.addItem)
        self.toolButton.clicked.connect(self.refresh)
        self.btn_delete.clicked.connect(self.deleteItem)
        self.refresh()

    
    def clickHandler():
        pass


    def deleteItem(self):
        itm=([item.text() for item in self.listWidget.selectedItems()])
        try:
            itm=itm[0]
            cur.execute("delete from  projects where fname = ?",(itm,))
            con.commit()
            self.refresh()
        except:
            print("!! no items selected")
        
    def clickItem(self,item):
        print("clicked on item "+item.text())
        currItem = item.text()
        data= cur.execute("SELECT fpath from projects where fname = ? ",(currItem,))
        data = data.fetchall() 
        data = data[0][0]
        pycmd= data.split("/")
        pycmd.remove(pycmd[-1])
        py=""
        for i in pycmd:
            py+=i+"/"
        if data[-2:] == "py":
            
            dir=os.listdir(py)
            for i in dir:
                if "env" in i :
                    env = i
                    command = py+"/{}/Scripts/python.exe ".format(env) +data
                    os.chdir(py)   
                    os.system(" start cmd.exe @cmd /c " +command)
                    return
            
            os.system(" start cmd.exe @cmd /c python " +data)
            return
        else:
            os.chdir(py)   
            os.system(" start cmd.exe @cmd /c " +data)


        


    def addItem(self):
        self.dialog = Dialog()  
        self.dialog.itemAdded.connect(self.refresh)
        self.dialog.show()
    
    def refresh(self):

        data = cur.execute("SELECT fname FROM projects")    
        data = data.fetchall()
        print(data)
        self.listWidget.clear()
        res = [list(ele) for ele in data]
        for i in data:
            self.listWidget.addItem(i[0])
            

class Dialog(QDialog, Ui_dialogAdd):

    itemAdded = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_add_add.clicked.connect(self.addItem)
        self.btn_browse.clicked.connect(self.browseItems)

    def browseItems(self):
        file = QFileDialog.getOpenFileName(self, 'Open file', '',"App (*)")
        self.filePath=fname=file[0]
        fname=fname.split("/")
        fname=fname[-1]
        self.lineEdit_2.setText(fname)
        

    def addItem(self):
        filename = self.addItem_lineEdit_2.text()
        qry="Insert into projects values(?,?)"
        para=(filename,self.filePath)
        try:
            cur.execute(qry,para)
            con.commit()
            self.itemAdded.emit()
        except Exception as e:  
            print(e)
        
        self.close()
        

if __name__=="__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())