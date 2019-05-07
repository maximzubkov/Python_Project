# В этом файле находится много комментариев, которые Илья должен переправить в тех
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint 



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
		beta[ : , T - 1] = 1

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

	T = len(obs_seq)
	alpha = forward(pi, A, B, obs_seq)
	beta  = backward(pi, A, B, obs_seq)
	gamma = np.multiply(alpha, beta.T)
	for t in range(T):
		gamma[t] = gamma[t]/np.sum(alpha[t, :] * beta[:, t])
	return gamma 

def ksi_(alpha, beta, A, B, obs_seq):
	# ksi_t(i , j) = P(s-t = i, s_{t+1} = j | obs, \lambda) - вероятность находиться в состоянии i в момент времени t и в состоянии j в
	# момент времени t+1 при условии наблюдений obs и модели \lambda
	
	# Число скрытых состояний
	N = A.shape[0]

	# Длина последовательности наблюдений, она, очевидно, равна длине последовательностей пройденных 
	# скрытых состояний 
	T = len(obs_seq)

	ksi = np.zeros((T, N, N))

	# P = \sum_{i=1}^{N}\sum_{j=1}^{N} \alpha_t(i)A_{ij}B_j(y_{t+1})\beta_{t+1}(i)
	for t in range(T - 1):
		P = 0
		for i in range(N):
			for j in range(N):
				ksi[t, i, j] = alpha[t, i] * A[i, j] * B[j, obs_seq[t + 1]] * beta[j, t + 1]
				P += ksi[t, i, j]
		ksi[t, :, :] /= P
		
	for i in range(N):
			for j in range(N):
				ksi[T - 1, i, j] = alpha[T - 1, i] * A[i, j]
	ksi[T - 1, :, :] /= np.sum(ksi[T - 1,: ,: ])

	return ksi


def baum_welch(pi, A, B, obs_seq, epohs):

	N = A.shape[0]
	T = len(obs_seq)
	K = np.shape(B)[0]
	A_old = A.copy()
	B_old = B.copy()
	for _ in range(epohs):
		alpha = forward(pi, A, B, obs_seq)
		beta  = backward(pi, A, B, obs_seq)
		gamma = gamma_(pi, A, B, obs_seq)
		ksi = ksi_(alpha, beta, A, B, obs_seq)
		print(ksi)
		for i in range(N):
			pi[i] = np.sum(ksi[0, i, :])
			for j in range(N):
				A[i, j] = np.sum(ksi[: T - 1, i, j]) / np.sum(gamma[: T - 1, i])

			for k in range(max(obs)):
				print(K)
				found = (obs_seq == k).nonzero()
				print(found)
				B[i, k] = np.sum(ksi[found, i, :])/np.sum(ksi[:,i,:])
		error = (np.abs(A - A_old)).max() + (np.abs(B - B_old)).max() 
	return A, B, pi

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


# Матрица переходов между веб страницами -  матрица вероятностей попасть с web_i на web_j
# понятное дело, что сумма вероятностей перейти из состояния web_i во все остальные состояния равняется единице

# Теперь займемся скрытыми состояниями цепи. Скрытыми они называются потому, что мы никогда доподлино не знаем,
# в каком именно стостоянии нахоится пользователь, мы можем только рассуждать о наиболее вероятном состоянии соответсвующему
# пройденному пути

hidden_states = ['good', 'bad']

# # Легко понять, что начальное распределение лучше выбрать равновероятным

pi = [0.5, 0.5]

# # Изначально матрица переходов между скрытыми состояниями также лучше выбрать такой

a_df = pd.DataFrame(columns=hidden_states, index=hidden_states)
a_df.loc[hidden_states[0]] = [0.5, 0.5]
a_df.loc[hidden_states[1]] = [0.5, 0.5]

print(a_df, "\n\n")

# # Создадим теперь матрицу вероятностей наблюдейний, то есть матрицу в которой записаны условные вероятности
# # получить наблюдение o_k^ находиться в состоянии i
# # Матрица имеет размер (M x Q), где M - число скрытых состояний, а Q - число наблюдений. 

observable_states = ['o1', 'o2', 'o3']

b_df = pd.DataFrame(columns=observable_states, index=hidden_states)
b_df.loc[hidden_states[0]] = [0.5, 0.4, 0.1]
b_df.loc[hidden_states[1]] = [0.1, 0.3, 0.6]

print(b_df, "\n\n")

# # Последовательность наблюдений поведения пользователя закодируем числами

observ_map = {'o1':0, 'o2':1, 'o3':2}
observ = np.array([1,1,2,1,0,1,2,1,0,2,2,0,1,0,1])


a = a_df.values
b = b_df.values

print(a, b, type(a), type(b))

# HMM = hmm(hidden_states, pi, a, b)
# HMM.viterbi(observ)

# HMM = hmm(hidden_states, pi, a, b)
# HMM.learn(observ)
# print("A:\n", HMM.A)
# print("B:\n",HMM.B)
# print("pi:\n",HMM.pi)






