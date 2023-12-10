from degenerator import task_generator
from texCreator import make_tex_code
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog


class DegeneratorApp(tk.Tk):
    WINDOW_TITLE = 'Генератор псевдобулевских уравнений'
    FONT = 'TkTextFont 18'

    def __init__(self):
        super().__init__()

        self.title(self.WINDOW_TITLE)
        self.eval('tk::PlaceWindow . center')

        self.frame = tk.Frame(self, padx=10, pady=10)
        self.frame.grid()

        self.pady = 5

        self.seed_label = tk.Label(self.frame, text='Сид генератора:',
                                   font=self.FONT, justify='right')
        self.seed_label.grid(row=0, column=0, sticky='se', pady=self.pady)

        self.variants_begin_label = tk.Label(self.frame, text='Номер начала вариантов:',
                                             font=self.FONT, justify='right')
        self.variants_begin_label.grid(row=1, column=0, sticky='se', pady=self.pady)

        self.variants_end_label = tk.Label(self.frame, text='Номер конца вариантов:',
                                           font=self.FONT, justify='right')
        self.variants_end_label.grid(row=2, column=0, sticky='se', pady=self.pady)

        self.tasks_number_per_variant_label = tk.Label(self.frame, text='Количество задач в варианте:',
                                                       font=self.FONT, justify='right')
        self.tasks_number_per_variant_label.grid(row=3, column=0, sticky='se', pady=self.pady)

        self.variables_number_per_task_label = tk.Label(self.frame, text='Количество переменных в задаче:',
                                                        font=self.FONT, justify='right')
        self.variables_number_per_task_label.grid(row=4, column=0, sticky='se', pady=self.pady)

        self.seed_entry = tk.Entry(self.frame, font=self.FONT)
        self.seed_entry.grid(row=0, column=1, sticky='swe', pady=self.pady)

        self.variants_begin = tk.IntVar(value=1)
        self.variants_begin_scale = tk.Scale(self.frame, font=self.FONT,
                                             variable=self.variants_begin,
                                             from_=1, to=49, orient=tk.HORIZONTAL)
        self.variants_begin_scale.bind('<ButtonRelease-1>', self.update_variants_end_scale)
        self.variants_begin_scale.grid(row=1, column=1, sticky='swe', pady=self.pady)

        self.variants_end = tk.IntVar(value=5)
        self.variants_end_scale = tk.Scale(self.frame, font=self.FONT,
                                           variable=self.variants_end,
                                           from_=2, to=50, orient=tk.HORIZONTAL)
        self.variants_end_scale.grid(row=2, column=1, sticky='swe', pady=self.pady)

        self.tasks_number_per_variant = tk.IntVar(value=3)
        self.tasks_number_per_variant_scale = tk.Scale(self.frame, font=self.FONT,
                                                       variable=self.tasks_number_per_variant,
                                                       from_=1, to=50, orient=tk.HORIZONTAL)
        self.tasks_number_per_variant_scale.grid(row=3, column=1, sticky='swe', pady=self.pady)

        self.variables_number_per_task = tk.IntVar(value=5)
        self.variables_number_per_task_scale = tk.Scale(self.frame, font=self.FONT,
                                                        variable=self.variables_number_per_task,
                                                        from_=1, to=10, orient=tk.HORIZONTAL)
        self.variables_number_per_task_scale.grid(row=4, column=1, sticky='swe', pady=self.pady)

        self.generate_button = tk.Button(self, text='Сгенерировать!', command=self.generate,
                                         font=self.FONT, bg='#006eb9', fg='white')
        self.generate_button.grid(column=0, row=5, columnspan=2, pady=self.pady + 5)

        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        self.minsize(w, h)
        self.maxsize(w, h)

        self.mainloop()

    def update_variants_end_scale(self, _event):
        self.variants_end_scale.configure(from_=self.variants_begin_scale.get() + 1)

    def generate(self):
        if self.variants_begin.get() > self.variants_end.get():
            messagebox.showerror('Ошибка', 'Номер начала вариантов больше номера конца вариантов!')
            return

        selected_directory = filedialog.askdirectory(title='Выберите папку')
        if selected_directory == '':
            return

        tasks, answers = task_generator(self.seed_entry.get(),
                                        self.variants_begin.get() - 1,
                                        self.variants_end.get(),
                                        self.tasks_number_per_variant.get(),
                                        self.variables_number_per_task.get())

        make_tex_code(tasks, answers, self.variants_begin.get(),
                      self.variants_end.get(), self.tasks_number_per_variant.get(),
                      selected_directory)

        messagebox.showinfo('Успех',
                            'Задачи успешно сгенерированы по указанному пути ({}).'.format(selected_directory))


def main():
    DegeneratorApp()


if __name__ == '__main__':
    main()
