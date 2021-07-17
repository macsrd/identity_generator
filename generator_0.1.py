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

#generating dataframes with man identity

mezczyzni = dataframe
mezczyzni = mezczyzni.assign(Imie=random_m_i)
mezczyzni = mezczyzni.assign(Nazwisko=random_m_n)

#generating pesel numbers for men

for x in range(number_m):
    pesel = RandomPESEL()
    pesel = pesel.generate(gender='m')
    pesele_m.append(pesel)

mezczyzni['pesel'] = pesele_m


#ponizej nie dziala
numer = np.random.randint(0, 300, size = number_m)
df = pd.DataFrame(numer, columns = ['numery']) 
ulice['ulica'] = ulice['CECHA'] + ' ' + ulice['NAZWA_1'] + ' ' + df['numery'].astype(str)
u_m = ulice['ulica'].values.tolist()
print(random.sample(u_m, number_m))

print(kobiety)
print(mezczyzni)

