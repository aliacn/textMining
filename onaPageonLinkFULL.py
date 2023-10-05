import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin  # URL'leri birleştirmek için kullanılır
import csv

# Ana sayfanın URL'sini belirtin
ana_sayfa_url = 'https://ebs.bilecik.edu.tr/Program/DersKategoriListesi?BolumNo=188'
ana_sayfa='https://ebs.bilecik.edu.tr/'
# Ana sayfanın HTML içeriğini çekin
response = requests.get(ana_sayfa_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Ana sayfa içerisindeki tüm linkleri bulun
linkler = soup.find_all('a')

# Linkleri içeren URL'leri toplayın ve sadece "DersNo=" içerenleri alın
sayfa_url_listesi = [link.get('href') for link in linkler if link.get('href') is not None and 'DersNo=' in link.get('href')]

print (sayfa_url_listesi)

# Tüm sayfa verilerini saklamak için boş bir liste oluşturun
tum_sayfa_verileri = []

# Linklerden sayfa içeriklerini çekin
for link in sayfa_url_listesi:
    # Linki tam URL'ye dönüştürün (gerekirse)
    if not link.startswith('https'):
        link = ana_sayfa + link
        # Sayfa içeriğini çekin
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        ders_icerik = soup.find('div', id='collapse5')
        sayfa_basligi = soup.title.text if soup.title else 'Başlık Bulunamadı'

        if ders_icerik:
            # HTML etiketlerini temizleyin ve metin içeriğini elde edin
            print(ders_icerik.get_text())
            temizlenmis_veri = ders_icerik.get_text()
            tum_sayfa_verileri.append((sayfa_basligi, temizlenmis_veri))
        else:
            tum_sayfa_verileri.append((sayfa_basligi, ''))

# Şimdi tum_sayfa_verileri içinde tüm sayfa içeriklerine sahipsiniz.

# Verileri bir CSV dosyasına kaydedin
with open('sayfa_verileri.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['pageTitle', 'pageContent'])

    for veri in tum_sayfa_verileri:
        csv_writer.writerow([veri[0], veri[1]])

print("Veriler CSV dosyasına kaydedildi.")
