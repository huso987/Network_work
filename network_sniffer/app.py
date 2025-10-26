import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget, QComboBox, QLabel, QFileDialog
)
from sniffer import PacketSniffer

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Wireshark ")
        self.setGeometry(200, 200, 1000, 600)

        self.packets = []
        self.sniffer = None

        layout = QVBoxLayout()

        self.filter_box = QComboBox()
        self.filter_box.addItems(["All", "TCP", "UDP", "ICMP"])
        layout.addWidget(QLabel("Protocol Filter:"))
        layout.addWidget(self.filter_box)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Time", "Source", "Destination", "Protocol", "Length"])
        layout.addWidget(self.table)

        self.btn_start = QPushButton("Start Sniffing")
        self.btn_start.clicked.connect(self.start_sniffing)
        layout.addWidget(self.btn_start)

        self.btn_stop = QPushButton("Stop Sniffing")
        self.btn_stop.clicked.connect(self.stop_sniffing)
        layout.addWidget(self.btn_stop)

        self.btn_save = QPushButton("Save as CSV")
        self.btn_save.clicked.connect(self.save_csv)
        layout.addWidget(self.btn_save)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_sniffing(self):
        proto = self.filter_box.currentText()
        proto = None if proto == "All" else [proto]

        self.sniffer = PacketSniffer(self.add_packet, "your_interface", proto)
        self.sniffer.start_sniffing()
        self.btn_start.setEnabled(False)

    def stop_sniffing(self):
        if self.sniffer:
            self.sniffer.stop_sniffing()
        self.btn_start.setEnabled(True)

    def add_packet(self, packet):
        self.packets.append(packet)
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col, data in enumerate(packet):
            self.table.setItem(row, col, QTableWidgetItem(str(data)))
        self.table.scrollToBottom()

    def save_csv(self):
        if not self.packets:
            print("No packets to save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Packets", "", "CSV Files (*.csv)")
        if not file_path:
            return

        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Time", "Source", "Destination", "Protocol", "Length"])
            writer.writerows(self.packets)

        print(f"✅ Saved: {file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = App()
    ui.show()
    sys.exit(app.exec_())
