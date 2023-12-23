from gui import *

# Создаем экземпляр Tkinter
root = tk.Tk()
root.option_add('*Font', 'Arial 12')
root.resizable(width=False, height=False)

# Создаем объект GUI
app = CustomsCalculatorGUI(root)

# Запускаем цикл обработки событий Tkinter
root.mainloop()