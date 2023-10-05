import pandas as pd
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

# Her ders için en benzer 5 dersi bulun
en_uyumlu_dersler = {}

for i, ders in enumerate(ders_basliklari):
    benzerlik_skorlari = list(enumerate(benzerlik_matrisi[i]))
    benzerlik_skorlari = sorted(benzerlik_skorlari, key=lambda x: x[1], reverse=True)

    # Benzerlik skoru 0 olanları ve "- Eğitim Bilgi Sistemi" ifadesini temizleyin
    en_uyumlu_dersler[ders] = [(ders_basliklari[j], benzerlik) for j, benzerlik in benzerlik_skorlari[1:6] if
                               benzerlik > 0]
    en_uyumlu_dersler[ders] = [(uyumlu_ders.replace(" - Eğitim Bilgi Sistemi", ""), benzerlik) for
                               uyumlu_ders, benzerlik in en_uyumlu_dersler[ders]]

# Her dersin en uyumlu 5 dersini yazdırın
for ders, uyumlu_dersler in en_uyumlu_dersler.items():
    print(f"{ders}:")
    for uyumlu_ders, benzerlik in uyumlu_dersler:
        print(f"- {uyumlu_ders} (Benzerlik Skoru: {benzerlik:.2f})")
    print()
