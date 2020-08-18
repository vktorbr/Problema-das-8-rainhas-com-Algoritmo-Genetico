import random
import statistics

tamanho_individuo = 24
tamanho_populacao = 100
pais = 2
probabilidade_mutacao = 0.4
probabilidade_recombinacao = 0.9
fitness = 0

def individuo():
    individuo = []
    individuo = random.sample([0,1,2,3,4,5,6,7], 8)
    #print(individuo)
    return intToBin(individuo)

def populacao():
    populacao = []
    for i in range(tamanho_populacao):
        populacao.append(individuo())
    return populacao

def fitness(individual):
    #lista_int = binToInt(individual)
    #qtd = len(set([item for item in lista_int if lista_int.count(item) > 1]))
    #if(qtd > 0):
    #    return 0
    #else:
    n_colisoes = 0
    cont = 0
    for i in range(8):
        for j in range(i+1, 8):
            if (int(individual[(i*3) : ((i*3)+3)], 2)) == (int(individual[(j*3): ((j*3)+3)], 2)):
                n_colisoes = n_colisoes + 1
            #print("linha i:", i, "coluna i:", int(individual[(i*3) : ((i*3)+3)], 2), "linha j:", j, "coluna j:", int(individual[(j*3): ((j*3)+3)], 2), "J:", j)
            if (i - ((int(individual[(i*3) : ((i*3)+3)], 2))) == (j - (int(individual[(j*3): ((j*3)+3)], 2)))):
                #print("passou")
                n_colisoes = n_colisoes + 1
            if (i + ((int(individual[(i*3) : ((i*3)+3)], 2))) == (j + (int(individual[(j*3): ((j*3)+3)], 2)))):
                #print("passou novo")
                n_colisoes = n_colisoes + 1

    return (1/(1 + n_colisoes))

def selecao(populacao):
    selecionados = []
    #pegamos 5 candidados aleatoriamente da populacao
    for i in range(5):
        selecionados.append(populacao[random.randint(0, tamanho_populacao-1)])
    scored = [(fitness(i), i) for i in selecionados]
    #ordenamos os 5 candidados pelo fitness do pior para o melhor
    scored2 = [i[0] for i in sorted(scored)]
    scored = [i[1] for i in sorted(scored)]
    #pega apenas os 2 melhores ou seja os dois ultimos da lista
    selected = scored[(len(scored) - pais):]
    return selected

def selecaoRoleta(populacao):
    selecionados = []
    fitness_total = [fitness(i) for i in populacao]
    total = sum(fitness_total)
    probabilidade = []
    prob_anterior = 0
    #print(total)
    for i in populacao:
        prob = prob_anterior+(fitness(i)/total)
        #print(fitness(i), fitness(i)/total)
        probabilidade.append((prob_anterior, prob, i))
        prob_anterior = prob
    #print(probabilidade)
    cont = 2
    for j in range(2):
        aleatorio = random.uniform(0, 0.99999999999999999)
        #print(aleatorio)
        for i in probabilidade:
            if(aleatorio >= i[0] and aleatorio < i[1] and cont > 0):
                selecionados.append(i[2])
                cont -= 1
                #print(selecionados)
                break

    if(len(selecionados) == 0):
        scored = [(fitness(i), i) for i in populacao]
        scored = [i[1] for i in sorted(scored)]
        selecionados = scored[(len(scored) - pais):]
    return selecionados

def intToBin(lista):
    individuo = []
    for i in range(8):
        if(lista[i] == 0 or lista[i] == 1):
            individuo.append('00'+(bin(lista[i])[2:]))
        if (lista[i] == 2 or lista[i] == 3):
            individuo.append('0'+(bin(lista[i])[2:]))
        if lista[i] > 3:
            individuo.append(bin(lista[i])[2:])
    individuo_string = ''.join(individuo)
    return individuo_string

def binToInt(lista):
    listaNova = []
    for i in range(8):
        listaNova.append(int(lista[i*3:(i*3)+3], 2))
    return listaNova

def recombinacaoOrdem1(pais):
    filhos = [[-1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1]]
    if(random.random() <= probabilidade_recombinacao and pais[0] != pais[1]):
        aux = random.sample([0,1,2,3,4,5,6,7], 2)
        aux.sort()
        #print(aux)
        parents = []
        parents.append(binToInt(pais[0]))
        parents.append(binToInt(pais[1]))
        parent = random.sample(parents, 2)
        filhos[0][aux[0]:aux[1]+1] = parent[0][aux[0]:aux[1]+1]
        filhos[1][aux[0]:aux[1]+1] = parent[1][aux[0]:aux[1]+1]
        #print(filhos)
        cont_filho0 = aux[1]
        cont_filho1 = aux[1]
        for i in range(aux[1]+1, 8):
            if((parent[1][i] in filhos[0]) == False):
                cont_filho0 += 1
                filhos[0][cont_filho0] = parent[1][i]
            if ((parent[0][i] in filhos[1]) == False):
                cont_filho1 += 1
                filhos[1][cont_filho1] = parent[0][i]
        for j in range(0, 8):
            if -1 in filhos[0]:
                if ((parent[1][j] in filhos[0]) == False):
                    if cont_filho0 >= 7:
                        cont_filho0 = -1
                    cont_filho0 += 1
                    filhos[0][cont_filho0] = parent[1][j]
            if -1 in filhos[1]:
                if ((parent[0][j] in filhos[1]) == False):
                    if cont_filho1 >= 7:
                        cont_filho1 = -1
                    cont_filho1 += 1
                    filhos[1][cont_filho1] = parent[0][j]
    return filhos


def mutacao(filhos):
    for i in range(len(filhos)):
        if(random.random() <= probabilidade_mutacao):
            aux = random.sample([0,1,2,3,4,5,6,7], 2)
            pos1 = aux[0]
            pos2 = aux[1]
            aux2 = filhos[i][pos1]
            filhos[i][pos1] = filhos[i][pos2]
            filhos[i][pos2] = aux2
    return filhos

def mutacaoString(filhos):
    for i in range(len(filhos)):
        if(random.random() <= probabilidade_mutacao):
            aux =  random.sample([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23], 2)
            aux.sort()
            #print(aux)
            #print(filhos[i][0:aux[0]], "+", filhos[i][aux[0]], "+", filhos[i][aux[0]+1:aux[1]], "+", filhos[i][aux[1]], "+", filhos[i][aux[1]+1:tamanho_individuo])
            filhos[i] = filhos[i][0:aux[0]] + filhos[i][aux[0]] + filhos[i][aux[0]+1:aux[1]] + filhos[i][aux[1]] + filhos[i][aux[1]+1:tamanho_individuo]
    return filhos

def selecao_sobrevivencia(populacao, melhor_filho):
    scored = [(fitness(i), i) for i in populacao]
    #print("scored:", scored)
    # ordenamos pelo fitness do pior para o melhor
    scored2 = [i[0] for i in sorted(scored)]
    scored = [i[1] for i in sorted(scored)]
    populacao = scored
    #print(populacao)
    if (fitness(melhor_filho) > fitness(populacao[0])):
        populacao[0] = melhor_filho
        scored = [(fitness(i), i) for i in populacao]
        scored2 = [i[0] for i in sorted(scored)]
        scored = [i[1] for i in sorted(scored)]
        populacao = scored
    return populacao

#print(individuo())
#print(populacao())
#print(fitness('000001000001000001000001 '))
#print(selecao(populacao()))
#print(binToInt('000001000011010011110111'))
#print(intToBin([0, 1, 0, 3, 2, 3, 6, 7]))
#print("filhos:", recombinacao(['000001010011100101110111', '111110101100011010001000']))
#print(mutacao([[0,1,2,3,4,5,6,7], [7,6,5,4,3,2,1,0]]))

numero_convergencias = 0
numero_iteracoes = 0
lista_iteracoes = []
lista_qtd_convergencias = []
lista_fitness_medio = []
lista_todos_convergem = []

for k in range(30):
    qtd_convergencias = 0
    melhor_populacao = ([],0)
    pop = populacao()

    for i in range(10000):
        #selecao
        pais_selecionados = selecao(pop)
        #pais_selecionados = selecaoRoleta(pop)

        #print(pais_selecionados)
        #print("pais selecionados:", pais_selecionados)
        filhos_criados = recombinacaoOrdem1(pais_selecionados)

        qtd = len(set([item for item in filhos_criados[0] if filhos_criados[0].count(item) > 1]))
        qtd2 = len(set([item for item in filhos_criados[1] if filhos_criados[1].count(item) > 1]))

        if(-1 not in filhos_criados[0] and -1 not in filhos_criados[1] and qtd == 0 and qtd2 == 0):
            #print("-----------------------------------------------PASSOU------------------------------------------------------")
            #print("filhos criados:", filhos_criados)
            filhos_mutantes = mutacao(filhos_criados)
            #print('mutantes:', filhos_mutantes)
            filhos_mutantes[0] = intToBin(filhos_mutantes[0])
            filhos_mutantes[1] = intToBin(filhos_mutantes[1])
            #print('mutantes:', filhos_mutantes)
            scored = [(fitness(i), i) for i in filhos_mutantes]
            #print(scored)
            scored = [i[1] for i in sorted(scored, reverse=True)]
            listaFitness = [fitness(l) for l in pop]

            lista_fitness_medio.append(sum(listaFitness)/tamanho_populacao)
            #print(scored)
            melhor_filho = scored[0]
            #print(melhor_filho)
            f_melhor_filho = fitness(melhor_filho)
            #print(f_melhor_filho)
            pop = selecao_sobrevivencia(pop, melhor_filho)
            #print(pop)

        melhor_populacao = (pop[tamanho_populacao - 1], fitness(pop[tamanho_populacao - 1]))
        #print("MELHOR FITNESS:", melhor_populacao)
        pior_populacao = (pop[0], fitness(pop[0]))
        #print("PIOR FITNESS:", pior_populacao)
        #print("MELHOR FITNESS:", binToInt(melhor_populacao[0]))


        if (melhor_populacao[1] == 1):
            for j in pop:
                if (fitness(j) == 1):
                    qtd_convergencias += 1
            lista_qtd_convergencias.append(qtd_convergencias)
            numero_convergencias += 1
            #numero_iteracoes += i
            lista_iteracoes.append(i)
            print("MELHOR FITNESS:", melhor_populacao)
            print("PIOR FITNESS:", pior_populacao)
            break

        # todos convergirem
        #if (fitness(pop[0]) == 1):
        #    lista_todos_convergem.append(i)
        #    break


print("MEDIA EXECUCOES COM CONVERGENCIAS:", numero_convergencias/30)
print("MEDIA ITERACOES CONVERGIU:", statistics.median(lista_iteracoes))
print("DESVIO PADRAO ITERCOES CONVERGENCIA:", statistics.pstdev(lista_iteracoes))
print("LISTA DE QTD DE CONVERGENCIAS:", lista_qtd_convergencias)
print("LISTA DA MEDIA DOS FITNESS NAS EXEC:", lista_fitness_medio)
print("MEDIA DO FITNESS NAS EXECUCOES:", statistics.mean(lista_fitness_medio))

#print("MEDIA DE ITERACOES PARA TODOS CONVERGIREM:", statistics.mean(lista_todos_convergem))



