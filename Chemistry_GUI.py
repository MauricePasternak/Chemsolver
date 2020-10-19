from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QTabWidget, QFormLayout, QLabel, \
    QMessageBox, QVBoxLayout, QRadioButton
from PyQt5.QtGui import QIcon, QPixmap, QFont, QDoubleValidator
from PyQt5.QtCore import QRect, Qt, QMetaObject, QCoreApplication
import sys
import os
import json
from math import *


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# noinspection PyArgumentList
class MyChemistryApp(QMainWindow):
    def __init__(self, data):
        super().__init__()

        # Main Window Characteristics
        self.chem_widget_window = None
        self.eqn_data = data
        self.resize(574, 423)
        self.setWindowIcon(QIcon(QPixmap(os.path.join(os.getcwd(), 'Chemistry.png'))))
        self.setWindowTitle("Chemistry Solver")
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        # Main Tab Menu
        self.main_tabmenu = QTabWidget(self.centralwidget)
        self.main_tabmenu.setGeometry(QRect(0, 40, 569, 351))
        self.main_tabmenu.setAcceptDrops(False)
        self.main_tabmenu.setTabBarAutoHide(False)
        self.main_tabmenu.setObjectName("main_tabmenu")

        # Top Label
        self.label_chemsolver = QLabel(self.centralwidget)
        self.font = QFont()
        self.font.setFamily("Segoe UI")
        self.setup_alabel_UI(self.label_chemsolver, self.font, QRect(10, 0, 131, 31), 12, True, 75, False)
        self.label_chemsolver.setTextFormat(Qt.AutoText)
        self.label_chemsolver.setScaledContents(False)

        # Individual Tabs Setup
        self.setup_quantum_tabUI()
        self.setup_gaslaws_tabUI()
        self.setup_thermo_tabUI()
        self.setup_equilibrium_tabUI()
        self.setup_kinetics_tabUI()
        self.setup_electrochem_tabUI()

        # Text Setup and Misc
        self.alert = QMessageBox()
        self.retranslateUi(self)
        self.main_tabmenu.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(self)

    def setup_quantum_tabUI(self):
        # Layout
        self.tab_quantum = QWidget()
        self.verticalLayoutWidget = QWidget(self.tab_quantum)
        self.verticalLayoutWidget.setGeometry(QRect(10, 40, 231, 191))
        self.vbox_quantum_eqns = QVBoxLayout(self.verticalLayoutWidget)
        self.vbox_quantum_eqns.setContentsMargins(0, 0, 0, 0)

        # Radio Buttons
        self.rbut_e_wave_eqn = QRadioButton(self.verticalLayoutWidget)
        self.vbox_quantum_eqns.addWidget(self.rbut_e_wave_eqn)
        self.rbut_heisen_eqn = QRadioButton(self.verticalLayoutWidget)
        self.vbox_quantum_eqns.addWidget(self.rbut_heisen_eqn)
        self.rbut_e_elec_at_lvl_eqn = QRadioButton(self.verticalLayoutWidget)
        self.vbox_quantum_eqns.addWidget(self.rbut_e_elec_at_lvl_eqn)
        self.rbut_ryd_wave = QRadioButton(self.verticalLayoutWidget)
        self.vbox_quantum_eqns.addWidget(self.rbut_ryd_wave)
        self.rbut_ryd_energy = QRadioButton(self.verticalLayoutWidget)
        self.vbox_quantum_eqns.addWidget(self.rbut_ryd_energy)
        self.quantum_rbuts = [self.rbut_e_wave_eqn, self.rbut_heisen_eqn, self.rbut_e_elec_at_lvl_eqn,
                              self.rbut_ryd_wave, self.rbut_ryd_energy]

        # Push Buttons
        self.but_letssolve_quantum = QPushButton(self.tab_quantum)
        self.but_letssolve_quantum.setGeometry(QRect(10, 240, 225, 40))
        self.but_letssolve_quantum.clicked.connect(lambda: self.open_minisolver(self.quantum_rbuts))

        # Labels
        self.label_quantum_eqns = QLabel(self.tab_quantum)
        self.setup_alabel_UI(self.label_quantum_eqns, self.font, QRect(10, 0, 225, 40), 11, True, 75, True)
        self.label_quantum_picture = QLabel(self.tab_quantum)
        self.label_quantum_picture.setGeometry(QRect(275, 25, 250, 250))
        self.label_quantum_picture.setPixmap(QPixmap(os.path.join(os.getcwd(), 'Quantum.png')))
        self.label_quantum_picture.setScaledContents(True)
        self.main_tabmenu.addTab(self.tab_quantum, "")

    def setup_gaslaws_tabUI(self):
        # Layout
        self.tab_gaslaws = QWidget()
        self.verticalLayoutWidget_2 = QWidget(self.tab_gaslaws)
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 40, 231, 191))
        self.vbox_gaslaw_eqns = QVBoxLayout(self.verticalLayoutWidget_2)
        self.vbox_gaslaw_eqns.setContentsMargins(0, 0, 0, 0)

        # Radio Buttons
        self.rbut_ideal_std_eqn = QRadioButton(self.verticalLayoutWidget_2)
        self.vbox_gaslaw_eqns.addWidget(self.rbut_ideal_std_eqn)
        self.rbut_ideal_mw_eqn = QRadioButton(self.verticalLayoutWidget_2)
        self.vbox_gaslaw_eqns.addWidget(self.rbut_ideal_mw_eqn)
        self.rbut_real_gas_eqn = QRadioButton(self.verticalLayoutWidget_2)
        self.vbox_gaslaw_eqns.addWidget(self.rbut_real_gas_eqn)
        self.rbut_graham_eqn = QRadioButton(self.verticalLayoutWidget_2)
        self.vbox_gaslaw_eqns.addWidget(self.rbut_graham_eqn)
        self.rbut_rms_eqn = QRadioButton(self.verticalLayoutWidget_2)
        self.vbox_gaslaw_eqns.addWidget(self.rbut_rms_eqn)
        self.rbut_kinetic_eqn = QRadioButton(self.verticalLayoutWidget_2)
        self.vbox_gaslaw_eqns.addWidget(self.rbut_kinetic_eqn)
        self.gaslaw_rbtns = [self.rbut_ideal_std_eqn, self.rbut_ideal_mw_eqn, self.rbut_real_gas_eqn,
                             self.rbut_graham_eqn, self.rbut_rms_eqn, self.rbut_kinetic_eqn]

        # Push Buttons
        self.but_letssolve_gaslaws = QPushButton(self.tab_gaslaws)
        self.but_letssolve_gaslaws.setGeometry(QRect(10, 240, 225, 40))
        self.but_letssolve_gaslaws.clicked.connect(lambda: self.open_minisolver(self.gaslaw_rbtns))

        # Labels
        self.label_gaslaw_eqns = QLabel(self.tab_gaslaws)
        self.setup_alabel_UI(self.label_gaslaw_eqns, self.font, QRect(10, 0, 225, 40), 11, True, 75, True)
        self.label_gaslaw_picture = QLabel(self.tab_gaslaws)
        self.label_gaslaw_picture.setGeometry(QRect(275, 25, 250, 250))
        self.label_gaslaw_picture.setPixmap(QPixmap(os.path.join(os.getcwd(), 'Chem_Gas.png')))
        self.label_gaslaw_picture.setScaledContents(True)

        self.main_tabmenu.addTab(self.tab_gaslaws, "")

    def setup_thermo_tabUI(self):
        # Layout
        self.tab_thermo = QWidget()
        self.verticalLayoutWidget_3 = QWidget(self.tab_thermo)
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 40, 271, 281))
        self.vbox_thermo_eqns = QVBoxLayout(self.verticalLayoutWidget_3)
        self.vbox_thermo_eqns.setContentsMargins(0, 0, 0, 0)

        # Radio Buttons
        self.rbut_entr_chngvol = QRadioButton(self.verticalLayoutWidget_3)
        self.vbox_thermo_eqns.addWidget(self.rbut_entr_chngvol)
        self.rbut_entr_chngprs = QRadioButton(self.verticalLayoutWidget_3)
        self.vbox_thermo_eqns.addWidget(self.rbut_entr_chngprs)
        self.rbut_entr_chngtemp = QRadioButton(self.verticalLayoutWidget_3)
        self.vbox_thermo_eqns.addWidget(self.rbut_entr_chngtemp)
        self.rbut_entr_micro = QRadioButton(self.verticalLayoutWidget_3)
        self.vbox_thermo_eqns.addWidget(self.rbut_entr_micro)
        self.rbut_gibbs_quot = QRadioButton(self.verticalLayoutWidget_3)
        self.vbox_thermo_eqns.addWidget(self.rbut_gibbs_quot)
        self.rbut_gibbs_keq = QRadioButton(self.verticalLayoutWidget_3)
        self.vbox_thermo_eqns.addWidget(self.rbut_gibbs_keq)
        self.rbut_gibbs_qandkeq = QRadioButton(self.verticalLayoutWidget_3)
        self.vbox_thermo_eqns.addWidget(self.rbut_gibbs_qandkeq)
        self.rbut_gibbs_enth_entr = QRadioButton(self.verticalLayoutWidget_3)
        self.vbox_thermo_eqns.addWidget(self.rbut_gibbs_enth_entr)
        self.rbut_cal_heat_temp = QRadioButton(self.verticalLayoutWidget_3)
        self.vbox_thermo_eqns.addWidget(self.rbut_cal_heat_temp)
        self.rbut_cal_heat_enth = QRadioButton(self.verticalLayoutWidget_3)
        self.vbox_thermo_eqns.addWidget(self.rbut_cal_heat_enth)
        self.rbut_hess_law = QRadioButton(self.verticalLayoutWidget_3)
        self.vbox_thermo_eqns.addWidget(self.rbut_hess_law)
        self.thermo_rbtns = [self.rbut_entr_chngvol, self.rbut_entr_chngprs, self.rbut_entr_chngtemp,
                             self.rbut_entr_micro, self.rbut_gibbs_quot, self.rbut_gibbs_keq, self.rbut_gibbs_qandkeq,
                             self.rbut_gibbs_enth_entr, self.rbut_cal_heat_temp, self.rbut_cal_heat_enth,
                             self.rbut_hess_law]

        # Push Buttons
        self.but_letssolve_thermo = QPushButton(self.tab_thermo)
        self.but_letssolve_thermo.setGeometry(QRect(300, 40, 225, 40))
        self.but_letssolve_thermo.clicked.connect(lambda: self.open_minisolver(self.thermo_rbtns))

        # Labels
        self.label_thermo_eqns = QLabel(self.tab_thermo)
        self.setup_alabel_UI(self.label_thermo_eqns, self.font, QRect(10, 0, 225, 40), 11, True, 75, True)
        self.label_thermo_picture = QLabel(self.tab_thermo)
        self.label_thermo_picture.setGeometry(QRect(290, 90, 225, 225))
        self.label_thermo_picture.setPixmap(QPixmap(os.path.join(os.getcwd(), 'ThermoChem.png')))
        self.label_thermo_picture.setScaledContents(True)

        self.main_tabmenu.addTab(self.tab_thermo, "")

    def setup_equilibrium_tabUI(self):
        # Layout
        self.tab_equilib = QWidget()
        self.verticalLayoutWidget_4 = QWidget(self.tab_equilib)
        self.verticalLayoutWidget_4.setGeometry(QRect(10, 50, 234, 211))
        self.vbox_equilibrium_eqns = QVBoxLayout(self.verticalLayoutWidget_4)
        self.vbox_equilibrium_eqns.setContentsMargins(0, 0, 0, 0)

        # Radio Buttons
        self.rbut_dilution = QRadioButton(self.verticalLayoutWidget_4)
        self.vbox_equilibrium_eqns.addWidget(self.rbut_dilution)
        self.rbut_keq_of_rxn = QRadioButton(self.verticalLayoutWidget_4)
        self.vbox_equilibrium_eqns.addWidget(self.rbut_keq_of_rxn)
        self.rbut_kp_kc_conv = QRadioButton(self.verticalLayoutWidget_4)
        self.vbox_equilibrium_eqns.addWidget(self.rbut_kp_kc_conv)
        self.rbut_mol_solub = QRadioButton(self.verticalLayoutWidget_4)
        self.vbox_equilibrium_eqns.addWidget(self.rbut_mol_solub)
        self.rbut_vant_onekeq = QRadioButton(self.verticalLayoutWidget_4)
        self.vbox_equilibrium_eqns.addWidget(self.rbut_vant_onekeq)
        self.rbut_vant_twokeq = QRadioButton(self.verticalLayoutWidget_4)
        self.vbox_equilibrium_eqns.addWidget(self.rbut_vant_twokeq)
        self.rbut_hh_pka = QRadioButton(self.verticalLayoutWidget_4)
        self.vbox_equilibrium_eqns.addWidget(self.rbut_hh_pka)
        self.rbut_hh_pkb = QRadioButton(self.verticalLayoutWidget_4)
        self.vbox_equilibrium_eqns.addWidget(self.rbut_hh_pkb)
        self.equilibrium_rbtns = [self.rbut_dilution, self.rbut_keq_of_rxn, self.rbut_kp_kc_conv, self.rbut_mol_solub,
                                  self.rbut_vant_onekeq, self.rbut_vant_twokeq, self.rbut_hh_pka, self.rbut_hh_pkb]
        # Push Buttons
        self.but_letssolve_equi = QPushButton(self.tab_equilib)
        self.but_letssolve_equi.setGeometry(QRect(10, 270, 225, 40))
        self.but_letssolve_equi.clicked.connect(lambda: self.open_minisolver(self.equilibrium_rbtns))

        # Labels
        self.label_equi_eqns = QLabel(self.tab_equilib)
        self.setup_alabel_UI(self.label_equi_eqns, self.font, QRect(10, 0, 241, 40), 11, True, 75, True)
        self.label_equi_picture = QLabel(self.tab_equilib)
        self.label_equi_picture.setGeometry(QRect(275, 45, 250, 250))
        self.label_equi_picture.setPixmap(QPixmap(os.path.join(os.getcwd(), 'Equilibrium.png')))
        self.label_equi_picture.setScaledContents(True)

        self.main_tabmenu.addTab(self.tab_equilib, "")

    def setup_kinetics_tabUI(self):
        # Layout
        self.tab_kinetics = QWidget()
        self.verticalLayoutWidget_5 = QWidget(self.tab_kinetics)
        self.verticalLayoutWidget_5.setGeometry(QRect(10, 50, 231, 211))
        self.vbox_kinetics_eqns = QVBoxLayout(self.verticalLayoutWidget_5)
        self.vbox_kinetics_eqns.setContentsMargins(0, 0, 0, 0)

        # Radio Buttons
        self.rbut_main_rate_law = QRadioButton(self.verticalLayoutWidget_5)
        self.vbox_kinetics_eqns.addWidget(self.rbut_main_rate_law)
        self.rbut_order_reactant = QRadioButton(self.verticalLayoutWidget_5)
        self.vbox_kinetics_eqns.addWidget(self.rbut_order_reactant)
        self.rbut_avrg_rate = QRadioButton(self.verticalLayoutWidget_5)
        self.vbox_kinetics_eqns.addWidget(self.rbut_avrg_rate)
        self.rbut_0thorder = QRadioButton(self.verticalLayoutWidget_5)
        self.vbox_kinetics_eqns.addWidget(self.rbut_0thorder)
        self.rbut_1storder = QRadioButton(self.verticalLayoutWidget_5)
        self.vbox_kinetics_eqns.addWidget(self.rbut_1storder)
        self.rbut_2ndorder = QRadioButton(self.verticalLayoutWidget_5)
        self.vbox_kinetics_eqns.addWidget(self.rbut_2ndorder)
        self.rbut_arrhen = QRadioButton(self.verticalLayoutWidget_5)
        self.vbox_kinetics_eqns.addWidget(self.rbut_arrhen)
        self.rbut_ratek_from_temp = QRadioButton(self.verticalLayoutWidget_5)
        self.vbox_kinetics_eqns.addWidget(self.rbut_ratek_from_temp)
        self.kinetics_rbtns = [self.rbut_main_rate_law, self.rbut_order_reactant, self.rbut_avrg_rate,
                               self.rbut_0thorder, self.rbut_1storder, self.rbut_2ndorder, self.rbut_arrhen,
                               self.rbut_ratek_from_temp]

        # Push Buttons
        self.but_letssolve_kinetics = QPushButton(self.tab_kinetics)
        self.but_letssolve_kinetics.setGeometry(QRect(10, 270, 225, 40))
        self.but_letssolve_kinetics.clicked.connect(lambda: self.open_minisolver(self.kinetics_rbtns))

        # Labels
        self.label_kinetics_eqns = QLabel(self.tab_kinetics)
        self.setup_alabel_UI(self.label_kinetics_eqns, self.font, QRect(10, 0, 225, 40), 11, True, 75, True)
        self.label_kinetics_picture = QLabel(self.tab_kinetics)
        self.label_kinetics_picture.setGeometry(QRect(275, 45, 250, 250))
        self.label_kinetics_picture.setPixmap(QPixmap(os.path.join(os.getcwd(), 'Kinetics.png')))
        self.label_kinetics_picture.setScaledContents(True)

        self.main_tabmenu.addTab(self.tab_kinetics, "")

    def setup_electrochem_tabUI(self):
        self.tab_electro = QWidget()

        self.verticalLayoutWidget_6 = QWidget(self.tab_electro)
        self.verticalLayoutWidget_6.setGeometry(QRect(10, 40, 231, 191))
        self.vbox_electro_eqns = QVBoxLayout(self.verticalLayoutWidget_6)
        self.vbox_electro_eqns.setContentsMargins(0, 0, 0, 0)
        self.rbut_nernst = QRadioButton(self.verticalLayoutWidget_6)
        self.vbox_electro_eqns.addWidget(self.rbut_nernst)
        self.rbut_electroplat = QRadioButton(self.verticalLayoutWidget_6)
        self.vbox_electro_eqns.addWidget(self.rbut_electroplat)
        self.electro_rbtns = [self.rbut_nernst, self.rbut_electroplat]

        # Push Buttons
        self.but_letssolve_electro = QPushButton(self.tab_electro)
        self.but_letssolve_electro.setGeometry(QRect(10, 240, 225, 40))
        self.but_letssolve_electro.clicked.connect(lambda: self.open_minisolver(self.electro_rbtns))

        # Labels
        self.label_electro_eqns = QLabel(self.tab_electro)
        self.setup_alabel_UI(self.label_electro_eqns, self.font, QRect(10, 0, 251, 40), 11, True, 75, True)
        self.label_electro_picture = QLabel(self.tab_electro)
        self.label_electro_picture.setGeometry(QRect(275, 25, 250, 250))
        self.label_electro_picture.setPixmap(QPixmap(os.path.join(os.getcwd(), 'Battery.png')))
        self.label_electro_picture.setScaledContents(True)

        self.main_tabmenu.addTab(self.tab_electro, "")

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        self.rbut_e_wave_eqn.setText(_translate("MainWindow", "Energy - Wavelength Equation"))
        self.rbut_heisen_eqn.setText(_translate("MainWindow", "Heisenberg Uncertainty Equation"))
        self.rbut_e_elec_at_lvl_eqn.setText(_translate("MainWindow", "Energy of an Electron at Particular Level"))
        self.rbut_ryd_wave.setText(_translate("MainWindow", "Rydberg Equation - Wavelength"))
        self.rbut_ryd_energy.setText(_translate("MainWindow", "Rydberg Equation - Energy"))
        self.label_quantum_eqns.setText(_translate("MainWindow", "Quantum Equations:"))
        self.but_letssolve_quantum.setText(_translate("MainWindow", "Let\'s Solve it!"))
        self.main_tabmenu.setTabText(self.main_tabmenu.indexOf(self.tab_quantum), _translate("MainWindow", "Quantum"))

        self.label_gaslaw_eqns.setText(_translate("MainWindow", "Gas Law Equations:"))
        self.rbut_ideal_std_eqn.setText(_translate("MainWindow", "Ideal Gas Law - standard"))
        self.rbut_ideal_mw_eqn.setText(_translate("MainWindow", "Ideal Gas Law - Mass and Molar Mass"))
        self.rbut_real_gas_eqn.setText(_translate("MainWindow", "Real Gas Law"))
        self.rbut_graham_eqn.setText(_translate("MainWindow", "Grahams Law"))
        self.rbut_rms_eqn.setText(_translate("MainWindow", "RMS Particle Velocity"))
        self.rbut_kinetic_eqn.setText(_translate("MainWindow", "Kinetic Energy Equation"))
        self.but_letssolve_gaslaws.setText(_translate("MainWindow", "Let\'s Solve it!"))
        self.main_tabmenu.setTabText(self.main_tabmenu.indexOf(self.tab_gaslaws), _translate("MainWindow", "Gas Laws"))

        self.label_thermo_eqns.setText(_translate("MainWindow", "Thermodynamics Equations:"))
        self.rbut_entr_chngvol.setText(_translate("MainWindow", "Entropy for an Isothermal Rxn - Changing Volume"))
        self.rbut_entr_chngprs.setText(_translate("MainWindow", "Entropy for an Isothermal Rxn - Changing Pressure"))
        self.rbut_entr_chngtemp.setText(_translate("MainWindow", "Entropy for an Isobaric Rxn - Changing Temp"))
        self.rbut_entr_micro.setText(_translate("MainWindow", "Entropy from Microstates"))
        self.rbut_gibbs_quot.setText(_translate("MainWindow", "Gibb\'s Free Energy - Rxn Quotient"))
        self.rbut_gibbs_keq.setText(_translate("MainWindow", "Gibb\'s Free Energy - Keq Constant"))
        self.rbut_gibbs_qandkeq.setText(_translate("MainWindow", "Gibb\'s Free Energy - Quotient vs Keq"))
        self.rbut_gibbs_enth_entr.setText(_translate("MainWindow", "Gibb\'s Free Energy - Enthalpy and Entropy"))
        self.rbut_cal_heat_temp.setText(_translate("MainWindow", "Calorimetry - Heat from Temp Change"))
        self.rbut_cal_heat_enth.setText(_translate("MainWindow", "Calorimetry - Heat from Enthalpy"))
        self.rbut_hess_law.setText(_translate("MainWindow", "Hess\'s Law - Heats of Formation"))
        self.but_letssolve_thermo.setText(_translate("MainWindow", "Let\'s Solve it!"))
        self.main_tabmenu.setTabText(self.main_tabmenu.indexOf(self.tab_thermo),
                                     _translate("MainWindow", "Thermodynamics"))

        self.rbut_dilution.setText(_translate("MainWindow", "Dilution Equation"))
        self.rbut_keq_of_rxn.setText(_translate("MainWindow", "Keq of a Reaction: aA + bB <--> cC + dD"))
        self.rbut_kp_kc_conv.setText(_translate("MainWindow", "Kp - Kc Conversation"))
        self.rbut_mol_solub.setText(_translate("MainWindow", "Molar Solubility in Water for AB --> aA + bB"))
        self.rbut_vant_onekeq.setText(_translate("MainWindow", "Van\'t Hoff Equation - Single Keq"))
        self.rbut_vant_twokeq.setText(_translate("MainWindow", "Van\'t Hoff Equation - Two Keq"))
        self.rbut_hh_pka.setText(_translate("MainWindow", "Henderson Hasselbach - pKa"))
        self.rbut_hh_pkb.setText(_translate("MainWindow", "Henderson Hasselbach - pKb"))
        self.label_equi_eqns.setText(_translate("MainWindow", "Equilibrium Equations:"))
        self.but_letssolve_equi.setText(_translate("MainWindow", "Let\'s Solve it!"))
        self.main_tabmenu.setTabText(self.main_tabmenu.indexOf(self.tab_equilib),
                                     _translate("MainWindow", "Equilibrium && Solutions"))

        self.rbut_main_rate_law.setText(_translate("MainWindow", "Main Rate Law"))
        self.rbut_order_reactant.setText(_translate("MainWindow", "Order of Reactant from Initial Rates"))
        self.rbut_avrg_rate.setText(_translate("MainWindow", "Average Rate of a Reactant"))
        self.rbut_0thorder.setText(_translate("MainWindow", "0th Order Integrated Rate Law"))
        self.rbut_1storder.setText(_translate("MainWindow", "1st Order Integrated Rate Law"))
        self.rbut_2ndorder.setText(_translate("MainWindow", "2nd Order Integrated Rate Law"))
        self.rbut_arrhen.setText(_translate("MainWindow", "Arrhenius Equation"))
        self.rbut_ratek_from_temp.setText(_translate("MainWindow", "Rate Constant from changing Temp"))
        self.label_kinetics_eqns.setText(_translate("MainWindow", "Kinetics Equations:"))
        self.but_letssolve_kinetics.setText(_translate("MainWindow", "Let\'s Solve it!"))
        self.main_tabmenu.setTabText(self.main_tabmenu.indexOf(self.tab_kinetics), _translate("MainWindow", "Kinetics"))

        self.but_letssolve_electro.setText(_translate("MainWindow", "Let\'s Solve it!"))
        self.rbut_nernst.setText(_translate("MainWindow", "Nernst Equation"))
        self.rbut_electroplat.setText(_translate("MainWindow", "Electroplating Relationship"))
        self.main_tabmenu.setTabText(self.main_tabmenu.indexOf(self.tab_electro),
                                     _translate("MainWindow", "Electrochemistry"))

        self.label_chemsolver.setText(_translate("MainWindow", "Chemistry Solver"))

    def setup_alabel_UI(self, a_label, font_obj, qrect_obj, pt_size, is_boldfont, font_weight, is_fontwrap):
        a_label.setGeometry(qrect_obj)
        font_obj.setPointSize(pt_size)
        font_obj.setBold(is_boldfont)
        font_obj.setWeight(font_weight)
        a_label.setFont(font_obj)
        a_label.setWordWrap(is_fontwrap)

    def open_minisolver(self, btn_list):
        selected_eqn = False
        for btn in btn_list:
            if btn.isChecked():
                selected_eqn = btn.text()
                print(f"Selecting the radiobutton labelled: {selected_eqn}")

        if selected_eqn:
            dict_to_feed = self.eqn_data[selected_eqn]
            self.chem_widget_window = Chemistry_Widget(selected_eqn, dict_to_feed)
            self.chem_widget_window.show()

        else:
            self.alert.warning(self, "No Equation Selected!", "You must select an equation.", QMessageBox.Ok)


class Chemistry_Widget(QWidget):
    def __init__(self, eqn_name, var_dict):
        super(QWidget, self).__init__()

        # Set up meta-variables
        self.law_name = eqn_name
        self.var_names = list(var_dict.keys())
        self.eqns = list(var_dict.values())
        self.globals = {'sqrt': sqrt, 'exp': exp, 'log': log}
        self.labels = []
        self.lineedits = []

        # Set up main window variables and settings
        self.setWindowTitle(f"Chemistry Solver: {self.law_name}")
        self.setFixedWidth(10 * len(f"Chemistry Solver: {self.law_name}"))
        self.form = QFormLayout(self)
        self.setWindowIcon(QIcon(QPixmap(os.path.join(os.getcwd(), 'Chemistry.png'))))

        # Set up ancillary widgets
        self.dval_sci = QDoubleValidator()
        self.b_solve = QPushButton("Solve")
        self.b_solve.setEnabled(False)
        self.b_solve.clicked.connect(self.chem_solve)

        # Main form-like UI setup
        for var in self.var_names:
            var_label, var_le = self.create_label_lineedit_pair(var)
            self.labels.append(var_label)
            self.lineedits.append(var_le)
            self.form.addRow(var_label, var_le)
        self.form.addRow(self.b_solve)
        self.setLayout(self.form)

    def create_label_lineedit_pair(self, var_name):
        label = QLabel(var_name)
        le = QLineEdit()
        le.setValidator(self.dval_sci)
        le.textEdited.connect(self.reset_color)
        le.textChanged.connect(self.check_if_all_empty)
        return label, le

    def find_blank_field(self):
        for idx, lineedits in enumerate(self.lineedits):
            if lineedits.text() == "":
                self.to_solve_for_idx = idx
                self.to_solve_for_var = self.var_names[idx]

    def chem_solve(self):
        self.find_blank_field()
        self.locals_dict = {}
        for variable, lineedit in zip(self.var_names, self.lineedits):
            if variable != self.to_solve_for_var:
                value = float(lineedit.text())
                exec(f"{variable} = {value}")
                self.locals_dict[variable] = value

        self.eqn_of_interest = self.eqns[self.to_solve_for_idx]
        self.answer = eval(self.eqn_of_interest, self.globals, self.locals_dict)
        self.answer = float(self.answer)
        if abs(self.answer) > 1000.0 or 0 < abs(self.answer) < 0.001:
            self.answer = f"{self.answer:.2E}"
        else:
            self.answer = f"{self.answer:.3f}"
        le_of_interest = self.lineedits[self.to_solve_for_idx]
        le_of_interest.setStyleSheet("color: orange;")
        le_of_interest.setText(str(self.answer))

    def reset_color(self):
        for lineedit in self.lineedits:
            lineedit.setStyleSheet("color: white;")

    def check_if_all_empty(self):
        checkmarks = [lineedit.text() == "" for lineedit in self.lineedits]
        if sum(checkmarks) != 1:
            self.b_solve.setEnabled(False)
        else:
            self.b_solve.setEnabled(True)





def window(css_file="qt_dark_orange.qss"):
    app = QApplication(sys.argv)
    path_to_custom_style = os.path.join(os.getcwd(), css_file)
    if os.path.exists(path_to_custom_style):
        with open(path_to_custom_style) as f:
            style = f.read()
            app.setStyleSheet(style)
    else:
        app.setStyle("Fusion")

    with open(os.path.join(os.getcwd(), 'eqns.json')) as f:
        data = json.load(f)

    win = MyChemistryApp(data)
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    window()
