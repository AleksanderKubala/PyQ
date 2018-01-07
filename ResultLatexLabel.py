from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from config import label_width, label_height, figure_dpi
from sympy import *

class ResultLatexLabel(FigureCanvasQTAgg):

    def __init__(self, text, color):
        super().__init__(self._create_latex(text, color))

    def _create_latex(self, value, color):
        r, g, b, a = color.getRgbF()
        figure = Figure(dpi=figure_dpi, edgecolor=(r,g,b), facecolor=(r,g,b))
        figure.clear()
        figure.suptitle(r'$' + latex(sympify(value)) + '$', y=0.875)
        figure.set_figwidth(label_width/figure_dpi)
        figure.set_figheight(label_height/figure_dpi)
        return figure
