import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint 

# TODO: классовая структура

# Представим, что мы переходим только между тремя веб страницами: web_1, web_2 и web_3. Вообще говороя 
# состояния необходимо делать с более сложно структурой: кроме веб страниц, состояния будут 
# отображать мат ожидание и дисперсиюс корости движения мыши, скорости печати и пр. на данной странице, но 
# в данной тестовой версии мы ипользуем в качестве состояний только название веб страницы.  
# Легко понять, что в модели цепей Маркова веб страницы является явными состоянием, 
# то есть таким состояния, о которых в любой момент времени можно точно сказать, 
# находится ли наблюдаемый объект в нем или нет. В противовес явным существуют скрытые,
# но о них будет скзаано позже. Также стоит заметить, что вообще говоря, такая модель цепи Маркова является 
# не полной из-а того, что в ней подрузамивается, что все параметры являются дискртными6 когда на самом деле
# правильнее было бы считать скорости нормально распределенными случайнми величиными6 но это уже следующий этап

states = ['web_1', 'web_2', 'web_3']

# Начальное распрпеделение вероятностей. Сложно интерпретировать начальное распределение в случае
# веб страниц, проще будет пояснить на более живом примере: человек спит с вероятностью 0.35, ест с 
# вероятнстью 0.35 и гуяет с вероятностью 0.3, сложно сказать в каком именно состоянии нахордится человек 
# в момент начала наблюдения, поэтому вводится начальное распределение вероятностей

pi = [0.35, 0.35, 0.3]

# Задаим теперь матрицу переходов между веб страницами - просто матрица вероятностей попасть с web_i на web_j
# понятное дело, что сумма вероятностей перейти из состояния web_i во все остальные состояния равняется единице

q_df = pd.DataFrame(columns=states, index=states)
q_df.loc[states[0]] = [0.4, 0.2, 0.4]
q_df.loc[states[1]] = [0.45, 0.45, 0.1]
q_df.loc[states[2]] = [0.45, 0.25, 0.3]

print(q_df)
print("\n\n")

# create a function that maps transition probability dataframe 
# to markov edges and weights

def _get_markov_edges(df):
	edges = {}
	for col in df.columns:
		for idx in df.index:
			edges[(idx,col)] = df.loc[idx,col]
	return edges

edges_wts = _get_markov_edges(q_df)
pprint(edges_wts)
print("\n\n")

# Теперь займемся скрытыми состояниями цепи. Скрытыми они называются потому, что мы никогда доподлино не знаем,
# в каком именно стостоянии нахоится пользователь, мы можем только рассуждать о наиболее вероятном состоянии соответсвующему
# пройденному пути

hidden_states = ['good', 'bad']

# Легко понять, что начальное распределение лучше выбрать равновероятным

pi = [0.5, 0.5]

# Матрица переходов между скрытыми состояниями

a_df = pd.DataFrame(columns=hidden_states, index=hidden_states)
a_df.loc[hidden_states[0]] = [0.7, 0.3]
a_df.loc[hidden_states[1]] = [0.4, 0.6]

print(a_df, "\n\n")

# Создадим теперь матрицу вероятностей наблюдейний, то есть матрицу в которой записаны вероятности
# Матрица имеет размер (M x Q), где M - число скрытых состояний, а Q - число наблюдений, то есть явных состояний. 
# Важно понимать, что это матрица условных вероятностей.

observable_states = states

b_df = pd.DataFrame(columns=observable_states, index=hidden_states)
b_df.loc[hidden_states[0]] = [0.2, 0.6, 0.2]
b_df.loc[hidden_states[1]] = [0.4, 0.1, 0.5]

print(b_df, "\n\n")

# Созданим из весго имеющегося ребра графа, чтобы было удобнее

hide_edges_wts = _get_markov_edges(a_df)
pprint(hide_edges_wts)
print("\n\n")

emit_edges_wts = _get_markov_edges(b_df)
pprint(emit_edges_wts)
print("\n\n")

# Последовательность наблюдений поведения пользователя закодируем числами

observ_map = {'web_1':0, 'web_2':1, 'web_3':2}
observ = np.array([1,1,2,1,0,1,2,1,0,2,2,0,1,0,1])

# Алгоритм Витерби — алгоритм поиска наиболее подходящего списка состояний (называемого путём Витерби), который в контексте цепей Маркова
# получает наиболее вероятную последовательность произошедших событий. Великолепно написано на https://en.wikipedia.org/wiki/Viterbi_algorithm
# 

def viterbi(pi, A, B, obs):
	
	# A - матрица переходов между сокрытыми состояниями, B - матрица условных вероятностей  
	# получить наблюдение (obs), находясь в сокрытом состоянии s, pi - распределение вероятностей

	# Количество состояний
	K = np.shape(B)[0]
	
	# Число намблюдений
	T = np.shape(obs)[0]
	
	# Инициализируем путь по состояниям нулями
	path = np.zeros(T)

	# T1[i, j] - вероятность наиболее вероятного пути, достигающего вершину i и 
	# генерирующего последовательность obs[: j]
	T1 = np.zeros((K, T))

	# T2[i, j] - хранит в себе элементы x_{j-1} такие, что x_{j} = s_{i} 
	# T2 существует для того, чтобы по T1 потом востановить последовательность
	# скрытых вершин
	T2 = np.zeros((K, T))
	
	# Начальная инициализация
	T1[:, 0] = pi * B[:, obs[0]]
	T2[:, 0] = 0
  
	# Для каждого наблюдения
	for i in range(1, T):
		# Для каждого состояния
		for j in range(K):
			T1[j, i] = np.max(T1[:, i - 1] * A[:, j]) * B[j, obs[i]] 
			T2[j, i] = np.argmax(T1[:, i - 1] * A[:, j] * B[j, obs[i]])
			print('j = {j} and i = {i}: T2[{j}, {i}] = {T2}'.format(j = j, i = i, T2 = T2[j, i]))
	
	# Ищем оптимальный путь
	print('-----------------------------------------------------------------------------------')
	path[T - 1] = np.argmax(T1[:, T - 1])
	for i in range(T - 2, -1, -1):
		path[i] = T2[int(path[i + 1]), i + 1]
		
	return path, T1, T2

# Теперь алгоритм foraward-backward. Допустим нам дана некоторая марковская модель \lambda с матрицей A
# и матрицей B, пусть там также дана последовательность наблюдейний obs = \{o_i\}_{i=1}^{T} и начальное распределение 
# pi. Нам необходимо найти величину P(obs|\lambda), то есть вероятность того насколько возможно получить данную
# последовательность наблюдений в условиях данной модели. Алгоритм backward-forward является частью алгоритма baum-welch,
# который изменяет модель \lambda так, чтобы веротность P(obs|\lambda) была максимальной, то есть 
# настраивает модель под данного пользователя

def forward(pi, A, B, obs):

		# Длина последовательности наблюдений, она, очевидно, равна длине последовательностей пройденных 
		# скрытых состояний 
		T = len(obs)

		# Число скрытых состояний
		N = A.shape[0]

		# Обозначим \aplha_t(i) = P(o_1, o_2, ... , o_t, s_t = i | \lambda) - вероятность на t-том шаге встретить 
		# последовательность o_1, o_2, ... , o_t и оказаться в состоянии i. Таким образом для любого i: \alpha_1(i) = P(o_1, s_1 = i | \lambda) = 
		# P(o_1 | s_1 = i, \lambda) * P(s_1 = i | \lambda) = \pi_i * B[i, o_1]
		alpha = np.zeros((T, N))
		alpha[0] = pi * B[ : , obs[0]]

		# Далее по индукции заполним \alpha_t(i) = P(o_1, o_2, ... , o_t, s_t = i | \lambda) = 
		# \sum_{j=1}^{N} P(o_1, o_2, ... , o_t, s_{t-1} = j, s_t = i | \lambda) = 
		# \sum_{j=1}^{N} P(o_t | s_{t-1} = j, s_t = i, o_1, o_2, ... , o_{t-1}, \lambda) *
		# P(s_t = i | s_{t-1} = j, o_1, o_2, ... , o_{t-1}, \lambda) * P(s_{t-1} = j, o_1, o_2, ... , o_{t-1}, \lambda) = 
		# P(o_t | s_t = i, \lambda) \sum_{j=1}^{N} P(s_t = i| o_1, o_2, ... , o_t, s_{t-1} = j, \lambda) P(o_1, o_2, ... , o_{t-1}, s_{t-1} = j, \lambda) = 
		# B[i, o_t] * \sum_{j=1}^N \alpha_{t-1}(i)A[i, j]
		# Доказательство второго равенства будет в pdf
		for t in range(1, T):
			alpha[t] = alpha[t - 1].dot(A) * B[ : , obs[t]]

		# P(obs|\lambda) = \sum_{i=1}^{N} P(o_1, ... , o_T, s_T = i | \lambda) = \sum_{i=1}^{N} \alpha_T(i)
		return alpha

def backward(pi, A, B, obs):

		# Длина последовательности наблюдений, она, очевидно, равна длине последовательностей пройденных 
		# скрытых состояний 
		T = len(obs)

		# Число скрытых состояний
		N = A.shape[0]

		# \beta_{t}(i) = P(o_{t+1}, o_{t+2}, ... , o_{T} | s_t = i, \lambda) - вероятность наблюдаемой части 
		# последовательных наблюдений o_{t+1}, o_{t+2}, ... , o_{T} при условии, что в момент времени t состояние было i
		# и при модели \lambda. \beta_{T}(i) = 1 \forall i
		beta = np.zeros((N, T))
		beta[ : , -1 : ] = 1

		# Далее по индукции заполним \beta_t(j) = P(o_{t+1}, o_{t+2}, ... , o_{T}| s_t = j, \lambda) = 
		# Объяснение следует закинуть в tex
		# \[
		# \sum_{i=1}^{N} P(o_{t+1}, ... , o_{T}, s_{t+1} = i| s_t = i, \lambda) = \]
		# \[ \sum_{i=1}^{N} \dfrac{P(o_{t+1}, ... , o_{T}, s_{t+1} = i, s_t = j, \lambda)}{P(s_t = j, \lambda)} =\]\[ \sum_{i=1}^{N} P(o_{t+1}|o_{t+2} ... , o_{T}, s_{t+1} = i, s_t = j, \lambda) \cdot P(o_{t+2} ... , o_{T}| s_{t+1} = i, s_t = j, \lambda)  \cdot \frac{P(s_{t+1} = i, s_t = j, \lambda))}{P(s_t = j, \lambda)} \]
		# Согласно свойству марковских цепей: $P(S_t | S_{t-1},O_{t-1},\ldots,S_1, O_1)=P(S_t| S_{t-1})$ и $P(O_t | Q_t,Q_{t-1},O_{t-1},\ldots,S_1,O_1)=P(O_t | S_t)$, тогда $P(o_{t+1}|o_{t+2} ... , o_{T}, s_{t+1} = i, s_t = j, \lambda) = P(o_{t+1} | s_{t+1} = i) = B_i(o_{t+1})$,  кроме того легко понять, что $P(o_{t+2} ... , o_{T}| s_{t+1} = i, s_t = j, \lambda) = \beta_{t+1}(i)$ и по формуле Байеса $\frac{P(s_{t+1} = i, s_t = j, \lambda))}{P(s_t = j, \lambda)} = P(s_{t+1} = i | s_{t} = j, \lambda) = a_{ij}$, тогда 
		# \[ \beta_t(j) =  \sum_{i=1}^{N} A[i, j]\beta_{t+1}(j)B[i, obs(t+1)]\]
		for t in reversed(range(T - 1)):
			for n in range(N):
				beta[n , t] = np.sum(beta[ : , t + 1] * A[n , : ] * B[ : , obs[t + 1]])

		return beta

def likelihood(pi, A, B, obs_seq):
		# P(obs | \lambda) = \sun_{i=1}^{N} P(o_1, ... , o_T, s_T = i | \lambda) = \sum_{i=1}^{N} \aplha_{T}(i)
		return  forward(pi, A, B, obs_seq)[-1].sum()    

def gamma_(pi, A, B, obs_seq):
	# Зная \alpha \beta можно посчитать величину \gamma_t(i) = \frac{P(s_t = i, obs | \lambda)}{P(obs | \lambda)} = 
	# \frac{P(o_1, ... o_t, s_t = i | \lambda)}{P(obs | \lambda)}. Легко доказать, что P(o_1, ... o_t, s_t = i | \lambda) = 
	# P(o_1, ... o_t | s_t = i, \lambda)P(o_{t+1}, ... o_T | s_t = i, \lambda)P(s_t = i | \lambda) = \alpha_t(i)\beta_t(i)
	# Таким образом \gamma_t(i) = \alpha_t(i) \beta_t(i) / P(obs | \lambda). Знаменатель вычислялся ранее
	# P(obs|\lambda) = \sum_{i=1}^{N} P(o_1, ... , o_T, s_t = i | \lambda) = \sum_{i=1}^{N} \alpha_T(i)


	alpha = forward(pi, A, B, obs_seq)
	beta  = backward(pi, A, B, obs_seq)
	obs_prob = likelihood(pi, A, B, obs_seq)
	return (np.multiply(alpha, beta.T) / obs_prob)  

def ksi_(alpha, beta, A, B, obs_seq):
	# ksi_t(i , j) = P(s-t = i, s_{t+1} = j | obs, \lambda) - вероятность находиться в состоянии i в момент времени t и в состоянии j в
	# момент времени t+1 при условии наблюдений obs и модели \lambda
	
	# Число скрытых состояний
	N = A.shape[0]

	# Длина последовательности наблюдений, она, очевидно, равна длине последовательностей пройденных 
	# скрытых состояний 
	T = len(obs_seq)

	ksi = np.zeros((T - 1, N, N))

	# P = \sum_{i=1}^{N}\sum_{j=1}^{N} \alpha_t(i)A_{ij}B_j(y_{t+1})\beta_{t+1}(i)
	P = 0
	for i in range(N):
		for j in range(N):
			for t in range(T - 1):
				ksi[t, i, j] = alpha[t, i] * A[i, j] * B[j, obs_seq[t + 1]] * beta[j, t + 1]
				P += ksi[t, i, j]
			ksi[:, i, j] = ksi[:, i, j] / P
	print("ksi ", ksi)
	return ksi


def baum_welch(pi, A, B, obs_seq, epohs):
	N = A.shape[0]
	T = len(obs_seq)
	K = np.shape(B)[0]
	for _ in range(epohs):
		alpha = forward(pi, A, B, obs_seq)
		beta  = backward(pi, A, B, obs_seq)
		gamma = gamma_(pi, A, B, obs_seq)
		ksi = ksi_(alpha, beta, A, B, obs_seq)
		pi[:] = gamma[:, 1]
		for i in range(N):
			for j in range(N):
				A[i, j] = sum(ksi[1: T - 2, i, j]) / sum(gamma[i, 1 : T - 2])
		for i in range(N):
			for k in range(K):
				tmp_sum = 0
				for t in range(T):
					if obs_seq[t] == k:
						tmp_sum += obs_seq[t]
				B[i, k] = tmp_sum / sum(gamma[i, :])
	return A, B, pi

a = a_df.values
b = b_df.values

path, T1, T2 = viterbi(pi, a, b, observ)
print('single best state path: \n', path)
print('T1:\n', T1)
print('T2:\n', T2)


hidden_states = ['state1', 'state2']

pi = [0.2, 0.8]

a_df = pd.DataFrame(columns=hidden_states, index=hidden_states)
a_df.loc[hidden_states[0]] = [0.5, 0.5]
a_df.loc[hidden_states[1]] = [0.3, 0.7]

print(a_df, "\n\n")

observable_states = ['eggs', 'no_eggs']

b_df = pd.DataFrame(columns=observable_states, index=hidden_states)
b_df.loc[hidden_states[0]] = [0.3, 0.7]
b_df.loc[hidden_states[1]] = [0.8, 0.2]

print(b_df, "\n\n")

observ_map = {'eggs':0, 'no_eggs':1}
observ = np.array([0,0,0,0,0,1,1,0,0,0])

a = a_df.values
b = b_df.values

A, B, pi = baum_welch(pi, a, b, observ, 1)
print("A:\n", A)
print("B:\n",B)
print("pi:\n",pi)

a = [[[1, 2], [4, 6], [7, 8]], [[10, 22], [42, 26], [17, 18]]]
print(a[1])



