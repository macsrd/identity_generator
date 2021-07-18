import pandas as pd
import random
from random_pesel import RandomPESEL
import numpy as np

#script made by maciej.srodulski@gmail.com

dataframe = pd.DataFrame(columns = ['Imie', 'Nazwisko', 'pesel', 'adres', 'telefon', 'haslo', 'email', 'login', 'data_urodzenia'])

#opening pesel database files

imiona_kobiet = pd.read_csv(r'Wykaz_imion_żeńskich_osób_żyjących_wg_pola_imię_pierwsze_występujących_w_rejestrze_PESEL_bez_zgonów.csv', index_col=None, header=0, encoding='utf-8')
imiona_mezczyzn = pd.read_csv(r'Wykaz_imion_męskich_osób_żyjących_wg_pola_imię_pierwsze_występujących_w_rejestrze_PESEL_bez_zgonów.csv', index_col=None, header=0, encoding='utf-8')
nazwiska_kobiet = pd.read_csv(r'nazwiska_żeńskie-z_uwzględnieniem_osób_zmarłych.csv', index_col=None, header=0, encoding='utf-8')
nazwiska_mezczyzn = pd.read_csv(r'nazwiska_męskie-z_uwzględnieniem_osób_zmarłych.csv', index_col=None, header=0, encoding='utf-8')
ulice = pd.read_csv(r'ULIC_Urzedowy_2021-07-17.csv', index_col=None, header=0, encoding='utf-8', error_bad_lines=False, sep='delimiter', delimiter = ';')
miasta = pd.read_csv(r'SIMC_Urzedowy_2021-07-18.csv', index_col=None, header=0, encoding='utf-8', error_bad_lines=False, sep='delimiter', delimiter = ';')
#source https://eteryt.stat.gov.pl/eTeryt/rejestr_teryt/udostepnianie_danych/baza_teryt/uzytkownicy_indywidualni/pobieranie/pliki_pelne.aspx?contrast=default


#copying first names and last names into lists
i_k = (imiona_kobiet['IMIĘ_PIERWSZE'].values.tolist())
i_m = (imiona_mezczyzn['IMIĘ_PIERWSZE'].values.tolist())
n_k = (nazwiska_kobiet['Nawisko aktualne'].values.tolist())
n_m = (nazwiska_mezczyzn['Nawisko aktualne'].values.tolist())

#generating random women first/last names lists

number_k = 5

random_k_i = random.sample(i_k, number_k)
random_k_n = random.sample(n_k, number_k)


#generating random man first/last names lists

number_m = 5

random_m_i = random.sample(i_m, number_m)
random_m_n = random.sample(n_m, number_m)


#generating dataframes with women identity

kobiety = dataframe
kobiety = kobiety.assign(Imie=random_k_i)
kobiety = kobiety.assign(Nazwisko=random_k_n)

pesele_k=[]
pesele_m=[]

#generating pesel numbers for women

for x in range(number_k):
    pesel = RandomPESEL()
    pesel = pesel.generate(gender='f')
    pesele_k.append(pesel)

kobiety['pesel'] = pesele_k

#generating adress for women
numer_k = np.random.randint(0, 300, size = number_k*100)
df = pd.DataFrame(numer_k, columns = ['numery'])

m_k = miasta['NAZWA'].values.tolist()
m_k = random.sample(m_k, number_k)
m_k = [x for x in m_k if pd.isnull(x) == False]
df_2 = pd.DataFrame(m_k, columns = ['miasto'])

ulice['ulica'] = ulice['CECHA'] + ' ' + ulice['NAZWA_1'] + ' ' + df['numery'].astype(str) + ', ' + df_2['miasto']
u_k = ulice['ulica'].values.tolist()
u_k = [x for x in u_k if pd.isnull(x) == False]
random_u_k = random.sample(u_k, number_k)

kobiety = kobiety.assign(adres=random_u_k)

#generating dataframes with man identity

mezczyzni = dataframe
mezczyzni = mezczyzni.assign(Imie=random_m_i)
mezczyzni = mezczyzni.assign(Nazwisko=random_m_n)

#generating pesel numbers for men

for x in range(number_m):
    pesel = RandomPESEL()
    pesel = pesel.generate(gender='m')
    pesele_m.append(pesel)

#adding pesel to dataframe
mezczyzni['pesel'] = pesele_m


#generating adress for men
numer_m = np.random.randint(0, 300, size = number_m*100)
df = pd.DataFrame(numer_m, columns = ['numery'])

m_m = miasta['NAZWA'].values.tolist()
m_m = random.sample(m_m, number_m)
m_m = [x for x in m_m if pd.isnull(x) == False]
df_2 = pd.DataFrame(m_m, columns = ['miasto'])

ulice['ulica'] = ulice['CECHA'] + ' ' + ulice['NAZWA_1'] + ' ' + df['numery'].astype(str) + ', ' + df_2['miasto']
u_m = ulice['ulica'].values.tolist()
u_m = [x for x in u_m if pd.isnull(x) == False]
random_u_m = random.sample(u_m, number_m)

#adding address to dataframe
mezczyzni = mezczyzni.assign(adres=random_u_m)

print(kobiety['adres'])
print(mezczyzni['adres'])

