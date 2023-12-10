import os
import shutil
import subprocess


def make_tex_code(tasks,
                  answers,
                  group_number_first,
                  group_number_last,
                  task_per_group,
                  dir_path=os.path.dirname(__file__)):
    if not os.path.isdir(dir_path):
        raise ValueError('Path is not a directory')

    tasks_text = ''

    # превращаем лист задач в текст
    for i in range(group_number_last - group_number_first + 1):
        tasks_text += '\\textbf{Вариант ' + str(i + group_number_first) + '\hspace{2cm} Студент:\hrulefill \hrulefill \hrulefill \hspace{2cm} Сдано:\hrulefill}\n\n'
        for j in range(len(tasks[i])):
            tasks_text += '{}. Решите уравнение: \n\n $'.format(j + 1)

            tasks_string = ''

            for k in range(len(tasks[i][j][0])):
                if tasks[i][j][0][k] > 0:
                    tasks_string += '+ ' + str(tasks[i][j][0][k]) + 'x_{' + str(k + 1) + '} '
                if tasks[i][j][0][k] < 0:
                    tasks_string += '- ' + str(abs(tasks[i][j][0][k])) + 'x_{' + str(k + 1) + '} '
                if tasks[i][j][0][k] == 0:
                    tasks_string += ''

                if tasks[i][j][1][k] > 0:
                    tasks_string += '+ ' + str(tasks[i][j][1][k]) + '\\bar{x}_{' + str(k + 1) + '} '
                if tasks[i][j][1][k] < 0:
                    tasks_string += '- ' + str(abs(tasks[i][j][1][k])) + '\\bar{x}_{' + str(k + 1) + '} '
                if tasks[i][j][1][k] == 0:
                    tasks_string += ''

            if tasks_string[0] == '+':
                tasks_string = tasks_string.replace('+ ', '', 1)

            tasks_text += tasks_string + '= ' + str(tasks[i][j][2]) + '$ \n\n \\ \n\n'

    answers_text = ''

    # превращаем лист ответов в текст
    for i in range(group_number_last - group_number_first + 1):
        answers_text += '\\textbf{Вариант ' + str(i + group_number_first) + '}\n\n'
        for h in range(task_per_group):
            solution = answers[i][h]
            answers_text += 'Уравнение {}: '.format(h + 1)
            if not solution:
                answers_text += 'Нет решения\n\n'
            else:
                answers_text += '($'
                for x in range(len(solution)):
                    for y in range(len(solution[x])):
                        answers_text += str(solution[x][y]) + ','
                    answers_text = answers_text[:-1]
                    answers_text += '$), ($'
                answers_text = answers_text[:-3]
                answers_text = answers_text[:-1]
                answers_text += '\n\n \\ \n\n'

    content = r'''\documentclass[a4paper, 12pt, russian, utf8]{article}
    
\usepackage[T1,T2A]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[russian]{babel}
\usepackage{geometry}


\begin{document}

\textbf{\Large Постройте общее решение псевдобулевского уравнения. \\}



''' + tasks_text + r'''

\newpage
\newgeometry{left=2cm, right=5cm, top=2cm, bottom=2cm}

\textbf{\huge Ответы \\}



''' + answers_text + r'''
    
\end{document}'''

    with open(dir_path + r'\cover.tex', 'w', encoding='utf8') as f:
        f.write(content)

    cmd = ['pdflatex', '-interaction', 'nonstopmode', dir_path + r'\cover.tex']
    proc = subprocess.Popen(cmd)
    proc.communicate()

    ret_code = proc.returncode
    if not ret_code == 0:
        # os.unlink('cover.pdf')
        raise ValueError('Error {} executing command: {}'.format(ret_code, ' '.join(cmd)))

    # os.unlink('cover.tex')

    # os.replace('cover.pdf', dir_path + r'\cover.pdf')
    shutil.move('cover.pdf', dir_path + r'\cover.pdf')
    os.unlink('cover.log')
    os.unlink('cover.aux')

    return
