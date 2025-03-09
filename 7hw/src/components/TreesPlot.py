from pathlib import Path
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QScatterSeries
import pandas as pd
from .Flex import ColLayout


def find_file(rel_path: str):
    return str(Path(__file__).resolve().parent / rel_path)


class TreesPlot(QWidget):
    def __init__(self):
        super().__init__()

        try:
            file_path = find_file("../public/trees.csv")
            df = pd.read_csv(file_path)

            chart = QChart()
            chart.setTitle("Trees Data")

            scatter = QScatterSeries()
            scatter.setName("Scatter")

            if "x" in df.columns and "y" in df.columns:
                for index, row in df.iterrows():
                    scatter.append(row["x"], row["y"])
            else:
                numeric_cols = df.select_dtypes(include=["number"]).columns
                if len(numeric_cols) >= 2:
                    for index, row in df.iterrows():
                        scatter.append(row[numeric_cols[0]], row[numeric_cols[1]])

            bar = QBarSeries()
            bar_set = QBarSet("Bars")

            if len(numeric_cols) > 0:
                for index, row in df.iterrows():
                    bar_set.append(row[numeric_cols[0]])
                bar.append(bar_set)

            if scatter.count() > 0:
                chart.addSeries(scatter)
            if bar.count() > 0:
                chart.addSeries(bar)

            chart.createDefaultAxes()

            chart_view = QChartView(chart)

            layout = ColLayout(chart_view)
            self.setLayout(layout)

        except Exception as e:
            error_label = QLabel(f"Error loading data: {str(e)}")
            layout = ColLayout(error_label)
            self.setLayout(layout)
