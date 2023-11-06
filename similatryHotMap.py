import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# CSV dosyasını okuyun
df = pd.read_csv('sayfa_verileri.csv')

# NaN değerleri temizleyin veya boş bir değerle doldurun
df['pageContent'].fillna('', inplace=True)

# İlgili dersin indeksini seçin (örneğin, BM402)
ilgili_ders_indeksi = df[df['pageTitle'].str.startswith('BM402')].index[0]

# TfidfVectorizer kullanarak içerikleri vektörlere dönüştürün
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['pageContent'])

# İlgili dersin diğer derslerle benzerlik skorlarını hesaplayın
benzerlik_skorlari = cosine_similarity(tfidf_matrix[ilgili_ders_indeksi], tfidf_matrix)

# İlgili dersin en yüksek benzerlik skorlarına sahip terimlerini seçin
en_yuksek_skorlar = benzerlik_skorlari[0].argsort()[-11:-1]

# Terimler ve benzerlik skorlarını alın
terimler = tfidf_vectorizer.get_feature_names_out()
en_yuksek_skor_terimler = [terimler[i] for i in en_yuksek_skorlar]
en_yuksek_skor_degerler = [benzerlik_skorlari[0][i] for i in en_yuksek_skorlar]

# Terimleri ve benzerlik skorlarını görselleştirin
plt.figure(figsize=(10, 6))
plt.barh(en_yuksek_skor_terimler, en_yuksek_skor_degerler, color='skyblue')
plt.xlabel('Benzerlik Skoru')
plt.title('BM402 Dersinin Diğer Derslerle En Yüksek Benzerlik Gösteren Terimleri')
plt.gca().invert_yaxis()  # Terimleri büyükten küçüğe sırala
plt.show()
