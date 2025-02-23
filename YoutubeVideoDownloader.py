import sys
import os
import yt_dlp as ytdlp
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QFileDialog, QProgressBar, QHBoxLayout
from PyQt5.QtGui import QFont
from win10toast import ToastNotifier
import psutil
import time
import socket

# Socket zaman aşımı süresi ayarlanıyor
socket.setdefaulttimeout(120)  # 120 saniye

# Sistem kaynakları izleme
class SystemResourcesMonitor(QThread):
    update_cpu = pyqtSignal(str)
    update_ram = pyqtSignal(str)

    def run(self):
        while True:
            self.update_cpu.emit(f"CPU Kullanımı: {psutil.cpu_percent()}%")
            self.update_ram.emit(f"RAM Kullanımı: {psutil.virtual_memory().percent}%")
            time.sleep(2)

# İndirme işlemi için ayrı bir thread
class DownloadThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal()

    def __init__(self, playlist_urls, download_folder, quality):
        super().__init__()
        self.playlist_urls = playlist_urls
        self.download_folder = download_folder
        self.quality = quality
        self.toaster = ToastNotifier()

    def run(self):
        for playlist_url in self.playlist_urls:
            try:
                # Kalite seçimine göre formatı güncelleme
                ydl_opts = {
                    'outtmpl': os.path.join(self.download_folder, '%(playlist_title)s/%(title)s.%(ext)s'),
                    'noplaylist': True,  # Tüm playlist yerine tek tek video indirir
                    'progress_hooks': [self.progress_hook],
                    'socket_timeout': 120,  # Bağlantı zaman aşımı süresi
                    'concurrent_fragment_downloads': 3,  # Aynı anda 3 video indir
                }

                # Kalite seçenekleri
                if self.quality == "8K":
                    ydl_opts['format'] = 'bestaudio[ext=m4a]+bestvideo[height<=4320]'
                elif self.quality == "4K":
                    ydl_opts['format'] = 'bestaudio[ext=m4a]+bestvideo[height<=2160]'
                elif self.quality == "2K":
                    ydl_opts['format'] = 'bestaudio[ext=m4a]+bestvideo[height<=1440]'
                elif self.quality == "1080p":
                    ydl_opts['format'] = 'bestaudio[ext=m4a]+bestvideo[height<=1080]'
                elif self.quality == "720p":
                    ydl_opts['format'] = 'bestaudio[ext=m4a]+bestvideo[height<=720]'
                elif self.quality == "480p":
                    ydl_opts['format'] = 'bestaudio[ext=m4a]+bestvideo[height<=480]'
                elif self.quality == "360p":
                    ydl_opts['format'] = 'bestaudio[ext=m4a]+bestvideo[height<=360]'
                elif self.quality == "144p":
                    ydl_opts['format'] = 'bestaudio[ext=m4a]+bestvideo[height<=144]'

                with ytdlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([playlist_url])

            except Exception as e:
                print(f"İndirme sırasında hata oluştu: {str(e)}")

        self.finished_signal.emit()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', 1)
            percentage = (downloaded / total) * 100
            self.progress_signal.emit(int(percentage))  # Yüzdeyi pyqtSignal olarak ayarlıyoruz
        elif d['status'] == 'finished':
            self.toaster.show_toast("İndirme Tamamlandı", "Video başarıyla indirildi!", duration=10)


class DownloadApp(QWidget):
    def __init__(self):
        super().__init__()

        # Arayüz elemanları
        self.init_ui()

        # Sistem kaynakları izleme thread'i başlat
        self.system_monitor = SystemResourcesMonitor()
        self.system_monitor.update_cpu.connect(self.update_cpu_usage)
        self.system_monitor.update_ram.connect(self.update_ram_usage)
        self.system_monitor.start()

        self.download_thread = None

    def init_ui(self):
        self.setWindowTitle("YouTube Playlist İndirici")
        self.setGeometry(100, 100, 800, 750)
        self.setStyleSheet("background-color: #2F2F2F; color: white;")

        self.layout = QVBoxLayout()

        self.title_label = QLabel("YouTube Playlist İndirici")
        self.title_label.setFont(QFont("Helvetica", 18, QFont.Bold))
        self.layout.addWidget(self.title_label)

        # Playlist URL'leri girişi
        self.label_playlist_url = QLabel("YouTube Playlist URL'leri:")
        self.layout.addWidget(self.label_playlist_url)

        self.playlist_url_entry = QTextEdit(self)
        self.layout.addWidget(self.playlist_url_entry)

        # İndirilecek klasör seçimi
        self.label_folder_path = QLabel("İndirilecek Klasör:")
        self.layout.addWidget(self.label_folder_path)

        self.folder_path_entry = QLineEdit(self)
        self.layout.addWidget(self.folder_path_entry)

        self.browse_button = QPushButton("Klasör Seç", self)
        self.browse_button.clicked.connect(self.choose_folder)
        self.layout.addWidget(self.browse_button)

        # Kalite seçimi
        self.label_quality = QLabel("Kalite Seçin:")
        self.layout.addWidget(self.label_quality)

        self.quality_combobox = QComboBox(self)
        quality_choices = ["8K", "4K", "2K", "1080p", "720p", "480p", "360p", "144p"]
        self.quality_combobox.addItems(quality_choices)
        self.layout.addWidget(self.quality_combobox)

        # Başlat, Durdur, İptal Butonları
        self.start_button = QPushButton("İndirmeye Başla", self)
        self.start_button.clicked.connect(self.start_download)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("İndirmeyi Durdur", self)
        self.stop_button.clicked.connect(self.stop_download)
        self.stop_button.setEnabled(False)
        self.layout.addWidget(self.stop_button)

        self.cancel_button = QPushButton("İndirmeyi İptal Et", self)
        self.cancel_button.clicked.connect(self.cancel_download)
        self.cancel_button.setEnabled(False)
        self.layout.addWidget(self.cancel_button)

        # İlerleme barı
        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        # Sistem kaynakları bilgisi
        self.cpu_label = QLabel("CPU Kullanımı: 0%")
        self.layout.addWidget(self.cpu_label)

        self.ram_label = QLabel("RAM Kullanımı: 0%")
        self.layout.addWidget(self.ram_label)

        self.setLayout(self.layout)

    def choose_folder(self):
        folder_selected = QFileDialog.getExistingDirectory(self, "Klasör Seç")
        if folder_selected:
            self.folder_path_entry.setText(folder_selected)

    def start_download(self):
        playlist_urls = list(filter(None, map(str.strip, self.playlist_url_entry.toPlainText().split("\n"))))
        download_folder = self.folder_path_entry.text().strip()
        selected_quality = self.quality_combobox.currentText()

        if not playlist_urls or not download_folder:
            print("Lütfen geçerli URL'ler ve klasör yolu girin.")
            return

        self.download_thread = DownloadThread(playlist_urls, download_folder, selected_quality)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.finished_signal.connect(self.on_download_finished)
        self.download_thread.start()

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.cancel_button.setEnabled(True)

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def on_download_finished(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.cancel_button.setEnabled(False)

    def stop_download(self):
        if self.download_thread:
            self.download_thread.terminate()
            self.on_download_finished()

    def cancel_download(self):
        self.on_download_finished()

    def update_cpu_usage(self, cpu_usage):
        self.cpu_label.setText(cpu_usage)

    def update_ram_usage(self, ram_usage):
        self.ram_label.setText(ram_usage)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DownloadApp()
    window.show()
    sys.exit(app.exec_())
