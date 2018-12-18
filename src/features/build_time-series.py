import pandas as pd

df = pd.read_csv('../../data/interim/vuelos.csv')

df = df.fillna(0)

#Creamos la nueva columna de delays
df['DELAY'] = df['CARRIER_DELAY'] + df['WEATHER_DELAY'] + df['NAS_DELAY'] + df['SECURITY_DELAY'] + df['LATE_AIRCRAFT_DELAY'] 

cols = ['CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']
df = df.drop(cols, axis = 1)

df = df.drop(['DAY_OF_WEEK', 'OP_UNIQUE_CARRIER',
       'OP_CARRIER_FL_NUM', 'ORIGIN_AIRPORT_ID', 'DEST_AIRPORT_ID',
       'CRS_DEP_TIME', 'DEP_TIME', 'DEP_DELAY', 'TAXI_OUT', 'TAXI_IN',
       'CRS_ARR_TIME', 'ARR_TIME', 'ARR_DELAY', 'CANCELLED',
       'CANCELLATION_CODE', 'DIVERTED', 'CRS_ELAPSED_TIME',
       'ACTUAL_ELAPSED_TIME', 'AIR_TIME', 'DISTANCE'], axis=1)

df_tail = pd.read_csv('../../data/external/TAIL_TO_TYPE.csv')

planes = {}
for index, row in df_tail.iterrows():
    planes[row['tailnum']] = row['model']
dfmodel = pd.DataFrame.from_dict(planes, orient='index')

df['MODEL'] = df['TAIL_NUM'].map(dfmodel[0])

df = df.dropna(axis = 0)

df = df.drop('TAIL_NUM', axis=1)