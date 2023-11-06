import pandas as pd
import matplotlib.pyplot
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

# CSV dosyasını okuyun
df = pd.read_csv('sayfa_verileri.csv')

# NaN değerleri temizleyin veya boş bir değerle doldurun
df['pageContent'].fillna('', inplace=True)

# Tüm ders içeriklerini birleştirin
tum_icerik = ' '.join(df['pageContent'])

# İstediğiniz kelimeleri hariç tutun (örneğin, "ders" ve "konu")
hariç_tutulan_kelimeler = ['ders','çalışması','bir','etik','sınıf','uygulamaları','dışı','çalışma', 'konu',"hafta","metodu","öğretim","ile","ara","proje","tartışmalı","giriş","temel","sınav"]

# Kelime sıklıklarını saymak için CountVectorizer kullanın
count_vectorizer = CountVectorizer(stop_words=hariç_tutulan_kelimeler, token_pattern=r'\b\w{3,}\b')
kelime_sikliklari = count_vectorizer.fit_transform([tum_icerik])

# Kelimeleri ve sıklıkları alın
kelimeler = count_vectorizer.get_feature_names_out()
sikliklar = kelime_sikliklari.toarray()[0]

# En çok geçen 10 kelimeyi seçin
en_cok_gecen_kelimeler = [kelimeler[i] for i in sikliklar.argsort()[-10:][::-1]]
en_cok_gecen_sikliklar = [sikliklar[i] for i in sikliklar.argsort()[-10:][::-1]]

# Kelimeleri ve sıklıklarını görselleştirin
plt.figure(figsize=(10, 6))
plt.barh(en_cok_gecen_kelimeler, en_cok_gecen_sikliklar, color='skyblue')
plt.xlabel('Sıklık')
plt.title('Derslerde En Çok Geçen 10 Kelimenin Sıklığı (Özel Kelimeler Hariç)')
plt.gca().invert_yaxis()  # Kelimeleri büyükten küçüğe sırala
plt.show()
