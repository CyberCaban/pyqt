from pathlib import Path
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCharts import QChart, QChartView, QPieSeries
import pandas as pd
from .Flex import ColLayout


def find_file(rel_path: str):
    return str(Path(__file__).resolve().parent / rel_path)


class HurricanesPlot(QWidget):
    def __init__(self):
        super().__init__()

        try:
            file_path = find_file("../public/hurricanes.csv")
            df = pd.read_csv(file_path)
            print(df)

            self.setLayout(
                ColLayout(self._add_yearly_plot(df), self._add_monthly_plot(df))
            )

        except Exception as e:
            error_label = QLabel(f"Error loading hurricanes data: {str(e)}")
            layout = ColLayout(error_label)
            self.setLayout(layout)

    def _add_monthly_plot(self, df):
        series = QPieSeries()
        series.setName("Hurricanes by month")

        for index, row in df.iterrows():
            month = row["Month"]
            count = row[2:].sum()
            series.append(month, count)

        if series.slices():
            max_slice = max(series.slices(), key=lambda s: s.value())
            max_slice.setExploded(True)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Hurricanes in 2007 by month")

        return QChartView(chart)

    def _add_yearly_plot(self, df):
        series = QPieSeries()
        series.setName("Hurricanes by year")

        yearly_counts = df.iloc[:, 2:].sum()

        for year_index in range(2005, 2016):
            series.append(str(year_index), yearly_counts.iloc[year_index - 2005])

        if series.slices():
            min_slice = min(series.slices(), key=lambda s: s.value())
            min_slice.setExploded(True)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Hurricanes by year")

        return QChartView(chart)
