from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import ssl
import csv

ssl._create_default_https_context = ssl._create_unverified_context

# Lista de URL's
lista_urls = []

# Lista com os estados brasileiros
estados = [
    "Acre",
    "Alagoas",
    "Amapa",
    "Amazonas",
    "Bahia",
    "Ceara",
    "Distrito+Federal",
    "Espirito+Santo",
    "Goias",
    "Maranhao",
    "Mato+Grosso",
    "Mato+Mato+do+Sul",
    "Minas+Gerais",
    "Para",
    "Paraiba",
    "Parana",
    "Pernambuco",
    "Piaui",
    "Rio+de+Janeiro",
    "Rio+Grande+do+Norte",
    "Rio+Grande+do+Sul",
    "Rondonia",
    "Roraima",
    "Santa+Catarina",
    "Sao+Paulo",
    "Sergipe",
    "Tocantins",
]

# Este primeiro loop realiza a formatação das URL's, as gerando dinamicamente com todos os estados brasileiros entre os anos de 2018 e 2022, pois de 2018 pra trás os dados são iguais.
# Ajuste o loop para gerar URLs corretamente
for cont_ano in range(2022, 2023):
    print(cont_ano)
    for estado in estados:
        print(estado)
        url = ("https://publicacoes.estadao.com.br/guia-da-faculdade/page/1/?post_type=faculdades_"+str(cont_ano)+"&ano="+str(cont_ano)+"&s="+estado+"&tipo=&modalidade=&estado=&cidade=&classificacao=")
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"})
        print(url)
        webpage = urlopen(req).read()
        page_soup = soup(webpage, "html.parser")

        try:
            page_number = page_soup.find("a", attrs={"class": "page-numbers"})
            x = int(page_number.text)

            for i in range(1, x + 1):
                stateurl = ("https://publicacoes.estadao.com.br/guia-da-faculdade/page/"+str(i)+"/?post_type=faculdades_"+str(cont_ano)+"&ano="+str(cont_ano)+"&s="+estado+"&tipo=&modalidade=&estado=&cidade=&classificacao=")
                lista_urls.append(stateurl)
                print(lista_urls)

        except:
            lista_urls.append(url)

    # Incrementa o ano
    cont_ano = cont_ano + 1

resultado = []
print(resultado)
ano = ""
print(ano)
# Este segundo loop realiza a coleta dos dados de fato. Ocorre uma iteração sobre a lista de URL's gerada, e os dados são capturados dentro deste loop.
for url in lista_urls:
    print("Em progresso...")

    ano = ""

    if "2023" in url:
        ano = "2023"
    # elif "2019" in url:
    #     ano = "2019"
    # elif "2020" in url:
    #     ano = "2020"
    # elif "2021" in url:
    #     ano = "2021"
    # elif "2022" in url:
    #     ano = "2022"
    else:
        ano = "Não encontrado"

    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    webpage = urlopen(req).read()
    page_soup = soup(webpage, "html.parser")

    # Aqui se encontra no HTML todas as tags p, que contém os dados de interesse.
    info = page_soup.find_all("p")

    texto = []

    # Aqui é gerada uma lista com os dados das tag's p adquiridas.
    for e in info:
        texto.append(e.text)

    # Retira as 7 primeiras posicoes da lista e as 5 últimas, pois essas são lixo.
    del texto[:7]
    del texto[-5:]

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

    # Aqui as informações de avaliação são adquiridas
    avaliacao = page_soup.find_all("span", class_="box-estrelas")
    print(avaliacao)

    # Aqui uma lista é criada de acordo com as informações coletadas anteriormente
    notas = []
    for nota in avaliacao:
        nota_text = nota.text.strip()
        if nota_text == "Não Estrelado" or nota_text == "Sem notas" or nota_text == "Não avaliado":
            notas.append("N/A")
        elif "Excelente" in nota_text:
            notas.append("5")
        elif "Muito Bom" in nota_text:
            notas.append("4")
        elif "Bom" in nota_text:
            notas.append("3")

    cont = 0

    # Neste loop ocorre a formatação dos dados no modelo final para ser escrito no arquivo CSV.
    for e in texto_out:
        print(e)

        # Formata Curso
        texto_out[cont][0] = e[0]

        # Formata IES
        ies = str(e[2])
        ies = ies.replace("IES: ", "")
        texto_out[cont][1] = ies
        print(texto_out[cont][1])

        # Formata Modalidade
        try:
            modalidade = str(e[4])
            modalidade = modalidade.split()
            texto_out[cont][2] = modalidade[2]
            print(texto_out[cont][2])

        except:
            if "Rua:" in str(e[10]):
                texto_out[cont][2] = "Presencial"
            else:
                texto_out[cont][2] = "EaD"

        # Formata Verbete
        verbete = str(e[5])
        verbete = verbete.replace("Verbete: ", "")
        texto_out[cont][3] = verbete
        print(verbete)

        # Formata Titulação
        titulacao = str(e[6])
        titulacao = titulacao.split()
        texto_out[cont][4] = titulacao[1] if len(titulacao) > 1 else "N/A"
        print(texto_out[cont][4])

        # Formata Campus
        campus = str(e[7])
        campus = campus.replace("Campus: ", "")
        texto_out[cont][5] = campus

        # Formata Categoria
        categoria = str(e[8])
        categoria = categoria.replace("Categoria: ", "")
        texto_out[cont][6] = categoria

        # Formata Duração:
        duracao = str(e[9])
        duracao = duracao.replace("Duração: ", "")
        texto_out[cont][7] = duracao

        # Formata Endereço
        # Verifica se é EAD ou não
        if texto_out[cont][2] == "EaD":
            texto_out[cont][8] = ""  # -> Endereço
            texto_out[cont][9] = ""  # -> Cidade
            texto_out[cont][10] = ""  # -> Estado
        else:
            texto_out[cont][8] = str(e[10])  # -> Endereço
            texto_out[cont][9] = e[11].replace("Cidade:  ", "") if len(e) > 11 else "N/A"  # -> Cidade
            texto_out[cont][10] = e[12].replace("Estado: ", "") if len(e) > 12 else "N/A"  # -> Estado

        # Formata Site
        site = str(e[-1])
        site = site.replace("Site: ", "")
        print(site)

        # Formata Avaliação
        try:
            texto_out[cont][11] = site
            texto_out[cont][12] = notas[cont] if cont < len(notas) else "N/A"
            texto_out[cont][13] = ano

        except:
            texto_out[cont].append(site)
            texto_out[cont].append(notas[cont] if cont < len(notas) else "N/A")
            texto_out[cont].append(ano)

        cont = cont + 1

    # Aqui os dados são inseridos em uma lista que será iterada posteriormente para a escrita dos dados no arquivo CSV.
    resultado.append(texto_out)

print(resultado)

# Criação do Arquivo CSV

header = [
    "Curso",
    "IES",
    "Modalidade",
    "Verbete",
    "Titulação",
    "Campus",
    "Categoria",
    "Duração",
    "Endereço",
    "Cidade",
    "Estado",
    "Site",
    "Avaliação",
    "Ano da Avaliação",
]

with open("guia_da_faculdade_definitivo.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    print(writer)

    # Escreve o Header
    writer.writerow(header)

    for e in resultado:
        print(e)
        for i in e:
            # Escreve os dados
            writer.writerow(i)

print("Finalizado!")
