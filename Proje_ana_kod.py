# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 15:38:07 2020

@author: kosea

"""

"""Kullanılan kütüphanelerin import edilmesi"""

import pandas as pd
from string import punctuation
from snowballstemmer import stemmer
from collections import Counter

"""Veri Setinin import edilmesi"""
#  Kaydedilen verinin okunması ve kullanılacak niteliklerin seçilmesi

data_filtreli = pd.read_csv("dirty_data.csv")
pre_data = data_filtreli[["date", "username", "tweet", "replies_count", "retweets_count", "likes_count"]]

# seçilen özniteliklerin yedeğinin alınması

pre_data.to_csv("pre_data.csv")


"""Verinin Filtrelenmesi"""
# Veri üzerinde tekrardan tarihe göre filtrelenmesi

mask = pre_data['date'] == "2020-12-28"
mask_2 = pre_data['date'] == "2020-12-29"
data_28tarihli = pre_data[mask]
data_29tarihli = pre_data[mask_2]
data_digertarihli = pre_data[~mask]

# Filtre uygulanan verilerin düzenlenmesi
data_digertarihli = data_digertarihli[~mask_2]
data_2829_tarihli = pd.concat([data_28tarihli, data_29tarihli])


 
# Metin olarak işlem yapılacak niteliğin veri seti üzerinden seçilmesi
tweetler_2829 = data_2829_tarihli[["tweet"]]
tweetler2829_degerler = tweetler_2829.iloc[:, 0].values

"""Verinin Temizlenmesi"""

# Veri içerisinde geçen noktalama işaretlerinin kaldırılması

noktalama = str.maketrans('', '', punctuation)

# Veri içerisinde geçen türkçe karakterlerin latin karakterlere çevrilip bir standarta oturtulması
Tr2Eng = str.maketrans("çğıöşü", "cgiosu")

kelime_listesi = []
sayi_listesi = []
tweet_listesi = []

for i in range(1336):
    yorum = tweetler2829_degerler[i]
    yorum = yorum.lower() # cümledeki her karakterin küçük hale çevrilmesi
    yorum = yorum.translate(noktalama) # noktalama işaretlerinin kaldırılması
    yorum = yorum.translate(Tr2Eng)  # latin alfabesine çevrilmesi
    tweet_listesi.append(yorum) # tweetlerin şimdiki hali ile cümle olarak listelenmesi
    yorum = yorum.split() # tüm cümlelerdeki kelimelerin ayrılması
    yorum_length = len(yorum) 
    """Kelime çantası için gerekli verinin hazırlanması"""
    for j in range(yorum_length):
        kelime_listesi.append(yorum[j]) #Tüm Kelimelerin listelenmesi

    yorum_rakam = [int(s) for s in yorum if s.isdigit()] # cümlelerde geçen rakamların tespiti
    yorum_rakam_length = len(yorum_rakam)
    for k in range(yorum_rakam_length):
        sayi_listesi.append(yorum_rakam[k]) # Tüm sayıların listelenmesi

# Snowballstemmer kütüphanesi ile kelimelerin köklerine ayrılması
kokbul = stemmer('turkish')

yorumlist_kok = kokbul.stemWords(kelime_listesi) # köklerine ayrılan kelime listesi

# köklere ayırınca 9433 den 6722 ye kadar kelime sayısı indi.

kelime_sayi = Counter(yorumlist_kok) # kök kelimelerin aynı olanların sayılması

rakam_sayi = Counter(sayi_listesi) # aynı sayıların kaç tane olduğunun sayılması

"""Kelime Çantasının Hazırlanması"""

list_of_words_and_counter = []
list_of_numbers_and_counter = []


counter_kelime = 0
canta_veri_esik = 10

 # en çok geçen 20 kelimenin ilk 10 tanesinin alınması
for kelime in kelime_sayi.most_common(20):
    if counter_kelime < canta_veri_esik:
        list_of_words_and_counter.append(kelime[0])
    else:
        break

    counter_kelime +=1


counter_kelime = 0

#  en çok geçen 20 sayının ilk 10 tanesinin alınması
counter_rakam = 0

for rakam in rakam_sayi.most_common(20):

    if counter_rakam < canta_veri_esik:
        list_of_numbers_and_counter.append(rakam[0])
    counter_rakam += 1

"""Kelime Çantasının Oluşturulması"""

words_and_number_list = []
words_and_number_list.extend(list_of_numbers_and_counter)
words_and_number_list.extend(list_of_words_and_counter)

"""Kurala göre Kelime Çantası Kullanılarak Tweetlerin Sınıflandırılması"""

match_points_list = []

tweet_etiketi = []

counter_tweet = 0

match_counter = 0
eslesme_esik = 8
for i in tweet_listesi:

    for j in words_and_number_list:

        if str(j) + ' ' in i:
            match_counter +=1

    if match_counter < eslesme_esik:
        tweet_etiketi.append(0) # true list
    else:
        tweet_etiketi.append(1)
    match_points_list.append(match_counter)
    match_counter = 0
print()


dict = {'tahmin' : tweet_etiketi}

etiket_kaydi = pd.DataFrame(dict)

etiket_kaydi.to_csv('tahmin_degerleri.csv')


def test_fonksiyonu(test_yazisi,kelime_cantasi,esik):
    test_yazisi = test_yazisi.lower()
    test_yazisi = test_yazisi.translate(noktalama)
    test_yazisi = test_yazisi.translate(Tr2Eng)
    test_yazisi = [test_yazisi.split()]
    match_counter = 0
    for i in test_yazisi:
        
        for j in kelime_cantasi:
            
            if str(j) in i:
                match_counter += 1
                
        if match_counter < esik:
            print('Yanlis Haber, Eslesme =', match_counter)
        else:
            print('Dogru Haber')

             
            

test = "Asgari ucret 2021 yili icin 2825 tl 90 kurus olarak aciklanmistir. "


test_fonksiyonu(test, words_and_number_list, 8)







