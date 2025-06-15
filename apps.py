import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox,
    QFileDialog, QListWidget, QLabel, QComboBox, QProgressBar, QDialog
)
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon
from PyQt5.QtCore import Qt


class BenzinApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WiiBrlyt")
        self.setGeometry(300, 200, 520, 500)
        self.setMinimumSize(520, 500)
        self.setMaximumSize(520, 500)
        self.files = []

        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))

        self.apply_dark_theme()
        self.init_ui()

    def apply_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 51, 153))  # Blue background
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(0, 38, 102))  # Slightly darker blue
        palette.setColor(QPalette.AlternateBase, QColor(0, 51, 153))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(0, 51, 153))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.white)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
        QApplication.instance().setPalette(palette)

        self.setStyleSheet("""
            QWidget {
                background-color: #181818;
                color: #fff;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton {
                border-radius: 12px;
                background-color: #222;
                color: white;
                padding: 8px 24px;
                border: 1px solid #444;
            }
            QPushButton:hover {
                background-color: #292929;
                border: 1px solid #2980b9;
            }
            QListWidget, QLabel, QComboBox, QProgressBar {
                background-color: #181818;
                color: #fff;
                border: 1px solid #333;
                padding: 4px;
            }
            QProgressBar {
                border-radius: 10px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2980b9;
                border-radius: 10px;
            }
        """)

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Fichiers sélectionnés :"))
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["r (brlyt/brlan → xml)", "m (xml → brlyt/brlan)"])
        layout.addWidget(QLabel("Choisir la commande à utiliser :"))
        layout.addWidget(self.mode_selector)

        btn_add = QPushButton("+ Ajouter des fichiers")
        btn_add.clicked.connect(self.add_files)
        layout.addWidget(btn_add)

        btn_convert = QPushButton("Convertir les fichiers")
        btn_convert.clicked.connect(self.convert_files)
        layout.addWidget(btn_convert)

        btn_credits = QPushButton("Crédits")
        btn_credits.clicked.connect(self.show_credits)
        layout.addWidget(btn_credits)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def add_files(self):
        mode = self.mode_selector.currentText().split(" ")[0]
        if mode == "r":
            file_filter = "Fichiers brlyt/brlan (*.brlyt *.brlan)"
            allowed_exts = (".brlyt", ".brlan")
        else:
            file_filter = "Fichiers xmlyt/xmlan (*.xmlyt *.xmlan)"
            allowed_exts = (".xmlyt", ".xmlan")

        files, _ = QFileDialog.getOpenFileNames(self, "Choisir les fichiers à convertir", "", file_filter)
        for file in files:
            if file.lower().endswith(allowed_exts) and file not in self.files:
                self.files.append(file)
                self.list_widget.addItem(file)

    def convert_files(self):
        if not self.files:
            QMessageBox.warning(self, "Aucun fichier", "Veuillez d'abord ajouter des fichiers.")
            return

        command_mode = self.mode_selector.currentText().split(" ")[0]

        total_steps = len(self.files) * 3
        self.progress_bar.setMaximum(total_steps)
        self.progress_bar.setValue(0)

        all_success = True
        error_messages = []

        for full_path in self.files:
            folder = os.path.dirname(full_path)
            filename = os.path.basename(full_path)
            base, ext = os.path.splitext(filename)
            ext = ext.lower().strip(".")
            output_file = ""

            self.progress_bar.setValue(self.progress_bar.value() + 1)
            QApplication.processEvents()

            if command_mode == "r":
                if ext == "brlyt":
                    output_file = base + ".xmlyt"
                elif ext == "brlan":
                    output_file = base + ".xmlan"
                else:
                    error_messages.append(f"Extension non supportée pour 'r' : .{ext}")
                    all_success = False
                    continue
            elif command_mode == "m":
                if ext == "xmlyt":
                    output_file = base + ".brlyt"
                elif ext == "xmlan":
                    output_file = base + ".brlan"
                else:
                    error_messages.append(f"Extension non supportée pour 'm' : .{ext}")
                    all_success = False
                    continue

            cwd = os.getcwd()
            os.chdir(folder)
            try:
                result = subprocess.run(
                    ["benzin.exe", command_mode, filename, output_file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                exit_code = result.returncode
            except Exception as e:
                error_messages.append(f"Erreur lors de l'exécution de la commande : {e}")
                all_success = False
                exit_code = 1
            finally:
                os.chdir(cwd)

            self.progress_bar.setValue(self.progress_bar.value() + 1)
            QApplication.processEvents()

            if exit_code != 0:
                error_messages.append(f"Échec de la commande : {filename}")
                all_success = False
                continue

            try:
                os.remove(full_path)
            except Exception as e:
                error_messages.append(f"Suppression échouée pour {filename} : {e}")
                all_success = False

            self.progress_bar.setValue(self.progress_bar.value() + 1)
            QApplication.processEvents()

        self.files.clear()
        self.list_widget.clear()

        if all_success:
            QMessageBox.information(self, "Succès", "Tous les fichiers ont été convertis et supprimés avec succès.")
        else:
            msg = "Certaines erreurs sont survenues :\n" \
                  "Vérifiez les fichiers présents dans le dossier de l'application.\n\n" + "\n".join(error_messages)
            QMessageBox.warning(self, "Attention", msg)

        self.progress_bar.setValue(0)

    def show_credits(self):
        class CreditsDialog(QDialog):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setWindowTitle("Crédits")
                self.setFixedSize(350, 220)
                self.setStyleSheet("""
                    QDialog {
                        background-color: #181818;
                        border-radius: 16px;
                    }
                    QLabel {
                        color: #fff;
                        font-size: 15px;
                        padding: 8px;
                    }
                    QPushButton {
                        border-radius: 10px;
                        background-color: #222;
                        color: white;
                        padding: 6px 18px;
                        border: 1px solid #444;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                        border: 1px solid #2980b9;
                    }
                """)
                layout = QVBoxLayout()
                label = QLabel(
                    "<b>WiiBrlyt</b><br>"
                    "<b>Développé avec Benzin :</b> CountZero<br>"
                    "<b>Développé avec GUI : </b>Mininator<br>"
                    "<b>Version :</b> 1.0.0<br>"
                )
                label.setAlignment(Qt.AlignCenter)
                label.setFont(QFont("Segoe UI", 12))
                layout.addWidget(label)
                btn = QPushButton("Fermer")
                btn.clicked.connect(self.accept)
                layout.addWidget(btn, alignment=Qt.AlignCenter)
                self.setLayout(layout)

        dlg = CreditsDialog(self)
        dlg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BenzinApp()
    window.show()
    sys.exit(app.exec_())
