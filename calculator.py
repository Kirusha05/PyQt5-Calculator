from PyQt5 import QtWidgets
from ui_calculator import Ui_Calculator

class CalculatorWindow(QtWidgets.QMainWindow, Ui_Calculator):

    firstNum = None

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()


        #Connect buttons
        self.pushButton_0.clicked.connect(self.digit_pressed)
        self.pushButton_1.clicked.connect(self.digit_pressed)
        self.pushButton_2.clicked.connect(self.digit_pressed)
        self.pushButton_3.clicked.connect(self.digit_pressed)
        self.pushButton_4.clicked.connect(self.digit_pressed)
        self.pushButton_5.clicked.connect(self.digit_pressed)
        self.pushButton_6.clicked.connect(self.digit_pressed)
        self.pushButton_7.clicked.connect(self.digit_pressed)
        self.pushButton_8.clicked.connect(self.digit_pressed)
        self.pushButton_9.clicked.connect(self.digit_pressed)

        self.pushButton_decimal.clicked.connect(self.decimal_pressed)

        self.pushButton_plusMinus.clicked.connect(self.unary_operation_pressed)
        self.pushButton_percent.clicked.connect(self.unary_operation_pressed)

        self.pushButton_add.clicked.connect(self.binary_operation_pressed)
        self.pushButton_substract.clicked.connect(self.binary_operation_pressed)
        self.pushButton_multiply.clicked.connect(self.binary_operation_pressed)
        self.pushButton_divide.clicked.connect(self.binary_operation_pressed)

        self.pushButton_equals.clicked.connect(self.equals_pressed)

        self.pushButton_add.setCheckable(True)
        self.pushButton_substract.setCheckable(True)
        self.pushButton_multiply.setCheckable(True)
        self.pushButton_divide.setCheckable(True)

        self.pushButton_clear.clicked.connect(self.clear_screen)

        self.pushButton_arrow.clicked.connect(self.rmv_last_digit)


    def digit_pressed(self, char=','):
        button = self.sender()

        if (self.pushButton_add.isChecked() or self.pushButton_substract.isChecked() or
                self.pushButton_multiply.isChecked() or self.pushButton_divide.isChecked()):
            newLabel = format(float(button.text()), '.15g')
        else:
            newLabel = format(float(self.operation_screen.text() + button.text()), '.15g')  # '.15g'

        if len(self.operation_screen.text()) < 15:
            self.operation_screen.setText(newLabel)
            self.fit_digits()

    def decimal_pressed(self):
        if len(self.operation_screen.text()) < 14:
            if '.' not in self.operation_screen.text():
                self.operation_screen.setText(self.operation_screen.text() + '.')
                if self.operation_screen.text()[0] == '.':
                    self.operation_screen.setText('0.')

    def unary_operation_pressed(self):
        button = self.sender()

        labelNumber = float(self.operation_screen.text())

        if button.text() == '+/-':
            labelNumber = labelNumber * -1
        else:  # buttontext == '%'
            labelNumber = labelNumber * 0.01

        newLabel = format(labelNumber, '.15g')
        self.operation_screen.setText(newLabel)

    def binary_operation_pressed(self):
        button = self.sender()

        self.firstNum = float(self.operation_screen.text())

        button.setChecked(True)

    def equals_pressed(self):

        secondNum = float(self.operation_screen.text())

        if self.pushButton_add.isChecked():
            labelNumber = self.firstNum + secondNum
            newLabel = format(labelNumber, '.15g')
            self.operation_screen.setText(newLabel)
            self.pushButton_add.setChecked(False)

        elif self.pushButton_substract.isChecked():
            labelNumber = self.firstNum - secondNum
            newLabel = format(labelNumber, '.15g')
            self.operation_screen.setText(newLabel)
            self.pushButton_substract.setChecked(False)

        elif self.pushButton_multiply.isChecked():
            labelNumber = self.firstNum * secondNum
            newLabel = format(labelNumber, '.15g')
            self.operation_screen.setText(newLabel)
            self.pushButton_multiply.setChecked(False)

        elif self.pushButton_divide.isChecked():
            labelNumber = self.firstNum / secondNum
            newLabel = format(labelNumber, '.15g')
            self.operation_screen.setText(newLabel)
            self.pushButton_divide.setChecked(False)

        self.fit_digits()

    def clear_screen(self):
        self.operation_screen.setText('')
        self.operation_screen.setStyleSheet(" font: 75 50pt \"Calibri\";\n"
                                            " color: rgb(255, 255, 255);\n"
                                            " background-color: rgb(12, 16, 25);\n")

    def rmv_last_digit(self):
        last_digit_removed = self.operation_screen.text()[:-1]
        self.operation_screen.setText(last_digit_removed)
        self.fit_digits()

    def fit_digits(self):
        if len(self.operation_screen.text()) == 15:
            self.operation_screen.setStyleSheet(" font: 75 26pt \"Calibri\";\n"
                                                " color: rgb(255, 255, 255);\n"
                                                " background-color: rgb(12, 16, 25);\n")
        elif len(self.operation_screen.text()) == 14:
            self.operation_screen.setStyleSheet(" font: 75 28pt \"Calibri\";\n"
                                                " color: rgb(255, 255, 255);\n"
                                                " background-color: rgb(12, 16, 25);\n")
        elif len(self.operation_screen.text()) == 13:
            self.operation_screen.setStyleSheet(" font: 75 31pt \"Calibri\";\n"
                                                " color: rgb(255, 255, 255);\n"
                                                " background-color: rgb(12, 16, 25);\n")
        elif len(self.operation_screen.text()) == 12:
            self.operation_screen.setStyleSheet(" font: 75 34pt \"Calibri\";\n"
                                                " color: rgb(255, 255, 255);\n"
                                                " background-color: rgb(12, 16, 25);\n")
        elif len(self.operation_screen.text()) == 11:
            self.operation_screen.setStyleSheet(" font: 75 36.4pt \"Calibri\";\n"
                                                " color: rgb(255, 255, 255);\n"
                                                " background-color: rgb(12, 16, 25);\n")
        elif len(self.operation_screen.text()) == 10:
            self.operation_screen.setStyleSheet(" font: 75 40pt \"Calibri\";\n"
                                                " color: rgb(255, 255, 255);\n"
                                                " background-color: rgb(12, 16, 25);\n")
        elif len(self.operation_screen.text()) == 9:
            self.operation_screen.setStyleSheet(" font: 75 45pt \"Calibri\";\n"
                                                    " color: rgb(255, 255, 255);\n"
                                                    " background-color: rgb(12, 16, 25);\n")
        else:
            self.operation_screen.setStyleSheet(" font: 75 50pt \"Calibri\";\n"
                                                " color: rgb(255, 255, 255);\n"
                                                " background-color: rgb(12, 16, 25);\n")





