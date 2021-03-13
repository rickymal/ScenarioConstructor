# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 20:40:52 2021

@author: Henrique Mauler
"""
import pdb
import pandas as pd

from itertools import permutations
from itertools import combinations
from itertools import product
from collections import defaultdict
import numpy as np
from collections.abc import Iterable


"""
O pequeno trecho de código abaixo é uma implantanção para a criação de cenários utilizando apenas funções
Desenvolvi este pequeno código baseado em vários problemas que passei na universidade federal do Pará 
como desenvolvedor Python para Machine Learning..

Durante meu período na instituição, tive vários problemas para implementar um sistema em que eu pudesse avaliar
diferentes cenários com base nos resultados obtidos. Por exemplo: imagine que você deseje testar diferentes resultados
de uma função baseando-se em diferentes parâmetros. Não é algo complicado para quem já possui experiência, mas para 
mim que estava no começo foi responsável por uma necessidade de refatoração de quase quatro meses do meu projeto.

Este código busca trazer uma solução ergonômia para a criação destes cenários. apenas utilizando o objeto "Scenario"
e seu decorador "appender". Creio que com um exemplo fique bem mais simples:
    
supondo que tenhamos uma função que some dois números, mas queremos testar diferentes valores destes dois números
a = [10,20,30,],
b = [20,30,40,],

a função de soma receberá dois parâmetros 'a' e 'b', respectivamente, para o funcionamento a função deve ser
decorada com o método appender. os parâmetros deves ser encapsulados pelo método "set_parameters" ou por
alguma variáveis iterador como uma lista, contanto que seja setado para esta lista ser reconhecida como uma variável
para controle de cenário.

o valor resultante sempre é por definição uma tabela DataFrame contendo todas as combinações com os diferentes cenários

a função pode atualmente retornar um valor escalar (ou qualquer outro tipo) e um dicionário caso se tenha várias respostas



"""


"""
Atividades futuras:
    - Criar um objeto para outras pessoas implementarem funções para inserção e extração de parâmetros e forma personalizada (para a entrada)
    - Criar um objeto para outras pessoas implementarem funções para inserção e extração de parâmetros e forma personalizada (para a saida)
    - Aplicar concorrência para o aumento no desempenho ou o método np.apply_ufunc
    - ou seja, aumentar velocidade, concorrência e acoplamento na função

"""


class ScenarioParameterBuilder:
    def __init__(self,data,name,):
        self.data = data
        self.name = name

class Scenario:
    _scenarios = []
    
    def __init__(self,config):
        self.scenario_parameter = list()
        self.results = list()
        self.register_parameter = list()
        self.total_length = 0
        
        
        self.parameter_dtype = config['parameter_dtype']
        
    def list_extract(self,scenarios : ScenarioParameterBuilder):
        pair_content = list()  
        for s in scenarios:
            pair_content.append(s.data)
  
        return pair_content
    
    
    def get_value_parameter(self,array):
        key,value = array        
        if isinstance(value,ScenarioParameterBuilder):            
            return value.data
        elif isinstance(value,self.parameter_dtype):            
            return value
        elif not isinstance(value,Iterable):
            return [value]
        
        return np.nan
    
    
    def appender(self,function):

        def inner(*args, **kwargs):
            names_parameters = list()
            values_parameters = list()
            names_parameters = list(kwargs.keys())
            for key,value in kwargs.items():
                if isinstance(value,ScenarioParameterBuilder):
                    values_parameters.append(value.data)
                elif isinstance(value,self.parameter_dtype):
                    values_parameters.append(value)
                elif not isinstance(value,Iterable):
                    values_parameters.append([value])
                    
                    
            #values_parameters = np.apply_along_axis(func1d = self.get_value_parameter,
            #axis = 1,arr = tuple(kwargs.items()))
  
            responses = list()
            lister_parameters = [dict() for _ in range(len(tuple(product(*values_parameters))))]
            
            indexers_parameters_constructor = [tuple(range(len(x))) for x in values_parameters]
            
            matrix_index_for_dataframe = tuple(product(*indexers_parameters_constructor))
            matrix_index_for_dataframe = np.array(matrix_index_for_dataframe)
            
            
            indexers_parameters = [dict() for _ in range(len(tuple(product(*values_parameters))))]
        
            for extern_index,productors in enumerate(product(*values_parameters)):
                for ind,k in enumerate(names_parameters):
                    lister_parameters[extern_index][k] = productors[ind]     
            
            
            for parameters_input in lister_parameters:
                r = function(**parameters_input)
                responses.append(r)
                
            table_indexers_index = pd.DataFrame(matrix_index_for_dataframe, columns = names_parameters)
            table_indexers_value = table_indexers_index.apply(self.extract_value,axis = 'index', parameter = kwargs)
    

            if isinstance(responses[0],dict):
                table_responses = pd.DataFrame(data = responses)
            else:
                table_responses = pd.Series(data = responses)
                
            table_response = pd.concat([table_indexers_index,
                       table_indexers_value,
                       table_responses,],axis = 1,keys= ['parameters index','parameter value','responses'])
            return table_response
        return inner
    
    
    def extract_value(self,serie,parameter = None):
        key = serie.name
        if isinstance(parameter[key],ScenarioParameterBuilder):
            data = parameter[key].data
        elif isinstance(parameter[key],self.parameter_dtype):
            data = parameter[key]
        elif not isinstance(parameter[key],Iterable):
            data = [parameter[key]]
 
        return serie.apply(lambda x : data[x])
  
        
    def set_parameters(self,data,name = None):
        content = self.scenario_parameter
        parameter_metadata = ScenarioParameterBuilder(data = data,name = name)

        if self.total_length < len(parameter_metadata.data):
            self.total_length = len(parameter_metadata.data)
        self.register_parameter.append(parameter_metadata)
        
        return parameter_metadata


scenario = Scenario(config = {
    'parameter_dtype' : list,
    'return_dtype' : dict,
    })


if __name__ == '__main__':
        
    @scenario.appender
    def create_summarizations(a,b,c):
        return {
            'soma' : a + b + c,
            'subtração' : a - b - c,
            'multiplicação' : a * b * c,
            'divisão' : (a / b) / c
            
            }
    
    
    resultado = create_summarizations(
        a = scenario.set_parameters(data = [10,20,30],),
        b = scenario.set_parameters(data = [20,30,40],),
        c = 10,
        )
    
    resultado = create_summarizations(
        a = [10,20,30],
        b = [20,30,40],
        c = 10,
        )

    print(resultado)