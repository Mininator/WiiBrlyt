
import sys
import os
import subprocess

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QListWidget,
    QLabel,
    QComboBox,
    QProgressBar,
    QDialog
)
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon
from PyQt5.QtCore import Qt


class BenzinApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WiiBrlyt")
        self.setFixedSize(520, 500)
        self.files = []

        self.app_dir = self.get_app_dir()

        logo_path = self.resource_path(os.path.join("assets", "logo.png"))

        if os.path.isfile(logo_path):
            self.setWindowIcon(QIcon(logo_path))

        self.apply_dark_theme()
        self.init_ui()

    @staticmethod
    def get_app_dir():
        """Retourne le dossier de l'application."""
        if getattr(sys, "frozen", False):
            return os.path.dirname(os.path.abspath(sys.executable))

        return os.path.dirname(os.path.abspath(__file__))

    def apply_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 51, 153))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(0, 38, 102))
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
        palette.setColor(
            QPalette.Disabled,
            QPalette.WindowText,
            QColor(127, 127, 127)
        )

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
    
    
    def resource_path(self, relative_path):
        """Obtenir le chemin absolu aux ressources, fonctionne pour le développement et pour PyInstaller."""
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(base_path, relative_path)

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Fichiers sélectionnés :"))

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.mode_selector = QComboBox()
        self.mode_selector.addItems([
            "r (brlyt/brlan → xml)",
            "m (xml → brlyt/brlan)"
        ])

        layout.addWidget(
            QLabel("Choisir la commande à utiliser :")
        )
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
        mode = self.mode_selector.currentText().split()[0]

        if mode == "r":
            file_filter = (
                "Fichiers BRLYT/BRLAN (*.brlyt *.brlan)"
            )
            allowed_exts = (".brlyt", ".brlan")
        else:
            file_filter = (
                "Fichiers XMLYT/XMLAN (*.xmlyt *.xmlan)"
            )
            allowed_exts = (".xmlyt", ".xmlan")

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Choisir les fichiers à convertir",
            self.app_dir,
            file_filter
        )

        for file_path in files:
            file_path = os.path.abspath(file_path)

            if (
                file_path.lower().endswith(allowed_exts)
                and file_path not in self.files
            ):
                self.files.append(file_path)
                self.list_widget.addItem(file_path)

    def convert_files(self):
        if not self.files:
            QMessageBox.warning(
                self,
                "Aucun fichier",
                "Veuillez d'abord ajouter des fichiers."
            )
            return

        benzin_path = os.path.join(
            self.app_dir,
            "benzin.exe"
        )

        if not os.path.isfile(benzin_path):
            QMessageBox.critical(
                self,
                "Benzin introuvable",
                "Impossible de trouver benzin.exe.\n\n"
                "Placez benzin.exe à côté de WiiBrlyt.exe."
            )
            return

        command_mode = (
            self.mode_selector.currentText().split()[0]
        )

        files_to_convert = self.files.copy()

        self.progress_bar.setMaximum(len(files_to_convert))
        self.progress_bar.setValue(0)

        success_count = 0
        error_messages = []

        for full_path in files_to_convert:
            filename = os.path.basename(full_path)
            folder = os.path.dirname(os.path.abspath(full_path))
            base, ext = os.path.splitext(filename)
            ext = ext.lower()

            if command_mode == "r":
                extensions = {
                    ".brlyt": ".xmlyt",
                    ".brlan": ".xmlan"
                }
            else:
                extensions = {
                    ".xmlyt": ".brlyt",
                    ".xmlan": ".brlan"
                }

            if ext not in extensions:
                error_messages.append(
                    f"Extension non supportée : {filename}"
                )
                self.progress_bar.setValue(
                    self.progress_bar.value() + 1
                )
                QApplication.processEvents()
                continue

            output_file = base + extensions[ext]
            output_path = os.path.join(folder, output_file)

            try:
                result = subprocess.run(
                    [
                        benzin_path,
                        command_mode,
                        filename,
                        output_file
                    ],
                    cwd=folder,
                    capture_output=True,
                    text=True,
                    errors="replace",
                    timeout=120
                )

                if result.returncode != 0:
                    details = (
                        result.stderr.strip()
                        or result.stdout.strip()
                        or "Aucun détail fourni par Benzin."
                    )

                    error_messages.append(
                        f"Échec de conversion : {filename}\n"
                        f"{details}"
                    )

                    self.progress_bar.setValue(
                        self.progress_bar.value() + 1
                    )
                    QApplication.processEvents()
                    continue

                if not os.path.isfile(output_path):
                    error_messages.append(
                        "Le fichier de sortie n'a pas été créé : "
                        f"{output_file}"
                    )

                    self.progress_bar.setValue(
                        self.progress_bar.value() + 1
                    )
                    QApplication.processEvents()
                    continue

                # Retirer le chemin de la liste après conversion.
                if full_path in self.files:
                    self.files.remove(full_path)

                items = self.list_widget.findItems(
                    full_path,
                    Qt.MatchExactly
                )

                for item in items:
                    self.list_widget.takeItem(
                        self.list_widget.row(item)
                    )

                # Supprimer le fichier source après vérification.
                try:
                    os.remove(full_path)
                    success_count += 1

                except OSError as exc:
                    error_messages.append(
                        f"{filename} a été converti, mais le fichier "
                        f"source n'a pas pu être supprimé : {exc}"
                    )

            except subprocess.TimeoutExpired:
                error_messages.append(
                    f"Délai dépassé pendant la conversion : {filename}"
                )

            except OSError as exc:
                error_messages.append(
                    f"Erreur de lancement de Benzin pour "
                    f"{filename} : {exc}"
                )

            except Exception as exc:
                error_messages.append(
                    f"Erreur inattendue pour {filename} : {exc}"
                )

            self.progress_bar.setValue(
                self.progress_bar.value() + 1
            )
            QApplication.processEvents()

        self.progress_bar.setValue(0)

        if error_messages:
            QMessageBox.warning(
                self,
                "Résultat de la conversion",
                f"Conversions terminées avec suppression : "
                f"{success_count}\n\n"
                + "\n\n".join(error_messages)
            )
        else:
            QMessageBox.information(
                self,
                "Succès",
                f"{success_count} fichier(s) converti(s) "
                "avec succès."
            )

    def show_credits(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Crédits")
        dlg.setFixedSize(350, 220)

        dlg.setStyleSheet("""
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
            "<b>Interface graphique :</b> Mininator<br>"
            "<b>Version :</b> V1.0.1"
        )

        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Segoe UI", 12))
        layout.addWidget(label)

        btn = QPushButton("Fermer")
        btn.clicked.connect(dlg.accept)
        layout.addWidget(btn, alignment=Qt.AlignCenter)

        dlg.setLayout(layout)
        dlg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BenzinApp()
    window.show()
    sys.exit(app.exec_())
