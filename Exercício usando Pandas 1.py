#!/usr/bin/env python
# coding: utf-8

# # Exercício - Mini Projeto de Análise de Dados
# 
# 
# ### O que temos?
# 
# Temos os dados de 2019 de uma empresa de prestação de serviços. 
# 
# - CadastroFuncionarios
# - CadastroClientes
# - BaseServiçosPrestados
# 
# 
# ### O que queremos saber/fazer?
# 
# 1. Valor Total da Folha Salarial -> Qual foi o gasto total com salários de funcionários pela empresa? <br>
#     
#     
# 2. Qual foi o faturamento da empresa?<br>
#     
#     
# 3. Qual o % de funcionários que já fechou algum contrato?<br>
#     Dica: se você aplicar o método .unique() em uma variável que é apenas 1 coluna de um dataframe, ele vai excluir todos os valores duplicados daquela coluna.<br>
#     Ex: unicos_colunaA = dataframe['colunaA'].unique() te dá como resposta uma lista com todos os itens da colunaA aparecendo uma única vez. Todos os valores repetidos da colunaA são excluidos da variável unicos_colunaA 
#     
#     
# 4. Calcule o total de contratos que cada área da empresa já fechou
# 
# 
# 5. Calcule o total de funcionários por área
# 
# 
# 6. Qual o ticket médio mensal (faturamento médio mensal) dos contratos?<br>
#     Dica: .mean() calcula a média -> exemplo: media_colunaA = dataframe['colunaA'].mean()
# 
# Obs: Lembrando as opções mais usuais de encoding:<br>
# encoding='latin1', encoding='ISO-8859-1', encoding='utf-8' ou então encoding='cp1252'

# In[1]:


#Importação e folha salárial
import pandas as pd

#Criando DF com cadastro dos funcionários
cad_funcionarios_df = pd.read_csv('CadastroFuncionarios.csv', sep=';', decimal=',')
cad_funcionarios_df = cad_funcionarios_df.drop(['Estado Civil', 'Cargo'], axis=1)
display(cad_funcionarios_df)


# In[2]:


# Criando df com clientes
cad_clientes_df = pd.read_csv('CadastroClientes.csv', sep=';')
display(cad_clientes_df)


# In[3]:


# Criando DF com serviços prestados
base_serv_pres_df = pd.read_excel('BaseServiçosPrestados.xlsx')
display(base_serv_pres_df)


# ### Folha Salarial

# In[4]:


#Calculo de Folha salarial direto
folha_total = (cad_funcionarios_df['Salario Base'].sum()) + (cad_funcionarios_df['Impostos'].sum()) + (cad_funcionarios_df['Beneficios'].sum()) + (cad_funcionarios_df['VT'].sum()) + (cad_funcionarios_df['VR'].sum())
print('Total da folha de pagamento: R${:,.2f}'.format(folha_total))

#Criando coluna com salário total
cad_funcionarios_df['Salario Total'] = cad_funcionarios_df['Salario Base'] + cad_funcionarios_df['Impostos'] + cad_funcionarios_df['Beneficios'] + cad_funcionarios_df['VT'] + cad_funcionarios_df['VR']
print('Total da Folha de Pagamento: R${:,.2f}'.format(sum(cad_funcionarios_df['Salario Total'])))


# ### Faturamento da empresa

# In[15]:


#Qual foi o faturamento da empresa?

# Unir e selecionar as colunas do DF
faturamentos_df = base_serv_pres_df[['ID Cliente' , 'Tempo Total de Contrato (Meses)']].merge(cad_clientes_df[['ID Cliente' , 'Valor Contrato Mensal']], on = 'ID Cliente')

#Calcular o faturamento total criando nova coluna
faturamentos_df['Faturamento'] = faturamentos_df['Tempo Total de Contrato (Meses)'] * faturamentos_df['Valor Contrato Mensal']
display(faturamentos_df)
print(f"O faturamento total da empresa foi de: R${sum(faturamentos_df['Faturamento']):,.2f}")


# ### 3. Qual o % de funcionários que já fechou algum contrato?<br>
#     Sugestão: na base de serviços temos o funcionário que fechou cada serviço. Mas nem todos os funcionários que a empresa tem já fecharam algum serviço.<br>
#     . Na base de funcionários temos uma lista com todos os funcionários<br>
#     . Queremos calcular Qtde_Funcionarios_Fecharam_Serviço / Qtde_Funcionários_Totais<br>
#     . Para calcular a qtde de funcionários que fecharam algum serviço, use a base de serviços e conte quantos funcionários tem ali. Mas lembre-se, cada funcionário só pode ser contado uma única vez.<br><br>
#     Dica: se você aplicar o método .unique() em uma variável que é apenas 1 coluna de um dataframe, ele vai excluir todos os valores duplicados daquela coluna.<br>
#     Ex: unicos_colunaA = dataframe['colunaA'].unique() te dá como resposta uma lista com todos os itens da colunaA aparecendo uma única vez. Todos os valores repetidos da colunaA são excluidos da variável unicos_colunaA

# In[23]:


# Criando DF relacionando ID Funcionário e contratos realizados
contratos_df = base_serv_pres_df[['ID Funcionário', 'Codigo do Servico']].merge(cad_funcionarios_df[['ID Funcionário', 'Nome Completo']])

# Criando uma lista com cada funcionário unico que já fechou contrato
funcionario_unicos = contratos_df['ID Funcionário'].unique()
display(contratos_df)
print(funcionario_unicos)

# Printando resultado e calculando a porcentagem de funcionários que já fechou contrato
# OBS: o 'len' de cada lista pode ser armazenado em variavel para facilitar entendimento
print('--------------------------------------')
print(f"A porcentagem de funcionários que já fechou algum contrato é de {len(funcionario_unicos)/len(cad_funcionarios_df['ID Funcionário']):.2%}")


# ### 4 - Calcule o total de contratos que cada área da empresa já fechou

# In[29]:


# Criando DF relacionando area com numero de contratos
contrato_area_df = base_serv_pres_df[['ID Funcionário']].merge(cad_funcionarios_df[['ID Funcionário', 'Area']], on = 'ID Funcionário')

# Descobrindo quantidade de vezes que cada area aparece na coluna
contrato_area_qtde = contrato_area_df['Area'].value_counts()

display(contrato_area_df)
print(contrato_area_qtde)


# ### 5 Calcule o total de funcionários por área

# In[32]:


# Criando DF filtrando funcionário e area
funcionario_area = cad_funcionarios_df[['ID Funcionário', 'Area']]

# Criando variavel contando o numero de funcionarios em cada area
total_area = funcionario_area['Area'].value_counts()
display(funcionario_area)
print('-----------')
print(total_area)


# ### 6. Qual o ticket médio mensal (faturamento médio mensal) dos contratos?<br>
#     Dica: .mean() calcula a média -> exemplo: media_colunaA = dataframe['colunaA'].mean()

# In[35]:


media_mensal = cad_clientes_df['Valor Contrato Mensal'].mean()
print(f'O ticket médio mensal é de R${media_mensal:,.2f}')

