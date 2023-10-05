import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# CSV dosyasını okuyun
df = pd.read_csv('sayfa_verileri.csv')

# NaN değerleri temizleyin veya boş bir değerle doldurun
df['pageContent'].fillna('', inplace=True)

# Ders başlıkları ve içeriklerini alın
ders_basliklari = df['pageTitle']
icerikler = df['pageContent']

# TfidfVectorizer kullanarak içerikleri vektörlere dönüştürün
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(icerikler)

# Cosine similarity kullanarak içerikler arasındaki benzerliği hesaplayın
benzerlik_matrisi = cosine_similarity(tfidf_matrix, tfidf_matrix)

# İlgilenilen dersin indeksini seçin (örneğin, 0 ile başlayan bir indeks)
ilgilenilen_ders_indeksi = 0

# İlgilenilen dersin adını ve benzer derslerin adlarını alın
ilgilenilen_ders_adı = ders_basliklari[ilgilenilen_ders_indeksi]
ilgilenilen_ders_benzerlikleri = benzerlik_matrisi[ilgilenilen_ders_indeksi]

# En yüksek benzerlik skorlarına sahip derslerin indekslerini ve skorlarını alın
en_yuksek_benzerlik_indeksleri = np.argsort(ilgilenilen_ders_benzerlikleri)[::-1][1:11]
en_yuksek_benzerlik_skorları = ilgilenilen_ders_benzerlikleri[en_yuksek_benzerlik_indeksleri]

# Ders başlıklarını alın
en_yuksek_benzerlik_ders_basliklari = [ders_basliklari[i] for i in en_yuksek_benzerlik_indeksleri]

# Çubuk grafik oluşturun
plt.figure(figsize=(10, 6))
plt.barh(en_yuksek_benzerlik_ders_basliklari, en_yuksek_benzerlik_skorları, color='skyblue')
plt.xlabel('Benzerlik Skoru')
plt.title(f'En Benzer Dersler Paketi - {ilgilenilen_ders_adı}')
plt.gca().invert_yaxis()  # Çubukları büyükten küçüğe sırala
plt.show()
