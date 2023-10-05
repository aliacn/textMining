import requests
from bs4 import BeautifulSoup

urls = ['https://ebs.bilecik.edu.tr/Program/DersBilgileri?BolumNo=188&DersNo=6993&Yil=2023', 'https://example.com/page2', ...]  # Sayfa URL'lerini burada belirtin

sayfa_verileri = []

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    ders_icerik = soup.find('div', id='collapse5')
    if ders_icerik:
        sayfa_verileri.append(ders_icerik.text)
    else:
        sayfa_verileri.append('')

# Şimdi sayfa verileriniz sayfa_verileri listesinde bulunuyor.
