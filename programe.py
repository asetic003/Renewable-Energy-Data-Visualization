from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QLabel, QComboBox, QPushButton, QSlider
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt
import sys
import pandas as pd

df = pd.read_csv(r"D:\pyqlt\factbook-2020\data.csv")

class Window(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setStyleSheet("background-color: grey; color: white;")

        self.xComboBox = QComboBox(self)
        self.xComboBox.addItems(df['Entity'].unique())

        self.xLabel = QLabel("&Country")
        self.xLabel.setBuddy(self.xComboBox)

        self.figure, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [])  

        self.canvas = FigureCanvas(self.figure)

        self.slider_start = QSlider(Qt.Horizontal, self)
        self.slider_end = QSlider(Qt.Horizontal, self)

   
        self.slider_start.setMinimum(1965)
        self.slider_start.setMaximum(2022)
        self.slider_start.setValue(1965)  

        self.slider_end.setMinimum(1965)
        self.slider_end.setMaximum(2022)
        self.slider_end.setValue(2022)  

        self.slider_start.setTickPosition(QSlider.TicksBothSides)
        self.slider_start.setTickInterval(5)

        self.slider_end.setTickPosition(QSlider.TicksBothSides)
        self.slider_end.setTickInterval(5)

        self.range_label = QLabel("Selected Range: N/A", self)

        button = QPushButton("Show me the graph", self)
        button.pressed.connect(self.changeValue)

        grid = QVBoxLayout(self)
        grid.addWidget(self.xLabel)
        grid.addWidget(self.xComboBox)
        grid.addWidget(self.range_label)
        grid.addWidget(self.slider_start)
        grid.addWidget(self.slider_end)
        grid.addWidget(button)
        grid.addWidget(self.canvas)

    def changeValue(self):
        print("Button pressed!")

        country = self.xComboBox.currentText()

        country_data = df[df['Entity'] == country]

        start_year = self.slider_start.value()
        end_year = self.slider_end.value()

        selected_years = country_data[(country_data['Year'] >= start_year) & (country_data['Year'] <= end_year)]

        self.ax.clear()

        self.ax.plot(selected_years['Year'], selected_years['percentage score'])

        self.ax.set(xlabel='Years', ylabel='Percentage', title=f'Renewable Energy Percentage Over Years - {country}')

        self.canvas.draw()

       
        self.range_label.setText(f"Selected Range: {start_year} to {end_year}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.setWindowTitle("Renewable Energy Data Visualization")
    main.show()
    sys.exit(app.exec_())
