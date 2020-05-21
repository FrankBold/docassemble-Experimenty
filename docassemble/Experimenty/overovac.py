import requests
import base64
from bs4 import BeautifulSoup
from docassemble.base.util import DAList

def overit(ico, firma):
  URL = 'https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi?ico='+ ico +'&obchodni_firma='+ firma
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, 'xml')
  if soup.find('are:Pocet_zaznamu').string == "0":
    return page.encoding
  elif soup.find('are:Pocet_zaznamu').string == "1":
    info = {
      "firma": soup.find('are:Obchodni_firma').string,
      "ico": soup.find('are:ICO').string,
      "sidlo": soup.find('dtt:Nazev_ulice').string +" "+ soup.find('dtt:Cislo_domovni').string +"/"+ soup.find('dtt:Cislo_orientacni').string +", "+ soup.find('dtt:PSC').string +" "+ soup.find('dtt:Nazev_obce').string
    }
    return info
  else:
    pole = []
    firmy = soup.find_all('are:Obchodni_firma')
    for polozka in firmy:
      pole.append(repr(polozka.string).strip("'"))
    return pole
  