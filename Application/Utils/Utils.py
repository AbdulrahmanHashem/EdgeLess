from PyQt6.QtWidgets import QKeySequenceEdit, QDoubleSpinBox, QSpinBox, QLabel, QLineEdit, QTextEdit, QCheckBox, \
    QRadioButton, QComboBox


def get_QWidget_content(widget):
    if [QKeySequenceEdit].__contains__(type(widget)):
        return widget.keySequence().toString()
    elif [QSpinBox, QDoubleSpinBox].__contains__(type(widget)):
        return widget.value()
    elif [QLineEdit, QLabel].__contains__(type(widget)):
        return widget.text()
    elif [QTextEdit].__contains__(type(widget)):
        return widget.toPlainText()
    elif [QRadioButton, QCheckBox].__contains__(type(widget)):
        return widget.isChecked()
    elif [QComboBox].__contains__(type(widget)):
        current = widget.currentText()
        widget.removeItem(widget.currentIndex())
        content_list = [current]
        for index in range(widget.__len__()):
            content_list.append(widget.itemText(index))
        widget.clear()
        widget.addItems(content_list)
        return content_list
    else:
        print(widget, "Widget Not Supported << Get")
        return None


def set_QWidget_content(widget, new_value):
    if [QKeySequenceEdit].__contains__(type(widget)):
        widget.setKeySequence(new_value)
    elif [QSpinBox, QDoubleSpinBox].__contains__(type(widget)):
        widget.setValue(new_value)
    elif [QLineEdit, QLabel, QTextEdit].__contains__(type(widget)):
        widget.setText(new_value)
    elif [QRadioButton, QCheckBox].__contains__(type(widget)):
        widget.setChecked(new_value)
    elif [QComboBox].__contains__(type(widget)):
        widget.clear()
        widget.addItems(new_value)
    else:
        print(widget, "Widget Not Supported << Set")