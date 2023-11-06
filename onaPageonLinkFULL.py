import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

ana_sayfa_url = 'https://ebs.bilecik.edu.tr/Program/DersKategoriListesi?BolumNo=188'
ana_sayfa = 'https://ebs.bilecik.edu.tr/'

tum_sayfa_verileri = []

response = requests.get(ana_sayfa_url)
print(f"Ana sayfa isteği: {response.status_code}")  # HTTP yanıt kodunu yazdır
soup = BeautifulSoup(response.text, 'html.parser')

linkler = soup.find_all('a')

benzersiz_ders_linkleri = set()

for link in linkler:
    href = link.get('href')
    if href and 'DersNo=' in href:
        ders_no = href.split('DersNo=')[1]
        if ders_no not in benzersiz_ders_linkleri:
            benzersiz_ders_linkleri.add(ders_no)
            sayfa_url = urljoin(ana_sayfa, href)

            response = requests.get(sayfa_url)
            print(f"Sayfa isteği: {response.status_code}")  # HTTP yanıt kodunu yazdır
            soup = BeautifulSoup(response.text, 'html.parser')
            ders_icerik = soup.find('div', id='collapse5')
            sayfa_basligi = soup.title.text if soup.title else 'Başlık Bulunamadı'

            if ders_icerik:
                print(f"İçerik alındı: {sayfa_basligi}")
                temizlenmis_veri = ders_icerik.get_text()
                tum_sayfa_verileri.append((sayfa_basligi, temizlenmis_veri))
            else:
                print(f"İçerik bulunamadı: {sayfa_basligi}")
                tum_sayfa_verileri.append((sayfa_basligi, ''))

with open('sayfa_verileri.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['pageTitle', 'pageContent'])

    for veri in tum_sayfa_verileri:
        csv_writer.writerow([veri[0], veri[1]])

print("Veriler CSV dosyasına kaydedildi.")
