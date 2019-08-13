from PyQt5 import QtWidgets
from ui_calculator import Ui_Calculator

class CalculatorWindow(QtWidgets.QMainWindow, Ui_Calculator):

    firstNum = None
    zeroDivision = False

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Ui == Ui_Calculator
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

        self.pushButton_plusMinus.clicked.connect(self.plusMinus_pressed)
        self.pushButton_percent.clicked.connect(self.percent_pressed)

        self.pushButton_add.clicked.connect(self.binary_operation_pressed)
        self.pushButton_substract.clicked.connect(self.binary_operation_pressed)
        self.pushButton_multiply.clicked.connect(self.binary_operation_pressed)
        self.pushButton_divide.clicked.connect(self.binary_operation_pressed)

        self.pushButton_equals.clicked.connect(self.equals_pressed)

        self.pushButton_add.setCheckable(True)         # ┐
        self.pushButton_substract.setCheckable(True)   # │╲ buttons can be checked
        self.pushButton_multiply.setCheckable(True)    # │╱ buttons can be checked
        self.pushButton_divide.setCheckable(True)      # ┘

        self.pushButton_clear.clicked.connect(self.clear_screen)

        self.pushButton_arrow.clicked.connect(self.rmv_last_digit)


    def digit_pressed(self):
        button = self.sender()
        if len(self.operation_screen.text().replace(',', '')) < 15:  # if there are less than 18 characters
            if (self.pushButton_add.isChecked() or self.pushButton_substract.isChecked() or  # if the operation buttons
                    self.pushButton_multiply.isChecked() or self.pushButton_divide.isChecked()):  # were pressed
                newLabel = self.operation_screen.text().replace(',', '') + button.text()
            else:  # if the operation buttons weren't pressed
                if self.zeroDivision:
                    newLabel = button.text()
                    self.zeroDivision = False
                else:
                    newLabel = self.operation_screen.text().replace(',', '') + button.text()

            self.operation_screen.setText(self.addComma(newLabel))
            self.fit_digits()

    def decimal_pressed(self):
        if len(self.operation_screen.text()) < 14:  # if there are less than 14 characters on the screen
            if '.' not in self.operation_screen.text():  # if there isn't another '.' on the screen
                if self.operation_screen.text() != "Error":  # if Error is on the screen
                    if '%' not in self.operation_screen.text():  # if there is % already on the screen
                        self.operation_screen.setText(self.operation_screen.text() + '.')
                        if self.operation_screen.text()[0] == '.':  # if the first character on the screen is '.'
                            self.operation_screen.setText('0.')
                else:  # if Error is on the screen
                    self.operation_screen.setText('0.')
                    self.zeroDivision = False

    def plusMinus_pressed(self):
        if self.operation_screen.text() == '-':  # if '-' is the only character on the screen
            self.operation_screen.setText('')

        elif self.operation_screen.text() != '':  # if the screen is not blank
            if self.operation_screen.text() != "Error":  # if Error isn't on the screen
                if '%' not in self.operation_screen.text():  # if % is not on the screen
                    labelNumber = float(self.operation_screen.text().replace(',', ''))

                    labelNumber = labelNumber * -1

                    newLabel = format(labelNumber, '.15g')

                    self.operation_screen.setText(self.addComma(newLabel))

                else:  # if % is the last character on the screen
                    if self.operation_screen.text().replace(',', '')[-1] == '%':  # if the last character on the screen is %
                        labelNumber = float(self.operation_screen.text().replace(',', '')[:-1])

                        labelNumber = labelNumber * -1

                        newLabel = format(labelNumber, '.15g') + '%'

                        self.operation_screen.setText(self.addComma(newLabel))
                    else:  # if there is a number after the %
                        percent_index = self.operation_screen.text().replace(',', '').index('%')
                        percent_number = self.operation_screen.text().replace(',', '')[percent_index:]
                        number = float(self.operation_screen.text().replace(',', '')[:percent_index])
                        number = number * -1

                        newLabel = format(number, '.15g') + percent_number
                        self.operation_screen.setText(self.addComma(newLabel))
            else:  # if Error is on the screen
                self.operation_screen.setText('-')
                self.zeroDivision = False

        else:  # if the screen is blank
            self.operation_screen.setText('-')

    def percent_pressed(self):
        if self.operation_screen.text() != '' and '%' not in self.operation_screen.text():  # if the screen is not blank and if
            labelPercent = self.operation_screen.text() + '%'                               # there isn't another %
            self.operation_screen.setText(labelPercent)
            self.fit_digits()

    def binary_operation_pressed(self):
        if self.operation_screen.text() != '' and self.operation_screen.text() != "Error":  # if the screen is not blank and
            if '%' not in self.operation_screen.text():                                     # Error isn't on the screen
                button = self.sender()

                self.firstNum = float(self.operation_screen.text().replace(',', ''))

                button.setChecked(True)

                self.operation_screen.setText("")
                print(self.firstNum)
            else:  # if percent is in first number
                button = self.sender()
                self.firstNum = float(self.calculate_percent())
                button.setChecked(True)
                self.operation_screen.setText("")
        elif self.operation_screen.text() == "Error":
            self.zeroDivision = False
            self.firstNum = None
            self.operation_screen.setText('')

    def equals_pressed(self):
        if (self.pushButton_add.isChecked() or self.pushButton_substract.isChecked() or  # if the operation buttons were pressed
                self.pushButton_multiply.isChecked() or self.pushButton_divide.isChecked()) and self.firstNum is not None:
            if self.operation_screen.text() != '':  # if second num isn't blank
                secondNum = float(self.operation_screen.text().replace(',', ''))
                print(secondNum)
                if self.pushButton_add.isChecked():  # add button was pressed
                    labelNumber = self.firstNum + secondNum
                    newLabel = format(labelNumber, '.15g')
                    self.operation_screen.setText(self.addComma(newLabel))
                    self.pushButton_add.setChecked(False)

                elif self.pushButton_substract.isChecked():  # subtract button was pressed
                    labelNumber = self.firstNum - secondNum
                    newLabel = format(labelNumber, '.15g')
                    self.operation_screen.setText(self.addComma(newLabel))
                    self.pushButton_substract.setChecked(False)

                elif self.pushButton_multiply.isChecked():  # multiply button was pressed
                    labelNumber = self.firstNum * secondNum
                    newLabel = format(labelNumber, '.15g')
                    print(newLabel)
                    self.operation_screen.setText(self.addComma(newLabel))
                    self.pushButton_multiply.setChecked(False)

                elif self.pushButton_divide.isChecked():  # divide button was pressed
                    if secondNum != 0:  # if the second num isn't 0
                        labelNumber = self.firstNum / secondNum
                        newLabel = format(labelNumber, '.15g')
                        self.operation_screen.setText(self.addComma(newLabel))
                        self.pushButton_divide.setChecked(False)
                    else:  # if the second num is 0
                        self.operation_screen.setText("Error")
                        self.pushButton_divide.setChecked(False)
                        self.zeroDivision = True
            else:  # if the second num is blank
                if self.firstNum is not None:
                    self.operation_screen.setText(format(self.firstNum, '.15g'))
                    self.pushButton_add.setChecked(False)
                    self.pushButton_substract.setChecked(False)
                    self.pushButton_divide.setChecked(False)
                    self.pushButton_multiply.setChecked(False)
        elif '%' in self.operation_screen.text():
            number = self.calculate_percent()
            self.operation_screen.setText(self.addComma(number))
            
    def clear_screen(self):
        self.operation_screen.setText('')
        self.operation_screen.setStyleSheet(" font: 75 50pt \"Calibri\";\n"
                                            " color: rgb(255, 255, 255);\n"
                                            " background-color: rgb(12, 16, 25);\n")
        self.firstNum = None

    def rmv_last_digit(self):
        if self.operation_screen.text() != "Error":  # if Error is on the screen
            last_digit_removed = self.operation_screen.text().replace(',', '')[:-1]
            self.operation_screen.setText(self.addComma(last_digit_removed))
            self.firstNum = None
            self.fit_digits()
        else:  # if Error is on the screen
            self.operation_screen.setText("")
            self.firstNum = None

    def calculate_percent(self):
        if self.operation_screen.text()[-1] == '%':  # if the last character on the screen is %
            number = float(self.operation_screen.text()[:-1].replace(',', ''))
            result = number * 0.01
            newLabel = format(result, '.15g')

        else:  # if there is a number after the %
            percent_index = self.operation_screen.text().replace(',', '').index('%')
            number = float(self.operation_screen.text().replace(',', '')[:percent_index])
            percent = float(self.operation_screen.text().replace(',', '')[percent_index + 1:])
            result = number / 100 * percent
            newLabel = format(result, '.15g')

        return newLabel

    def addComma(self, num):
        if '.' in str(num):  # if is float
            num = str(num)
            point_index = num.index('.')
            if '%' not in num:  # if % isn't in num
                post = num[point_index + 1:]
                num = num[:point_index]
            else:  # if % is in num
                percent_index = num.index('%')
                post = num[point_index + 1:percent_index]
                if num[-1] == '%':  # if % is the last character on the screen
                    num = num[:point_index] + '%'
                else:  # if there is a number after %
                    num = num[:point_index] + num[percent_index:]
            num = list(num)
            num.reverse()

            count1 = 0
            list1 = []
            count2 = 0
            list2 = []
            if '-' not in num:  # if number is positive
                if '%' not in num:  # if % isn't in num
                    for i in num:
                        count1 += 1
                        if count1 % 3 == 0:
                            list1.append(i)
                            list1.append(',')
                        else:
                            list1.append(i)

                    list1.reverse()

                    return ''.join(list1).strip(',') + '.' + post
                else:  # if % is in num
                    if num[0] == '%':  # if % was the last character in num
                        num.remove('%')
                        for i in num:
                            count1 += 1
                            if count1 % 3 == 0:
                                list1.append(i)
                                list1.append(',')
                            else:
                                list1.append(i)

                        list1.reverse()

                        return ''.join(list1).strip(',') + '.' + post + '%'
                    else:  # if there was a number after %
                        percent_index = num.index('%')
                        percent_number = num[0:percent_index]
                        for i in percent_number:
                            count2 += 1
                            if count2 % 3 == 0:
                                list2.append(i)
                                list2.append(',')
                            else:
                                list2.append(i)

                        list2.reverse()

                        del num[:percent_index + 1]
                        for i in num:
                            count1 += 1
                            if count1 % 3 == 0:
                                list1.append(i)
                                list1.append(',')
                            else:
                                list1.append(i)

                        list1.reverse()

                        return ''.join(list1).strip(',') + '.' + post + '%' + ''.join(list2).strip(',')

            else:  # if number is negative
                num.remove('-')
                if '%' not in num:  # if % isn't in num
                    for i in num:
                        count1 += 1
                        if count1 % 3 == 0:
                            list1.append(i)
                            list1.append(',')
                        else:
                            list1.append(i)

                    list1.reverse()

                    return '-' + ''.join(list1).strip(',') + '.' + post
                else:  # if % is in num
                    if num[0] == '%':  # if % was the last character in num
                        num.remove('%')
                        for i in num:
                            count1 += 1
                            if count1 % 3 == 0:
                                list1.append(i)
                                list1.append(',')
                            else:
                                list1.append(i)

                        list1.reverse()

                        return '-' + ''.join(list1).strip(',') + '.' + post + '%'
                    else:  # if there was a number after %
                        percent_index = num.index('%')
                        percent_number = num[0:percent_index]
                        for i in percent_number:
                            count2 += 1
                            if count2 % 3 == 0:
                                list2.append(i)
                                list2.append(',')
                            else:
                                list2.append(i)

                        list2.reverse()

                        del num[:percent_index + 1]
                        for i in num:
                            count1 += 1
                            if count1 % 3 == 0:
                                list1.append(i)
                                list1.append(',')
                            else:
                                list1.append(i)

                        list1.reverse()

                        return '-' + ''.join(list1).strip(',') + '.' + post + '%' + ''.join(list2).strip(',')
        else:  # if is int
            num = str(num)
            num = list(num)
            num.reverse()

            count1 = 0
            list1 = []
            count2 = 0
            list2 = []
            if '-' not in num:  # if number is positive
                if '%' not in num:  # if % isn't in num
                    for i in num:
                        count1 += 1
                        if count1 % 3 == 0:
                            list1.append(i)
                            list1.append(',')
                        else:
                            list1.append(i)

                    list1.reverse()

                    return ''.join(list1).strip(',')
                else:  # if % is in num
                    if num[0] == '%':  # if % was the last character in num
                        num.remove('%')
                        for i in num:
                            count1 += 1
                            if count1 % 3 == 0:
                                list1.append(i)
                                list1.append(',')
                            else:
                                list1.append(i)

                        list1.reverse()

                        return ''.join(list1).strip(',') + '%'
                    else:  # if there was a number after %
                        percent_index = num.index('%')
                        percent_number = num[0:percent_index]
                        for i in percent_number:
                            count2 += 1
                            if count2 % 3 == 0:
                                list2.append(i)
                                list2.append(',')
                            else:
                                list2.append(i)

                        list2.reverse()

                        del num[:percent_index + 1]
                        for i in num:
                            count1 += 1
                            if count1 % 3 == 0:
                                list1.append(i)
                                list1.append(',')
                            else:
                                list1.append(i)

                        list1.reverse()

                        return ''.join(list1).strip(',') + '%' + ''.join(list2).strip(',')

            else:  # if number is negative
                num.remove('-')
                if '%' not in num:  # if % isn't in num
                    for i in num:
                        count1 += 1
                        if count1 % 3 == 0:
                            list1.append(i)
                            list1.append(',')
                        else:
                            list1.append(i)

                    list1.reverse()

                    return '-' + ''.join(list1).strip(',')
                else:  # if % is in num
                    if num[0] == '%':  # if % was the last character in num
                        num.remove('%')
                        for i in num:
                            count1 += 1
                            if count1 % 3 == 0:
                                list1.append(i)
                                list1.append(',')
                            else:
                                list1.append(i)

                        list1.reverse()

                        return '-' + ''.join(list1).strip(',') + '%'
                    else:  # if there was a number after %
                        percent_index = num.index('%')
                        percent_number = num[0:percent_index]
                        for i in percent_number:
                            count2 += 1
                            if count2 % 3 == 0:
                                list2.append(i)
                                list2.append(',')
                            else:
                                list2.append(i)

                        list2.reverse()

                        del num[:percent_index + 1]
                        for i in num:
                            count1 += 1
                            if count1 % 3 == 0:
                                list1.append(i)
                                list1.append(',')
                            else:
                                list1.append(i)

                        list1.reverse()

                        return '-' + ''.join(list1).strip(',') + '%' + ''.join(list2).strip(',')

    def fit_digits(self):
        if len(self.operation_screen.text()) == 16:
            self.operation_screen.setStyleSheet(" font: 75 24pt \"Calibri\";\n"
                                                " color: rgb(255, 255, 255);\n"
                                                " background-color: rgb(12, 16, 25);\n")
        elif len(self.operation_screen.text()) == 15:
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



