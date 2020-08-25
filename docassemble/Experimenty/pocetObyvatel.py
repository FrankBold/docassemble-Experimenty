import csv
from docassemble.base.util import url_of

def pocetObyvatel(obec):
  vysledek = []
  with open(url_of('obyvatele_full.csv'), newline='', encoding='utf-8') as csvfile:
      reader = csv.reader(csvfile, delimiter=';')
      for row in reader:
          if row[1] == obec:
              vysledek.append(round(int(row[2])*0.005))
              
  if len(vysledek) == 0:
      return("Bohužel jsme nenašli zadanou obec")
  elif len(vysledek) > 1:
      return("Našli jsme toho příliš mnoho")
  else:
      return(vysledek[0])
