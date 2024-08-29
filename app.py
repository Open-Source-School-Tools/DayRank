import sys
import statistics
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit,
    QMainWindow, QAction, QMessageBox, QFileDialog, QGridLayout
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from qt_material import apply_stylesheet

# 
#    - - -  D A Y R A N K  - - -
#
# Property of DayRank - This code is licensed under GPL

class DayAssessmentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        # Central widget and layout
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)
        form_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        grid_layout = QGridLayout()
        self.setCentralWidget(central_widget)
        
        # Name input
        self.name_label = QLabel("Student's Name:")
        self.name_label.setAlignment(Qt.AlignLeft)
        self.name_edit = QTextEdit()
        self.name_edit.setFixedHeight(35)
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_edit)
        
        # Create a layout for headers
        header_subject = QLabel("Subject")
        header_rating = QLabel("Rating")
        grid_layout.addWidget(header_subject, 0, 0)  # Add Subject header
        grid_layout.addWidget(header_rating, 0, 1)
        
        # Period input dropdowns
        self.periods = []
        self.subjects = []
        subject_options = ["Math", "Science", "English", "History", "Art", "Physical Education", "Music", "Other"]
        rating_options = ["Very Bad", "Bad", "OK", "Good", "Great"]
        
        for i in range(1, 9):
            period_layout = QHBoxLayout()  # Horizontal layout for each period

            subject_combo_box = QComboBox()
            subject_combo_box.addItems(subject_options)
            self.subjects.append(subject_combo_box)
            
            rating_combo_box = QComboBox()
            rating_combo_box.addItems(rating_options)
            rating_combo_box.setCurrentIndex(3)  # Default to "Good"
            self.periods.append(rating_combo_box)
            
            period_label = QLabel(f"Period {i}:")
            period_label.setAlignment(Qt.AlignLeft)

            period_layout.addWidget(period_label)
            period_layout.addWidget(subject_combo_box)
            period_layout.addWidget(rating_combo_box)

            form_layout.addLayout(period_layout)
            
        
        # Calculate button
        self.calc_button = QPushButton("Calculate")
        self.calc_button.clicked.connect(self.calculate_day)
        button_layout.addWidget(self.calc_button)
        
        # Save button
        self.save_button = QPushButton("Save Result to Text File")
        self.save_button.clicked.connect(self.save_result)
        button_layout.addWidget(self.save_button)
        
        # Result text box
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setFixedHeight(70)
        self.result_box.hide()
        
        # Adding layouts to main layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.result_box)
        
        # Menu bar and About action
        self.create_menu_bar()

        # Window settings
        self.setWindowTitle("DayRank")
        self.setGeometry(300, 300, 300, 400)
        self.show()
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # Help Menu
        help_menu = menubar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        
        # Adding theme toggle
        view_menu = menubar.addMenu("View")
        theme_toggle = QAction("Toggle Dark Mode", self, checkable=True)
        theme_toggle.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(theme_toggle)
        
    def toggle_dark_mode(self, checked):
        if checked:
            apply_stylesheet(app, theme='dark_blue.xml')
        else:
            apply_stylesheet(app, theme='light_blue.xml')
        
    def show_about_dialog(self):
        logo_path = "Res/logodarb.png"
        qt_logo_path = "Res/qt.png"
        about_text = (
            f"<div style='display: flex; align-items: center;'>"
            f"<img src='{logo_path}' height='75' style='margin-right: 15px;'>"
            f"<div>"
            f"<h1 style='margin: 0; font-size: 24px; font-weight: bold;'>DayRank</h1>"
            f"<p>Version Dev</p>"
            f"<p>This tool helps students assess their school day by allowing them to rate each period "
            f"and calculate the median score. The program provides feedback on how the day went based "
            f"on the calculated score.</p>"
            f"<p>Created by DevelopCMD (https://github.com/DevelopCMD)</p>"
            f"<p>Part of the Open Source School Tools Collection</p>"
            f"<p>This program is licensed under the GNU-GPL license.</p>"
            f"<div style='display: flex; align-items: center; margin-top: 20px;'>"
            f"<img src='{qt_logo_path}' height='50' style='margin-right: 10px;'>"
            f"<p>Made with <b>Qt</b></p>"
            f"<p>This program uses Qt version 5.15.11. "
            f"Qt and the Qt logo are trademarks of The Qt Company Ltd.</p>"
            f"</div>"
            f"</div>"
            f"</div>"
            f"</div>"
            
        )
        QMessageBox.about(self, "About DayRank", about_text)
        
    def calculate_day(self):
        score_mapping = {
            "Very Bad": 0,
            "Bad": 25,
            "OK": 50,
            "Good": 75,
            "Great": 100
        }
    
        scores = [score_mapping[period.currentText()] for period in self.periods]
        subjects = [subject.currentText() for subject in self.subjects]
        
        # Check if there was any "Very Bad" period
        if any(score == 0 for score in scores):
            # If there is a "Very Bad" period, penalize the median score
            median_score = max(0, statistics.median(scores) - 25)  # Apply a penalty
            assessment = "Your day was significantly impacted with very bad period(s)."
            color = QColor(255, 0, 0)  # Red
        else:
            median_score = statistics.median(scores)
            if median_score == 100:
                assessment = "Your day was excellent!"
                color = QColor(25, 200, 30)  # Green
            elif 75 <= median_score < 100:
                assessment = "Your day was good."
                color = QColor(85, 195, 90)  # Light green
            elif 50 <= median_score < 75:
                assessment = "Your day was okay."
                color = QColor(185, 175, 15)  # Yellow
            elif 25 <= median_score < 50:
                assessment = "Your day wasn't great."
                color = QColor(215, 120, 15)  # Orange
            else:
                assessment = "Your day was bad."
                color = QColor(215, 15, 15)  # Red
        
        # Format the result
        result_text = f"{self.name_edit.toPlainText()}'s DayRank Report:\n\n"
        for i, (subject, score) in enumerate(zip(subjects, scores), start=1):
            result_text += f"Period {i} - {subject}: {score}%\n"
        result_text += f"\nMedian Score: {median_score}%\n{assessment}"
        
        # Update the result box
        self.result_box.setText(f"{self.name_edit.toPlainText()}'s median score for the day is: {median_score}%\n{assessment}")
        self.result_box.setStyleSheet(f"background-color: {color.name()}; color: white;")
        self.result_box.show()
        
        # Store the result for saving
        self.result_to_save = result_text

    def save_result(self):
        if hasattr(self, 'result_to_save'):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getSaveFileName(self, "Save DayRank Report", "", "Text Files (*.txt);;All Files (*)", options=options)
            if file_name:
                with open(file_name, 'w') as file:
                    file.write(self.result_to_save)
                QMessageBox.information(self, "Saved", "DayRank Report saved successfully.")
        else:
            QMessageBox.warning(self, "Error", "No result to save. Please calculate the day first.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml')
    ex = DayAssessmentApp()
    sys.exit(app.exec_())
