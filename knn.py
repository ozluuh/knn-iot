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
        normalized_sample.insert(idx, round_default(value, decimal))
    
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
    _, no_recurrence, recurrence = info_dataset(samples, clazz, info)

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


# Dados pra teste
keys = {
    0: {
        "data": ["no-recurrence-events", "recurrence-events"],
        "decimal": 0
    },
    1: ["10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90-99"],
    2: ["lt40", "ge40", "premeno"],
    3: ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59"],
    4: ["0-2", "3-5", "6-8", "9-11", "12-14", "15-17", "18-20", "21-23", "24-26", "27-29", "30-32", "33-35", "36-39"],
    5: {
        "data": ["?", "yes", "no"],
        "min": 1,
        "decimal": 0
    },
    6: ["1","2","3"],
    7: ["left","right"],
    8: ["?","left_up", "left_low", "right_up", "right_low", "central"],
    9: {
        "data": ["?", "yes", "no"],
        "min": 1,
        "decimal": 0
    }
}

# Usando arquivo editado/simplificado contendo apenas 10 registros
amostras = open_file("breast-cancer.data", keys)

separate_samples(amostras, 0, 0.5)

info_dataset(amostras, 0)