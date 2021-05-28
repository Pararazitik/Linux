import multiprocessing as mp
import yaml
import random
from typing import List

MATRIX1_FILE = "./data/matrix1.yml"
MATRIX2_FILE = "./data/matrix2.yml"
RESULT_FILE = "./data/result.yml"


def matrixShow(matrix):
    r = "\n" + "\n".join(["\t".join([str(cell) for cell in row]) for row in matrix])
    print(r)


def matrixRead(file_name: str) -> List[List[int]]:
    with open(file_name, "r") as file:
        return yaml.safe_load(file)


def matrixAdd(matrix, file_name):
    with open(file_name, "w") as file:
        yaml.safe_dump(matrix, file)


def matrixGenerating(n, m):
    matrix = []
    for i in range(n):
        matrix.append([])
        for j in range(m):
            matrix[i].append(random.randint(1, 100))
    return matrix


def work(i, j, A, B, que):
    buffer_list = []
    for k in range(len(A[0]) or len(B)):
        buffer_list.append(A[i][k] * B[k][j])

    result_dict = {"result": sum(buffer_list), "i": i, "j": j}

    que.put(result_dict)


def new_matrix_input():
    n = int(input("Введите кол-во строк в матрице -> "))
    m = int(input("Введите кол-во столбцов в матрице -> "))

    matrix1 = matrixGenerating(n, m)
    matrix2 = matrixGenerating(m, n)

    matrixAdd(matrix1, MATRIX1_FILE)
    matrixAdd(matrix2, MATRIX2_FILE)
    return matrix1, matrix2


def old_matrix_input():
    return matrixRead(MATRIX1_FILE), matrixRead(MATRIX2_FILE)


manager = mp.Manager()
commands_dict = {
    "1": old_matrix_input,
    "2": new_matrix_input,
}

matrix1 = None
matrix2 = None

while True:
    command_input = input(
        "Как вы хотите получить данные матриц?\n1. Загрузить из файла\n2. Сгенерировать новые значения\n-> "
    )
    if command_input in commands_dict:
        matrix1, matrix2 = commands_dict[command_input]()
        break
    else:
        print("Команда не найдена")

matrix_result = [
    [0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix2[0]))
]

matrixShow(matrix1)
matrixShow(matrix2)

processes_list = []

que = manager.Queue()

for i in range(len(matrix_result)):
    for j in range(len(matrix_result[i])):
        p = mp.Process(target=work, args=(i, j, matrix1, matrix2, que,), )
        processes_list.append(p)

for p in processes_list:
    p.start()
for p in processes_list:
    p.join()

for i in range(len(matrix_result)):
    for j in range(len(matrix_result[i])):
        r = que.get()
        matrix_result[r["i"]][r["j"]] = r["result"]

matrixShow(matrix_result)
matrixAdd(matrix_result, RESULT_FILE)
