import sys
import os

# إضافة المسارات إلى النظام
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "GUI"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "GeometryFunctions"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "RadialStructure"))

import tkinter as tk
from GUI.gui_integrated import PolygonSubdivisionGUI

def main():
    root = tk.Tk()
    app = PolygonSubdivisionGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()