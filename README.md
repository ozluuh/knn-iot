# KNN - Aplicado a Medicina

Repositório dedicado a entrega do material para a realização do Checkpoint 2 de **Disruptive Architectures: Iot & IA**.

## Sobre

- **Informação Relevante:** Arquivo dataset possui instâncias que são descritas por 9 atributos, alguns deles são lineares e outros são nominais.
- **Número de Instâncias:** 286
- **Número de Atributos:** 9 + o atributo classe
- **Informação dos Atributos:** aqui são descritos os valores esperados em cada atributo
  |Atributo|Descrição|Valor|
  |-|-|-|
  |Class|Recorrência ou não após o tratamento|[no-recurrence-events, recurrence-events]|
  |age|Idade da paciente|[10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80-89, 90-99]|
  |menopause|Indica se a paciente é pré ou pós-menopausa no momento do diagnóstico|[lt40, ge40, premeno]|
  |tumor-size|Diâmetro do tumor (mm)|[0-4, 5-9, 10-14, 15-19, 20-24, 25-29, 30-34, 35-39, 40-44, 45-49, 50-54, 55-59]|
  |inv-nodes|Número de linfonodos axilares|[0-2, 3-5, 6-8, 9-11, 12-14, 15-17, 18-20, 21-23, 24-26, 27-29, 30-32, 33-35, 36-39]|
  |node-caps|Penetração do tumor na cápsula do linfonodo|[yes, no]|
  |deg-malig|Grau de malignidade do tumor|[1, 2, 3]|
  |breast|Mama em que o câncer pode ocorrer|[left, right]|
  |breast-quad|Quadrante da mama afetado considerando o bico como o centro|[left-up, left-low, right-up, right-low, central]|
  |irradiat|Histórico de radioterapia|[yes, no]|
- **Atributos cujos valores estão ausentes:** denotado por "?"
  |Atributo|Número de instâncias com valores ausentes|
  |-|-:|
  |node-caps|8|
  |breast-quad|1|
- **Distribuição da Classe:**
  - **no-recurrence-events:** 201 instâncias
  - **recurrence-events:** 85 instâncias
- **Total de possíveis entradas por Atributo:**
  |Atributo|Total|
  |-|-:|
  |Class| 2|
  |age| 9|
  |menopause| 3|
  |tumor-size| 12|
  |inv-nodes| 13|
  |node-caps| 2|
  |deg-malig| 3|
  |breast| 2|
  |breast-quad| 5|
  |irradiat| 2|

## Integrantes

|  RM   | Nome           |
| :---: | -------------- |
| 84198 | Daiane Estenio |
| 85398 | Luís Paulino   |

## Links interessantes

Sites e documentos que tiveram base para a elaboração desse checkpoint:

https://archive.ics.uci.edu/ml/datasets/breast+cancer

https://www.komen.org/wp-content/uploads/How-Hormones-Affect-Breast-Cancer_Portuguese.pdf

https://www.espacodevida.org.br/seu-espaco/clinico/o-que-grau-de-agressividade-do-cncer

http://www.oncoguia.org.br/conteudo/linfonodos-e-cancer/6814/1/
