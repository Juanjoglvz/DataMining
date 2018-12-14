import pandas as pd

df = pd.read_csv('../../data/interim/vuelos.csv')

# Nos quedamos solo con los datos del verano
#df_m = df[(df['MONTH'] > 5) & (df['MONTH'] <= 8)]
df_m = df

#df_m.to_csv('../../data/interim/vuelos_verano.csv')

#df_m = pd.read_csv('../../data/interim/vuelos_verano.csv')

# Quitamos las filas canceladas y diverteds, porque no tienen delays
df_m = df_m[(df_m['CANCELLED'] != 1)]
df_m = df_m[(df_m['DIVERTED'] != 1)]

# Añadimos la columna de dia de verano para diferenciar entre el 1 de junio y julio
#df_m['SUMMER_DAY'] = ((df_m['MONTH'] - 6) * 31) + df_m['DAY_OF_MONTH']


# Quitamos las columnas que no nos interesan
cols = ['YEAR', 'MONTH', 'DAY_OF_MONTH', 'OP_CARRIER_FL_NUM', 'DEP_TIME', 'DEP_DELAY', 'TAXI_OUT', 'TAXI_IN', 'ARR_TIME', 'ARR_DELAY', 'CANCELLED', 'CANCELLATION_CODE', 'DIVERTED', 'ACTUAL_ELAPSED_TIME', 'AIR_TIME']
df_m_n = df_m.drop(cols, axis = 1)


# Cambiamos los nans por ceros
df_m_n = df_m_n.fillna(0)


#Creamos la nueva columna de delays
df_m_n['DELAY'] = df_m_n['CARRIER_DELAY'] + df_m_n['WEATHER_DELAY'] + df_m_n['NAS_DELAY'] + df_m_n['SECURITY_DELAY'] + df_m_n['LATE_AIRCRAFT_DELAY'] 

cols = ['CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']
df_m_n = df_m_n.drop(cols, axis = 1)

# Deteccion estadística de outliers. Quitamos los valores que esten más allá de 5 desviaciones estandar
# porque la distribución del delay es muy sesgada a la izquierda 
df_m_n = df_m_n.drop(df_m_n.index[(df_m_n['DELAY'] > (df_m_n['DELAY'].mean() + 5 * df_m_n['DELAY'].std()))])

dfiata = pd.read_csv('../../data/external/ID_TO_IATA.csv')

# Creamos un diccionario con las parejas ID - IATA
airports = {}
for index, row in dfiata.iterrows():
    airports[row['ORIGIN_AIRPORT_ID']] = row['ORIGIN']

# lo converitmos a dataframe y lo mapeamos para modificar nuestro dataframe (df_m_n)
dfiata_uni = pd.DataFrame.from_dict(airports, orient='index')

df_m_n['ORIGIN_AIRPORT_ID'] = df_m_n['ORIGIN_AIRPORT_ID'].map(dfiata_uni[0])
df_m_n['DEST_AIRPORT_ID'] = df_m_n['DEST_AIRPORT_ID'].map(dfiata_uni[0])

# Hay algunos aeropuertos que no tienen codigo IATA
# Como máximo 97 vuelos son los que no tienen código
# Así que los eliminamos
df_m_n = df_m_n.dropna()

# Añadimos columna booleana para clasificación
df_m_n['DELAYED'] = df_m_n.apply (lambda row: 0 if row['DELAY'] == 0 else 1 ,axis=1)

#df_m_n.to_csv('../../data/processed/vuelos_verano_c.csv')

# Nos quedamos solo con los vuelos retrasados para regresion

df_r = df_m_n[(df_m_n['DELAYED'] == 1)]

#df_r.to_csv('../../data/processed/vuelos_verano_r.csv')

# Creamos una columna nueva distribuyendo las horas
df_m_n["interval_dep"] = 0
df_m_n["interval_arr"] = 0

last_dep = 1.0
last_arr = 1.0
for i in [0.2, 0.4, 0.6, 0.8, 1]:
    q_dep = df_m_n.CRS_DEP_TIME.quantile(i)
    q_arr = df_m_n.CRS_ARR_TIME.quantile(i)
    interval_dep = pd.Interval(last_dep, q_dep)
    interval_arr = pd.Interval(last_arr, q_arr)
    df_m_n.loc[df_m_n["CRS_DEP_TIME"].between(last_dep, q_dep), "interval_dep"] = interval_dep
    df_m_n.loc[df_m_n["CRS_ARR_TIME"].between(last_arr, q_arr), "interval_arr"] = interval_arr
    last_dep = q_dep
    last_arr = q_arr

#df_m_n.to_csv('../../data/processed/vuelos_verano_intervalos_c.csv')
df_m_n.to_csv('../../data/processed/vuelos_intervalos.csv')

df_vuelos = pd.read_csv('../../data/processed/vuelos_intervalos.csv')
df_tail = pd.read_csv('../../data/external/TAIL_TO_TYPE.csv')

#tail_grouped = df_vuelos.groupby(by='TAIL_NUM',axis=1)
planes = {}
for index, row in df_tail.iterrows():
    planes[row['tailnum']] = row['model']
    
dfiata_uni = pd.DataFrame.from_dict(planes, orient='index')

df_vuelos['TAIL_NUM'] = df_vuelos['TAIL_NUM'].map(dfiata_uni[0])
df_droped = df_vuelos.dropna(axis = 0)


