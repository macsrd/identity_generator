import pandas as pd
import random
from random_pesel import RandomPESEL
import numpy as np
import string
import time

#script made by maciej.srodulski@gmail.com

dataframe = pd.DataFrame(columns = ['Imie', 'Nazwisko', 'pesel', 'adres', 'telefon', 'haslo', 'email', 'login', 'data_urodzenia'])

#opening pesel database files

imiona_kobiet = pd.read_csv(r'Wykaz_imion_żeńskich_osób_żyjących_wg_pola_imię_pierwsze_występujących_w_rejestrze_PESEL_bez_zgonów.csv', index_col=None, header=0, encoding='utf-8')
imiona_mezczyzn = pd.read_csv(r'Wykaz_imion_męskich_osób_żyjących_wg_pola_imię_pierwsze_występujących_w_rejestrze_PESEL_bez_zgonów.csv', index_col=None, header=0, encoding='utf-8')
nazwiska_kobiet = pd.read_csv(r'nazwiska_żeńskie-z_uwzględnieniem_osób_zmarłych.csv', index_col=None, header=0, encoding='utf-8')
nazwiska_mezczyzn = pd.read_csv(r'nazwiska_męskie-z_uwzględnieniem_osób_zmarłych.csv', index_col=None, header=0, encoding='utf-8')
ulice = pd.read_csv(r'ULIC_Urzedowy_2021-07-17.csv', index_col=None, header=0, encoding='utf-8', error_bad_lines=False, delimiter = ';')
miasta = pd.read_csv(r'SIMC_Urzedowy_2021-07-18.csv', index_col=None, header=0, encoding='utf-8', error_bad_lines=False, delimiter = ';')
#source https://eteryt.stat.gov.pl/eTeryt/rejestr_teryt/udostepnianie_danych/baza_teryt/uzytkownicy_indywidualni/pobieranie/pliki_pelne.aspx?contrast=default

#copying first names and last names into lists
i_k = (imiona_kobiet['IMIĘ_PIERWSZE'].values.tolist())
i_m = (imiona_mezczyzn['IMIĘ_PIERWSZE'].values.tolist())
n_k = (nazwiska_kobiet['Nawisko aktualne'].values.tolist())
n_m = (nazwiska_mezczyzn['Nawisko aktualne'].values.tolist())

#generating random first/last names lists

number_k = 50 #number of woman identities
random_k_i = random.sample(i_k, number_k)
random_k_n = random.sample(n_k, number_k)

number_m = 50 #number of man identities
random_m_i = random.sample(i_m, number_m)
random_m_n = random.sample(n_m, number_m)

#generating dataframes with random women identity

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

print(kobiety)

#generating dataframes with random man identity

mezczyzni = dataframe
mezczyzni = mezczyzni.assign(Imie=random_m_i)
mezczyzni = mezczyzni.assign(Nazwisko=random_m_n)

#generating pesel numbers for men

for x in range(number_m):
    pesel = RandomPESEL()
    pesel = pesel.generate(gender='m')
    pesele_m.append(pesel)

#adding pesel to men dataframe
mezczyzni['pesel'] = pesele_m

#concatenate tables
tabele = (kobiety, mezczyzni)
tozsamosci = pd.concat(tabele)

number_km = number_k + number_m


#generating identity adress
numer_k = np.random.randint(0, 300, size = (number_km)*100)
df = pd.DataFrame(numer_k, columns = ['numery'])

m_k = miasta['NAZWA'].values.tolist()
m_k = random.sample(m_k, number_km)
m_k = [x for x in m_k if pd.isnull(x) == False]
df_2 = pd.DataFrame(m_k, columns = ['miasto'])

ulice['ulica'] = ulice['CECHA'] + ' ' + ulice['NAZWA_1'] + ' ' + df['numery'].astype(str) + ', ' + df_2['miasto']
u_k = ulice['ulica'].values.tolist()
u_k = [x for x in u_k if pd.isnull(x) == False]
random_u_k = random.sample(u_k, number_km)

tozsamosci = tozsamosci.assign(adres=random_u_k)

#generating phone numbers

list_phones = []

def gen_phone():
    first = str(random.randint(600,800))
    second = str(random.randint(1,888)).zfill(3)

    last = (str(random.randint(1,999)).zfill(3))
    while last in ['1111','2222','3333','4444','5555','6666','7777','8888']:
        last = (str(random.randint(1,999)).zfill(3))

    return '{}-{}-{}'.format(first,second, last)
for _ in range(number_km):
    list_phones.append(gen_phone())

tozsamosci = tozsamosci.assign(telefon=list_phones)

#generating passwords

passwords = []

#for x in range(number_km):
#    password = ''.join(random.choice(string.printable) for i in range(8))
#    passwords.append(password)
    
for x in range(number_km):
    passw = string.ascii_letters
    password = ''.join(random.choice(passw) for i in range(8))
    passwords.append(password)

tozsamosci = tozsamosci.assign(haslo=passwords)

#generating email adress basing on first and last name

emails = ['@gmail.com', '@outlook.com', '@poczta.onet.pl']
 
tozsamosci['email'] = tozsamosci['Imie'] + '.' + tozsamosci['Nazwisko'] + random.sample(emails, 1)
tozsamosci['email'] = (tozsamosci['email'].str.lower()).str.replace(' ', '')

tozsamosci['login'] = tozsamosci['Imie'] + tozsamosci['Nazwisko']
tozsamosci['login'] = (tozsamosci['login'].str.lower()).str.replace(' ', '')

ExcelWriter = pd.ExcelWriter
timestr = time.strftime("%Y%m%d-%H%M%S")
file = ('klienci_upload_' + timestr +'.xlsx')

with ExcelWriter(file) as writer:
    tozsamosci.to_excel(writer, index=None, sheet_name='klienci')



