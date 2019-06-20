#CALCULO_SOLAR
#Create: 18/06/2019
#By: Alexsandro Oliveira

#https://developers.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes#parse-useragent



import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
import lxml
#===============================
#CEP
#===============================

global position

def cepcorreios(consultCEP):

  url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm'

  payload = {'relaxation': consultCEP,
            'tipoCEP':'ALL',
            'semelhante':'N'}

  r = requests.post(url, data=payload)
  soup = BeautifulSoup(r.text, 'html.parser')
  dados = soup.find_all('td')

  return dados

def cepcoord(consultCEP):

  url = 'https://www.mapacep.com.br/busca-cep.php'

  payload = { 'keywords': consultCEP,
              'submit': 'Pesquisar'
            }

  r = requests.post(url, data=payload)
  soup = BeautifulSoup(r.text, 'html.parser')
  dados2 = soup.find_all('title')

  return dados2

def calculogeral(cep):
  dados = cepcorreios(cep)
  dados2= cepcoord(cep)

  title = ['Local: ', 'Bairro: ', 'Cidade: ', 'CEP: ']
  edress = []

  #----------------------
  cont = 0
  for a in dados:
    for b in a:
      edress.append(title[cont] + b)
      print(b)
    cont += 1
  #----------------------

  for a in edress:
    print(a)

  local = dados[2].get_text()[:len(dados[2].get_text()) -4:]

  for a in dados2:
    for b in a:
      coordenadas = b.split()

  lat = coordenadas[len(coordenadas) - 3][-12:11:]
  log = coordenadas[len(coordenadas) - 1]

  print(lat)
  print(log)

  ##Acesso CRESESB

  table = []

  url = 'http://www.cresesb.cepel.br/index.php?section=sundata'

  payload = { 'latitude_dec':lat[1:len(lat):],
              'latitude':lat,
              'hemi_lat': '0',
              'longitude_dec': log[1:len(log):],
              'longitude': log,
              'formato': '1',
              'lang': 'pt',
              'section': 'sundata'}

  header = {  'Accept': 'text/html,application/xhtml+xmlapplication/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
              'Cache-Control': 'max-age=0',
              'Connection': 'keep-alive',
              'Content-Length': '136',
              'Content-Type': 'application/x-www-form-urlencoded',
              'Cookie': 'switchgroup_news=0; switchgroup1=none',
              'Host': 'www.cresesb.cepel.br',
              'Origin': 'http://www.cresesb.cepel.br',
              'Referer': 'http://www.cresesb.cepel.br/index.php',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' }

  r = requests.post(url, data=payload)

  print(r.status_code) #if return was 200, all ok
  if r.status_code == requests.codes.ok:
    print('Continua Programa... \n')

    print('\n')

  soup = BeautifulSoup(r.text, 'lxml')

  y = soup.select('table #tb_sundata > tbody > tr')
  soup2 = BeautifulSoup(str(y), 'lxml')
  z = soup2.find_all('tr')

  dados = []
  for a in z:
    #print(a.get_text())
    dados.append(a.get_text())
    
  dd = []
  var = []
  position = 0
  for a in dados:
    texto = a.split('\n')
    var.append(texto)
  cont = 0
  for b in var:
    #print(b)
    for c in b[3:]:
      #print(c)
      if c == unidecode(str(local)):
        print(' positin: ', cont)
        position = '{}'.format(cont)
        #print(b[8:len(b)-1])
        dd.append(b[8:len(b)-1])

    cont += 1

  mes = [
        'Distância [km]',
        'Jan',
        'Fev',
        'Mar',
        'Abr',
        'Mai',
        'Jun',
        'Jul',
        'Ago',
        'Set',
        'Out',
        'Nov',
        'Dez',
        'Média',
        'Delta'
  ]

  df = pd.DataFrame(data=dd,columns=mes)
  print('Irradiação solar diária média [kWh/m2.dia]')
  print(df)

  print('\n\n')

  #===================================================

  print(position)

  y2 = soup.select('table .tb_sundata > tbody > tr')
  soup3 = BeautifulSoup(str(y2), 'lxml')
  z2 = soup3.find_all('tr')

  dados2 = []
  for a in z2:
    #print(a.get_text())
    dados2.append(a.get_text())
    
  dd2 = []
  var2 = []
  for a in dados2:
    texto2 = a.split('\n')
    var2.append(texto2)

  '''  cont = 0
  dd2 = []
  for b in var2:
    for c in b[3:]:
      if c[:len(c) -2:] == '22°' or c[:len(c) -2:] == '23°':
        dd2.append(b)'''

  global result

  result = 0
  if int(position) == 0:
    print(var2[1])
    result = var2[1]
    
  elif int(position) == 1:
    print(var2[5])
    result = var2[5]
    
  elif int(position) == 2:
    print(var2[9])
    result = var2[9]

  mes2 = [
        'Jan',
        'Fev',
        'Mar',
        'Abr',
        'Mai',
        'Jun',
        'Jul',
        'Ago',
        'Set',
        'Out',
        'Nov',
        'Dez',
        'Média',
        'Delta'
  ]

  bass = pd.DataFrame(data=[result[4:18]], columns=mes2)

  bass

  return bass


#===============================
#Lat e Log
#===============================

def consultlog_lat(cep):
  dados2= cepcoord(cep)

  for a in dados2:
    for b in a:
      coordenadas = b.split()

  lat = coordenadas[len(coordenadas) - 3][-12:11:]
  log = coordenadas[len(coordenadas) - 1]

  print(lat)
  print(log)

  result_lat_log = []
  result_lat_log.append(lat)
  result_lat_log.append(log)

  print(result_lat_log)
  
  return result_lat_log
























'''from flask import Flask, render_template, url_for, request,send_from_directory
import pandas as pd
import numpy as np
import requests
import xlrd
import lxml
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime

#===============================
#CEP
#===============================

def cepcorreios(consultCEP):

  url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm'

  payload = {'relaxation': consultCEP,
            'tipoCEP':'ALL',
            'semelhante':'N'}

  r = requests.post(url, data=payload)
  soup = BeautifulSoup(r.text, 'html.parser')
  dados = soup.find_all('td')

  return dados

def cepcoord(consultCEP):

  url = 'https://www.mapacep.com.br/busca-cep.php'

  payload = { 'keywords': consultCEP,
              'submit': 'Pesquisar'
            }

  r = requests.post(url, data=payload)
  soup = BeautifulSoup(r.text, 'html.parser')
  dados2 = soup.find_all('title')

  return dados2


def calculogeral(cep):
#consultCEP = 23821065 #25955310

  dados = cepcorreios(cep)
  dados2= cepcoord(cep)

  title = ['Local: ', 'Bairro: ', 'Cidade: ', 'CEP: ']
  edress = []
  #----------------------
  cont = 0
  for a in dados:
    for b in a:
      edress.append(title[cont] + b)
      print(b)
    cont += 1

  #----------------------

  for a in edress:
    print(a)


  for a in dados2:
    for b in a:
      #print(b)
      coordenadas = b.split()

  lat = coordenadas[len(coordenadas) - 3][-12:11:]
  log = coordenadas[len(coordenadas) - 1]

  print(lat)
  print(log)

  #===============================
  ##Acesso CRESESB
  #===============================

  table = []

  url = 'http://www.cresesb.cepel.br/index.php?section=sundata'

  payload = { 'latitude_dec':lat[1:len(lat):],
              'latitude':lat,
              'hemi_lat': '0',
              'longitude_dec': log[1:len(log):],
              'longitude': log,
              'formato': '1',
              'lang': 'pt',
              'section': 'sundata'}

  header = {  'Accept': 'text/html,application/xhtml+xmlapplication/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
              'Cache-Control': 'max-age=0',
              'Connection': 'keep-alive',
              'Content-Length': '136',
              'Content-Type': 'application/x-www-form-urlencoded',
              'Cookie': 'switchgroup_news=0; switchgroup1=none',
              'Host': 'www.cresesb.cepel.br',
              'Origin': 'http://www.cresesb.cepel.br',
              'Referer': 'http://www.cresesb.cepel.br/index.php',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' }

  r = requests.post(url, data=payload)
  #Lista_1 = requests.get(url)

  #cotation = json.loads(Lista_1.text)

  print(r.status_code) #if return was 200, all ok
  if r.status_code == requests.codes.ok:
    print('Continua Programa... \n')
    #print(r.headers['Set-Cookie']) #Retorna Cookies
    print('\n')
    #print(r.request.headers)  #Retorna Cabeçalhos do Python
    #soup = BeautifulSoup(r.text, 'html.parser')
    #print(soup.find_all())

  soup = BeautifulSoup(r.text, 'lxml')
  tag1 = soup.find_all('a')
  tagxx = soup.find_all('table')
  tagx = soup.find_all('td')
  tag2 = soup.find_all('td', align="right")
  #tag2 = soup.find_all('tr', class_="tb_header")
  tag3 = soup.find_all('th')
  #<td align="right">4,80</td>
  #<tr class="tb_header">
  #<th>Jan</th>

  dados = []
  for a in tag2:
    for b in a:
      x = str(b)
      if len(x) > 25:
        qt = x[46:len(x) -7:]
        if len(qt) == 5:
          #print(x[47:len(x) -7:])
          dados.append(x[47:len(x) -7:])
          
        if len(qt) == 4:
          #print(x[46:len(x) -7:])
          dados.append(x[46:len(x) -7:])
          
      if len(x) > 10 and len(x) < 25 and x[3:len(x):] != 'style':
        #print(x[8:len(x) -9:])
        dados.append(x[8:len(x) -9:])

      else:
        for m in x.split():
          if m[:2-len(m):] != '<s' and m[:2-len(m):] != 'st' and m[:2-len(m):] != 'co' and m[:2-len(m):] != '#0':
            #print(m)
            dados.append(m)

  print(dados)

  Plano_Horizontal = dados[45:59]
  Angulo_igual_latitude = dados[59:73]
  Maior_media_anual = dados[73:87]
  Maior_minimo_mensal = dados[87:101]

  mes = [
        'Distância [km]',
        'Jan',
        'Fev',
        'Mar',
        'Abr',
        'Mai',
        'Jun',
        'Jul',
        'Ago',
        'Set',
        'Out',
        'Nov',
        'Dez',
        'Média',
        'Delta'
  ]

  df0 = pd.DataFrame(data=[dados[0:15]],columns=mes)
  print('Irradiação solar diária média [kWh/m2.dia]')

  mes2 = [
        'Jan',
        'Fev',
        'Mar',
        'Abr',
        'Mai',
        'Jun',
        'Jul',
        'Ago',
        'Set',
        'Out',
        'Nov',
        'Dez',
        'Média',
        'Delta'
  ]

  bass = pd.DataFrame(columns=mes2)

  df = pd.DataFrame(data=[Plano_Horizontal],columns=mes2)
  df1 = pd.DataFrame(data=[Angulo_igual_latitude],columns=mes2)
  df2 = pd.DataFrame(data=[Maior_media_anual],columns=mes2)
  df3 = pd.DataFrame(data=[Maior_minimo_mensal],columns=mes2)

  bas = bass.append(pd.concat([df]))
  bas = bas.append(pd.concat([df1]))
  bas = bas.append(pd.concat([df2]))
  bas = bas.append(pd.concat([df3]))

  print('Cálculo no Plano Inclinado')

  bas.index = pd.Index(np.arange(0,len(bas)))

  x = []
  for a in bas.loc[1]:
    x.append(a)

  base = pd.DataFrame(data=[x],columns=mes2)

  return base

#===============================
#Lat e Log
#===============================

def consultlog_lat(cep):
  dados2= cepcoord(cep)

  for a in dados2:
    for b in a:
      coordenadas = b.split()

  lat = coordenadas[len(coordenadas) - 3][-12:11:]
  log = coordenadas[len(coordenadas) - 1]

  print(lat)
  print(log)

  result_lat_log = []
  result_lat_log.append(lat)
  result_lat_log.append(log)

  print(result_lat_log)
  
  return result_lat_log
'''