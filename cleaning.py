#!/usr/bin/env python

import pandas as pd
import numpy as np

### Data loading and cleaning ###
precipitaciones = pd.read_csv('./data/precipitaciones.csv')
precipitaciones['date'] = pd.to_datetime(precipitaciones['date'], format = '%Y-%m-%d')
precipitaciones = precipitaciones.sort_values(by = 'date', ascending = True).reset_index(drop = True)

banco_central = pd.read_csv('./data/banco_central.csv')
banco_central['Periodo'] = banco_central['Periodo'].apply(lambda x: x[0:10])
banco_central['Periodo'] = pd.to_datetime(banco_central['Periodo'], format = '%Y-%m-%d', errors = 'coerce')
banco_central.drop_duplicates(subset = 'Periodo', inplace = True)
banco_central = banco_central[banco_central.Periodo.notna()]

# Extracting PIB columns from bc data
cols_pib = [x for x in list(banco_central.columns) if ('PIB' in x) or ('Periodo' in x)]
banco_central_pib = banco_central[cols_pib].dropna(how = 'any', axis = 0)
for col in cols_pib[1:]:
    banco_central_pib[col] = banco_central_pib[col].apply(lambda x: int(x.replace('.', '')))

banco_central_pib = banco_central_pib.sort_values(by = 'Periodo', ascending = True).reset_index(drop = True)

# Extracting Imacec columns from bc data
def to_100(x): 
    x = x.split('.')
    if x[0].startswith('1'): #es 100+
        if len(x[0]) > 2:
            return float(x[0] + '.' + x[1])
        else:
            x = x[0] + x[1]
            return float(x[0:3] + '.' + x[3:])
    else:
        if len(x[0]) > 2:
            return float(x[0][0:2] + '.' + x[0][-1])
        else:
            x = x[0] + x[1]
            return float(x[0:2] + '.' + x[2:])

cols_imacec = [x for x in list(banco_central.columns) if ('Imacec' in x) or ('Periodo' in x)]
banco_central_imacec = banco_central[cols_imacec].dropna(how = 'any', axis = 0)
for col in cols_imacec[1:]:
    banco_central_imacec[col] = banco_central_imacec[col].apply(lambda x: to_100(x))
    assert(banco_central_imacec[col].max()>100)
    assert(banco_central_imacec[col].min()>30)

banco_central_imacec = banco_central_imacec.sort_values(by = 'Periodo', ascending = True).reset_index(drop = True)

# Extracting IVCM from bc data
banco_central_ivcm = banco_central[['Periodo', 'Indice_de_ventas_comercio_real_no_durables_IVCM']]
banco_central_ivcm = banco_central_ivcm.dropna(how = 'any', axis = 0)
banco_central_ivcm['num'] = banco_central_ivcm.Indice_de_ventas_comercio_real_no_durables_IVCM.apply(lambda x: to_100(x))
banco_central_ivcm.drop(['Indice_de_ventas_comercio_real_no_durables_IVCM'], axis = 1, inplace = True)
banco_central_ivcm = banco_central_ivcm.sort_values(by = 'Periodo', ascending = True).reset_index(drop = True)

# Mergin all
banco_central_num = pd.merge(banco_central_pib, banco_central_imacec, on = 'Periodo', how = 'inner')
banco_central_num = pd.merge(banco_central_num, banco_central_ivcm, on = 'Periodo', how = 'inner')

## Suply data and feature engineering
precio_leche = pd.read_csv('./data/precio_leche.csv')
precio_leche.rename(columns = {'Anio': 'ano', 'Mes': 'mes_pal'}, inplace = True)

# [FIXME] Workaround because I'd problems installing ES locales
dic = {'Ene': 'Jan', 'Abr': 'Apr', 'Ago': 'Aug', 'Dic': 'Dec'}
precio_leche = precio_leche.replace({'mes_pal': dic})
precio_leche['mes'] = pd.to_datetime(precio_leche['mes_pal'], format = '%b').apply(lambda x: x.month)

precipitaciones['mes'] = precipitaciones['date'].apply(lambda x: x.month)
precipitaciones['ano'] = precipitaciones['date'].apply(lambda x: x.year)

banco_central_num['mes'] = banco_central_num['Periodo'].apply(lambda x: x.month)
banco_central_num['ano'] = banco_central_num['Periodo'].apply(lambda x: x.year)

precio_leche_pp = pd.merge(precio_leche, precipitaciones, on = ['mes', 'ano'], how = 'inner')
precio_leche_pp_pib = pd.merge(precio_leche_pp, banco_central_num, on = ['mes', 'ano'], how = 'inner')
precio_leche_pp_pib['mes_ano'] = precio_leche_pp_pib.apply(lambda x: f'{x.mes}-{x.ano}', axis =1)
precio_leche_pp_pib.drop(['ano', 'mes', 'date', 'Periodo', 'mes_pal'], axis = 1, inplace = True)
# Kept mes_ano case we need to create features based on the period

# Saving the final dataset
precio_leche_pp_pib.to_csv('./data/precio_leche_pp_pib.csv', index=False)
