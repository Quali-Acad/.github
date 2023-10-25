from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import ssl
import csv

ssl._create_default_https_context = ssl._create_unverified_context


# link = "https://publicacoes.estadao.com.br/guia-da-faculdade/page/1/?post_type=faculdades_2023&ano=2023&s=Bahia&tipo=&modalidade=&estado=&cidade=&classificacao="
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"}

# requisicao = requests.get(link, headers=headers)
# print(requisicao)
# # print(requisicao.text)
# site = BeautifulSoup(requisicao.text, "html.parser") # passer é como se fosse um leitor de HTML ajdua a organziar o código de forma masi facil
# # print(site.prettify()) # prettify é um método que organiza o código de forma mais legível, masi bonita
# print(site.title) # title é um método que retorna o título da página

# Lista de URL's
lista_urls = []

# Lista com os estados brasileiros
estados = ["Bahia"]

# Este primeiro loop realiza a formatação das URL's, as gerando dinamicamente com todos os estados brasileiros entre os anos de 2018 e 2022, pois de 2018 pra trás os dados são iguais.
cont_ano = 23
while cont_ano <= 24:
	
	for estado in estados: 

		url = 'https://publicacoes.estadao.com.br/guia-da-faculdade/page/1/?post_type=faculdades_20'+str(cont_ano)+'&ano=20'+str(cont_ano)+'&s='+estado+'&tipo=&modalidade=&estado=&cidade=&classificacao='
		req = Request(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'})

		webpage = urlopen(req).read()
		page_soup = soup(webpage, "html.parser")

		try:
			page_number = page_soup.find("a", attrs = {"class": "page-numbers"})

			x = int(page_number.next)

			for i in range(1, x + 1):

				# Adiciona as URL's de 2020
				stateurl = "https://publicacoes.estadao.com.br/guia-da-faculdade/page/" + str(i) + "/?post_type=faculdades_20"+str(cont_ano)+"&ano=20"+str(cont_ano)+"&s="+estado+"&tipo=&modalidade=&estado=&cidade=&classificacao="
				lista_urls.append(stateurl)

		except:

			lista_urls.append(url)

	# Incrementa o ano
	cont_ano = cont_ano + 1

resultado = []

ano = ""

if "2023" in url:
    ano = "2023"
else:
    ano = "Não encontrado"
        
# info=site.find_all("p") # find_all é um método que retorna todos os elementos que estão dentro da tag passada como parâmetro
# texto = []

req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
page_soup = soup(webpage, "html.parser")

# Aqui se encontra no HTML todas as tags p, que contém os dados de interesse.
info = page_soup.find_all('p')

texto = []


for e in info:
    texto.append(e.text)

    
del texto[0]
del texto[0]
del texto[0]
del texto[0]
del texto[0]
del texto[0]
del texto[0]
del texto[len(texto) - 1]
del texto[len(texto) - 1]
del texto[len(texto) - 1]
del texto[len(texto) - 1]
del texto[len(texto) - 1]
    
texto_in = []

texto_out = []

    
cont = 1
presencial = False
ead = False
    
for t in texto:
    texto_in.append(t)


    # Verifica modalidade, pois na modalidade EAD os campos de endereço não existem.
    if t == "Modalidade : Presencial":
        presencial = True
        ead = False
    elif t == "Modalidade : EaD":
        presencial = False
        ead = True
    elif "Rua:" in t:
        presencial = True
        ead = False

    if cont >= 14 and presencial:
        cont = 0
        texto_out.append(texto_in)
        texto_in = []
    elif cont >= 11 and ead:
        cont = 0
        texto_out.append(texto_in)
        texto_in = []
    else:
        pass

    cont = cont + 1
    
    
avaliacao = page_soup.find_all("span", class_="box-estrelas")

    # Aqui uma lista é criada de acordo com as informações coletadas anteriormente
notas = []


for nota in avaliacao:
    print(nota)
    if (
        nota.text == "\nNão Estrelado\n"
        or nota.text == "\nSem notas\n"
        or nota.text == "\nNão avaliado\n"
    ):
        notas.append("N/A")
    elif nota.text == "\n\n\n\n\n\n":  # Avaliação: Excelente (5 estrelas)
        notas.append("5")
    elif nota.text == "\n\n\n\n\n":  # Avaliação: Muito Bom (4 estrelas)
        notas.append("4")
    elif nota.text == "\n\n\n\n":  # Avaliação: Bom (3 estrelas)
        notas.append("3")

cont = 0

# Neste loop ocorre a formatação dos dados no modelo final para ser escrito no arquivo CSV.
dados = []

for e in texto_out:
    # print(e)
    # for i, value in enumerate(e):
    #     print(f"Índice {i}: {value}")
#     dados.append([
        e[0],  # Curso
#         e[2],  # IES
        e[1],  # Modalidade
        e[2],  # Verbete
        e[3],  # Titulação
        e[4],  # Campus
        e[5],  # Categoria
#         e[6],  # Duração
        e[7],  # Endereço
#         e[11],  # Cidade
#         e[12],  # Estado
        e[8],  # Site
#         notas[cont],  # Avaliação
#         ano,  # Ano da Avaliação
#     ])

# Crie o arquivo CSV
header = [
    "Curso", "IES", "Modalidade", "Verbete", "Titulação", "Campus", "Categoria", "Duração",
    "Endereço", "Cidade", "Estado", "Site", "Avaliação", "Ano da Avaliação"
]

with open('guia_da_faculdade_definitivo.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(dados)

print("Finalizado!")