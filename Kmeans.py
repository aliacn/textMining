import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

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

# K-means kümeleme modeli oluşturun
kmeans = KMeans(n_clusters=5)  # Örnek olarak 5 küme oluşturuyoruz
kmeans.fit(tfidf_matrix)

# Küme etiketlerini alın
kume_etiketleri = kmeans.labels_

# PCA ile boyut indirgeme yapın
pca = PCA(n_components=2)  # 2 boyuta indirgiyoruz
dusuk_boyutlu_veri = pca.fit_transform(tfidf_matrix.toarray())

# PCA sonuçlarını görselleştirin
plt.figure(figsize=(10, 6))
plt.scatter(dusuk_boyutlu_veri[:, 0], dusuk_boyutlu_veri[:, 1], c=kume_etiketleri, cmap='viridis')
plt.title('Ders İçeriklerinin Kümeleme Sonuçları')
plt.show()
