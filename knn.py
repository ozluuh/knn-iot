#!/usr/bin/env python
import math

# Math
def distancia_euclidiana(p1, p2):
    total = 0

    for i in range(len(p1)):
        total += (p1[i] - p2[i]) ** 2
    
    return math.sqrt(total)

def escala_normalizada(x, v_max, v_min):
    return (x - v_min) / (v_max - v_min)

# Util
def ler_arquivo(filename, keys):
    amostras = []
    total_descarte = 0

    with open(filename, "r") as dataset:
        for instancia in dataset.readlines():
            x = instancia.replace("\n", "").split(",")
            
            try:
                amostra_normalizada = normalizar_arquivo(x, keys)
                amostras.append(amostra_normalizada)
            except ValueError:
                total_descarte += 1


    with open("output.data", "w") as output:
        for item in amostras:
            item_string = str(item).replace("[","").replace("]","")
            output.write(f"{item_string}\n")

    print(f"Total amostras descartadas: {total_descarte}")

    return amostras

def normalizar_arquivo(amostra, names):
    amostra_normalizada = []

    for indice in range(len(amostra)):
        itens = names[indice] # Obtém os valores possíveis para aquela chave
        v_min = 0
        decimal = 2
        normalize = 1

        if type(itens) is dict: # verifica se os valores são chaves
            temp_itens = itens
            itens = temp_itens["data"] # Pega os valores para aquela chave

            if "remove" in temp_itens:
                continue

            if "min" in temp_itens: # se estipulado um mínimo, altera para ele invés do padrão
                v_min = temp_itens["min"]
            if "decimal" in temp_itens: # se possui decimal, usa ele invés do padrão
                decimal = temp_itens["decimal"]
            if "reverse" in temp_itens:
                itens.reverse()
            if "normalize" in temp_itens:
                normalize = temp_itens["normalize"]

            del temp_itens

        valor_atual = amostra[indice] # Posição atual na amostra
        valor = valor_atual

        if normalize:
            v_max = len(itens) - 1 # Tamanho total da lista - 1 (lista inicia em 0)
            item_indice = itens.index(valor_atual) # indíce do valor da amostra na lista de valores possíveis

            valor = escala_normalizada(item_indice, v_max, v_min)
        
        amostra_normalizada.append(arred(float(valor), decimal))
    
    return amostra_normalizada

def arred(valor, decimal = None):
    if decimal is None:
        return valor
    
    if decimal == 0:
        return round(valor)
    
    return round(valor, decimal)

# Análise
def info_dataset(amostras, classe, info=True):
    output1, output2 = 0,0

    for amostra in amostras:
        if amostra[classe] == 1:
            output1 += 1 # Paciente sem recorrências
        else:
            output2 += 1 # Paciente com recorrências

    if info == True:
        print(f"Total de amostras................: {len(amostras)}")
        print(f"Total Normal (Sem recorrência)...: {output1}")
        print(f"Total Alterado (Com recorrência).:  {output2}")

    return [len(amostras), output1, output2]

def separar_amostras(amostras, porcentagem, classe):
    _, output1, output2 = info_dataset(amostras, classe)

    treinamento = []
    teste = []

    max_output1 = int(porcentagem*output1)
    max_output2 = int((1 - porcentagem)*output2)

    total_output1 = 0
    total_output2 = 0

    for amostra in amostras:
        if(total_output1 + total_output2) < (max_output1 + max_output2):
            # Inserir em treinamento
            treinamento.append(amostra)
            if amostra[classe] == 1 and total_output1 < max_output1:
                total_output1 += 1
            else:
                total_output2 += 1
        else:
            # Insere em teste
            teste.append(amostra)

    return [treinamento, teste]

def knn(treinamento, nova_amostra, classe, k):
    distancias = {}
    tamanho_treino = len(treinamento)

    # Calcula distância euclidiana
    for i in range(tamanho_treino):
        d = distancia_euclidiana(treinamento[i], nova_amostra)
        distancias[i] = d

    # Obtém k-vizinhos
    k_vizinhos = sorted(distancias, key=distancias.get)[:k] # retorna do começo até o k-1

    # Votação
    qtd_output1 = 0
    qtd_output2 = 0
    for indice in k_vizinhos:
        if treinamento[indice][classe] == 1: # saída normal
            qtd_output1 += 1
        else:                                # saída alterada
            qtd_output2 += 1
    
    if qtd_output1 > qtd_output2:
        return 1
    else:
        return 0

# Definição
names = {
    # Class
    0:{
        "data": ["recurrence-events", "no-recurrence-events"],
        "decimal": 0,
        "reverse": 1
    },
    # Age
    1:{
        "data": ["10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90-99"],
        "decimal": 1
    },
    # Menopause
    2:["lt40", "ge40", "premeno"],
    # Tumor-size
    3:{
        "data": ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59"],
        "decimal": 1
    },
    # Inv-nodes
    4:{
        "data": ["0-2", "3-5", "6-8", "9-11", "12-14", "15-17", "18-20", "21-23", "24-26", "27-29", "30-32", "33-35", "36-39"],
        "decimal": 1,
        "min": 6
    },
    # Node-caps
    5:{
        "data": ["yes", "no"],
    },
    # Deg-malig
    6:{
        "data": ["1","2","3"],
        "normalize": 0,
        "decimal": 0
    },
    # Breast
    7:{
        "data": ["left","right"],
        "decimal": 0
    },
    # Breast-quad
    8:{
        "data": ["left_up", "left_low", "right_up", "right_low", "central"],
    },
    # Irradiant
    9:{
        "data": ["yes", "no"],
        "decimal": 0,
        "reverse": 1
    }
}

# Teste
acertos = 0
pos_classe = 0
porcentagem = 0.8
k = 17
amostras = ler_arquivo("breast-cancer.data", names)

treinamento, teste = separar_amostras(amostras, porcentagem, pos_classe)

for amostra in teste:
    classe_retornada = knn(treinamento, amostra, pos_classe, k)
    # print(classe_retornada, amostra[pos_classe])
    if amostra[pos_classe] == classe_retornada:
        acertos += 1

print(f"Total de treinamento..: {len(treinamento)}")
print(f"Total de testes.......: {len(teste)}")
print(f"Total de acertos......: {acertos}")
print(f"Porcentagem de acerto.: {arred(100*acertos/len(teste), 0)} %")