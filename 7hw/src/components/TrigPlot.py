from PySide6.QtWidgets import QWidget
from PySide6.QtCharts import QChart, QChartView, QSplineSeries
from PySide6.QtCore import Qt
import math
from components.Flex import ColLayout


class TrigPlot(QWidget):
    def __init__(self):
        super().__init__()

        chart = QChart()
        chart.setTitle("Trigonometric Functions")

        sin_series = QSplineSeries()
        cos_series = QSplineSeries()

        for i in range(31):
            x = i * math.pi / 15
            sin_series.append(x, math.sin(x))
            cos_series.append(x, math.cos(x))

        sin_series.setName("sin(x)")
        cos_series.setName("cos(x)")
        chart.addSeries(sin_series)
        chart.addSeries(cos_series)

        chart.createDefaultAxes()

        chart_view = QChartView(chart)

        self.setLayout(ColLayout(chart_view))
