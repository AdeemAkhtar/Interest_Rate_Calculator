# All Imports

from PyQt5.QtWidgets import QCheckBox, QMessageBox, QApplication, QWidget, QLabel, QPushButton, QTreeView, QHBoxLayout, QVBoxLayout, QLineEdit, QMainWindow, QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os
#

class FinanceApp(QMainWindow):
    """
    A PyQt5-based GUI application to calculate compound interest over time,
    display results in a tree view and chart, and allow saving to CSV.
    """
    def __init__(self):
        """
        Initialize the main window, UI widgets, layout, and signal connections.
        """
        super(FinanceApp, self). __init__()
        self.setWindowTitle("InterestMe 2.0")
        self.resize(800, 600)

        main_window = QWidget()

        # Input Fields
        self.rate_text = QLabel("Interest Rate (%): ")
        self.rate_input = QLineEdit()

        self.initial_text = QLabel("Initial Investment: ")
        self.initial_input = QLineEdit()

        self.years_text = QLabel("Years to Invest: ")
        self.years_input = QLineEdit()

         # Tree View for displaying results
        self.model = QStandardItemModel()
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)

        # Buttons
        self.calc_button = QPushButton("Calculate")
        self.clear_button = QPushButton("Clear")
        self.save_button = QPushButton("Save")

        # Chart
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # Dark Mode Toggle
        self.dark_mode = QCheckBox("Dark Mode")

        # Layouts
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()

        # Row 1 Layout
        self.row1.addWidget(self.rate_text)
        self.row1.addWidget(self.rate_input)
        self.row1.addWidget(self.initial_text)
        self.row1.addWidget(self.initial_input)
        self.row1.addWidget(self.years_text)
        self.row1.addWidget(self.years_input) 
        self.row1.addWidget(self.dark_mode)

        # Column Layouts
        self.col1.addWidget(self.tree_view)
        self.col1.addWidget(self.calc_button)
        self.col1.addWidget(self.clear_button)
        self.col1.addWidget(self.save_button)

        self.col2.addWidget(self.canvas)

        # Combine Row 2
        self.row2.addLayout(self.col1, 30)
        self.row2.addLayout(self.col2, 70)

        # Master Layout
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)

        main_window.setLayout(self.master_layout)
        self.setCentralWidget(main_window)


        # Signal connections
        self.calc_button.clicked.connect(self.calc_interest)
        self.clear_button.clicked.connect(self.reset)
        self.save_button.clicked.connect(self.save_data)
        self.dark_mode.stateChanged.connect(self.toggle_mode)

        self.apply_styles()


    
    # Apply style sheet
    def apply_styles(self):
        self.setStyleSheet(
            """
            FinanceApp {
                background-color: #f0f0f0;
            }
            QLabel, QLineEdit, QPushButton{
                background-color: #f8f8f8;
            }
            QTreeView{
                background-color: #ffffff    
            }

            """
        )
        """
        Applies light or dark styles based on the dark mode checkbox.
        """
        if self.dark_mode.isChecked():
            self.setStyleSheet(
                """
                FinanceApp {
                    background-color: #222222;
                }
                QLabel, QLineEdit, QPushButton{
                    background-color: #333333;
                    color: #eeeeee
                }
                QTreeView{
                    background-color: #ffffff  
                    color: #eeeeee  
                }

                """
            )

    def toggle_mode(self):
        """
        Toggles between dark mode and light mode.
        """
        self.apply_styles()

    # Calculate Interest
    def calc_interest(self):
        """
        Calculates compound interest and updates the tree view and chart.
        """
        initial_investment = None
        try:
            interest_rate = float(self.rate_input.text())
            initial_investment = float(self.initial_input.text())
            num_years = int(self.years_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Invelid Input , Enter A Number")

        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Year", "Total"])

        total = initial_investment
        for year in range (1, num_years+1):
            total += total*(interest_rate/100)
            item_year = QStandardItem(str(year))
            item_total = QStandardItem("{:.2f}".format(total))
            self.model.appendRow([item_year, item_total])

        # Update chart with data
        self.figure.clear()
        plt.style.use('seaborn-v0_8')
        ax = self.figure.subplots()
        years = list(range(1,num_years+1))
        totals = [initial_investment*(1+interest_rate/100)**year for year in years]

        ax.plot(years, totals)
        ax.set_title("Interest Chart")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total")
        self.canvas.draw()

    def save_data(self):
        """
        Saves tree view data and chart image to a user-selected directory.
        """
        dir_path = QFileDialog.getExistingDirectory(self, "Select Diractory")
        if dir_path:
            folder_path = os.path.join(dir_path, "Saved")
            os.makedirs(folder_path, exist_ok=True)

            file_path = os.path.join(folder_path, "results.csv")
            with open (file_path, 'w') as file:
                file.write("Year, Total\n")
                for row in range(self.model.rowCount()):
                    year = self.model.index(row, 0).data()
                    total = self.model.index(row, 1).data()

                    file.write("{},{}\n".format(year, total))


            plt.savefig("Saved/chart.png")
            QMessageBox.information(self, "Save Results", "Results we saved to the folder")
        else:
            QMessageBox.warning(self, "Save Results", "No Directory Selected")

    def reset(self):
        """
        Clears all input fields, chart, and tree view data.
        """
        self.rate_input.clear()
        self.initial_input.clear()
        self.years_input.clear()
        self.model.clear()

        self.figure.clear()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication([])
    my_app = FinanceApp()
    my_app.show()
    app.exec_()