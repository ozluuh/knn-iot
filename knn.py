#!/usr/bin/env python

# Módulos (Bibliotecas)
import math


# Definição das funções
# Utilizando como base Euclidiana
def calc_distance(item1, item2):
    if type(item1) is not list or type(item2) is not list:
        raise ValueError(f"É esperado uma lista como argumento e foi passado {type(item1)} e {type(item2)}")
    if len(item1) != len(item2):
        raise RuntimeError(f"Comprimento das listas divergentes. Verifique os dados de entrada.")

    total = 0

    for p in range(len(item1)):
        total += (item1[p] - item2[p]) ** 2

    return math.sqrt(total)


def calc_hypotenuse(a, b):
    return math.sqrt(a * a + b * b)


def open_file(filename, dic):
    samples = []

    with open(filename, "r") as dataset:
        for line in dataset.readlines():
            tempdata = line.replace("\n", "").split(",")

            data = format_with(tempdata, dic)
            samples.append(data)

    return samples


def format_with(sample_list, dict_):
    if type(sample_list) is not list:
        raise ValueError(f"É esperado uma lista como argumento e foi passado {type(sample_list)}")

    normalized_sample = []
    
    for idx in range(len(sample_list)):
        dict_items = dict_[idx]
        v_min = 0
        decimal = 2

        if type(dict_items) is dict:
            _temp = dict_items

            if "remove" in _temp:
                continue
            
            dict_items, v_min, decimal = normalize_obj_items(_temp)
            
            del _temp
        
        items_max_len = len(dict_items) - 1
        item_dict_pos = dict_items.index(sample_list[idx])

        value = normalize_scale(item_dict_pos, items_max_len, v_min)
        normalized_sample.append(round_default(value, decimal))
    
    return normalized_sample

def normalize_obj_items(item):
    dict_items = item["data"]
    v_min = 0
    decimal = 2

    if "min" in item:
        v_min = item["min"]
    if "decimal" in item:
        decimal = item["decimal"]
    if "reverse" in item:
        dict_items.reverse()
    
    return dict_items, v_min, decimal

# Realiza a conversão entre escalas
# Dica: em caso de trabalhar com lista, definir o comprimento - 1
def normalize_scale(x, v_max, v_min):
    return (x - v_min) / (v_max - v_min)

# Define a quantidade de casas decimais
def round_default(value, pos = None):
    if pos is None:
        return value
    
    if pos == 0:
        return round(value)
    
    return round(value, pos)


# Quantidade de amostras por classe
def info_dataset(samples, clazz_pos, info = True):
    output = {}

    for sample in samples:
        sample_clazz = sample[clazz_pos]
        try:
            output[sample_clazz] = output[sample_clazz] + 1
        except KeyError:
            output[sample_clazz] = 1

    if info:
        print('Total de amostras: ', len(samples))
        print('Amostras: ', output)

    # Total de amostras + Total por classes (ordenado de acordo com posição)
    return [len(samples)] + [x for x in output.values()]


# Separa o conjunto de treinamento e testes
# perc = Percentual de treinamento (teste será calculado automaticamente)
def separate_samples(samples, clazz, perc, info = True):
    _, recurrence, no_recurrence = info_dataset(samples, clazz, info)

    max_output_no_recurrence = int(perc * no_recurrence)
    max_output_recurrence = int((1.0 - perc) * recurrence)

    amount_no_recurrence = 0
    amount_recurrence = 0

    training_samples = []
    test_samples = []

    for sample in samples:
        if(amount_no_recurrence + amount_recurrence) < (max_output_no_recurrence + max_output_recurrence):
            # Conjunto de treinamento
            training_samples.append(sample)
            
            if sample[clazz] == 1 and amount_no_recurrence < max_output_no_recurrence:
                amount_no_recurrence += 1
            else:
                amount_recurrence += 1
        else:
            # Conjunto de teste
            test_samples.append(sample)
    
    if info:
        print(f"Máximo de amostras para não recorrência: {max_output_no_recurrence}")
        print(f"Máximo de amostras para recorrência: {max_output_recurrence}")

    return (training_samples, test_samples)

def knn(training_samples, sample_test, k, clazz):
    distances = {}
    
    # Distância euclidiana de uma amostra sobre o conjunto
    for idx in range(len(training_samples)):
        distance = calc_distance(training_samples[idx], sample_test)
        distances[idx] = distance

    # Chaves dos vizinhos mais próximos
    neighboors = sorted(distances, key=distances.get)[:k]

    # print(neighboors)

    # Votação
    amount_no_recurrence = 0
    amount_recurrence = 0

    for idx in neighboors:
        if training_samples[idx][clazz] == 1: # saída da classe 1 (Não Recorrência)
            amount_no_recurrence += 1
        else:
            amount_recurrence += 1
    
    if amount_no_recurrence > amount_recurrence:
        return 1
    
    return 0


# Dados pra teste
keys = {
    # Class
    0: {
        "data": ["recurrence-events", "no-recurrence-events"],
        "decimal": 0
    },
    # Age
    1: {
        "data": ["10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90-99"],
        "min": 4
    },
    # Menopause
    2: {
        "data": ["lt40", "ge40", "premeno"],
        "min": 1
    },
    # Tumor-size
    3: {
        "data": ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59"],
        "min": 5.5
    },
    # Inv-nodes
    4: {
        "data": ["0-2", "3-5", "6-8", "9-11", "12-14", "15-17", "18-20", "21-23", "24-26", "27-29", "30-32", "33-35", "36-39"],
        "min": 6,
        "remove": 1
    },
    # Node-caps
    5: {
        "data": ["?", "yes", "no"],
        "min": 1,
        "remove": 1
    },
    # Deg-malig
    6: ["1","2","3"],
    # Breast
    7: {
        "data": ["left","right"],
        # "remove": 1
    },
    # Breast-quad
    8: {
        "data": ["?","left_up", "left_low", "right_up", "right_low", "central"],
        "remove": 1
    },
    # Irradiant
    9: {
        "data": ["yes", "no"]
    }
}

amostras = open_file("breast-cancer.data", keys)

# print(f"Amostras: {amostras}")

# Percentual de treinamento
perc=0.8
clazz=0

training, test = separate_samples(amostras, clazz, perc)

amount_success = 0
k=17

for sample in test:
    class_result = knn(training, sample, clazz=clazz, k=k)
    if sample[clazz] == class_result:
        amount_success += 1

print(f"Total Treinamento: {len(training)}")
print(f"Total Teste: {len(test)}")
print(f"Total Acertos: {amount_success}")
print(f"Porcentagem Acerto: {round_default(100*amount_success/len(test), 0)}%")