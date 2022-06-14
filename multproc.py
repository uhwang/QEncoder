from PyQt4 import QtCore
from PyQt4 import QtGui 
import sys, re

from collections import OrderedDict
from functools import partial

_ydl_const_error = "ERROR"
_ydl_const_exist = "already been downloaded"

_exception_msg = lambda e : "=> {0} : {1}".format(type(e).__name__, str(e))
_find_percent = re.compile("\d+.\d+\%", re.MULTILINE )
_find_ydl_error = lambda x: x.strip() if x.find("ERROR:") >= 0 else None
_file_exist = lambda x: True if x.find(_ydl_const_exist) >= 0 else False

#-------------------------------------------------------------------------------
# Reference: 
# https://stackoverflow.com/questions/50930792/pyqt-multiple-qprocess-and-output
#-------------------------------------------------------------------------------

class QProcessProgressive(QtCore.QProcess):
    def __init__(self, key):
        super(QProcessProgressive, self).__init__()
        self.key = key
        self.step = 0
        self.file_exist = False
        self.error = False
        self.status = ""
        
class ProcessController(QtCore.QObject):

    status_changed = QtCore.pyqtSignal(QtCore.QObject)

    def __init__(self, job_list, formula = "Proc %d"):
        super(ProcessController, self).__init__()
        self.job_list = job_list
        self.nproc = 0
        self.proc_pool = None
        self.key_formula = formula

    def start(self):
        self.proc_pool = OrderedDict()
        self.nproc = 0
        
        for k, _ in enumerate(self.job_list):
            key = self.key_formula%k
            proc = QProcessProgressive(key)
            proc.setReadChannel(QtCore.QProcess.StandardOutput)
            proc.setProcessChannelMode(QtCore.QProcess.MergedChannels)
            QtCore.QObject.connect(proc, QtCore.SIGNAL("finished(int)"), partial(self.check_finshed,key))
            QtCore.QObject.connect(proc, QtCore.SIGNAL("readyRead()"), partial(self.read_data,key))
            self.proc_pool[key] = proc
            self.nproc += 1

        for j, p in zip(self.job_list, self.proc_pool.values()):
            p.start(j[0], j[1])
            
    def check_finshed(self, key):
        self.nproc -= 1
        if not self.proc_pool[key].file_exist:
            self.proc_pool[key].status = "finished"
            self.status_changed.emit(self.proc_pool[key])
        
    def kill(self):
        for p in self.proc_pool.values():
            if p: p.kill()
        
    def read_data(self, key):
        try:
            data = str(self.proc_pool[key].readLine(), 'cp949') # Windows only            
        except Exception as e:
            print(_exception_msg(e), data)
            return
            
        proc = self.proc_pool[key]
        if _find_ydl_error(data):
            proc.error = True
            proc.status = data
            self.status_changed.emit(proc)
            return
            
        if _file_exist(data):
            proc.file_exist = True
            proc.status = "already exist"
            self.status_changed.emit(proc)
            #print(key, " ... already exist")
            return
                       
        match = _find_percent.search(data)
        if match:
            self.proc_pool[key].step = int(float(match.group(0)[:-1]))

class TrackProcess(QtGui.QDialog):
    def __init__(self, proc_ctrl):
        super(TrackProcess, self).__init__()
        self.proc_ctrl = proc_ctrl
        self.initUI()
        
    def initUI(self):
        import icon_exit
        import icon_download
        import icon_cancel
        layout = QtGui.QFormLayout()
        
        grid = QtGui.QGridLayout()
        self.progress_bars = OrderedDict()
        
        for k, _ in enumerate(self.proc_ctrl.job_list):
            key = self.proc_ctrl.key_formula%k
            grid.addWidget(QtGui.QLabel(key), k, 0)
            p_bar = QtGui.QProgressBar()
            self.progress_bars[key] = p_bar
            grid.addWidget(p_bar, k, 1)
        
        self.start_btn = QtGui.QPushButton()
        self.start_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_download.table)))
        self.start_btn.setIconSize(QtCore.QSize(32,32))
        self.connect(self.start_btn, QtCore.SIGNAL('clicked()'), self.start_download)
        
        self.cancel_btn = QtGui.QPushButton()
        self.cancel_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_cancel.table)))
        self.cancel_btn.setIconSize(QtCore.QSize(32,32))
        self.connect(self.cancel_btn, QtCore.SIGNAL('clicked()'), self.cancel_download)

        self.exit_btn = QtGui.QPushButton()
        self.exit_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_exit.table)))
        self.exit_btn.setIconSize(QtCore.QSize(32,32))
        self.connect(self.exit_btn, QtCore.SIGNAL('clicked()'), self.exit_download)
        
        option = QtGui.QHBoxLayout()
        option.addWidget(self.start_btn)
        option.addWidget(self.cancel_btn)
        option.addWidget(self.exit_btn)
        
        layout.addRow(grid)
        layout.addRow(option)
        
        self.timer = QtCore.QBasicTimer()
        self.setLayout(layout)
    
    def timerEvent(self, e):
        if self.proc_ctrl.nproc <= 0:
            for p_bar in self.progress_bars.values():
                p_bar.setValue(100)
            self.timer.stop()
            self.proc_ctrl.kill()
            self.enable_download_buttons()
            print("=== Download Done! ===")
            return
            
        procs = self.proc_ctrl.proc_pool
        for p in procs.values():
            self.progress_bars[p.key].setValue(p.step)
            
    def start_download(self):
        for p_bar in self.progress_bars.values():
            p_bar.setValue(0)
            p_bar.setTextVisible(True)
            p_bar.setFormat("Download: %p%")
        self.disable_download_buttons()
        #self.download_t1 = time.time()
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)
            
        try:
            #self.global_message.appendPlainText(self.cmd_to_msg(sublist[0], sublist[1]))
            self.proc_ctrl.start()
        except (IOError, OSError) as err:
            QtGui.QMessageBox.question(self, 'Error', "%s"%err)
            #self.global_message.appendPlainText("=> Error: %s"%err)
            self.enable_single_download_buttons()        
            
    def disable_download_buttons(self):
        self.start_btn.setEnabled(False)

    def enable_download_buttons(self):
        self.start_btn.setEnabled(True)
        
    def cancel_download(self):
        self.proc_ctrl.kill()
        self.enable_download_buttons()
        
    def exit_download(self):
        self.proc_ctrl.kill()
        self.reject()
        
class QYoutubeDownloader(QtGui.QWidget):
    def __init__(self):
        super(QYoutubeDownloader, self).__init__()
        self.initUI()
        
    def initUI(self):
        layout = QtGui.QFormLayout()
      
        self.start_btn = QtGui.QPushButton("start")
        layout.addWidget(self.start_btn)
        self.connect(self.start_btn, QtCore.SIGNAL('clicked()'), self.start_download)
        
        self.setLayout(layout)
        self.show()
        
    def start_download(self):
        job_list = [
            ["youtube-dl", ["-f", "251", "https://youtu.be/giRY3ZSph2o"]],
            #["youtube-dl", ["-f", "18", "https://youtu.be/sfIPZ4134WU"]],
            ["youtube-dl", ["-f", "140", "https://youtu.be/giRY3ZSph2o"]]
            #["youtube-dl", ["-f", "18", "https://youtu.be/qz9QJoxFFqg"]]
            ] 
        pc = ProcessController(job_list)
        tp = TrackProcess(pc)
        pc.status_changed.connect(self.print_status)
        tp.exec_()
        
    def print_status(self, proc):
        print(proc.status)
        
        
def main():
    app = QtGui.QApplication(sys.argv)
    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(u'Plastique'))
    lppt = QYoutubeDownloader()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()	