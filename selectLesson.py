import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# CSV dosyasını oku
df = pd.read_csv('sayfa_verileri.csv')

# NaN değerleri temizle
df['pageContent'].fillna('', inplace=True)



# Hata - Eğitim Bilgi Sistemi dersini çıkar
df['pageTitle'] = df['pageTitle'].str.replace(' - Eğitim Bilgi Sistemi', '')

# Ders başlıklarını al
ders_basliklari = df['pageTitle']

# Ders isimlerini kısa kodlarla listeleyerek kullanıcıya göster
for i, ders in enumerate(ders_basliklari, start=1):
    print(f"{i}) {ders}")

# Kullanıcıdan seçim yapmasını iste
secilen_indeks = int(input("Lütfen bir ders seçin (1, 2, 3, ...): ")) - 1

# Kullanıcının seçtiği dersin adını al
secilen_ders_ad = ders_basliklari.iloc[secilen_indeks]

# TfidfVectorizer kullanarak içerikleri vektörlere dönüştür
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['pageContent'])

# Cosine similarity kullanarak içerikler arasındaki benzerliği hesapla
benzerlik_matrisi = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Seçilen dersin benzerlik skorlarını al
secilen_ders_benzerlik = benzerlik_matrisi[secilen_indeks]

# Benzerlik skorlarını sırala ve en uyumlu 5 dersi göster
en_uyumlu_dersler = [(ders_basliklari[i], benzerlik) for i, benzerlik in enumerate(secilen_ders_benzerlik)]
en_uyumlu_dersler = sorted(en_uyumlu_dersler, key=lambda x: x[1], reverse=True)[:5]

# Kullanıcıya en uyumlu 5 dersi göster
print(f"\nSeçtiğiniz ders: {secilen_ders_ad}\n")
for i, (ders, benzerlik) in enumerate(en_uyumlu_dersler, start=1):
    print(f"{i}) {ders} - Benzerlik Skoru: {benzerlik:.4f}")
