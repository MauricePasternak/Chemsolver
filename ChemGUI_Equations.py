from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from os.path import join, exists, abspath
from os import chdir, getcwd
from sys import argv, exit
import sys
from json import load
from math import sqrt, exp, log

class ChemGUI_Equations(QWidget):
    def __init__(self):
        super().__init__()
        with open(resource_path("eqns2.json")) as f: self.data = load(f)
        self.resize(800, 560)
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle("ChemSolver - Equations")
        self.setWindowIcon(QIcon(resource_path('Media/Chemistry.ico')))
        self.lineeditors = []
        self.labels = []
        self.globals = {'sqrt': sqrt, 'exp': exp, 'log': log}
        self.cont_leftarea, self.vlay_leftarea = create_container_layout_pair('widget', 'vlay', self, self.main_layout, 3)
        self.cont_rightarea, self.vlay_rightarea = create_container_layout_pair('widget', 'vlay', self, self.main_layout, 3)

        # Left Area - Settings
        settings_font = QFont()
        settings_font.setPointSize(12)
        self.grpbx_settings, self.vlay_settings = create_container_layout_pair('group', 'vlay', self.cont_leftarea, self.vlay_leftarea, 1)
        self.form_settings = QFormLayout()
        self.vlay_settings.addLayout(self.form_settings)
        self.grpbx_settings.setTitle("Equation Selector Settings")
        self.grpbx_settings.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.lab_settings_topic = QLabel("Area of Chemistry", self.grpbx_settings)
        self.comb_setting_topic = QComboBox(self.grpbx_settings)
        self.comb_setting_topic.addItem("Select an option")
        self.comb_setting_topic.addItems(self.data.keys())
        self.comb_setting_topic.currentTextChanged.connect(self.display_eqn_names)

        self.list_settings_eqns = QListWidget(self.grpbx_settings)
        self.list_settings_eqns.currentTextChanged.connect(self.update_solver)
        self.list_settings_eqns.setResizeMode(QListView.Adjust)
        self.form_settings.addRow(self.lab_settings_topic, self.comb_setting_topic)

        self.vlay_settings.addWidget(self.list_settings_eqns)

        # Right Area - Solver
        solver_font = QFont()
        solver_font.setPointSize(10)
        solver_sp = QSizePolicy()
        solver_sp.setRetainSizeWhenHidden(True)
        self.lab_solve_title = QLabel(" ", self.cont_rightarea)
        self.lab_solve_title.setFont(solver_font)
        self.lab_solve_title.setSizePolicy(solver_sp)
        self.vlay_rightarea.addWidget(self.lab_solve_title, 1)

        self.grpbx_solver, self.form_solver = create_container_layout_pair('group', 'form', self.cont_rightarea, self.vlay_rightarea)
        self.grpbx_solver.setTitle("Equation Solver")
        self.grpbx_solver.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vlay_rightarea.addWidget(self.grpbx_solver, 4)

        self.cont_btn_and_pic, self.hlay_btn_and_pic = create_container_layout_pair('widget', 'hlay', self, self.vlay_rightarea, 1)
        self.btn_solve = QPushButton("Solve for the missing variable")
        self.btn_solve.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.btn_solve.setMinimumHeight(round(self.height() / 4))
        self.btn_solve.clicked.connect(self.solve_for_unknown)
        self.btn_solve.setEnabled(False)
        self.lab_solve_pic = QLabel(self.cont_rightarea)
        self.lab_solve_pic.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.hlay_btn_and_pic.addWidget(self.btn_solve)
        self.hlay_btn_and_pic.addSpacing(20)
        self.hlay_btn_and_pic.addWidget(self.lab_solve_pic)

    def display_eqn_names(self, chem_topic):
        self.current_chemtopic = chem_topic
        # Remove the "Select an option" dialogue after the first time this function is invoked
        if self.comb_setting_topic.findText("Select an option", Qt.MatchRegExp) != -1:
            idx_to_remove = self.comb_setting_topic.findText("Select an option", Qt.MatchRegExp)
            self.comb_setting_topic.removeItem(idx_to_remove)

        # Update the list of equations
        self.eqn_names = self.data[chem_topic].keys()
        self.list_settings_eqns.clear()
        self.list_settings_eqns.addItems(self.eqn_names)

        # Update the Picture
        image = QImage(resource_path(f'Media/{chem_topic}.png'))
        new_image = image.scaled(round(self.width() / 4), round(self.height() / 4), Qt.KeepAspectRatio)
        self.lab_solve_pic.setPixmap(QPixmap().fromImage(new_image))

    def update_solver(self, eqn_name):
        self.current_eqn = eqn_name
        if eqn_name:
            # Remove the registered lineeditors and labels from the formlayout
            self.lineeditors.clear()
            self.labels.clear()
            # Remove all Previous items
            for row in range(self.form_solver.rowCount()):
                self.form_solver.removeRow(0)

            # Set the Text of the title to the new equation
            self.lab_solve_title.setText(eqn_name)
            variables = self.data[self.current_chemtopic][eqn_name].keys()
            # Add the new variables to the formlayout
            for variable in variables:
                label = QLabel(variable)
                lineedit = QLineEdit()
                # For each lineeditor, make sure it can only take in numbers and that it is primed to activate the
                # solve btn
                lineedit.setValidator(QDoubleValidator())
                lineedit.textChanged.connect(self.check_for_all_inputs)
                self.form_solver.addRow(label, lineedit)
                self.lineeditors.append(lineedit)
                self.labels.append(label)

    def solve_for_unknown(self):
        # Use a dict to store local variables for the eval function
        local_values = {}
        eqn_to_use = ''
        idx_to_use = None
        # First, find the index of the variable that is not solved for
        for idx, (label, le) in enumerate(zip(self.labels, self.lineeditors)):
            # If the blank lineedit is found, get the eqn associated with the variable to solve for
            # Also store index for referencing the appropriate lineedit later for inputting the answer
            if le.text() == "":
                var_to_solve_for = label.text()
                eqn_to_use = self.data[self.current_chemtopic][self.current_eqn][var_to_solve_for]
                idx_to_use = idx
            # Otherwise, store values for the local dict
            else:
                local_values[label.text()] = float(le.text())

        # Only proceed if the correct equation is selected
        if eqn_to_use != '' and idx_to_use is not None:
            self.answer = float(eval(eqn_to_use, local_values, self.globals))
            if abs(self.answer) > 1000.0 or 0 < abs(self.answer) < 0.001:
                self.answer = f"{self.answer:.2E}"
            else:
                self.answer = f"{self.answer:.3f}"
            self.lineeditors[idx_to_use].setText(self.answer)
        else:
            print("SOMETHING WENT WRONG!!!")

    def check_for_all_inputs(self):
        # Enable the button only if one of the lineedits has a blank field
        current_num_inputs = sum([True if le.text() != '' else False for le in self.lineeditors])
        if current_num_inputs == len(self.lineeditors) - 1:
            self.btn_solve.setEnabled(True)
        else:
            self.btn_solve.setEnabled(False)

def create_container_layout_pair(widget_type: str = 'widget',
                                 layout_type: str = 'hbox',
                                 parent_widget=None,
                                 parent_layout=None,
                                 stretch=0):
    """
    Convenience function for quickly making a container QWidget, the layout within it, and registering both to any
    appropriate parent widgets/layouts
    :param widget_type: the type of container to make: QWidget ('widget'), QGroupBox ('group'), QFrame ('frame')
    :param layout_type: the type of layout to make. QHBoxLayout ('hlay'), QVBoxLayout ('vlay'), QFormLayout ('form'), QGridLayout ('grid')
    :param parent_widget: the parent widget to which the container QWidget should be tied to
    :param parent_layout: the parent layout to which the container-layout pair will be added into
    :return: container, layout
    """
    # Define the widget; default to QWidget
    if widget_type.lower() == 'widget':
        container = QWidget(parent_widget)
    elif widget_type.lower() == 'group':
        container = QGroupBox(parent_widget)
    else:
        container = QWidget(parent_widget)

    # Define the layout; default to QHBoxLayout
    if layout_type.lower() in ['hlay', 'hbox', 'hlayout', 'hboxlayout']:
        layout = QHBoxLayout()
    elif layout_type.lower() in ['vlay', 'vbox', 'vlayout', 'vboxlayout']:
        layout = QVBoxLayout()
    elif layout_type.lower() in ['form', 'formlay', 'formlayout']:
        layout = QFormLayout()
    else:
        layout = QHBoxLayout()

    # Set the layout to the container
    container.setLayout(layout)

    # Have the parent layout add the container to itself, with an appropriate stretch factor applied
    parent_layout.addWidget(container, stretch)

    return container, layout


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = abspath(".")

    return join(base_path, relative_path)

if __name__ == '__main__':
    cwd = getcwd()
    chdir(cwd)

    app = QApplication(argv)
    win = ChemGUI_Equations()
    if exists(resource_path('qt_mp_dark_orange.qss')):
        with open(resource_path("qt_mp_dark_orange.qss")) as f:
            style = f.read()
        app.setStyleSheet(style)
    else:
        app.setStyle('Fusion')
    win.show()
    exit(app.exec())

