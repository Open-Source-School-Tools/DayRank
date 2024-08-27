import sys
import statistics
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit,
    QMainWindow, QAction, QMessageBox
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class DayAssessmentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        # Central widget and layout
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        
        form_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        
        # Name input
        self.name_label = QLabel("Student's Name:")
        self.name_label.setAlignment(Qt.AlignLeft)
        self.name_edit = QTextEdit()
        self.name_edit.setFixedHeight(30)
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_edit)

        # Period input dropdowns
        self.periods = []
        options = ["Very Bad", "Bad", "OK", "Good", "Great"]
        for i in range(1, 9):
            label = QLabel(f"Period {i}:")
            label.setAlignment(Qt.AlignLeft)
            combo_box = QComboBox()
            combo_box.addItems(options)
            combo_box.setCurrentIndex(3)  # Default to "Good"
            form_layout.addWidget(label)
            form_layout.addWidget(combo_box)
            self.periods.append(combo_box)
        
        # Calculate button
        self.calc_button = QPushButton("Calculate")
        self.calc_button.clicked.connect(self.calculate_day)
        button_layout.addWidget(self.calc_button)
        
        # Result text box
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setFixedHeight(50)
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
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about_dialog)
        
        help_menu.addAction(about_action)
        
    def show_about_dialog(self):
        about_text = (
            "DayRank\n\n"
            "Version 1.0\n"
            "This tool helps students assess their school day by allowing them to rate each period "
            "and calculate the median score. The program provides feedback on how the day went based "
            "on the calculated score.\n\n"
            "Created by DevelopCMD (https://github.com/DevelopCMD) \n"
            "Part of the Open Source School Tools Collection"
        )
        QMessageBox.about(self, "About School Day Assessment", about_text)
        
    def calculate_day(self):
        score_mapping = {
            "Very Bad": 0,
            "Bad": 25,
            "OK": 50,
            "Good": 75,
            "Great": 100
        }
        
        scores = [score_mapping[period.currentText()] for period in self.periods]
        
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
                color = QColor(0, 255, 0)  # Green
            elif 75 <= median_score < 100:
                assessment = "Your day was good."
                color = QColor(144, 238, 144)  # Light green
            elif 50 <= median_score < 75:
                assessment = "Your day was okay."
                color = QColor(255, 255, 0)  # Yellow
            elif 25 <= median_score < 50:
                assessment = "Your day wasn't great."
                color = QColor(255, 165, 0)  # Orange
            else:
                assessment = "Your day was bad."
                color = QColor(255, 0, 0)  # Red
        
        # Update the result box
        self.result_box.setText(f"{self.name_edit.toPlainText()}'s median score for the day is: {median_score}%\n{assessment}")
        self.result_box.setStyleSheet(f"background-color: {color.name()}; color: black;")
        self.result_box.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DayAssessmentApp()
    sys.exit(app.exec_())

