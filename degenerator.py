import numpy as np
import random
from solver import solve_equation_problem


# коментарии к переменным
# seed - seed
# group_number - номер варианта
# task_per_qroup - количество заданий в варианте
# number_of_parameters - i количество для x_i и x̄_i


def k_radit(a, b):
    first = 0
    second = 0

    for i in range(len(a)):
        first += min(a[i], b[i])
        second += np.abs(a[i] - b[i])

    second += first

    return first, second


def unison_shuffled_copies(a, b):
    assert len(a) == len(b)

    for i in range(len(a)):
        if bool(random.getrandbits(1)):
            a[i], b[i] = b[i], a[i]

    p = [i for i in range(len(a))]
    random.shuffle(p)
    return [a[i] for i in p], [b[i] for i in p]


# функция генерирования варианта
def task_generator(seed, group_number_first, group_number_last, task_per_qroup, number_of_parameters):
    # вставляем seed для случайных чисел
    random.seed(seed)

    # пропускаем все значения до этого варианта (это долго будет при больших вариантах)
    for i in range(group_number_first):
        for j in range(task_per_qroup):
            a = []
            b = []

            if number_of_parameters <= 1:
                a = []
                b = []
                a.append(random.randint(1, 10))
                if bool(random.getrandbits(1)):
                    a[-1] = -a[-1]
                b.append(random.randint(1, 10))
                if bool(random.getrandbits(1)):
                    b[-1] = -b[-1]

            if number_of_parameters == 2:
                a = []
                b = []

                a.append(random.randint(1, 10))
                if bool(random.getrandbits(1)):
                    a[-1] = -a[-1]
                a.append(random.randint(1, 10))
                if bool(random.getrandbits(1)):
                    a[-1] = -a[-1]
                b.append(random.randint(1, 10))
                if bool(random.getrandbits(1)):
                    b[-1] = -b[-1]
                b.append(0)

            if number_of_parameters > 2:
                k = random.randint(1, 5)
                if bool(random.getrandbits(1)):
                    k = -k

                answers = []

                for z in range((number_of_parameters - 1) // 2):
                    answers.append(random.randint(1, 10))
                    if bool(random.getrandbits(1)) or answers[-1] == k:
                        answers[-1] = -answers[-1]

                    answers.append(k - answers[-1])

                answers.append(0)

                if number_of_parameters % 2 == 0:
                    answers.append(random.randint(1, 5))
                    if bool(random.getrandbits(1)) or answers[-1] == k:
                        answers[-1] = -answers[-1]

                    answers.append(random.randint(1, 5))
                    if bool(random.getrandbits(1)) or answers[-1] == k:
                        answers[-1] = -answers[-1]

                    if answers[-1] == answers[0]:
                        answers[-1] = k - answers[0]

                    if answers[-1] + answers[-2] == k or answers[-1] + answers[-2] == 0:
                        answers[-1] += k + answers[0]

                    answers[-3] = k - answers[-1] - answers[-2]
                else:
                    answers.append(random.randint(1, 5))
                    if bool(random.getrandbits(1)) or answers[-1] == k:
                        answers[-1] = -answers[-1]

                    if answers[-1] == answers[0]:
                        answers[-1] = k - answers[0]

                    answers.append(random.randint(1, 5))
                    if bool(random.getrandbits(1)) or answers[-1] == k:
                        answers[-1] = -answers[-1]

                    if answers[-1] == answers[1]:
                        answers[-1] = k - answers[1]

                    if answers[-1] + answers[-2] == k or answers[-1] + answers[-2] == 0:
                        answers[-1] += k + answers[1]

                    answers[-3] = k - answers[-1] - answers[-2]

                a = answers[0:number_of_parameters]
                b = answers[number_of_parameters:]
                b = list(np.concatenate((b, list(np.repeat(0, number_of_parameters - len(b))))))

            unison_shuffled_copies(a, b)

    vlist = []
    dlist = []

    for v in range(group_number_last - group_number_first):
        # наш глист
        glist = []
        slist = []
        for i in range(task_per_qroup):
            # генерируем массивы коэфицентов для переменных x_i и x̄_i для каждой задачи
            a = []
            b = []
            k = 0

            if number_of_parameters <= 1:
                a = []
                b = []
                a.append(random.randint(1, 10))
                if bool(random.getrandbits(1)):
                    a[-1] = -a[-1]
                b.append(random.randint(1, 10))
                if bool(random.getrandbits(1)):
                    b[-1] = -b[-1]
                k = a[-1]

            if number_of_parameters == 2:
                a = []
                b = []

                a.append(random.randint(1, 10))
                if bool(random.getrandbits(1)):
                    a[-1] = -a[-1]
                a.append(random.randint(1, 10))
                if bool(random.getrandbits(1)):
                    a[-1] = -a[-1]
                k = np.sum(a)
                b.append(random.randint(1, 10))
                if bool(random.getrandbits(1)):
                    b[-1] = -b[-1]
                b.append(0)

            if number_of_parameters > 2:
                k = random.randint(1, 5)
                if bool(random.getrandbits(1)):
                    k = -k

                answers = []

                for j in range((number_of_parameters - 1) // 2):
                    answers.append(random.randint(1, 10))
                    if bool(random.getrandbits(1)) or answers[-1] == k:
                        answers[-1] = -answers[-1]

                    answers.append(k - answers[-1])

                answers.append(0)

                if number_of_parameters % 2 == 0:
                    answers.append(random.randint(1, 5))
                    if bool(random.getrandbits(1)) or answers[-1] == k:
                        answers[-1] = -answers[-1]

                    answers.append(random.randint(1, 5))
                    if bool(random.getrandbits(1)) or answers[-1] == k:
                        answers[-1] = -answers[-1]

                    if answers[-1] == answers[0]:
                        answers[-1] = k - answers[0]

                    if answers[-1] + answers[-2] == k or answers[-1] + answers[-2] == 0:
                        answers[-1] += k + answers[0]

                    answers[-3] = k - answers[-1] - answers[-2]
                else:
                    answers.append(random.randint(1, 5))
                    if bool(random.getrandbits(1)) or answers[-1] == k:
                        answers[-1] = -answers[-1]

                    if answers[-1] == answers[0]:
                        answers[-1] = k - answers[0]

                    answers.append(random.randint(1, 5))
                    if bool(random.getrandbits(1)) or answers[-1] == k:
                        answers[-1] = -answers[-1]

                    if answers[-1] == answers[1]:
                        answers[-1] = k - answers[1]

                    if answers[-1] + answers[-2] == k or answers[-1] + answers[-2] == 0:
                        answers[-1] += k + answers[1]

                    answers[-3] = k - answers[-1] - answers[-2]

                a = answers[0:number_of_parameters]
                b = answers[number_of_parameters:]
                b = list(np.concatenate((b, list(np.repeat(0, number_of_parameters - len(b))))))

            a, b = unison_shuffled_copies(a, b)
            glist.append([a, b, k])
            slist.append(solve_equation_problem(glist[-1][0], glist[-1][1], glist[-1][2]))

        vlist.append(glist)
        dlist.append(slist)

    return vlist, dlist
