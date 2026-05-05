# -*- coding: utf-8 -*-
"""MDF_exercicio_opcao3

# Exercício: Opção 2
Utilizando o Método das Diferenças Finitas, vamos resolver a seguinte equação diferencial:
$$
\begin{cases}
  \frac{\partial^2 u}{\partial x^2} + u + x = 0 \\
  u(0) = 0 \\
  u'(1) = 1
\end{cases}
$$

Para isso, vamos usar um $\Delta x = 0.25$. Note que agora a condição de contorno em $x = 1$ é uma derivada, isto é, não é conhecida. Isso exige que um novo ponto deva ser computado no sistema.

A fórmula de Diferença Finita para essa equação é dada por:

\begin{align}
u_{i+1} + [(\Delta x)^2 -2]u_i + u_{i-1} = -(\Delta x)^2 x_i
\end{align}
"""

#importação das bibliotecas

import numpy as np
import matplotlib.pyplot as plt

#Parâmetros do Problema

L = 1         #domínio
n = 4         #número de intervalos
dx = L/n      #tamanho do passo
print(dx)

#Condições de Contorno
u_0 = 0               #condição de contorno em x = 0

"""Opção 3: aproximar a condição de contorno natural com diferença progressiva.

\begin{equation}
    \frac{du}{dx}\Big|_{x=x_i} = \frac{u_5 - u_4}{0.25} = 1
\end{equation}
"""

#Construindo as matrizes

n_incog = n                         #agora temos apenas uma das condições de contorno
A = np.zeros((n_incog, n_incog))
b = np.zeros(n_incog)

"""Para esse caso, devemos também escrever a equação para o ponto $i=4$, dada por:

\begin{equation}
    u_5 - 1.9375u_4 + u_3 = -0.0625
\end{equation}

Como estamos aproximando por diferença progressiva, geramos um ponto $u_5$ fora do domínio. Por isso, temos que construir uma equação para ele também, dada por:

\begin{equation}
    u_5 = 0.25 + u_4
\end{equation}

É por isso que vamos construir

\begin{equation}
    (0.25 + u_4) - 1.9375u_4 + u_3 = -0.0625
\end{equation}
"""

#Já que transformamos nossa equação de diferença finitas na equação Ax = b, vamos montar a matriz A e o vetor b

for i in range(n_incog):
  xi = (i + 1)*dx          #valor de xi no índice i

  A[i,i] = (dx**2) - 2     #preenchendo a diagonal principal

  if i > 0:                #preenchendo a primeira diagonal à esquerda
    A[i, i-1] = 1

  if i < (n-1):            #preenchendo a primeira diagonal à direita
    A[i, i+1] = 1

  b[i] = -(dx**2)*xi       #vetor b

  #ajuste nas Condições de Contorno
  b[0] = b[0] - u_0

#
A[-1,-1] = (dx**2)  -  1   #coeficiente de u4
A[-1,-2] = 1               #coeficiente de u3
b[-1] = b[-1] - 0.25       #ajuste da condição de contorno na última equação

print("Matriz A =", A)
print("Vetor b =", b)

#Solução do sistema de equações

sol = np.linalg.solve(A, b)     #a função linalg.solve resolve o sistema de equações
print("Solução =", sol)

#Solução Analítica

def u(x):
  return 2*np.sin(x)/np.cos(1) - x

sol_analitica = []

for i in range (n_incog):
  xi = (i + 1)*dx
  valor = u(xi)
  sol_analitica.append(valor)
  print(f"u({xi}) =", valor)

#Diferença entre a solução analítica e a solução numérica

erro = sol_analitica - sol
erro
