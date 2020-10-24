from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sys
import os
import json
from math import *
from pprint import pprint


# noinspection PyArgumentList
class MyChemistryApp(QMainWindow):
    def __init__(self, data):
        super().__init__()

        # Misc Variables
        self.labels = []
        self.les = []
        self.globals = {'sqrt': sqrt, 'exp': exp, 'log': log}

        # Main Window Characteristics
        self.chem_widget_window = None
        self.eqn_data: dict = data
        self.resize(800, 500)
        self.setWindowIcon(QIcon(QPixmap("Media/Atom.svg")))
        self.setWindowTitle("Chemistry Solver")
        self.cw = QWidget(self)
        self.setCentralWidget(self.cw)
        self.mainlay, self.vlay_left, self.vlay_right = QHBoxLayout(self.cw), QVBoxLayout(), QVBoxLayout()
        self.mainlay.addLayout(self.vlay_left, 1)
        self.mainlay.addLayout(self.vlay_right, 1)
        # %%%%%%%%%
        # Left Side
        # %%%%%%%%%
        self.formlay_sections = QFormLayout()
        self.cmb_sections = QComboBox()
        self.cmb_sections.addItems(list(self.eqn_data.keys()))
        self.cmb_sections.currentTextChanged.connect(self.update_listed_eqns)
        self.formlay_sections.addRow("Select area of chemistry", self.cmb_sections)
        self.lst_eqns = QListWidget()
        self.lst_eqns.addItems(self.eqn_data[self.cmb_sections.currentText()])
        self.lst_eqns.currentTextChanged.connect(self.update_rightside)

        self.vlay_left.addLayout(self.formlay_sections)
        self.vlay_left.addWidget(self.lst_eqns)

        # %%%%%%%%%
        # Right Side
        # %%%%%%%%%
        self.grp_eqntosolve = QGroupBox(f"Currently-selected equation:\n")
        self.formlay_eqns = QFormLayout(self.grp_eqntosolve)
        self.btn_solve = QPushButton("Solve for the unknown", enabled=False, clicked=self.solve)
        self.vlay_right.addWidget(self.grp_eqntosolve)
        self.vlay_right.addWidget(self.btn_solve)

    def update_listed_eqns(self):
        """
        Updates the QListWidget to feature the equations pertaining to the chosen area of chemistry
        """
        self.clear_rightside()
        self.lst_eqns.clear()
        self.lst_eqns.addItems(list(self.eqn_data[self.cmb_sections.currentText()]))

    def update_rightside(self, selected_eqn):
        """
        Updates the right side of the application with the new givens once a particular equation is selected
        """
        print("Updating right side")
        self.clear_rightside()
        try:
            for variable in self.eqn_data[self.cmb_sections.currentText()][selected_eqn]:
                label, le = self.create_label_lineedit_pair(var_name=variable)
                self.labels.append(label)
                self.les.append(le)
                self.formlay_eqns.addRow(label, le)
        except KeyError:  # Happens during an area switch when an equation was already selected
            pass

    def clear_rightside(self):
        """
        Completely clears the right side of the application
        """
        print("Clearing Right Side")
        # Remove all widgets and lineedits
        for _ in range(self.formlay_eqns.rowCount()):
            self.formlay_eqns.removeRow(0)
        self.btn_solve.setEnabled(False)

        # Reset other variables
        self.labels.clear()
        self.les.clear()

    def create_label_lineedit_pair(self, var_name):
        """
        Convenience function for creating a pair of widgets for the right side of the eqn
        """
        label = QLabel(var_name)
        le = QLineEdit(placeholderText="Leave blank if wanting to solve for this", clearButtonEnabled=True)
        le.setValidator(QDoubleValidator())
        le.textEdited.connect(self.reset_color)
        le.textChanged.connect(self.check_if_all_empty)
        return label, le

    def check_if_all_empty(self):
        checkmarks = [lineedit.text() == "" for lineedit in self.les]
        if sum(checkmarks) != 1:
            self.btn_solve.setEnabled(False)
        else:
            self.btn_solve.setEnabled(True)

    def reset_color(self):
        pass

    def find_blank_field_idx(self):
        for idx, lineedits in enumerate(self.les):
            if lineedits.text() == "":
                return idx

    def solve(self):
        idx_of_blank = self.find_blank_field_idx()
        self.locals_dict = {}
        selected_area, selected_eqn = self.cmb_sections.currentText(), self.lst_eqns.currentItem().text()
        variables = self.eqn_data[selected_area][selected_eqn].keys()
        var_to_solve_for = None
        eqn_to_solve_for = None
        for variable, lineedit in zip(variables, self.les):
            if lineedit.text() != "":
                self.locals_dict[variable] = float(lineedit.text())
            else:
                var_to_solve_for = variable
                eqn_to_solve_for = self.eqn_data[selected_area][selected_eqn][variable]

        if var_to_solve_for is None or eqn_to_solve_for is None:
            print("ERROR")
            return

        answer = float(eval(eqn_to_solve_for, self.globals, self.locals_dict))
        if abs(answer) > 1000.0 or 0 < abs(answer) < 0.001:
            answer = f"{answer:.2E}"
        else:
            answer = f"{answer:.3f}"
        le_of_interest = self.les[idx_of_blank]
        le_of_interest.setText(str(answer))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open(os.path.join(os.getcwd(), 'eqns.json')) as f:
        eqn_data = json.load(f)
    win = MyChemistryApp(eqn_data)
    win.show()
    sys.exit(app.exec_())
