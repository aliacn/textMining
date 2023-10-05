import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# CSV dosyasını okuyun
df = pd.read_csv('sayfa_verileri.csv')

# NaN değerleri temizleyin veya boş bir değerle doldurun
df['pageContent'].fillna('', inplace=True)

# Ders başlıklarını alın ve "- Eğitim Bilgi Sistemi" ifadesini temizleyin
ders_basliklari = df['pageTitle'].str.replace('- Eğitim Bilgi Sistemi', '')

# İçerikleri alın
icerikler = df['pageContent']

# TfidfVectorizer kullanarak içerikleri vektörlere dönüştürün
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(icerikler)

# Cosine similarity kullanarak içerikler arasındaki benzerliği hesaplayın
benzerlik_matrisi = cosine_similarity(tfidf_matrix, tfidf_matrix)

# "BM402" sayfasının indeksini bulun
bm402_indeksi = ders_basliklari[df['pageTitle'].str.startswith("BM402")].index[0]

# "BM402" sayfasının benzerlik skorlarını alın
bm402_benzerlik = benzerlik_matrisi[bm402_indeksi]

# Benzerlik skorlarını sıralayın ve en uyumlu 5 dersi alın (kendi dersini çıkarın)
en_uyumlu_dersler = [(ders_basliklari[i], benzerlik) for i, benzerlik in enumerate(bm402_benzerlik) if i != bm402_indeksi]
en_uyumlu_dersler = sorted(en_uyumlu_dersler, key=lambda x: x[1], reverse=True)[:5]


# Grafik çizimi
dersler, benzerlikler = zip(*en_uyumlu_dersler)

plt.figure(figsize=(10, 6))
plt.barh(range(len(dersler)), benzerlikler, color='skyblue')
plt.yticks(range(len(dersler)), dersler)  # Başlıkları tam olarak göstermek için y-tick ayarı
plt.xlabel('Benzerlik Skoru')
plt.title('BM402 Dersinin En Uyumlu 5 Dersi')
plt.gca().invert_yaxis()  # Dersleri büyükten küçüğe sırala
plt.tight_layout()  # Grafiği sığdırmak için otomatik düzenleme
plt.show()