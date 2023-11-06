import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

# Türkçe stop kelimelerini kullanın
stop_words = set(stopwords.words("turkish"))

# CSV dosyasını okuyun
df = pd.read_csv('sayfa_verileri.csv')

# NaN değerleri temizleyin veya boş bir değerle doldurun
df['pageContent'].fillna('', inplace=True)

# Ders içeriklerini alın
icerikler = df['pageContent']

# CountVectorizer kullanarak kelime vektörlerini oluşturun
vectorizer = CountVectorizer()

# Stop kelimeleri yükleyin (örneğin: "ve", "in", "ders")
stop_words = set(stopwords.words("turkish"))

# Kelime vektörlerini güncelleyin, stop kelimeleri ve rakamları dışarıda bırakın
vectorizer.stop_words_ = stop_words

ders_vetorleri = vectorizer.fit_transform(icerikler)

# Tüm kelimeleri alın (stop kelimeleri ve rakamlar dışarıda)
tum_kelimeler = [kelime for kelime in vectorizer.get_feature_names_out() if kelime.isalpha()]

# Her ders için en çok geçen 20 kelimeyi ve frekanslarını listele
for i, ders_vektoru in enumerate(ders_vetorleri):
    kelime_frekanslari = [(kelime, frekans) for kelime, frekans in zip(tum_kelimeler, ders_vektoru.toarray()[0])]
    sırali_kelimeler = sorted(kelime_frekanslari, key=lambda x: x[1], reverse=True)

    print(f"Ders {i + 1} - En Çok Geçen 20 Kelime:")
    for kelime, frekans in sırali_kelimeler[:20]:
        print(f"- {kelime}: {frekans} kez")
