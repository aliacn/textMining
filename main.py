import requests
from bs4 import BeautifulSoup

# İnternet sitesinden veriyi çekin
url = 'https://ebs.bilecik.edu.tr/Program/DersBilgileri?BolumNo=188&DersNo=6993&Yil=2023'  # İlgili siteyi buraya ekleyin
response = requests.get(url)

# HTML içeriği analiz etmek için BeautifulSoup kullanın
soup = BeautifulSoup(response.text, 'html.parser')

# Ders içeriğini çekin (div elementi id'si "heading5" olan)
ders_icerik = soup.find('div', id='collapse5')

# Ders içeriğini yazdırın
if ders_icerik:
    print(ders_icerik.text)
else:
    print("Ders içeriği bulunamadı.")