from pandas import *
from matplotlib.pyplot import *

# CONDURACHE => 10 LITERE => 10%3=1;  SERGIU => 6 LITERE => 6/3=2;

df = read_csv('data.csv') #sau df = DataFrame(read_csv('data.csv'))
print(df.to_string())  #cu to_string afisez tot
print('\n')
bargraph1 = df.plot.bar()

print(df.head(10)) #cu head(n) afisez doar primele n radnuri
print('\n')
bargraph2 = df.head(10).plot.line()


df1 = df[["Durata", "Puls"]] #am creat un now DataFrame doar cu coloanele Durata si Puls din DataFrameul initial
print(df1.tail(6)) #am luat primele 6 de la coada
print('\n')
bargraph3 = df1.tail(6).plot.bar()

show()

