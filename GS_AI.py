from datetime import datetime as dt
import requests
import sys
import pyttsx3
import inflect
import speech_recognition as sr
from flask import Flask

reconhecedor = sr.Recognizer()
microfone = sr.Microphone()

escuta = pyttsx3.init()

dia = dt.today().day
mes = dt.today().month

app = Flask(__name__)

msg = ""

escuta.say("Peço que você digite o seu CEP para que possamos iniciar")
escuta.runAndWait()
codigo = input("Digite seu CEP: ")


def obter_uf():
    cep = codigo
    if "-" in cep:
        cep = cep.replace("-", "")
    url = f"https://viacep.com.br/ws/{cep}/json/"
    resposta = requests.get(url)
    dados = resposta.json()
    if "erro" in dados:
        print("CEP não encontrado!")
        sys.exit()
    uf = dados['uf']
    return uf


def obter_cidade():
    cep = codigo
    if "-" in cep:
        cep = cep.replace("-", "")
    url = f"https://viacep.com.br/ws/{cep}/json/"
    resposta = requests.get(url)
    dados = resposta.json()
    if "erro" in dados:
        print("CEP não encontrado!")
        sys.exit()
    localidade = dados['localidade']
    return localidade


def obter_clima(cidade, chave_api):
    url_localizacao = f"http://dataservice.accuweather.com/locations/v1/cities/search"
    params_localizacao = {
        "apikey": chave_api,
        "q": cidade,
        "language": "pt"
    }

    # Obtendo a localização
    resposta_localizacao = requests.get(url_localizacao, params=params_localizacao)
    dados_localizacao = resposta_localizacao.json()
    localizacao_key = dados_localizacao[0]['Key']

    # Obtendo o clima atual
    url_clima = f"http://dataservice.accuweather.com/currentconditions/v1/{localizacao_key}"
    params_clima = {
        "apikey": chave_api,
        "details": True,
        "language": "pt"
    }

    resposta_clima = requests.get(url_clima, params=params_clima)
    dados_clima = resposta_clima.json()

    temperatura = dados_clima[0]['Temperature']['Metric']['Value']
    weathertext = dados_clima[0]['WeatherText']
    umidade = dados_clima[0]['IndoorRelativeHumidity']
    uv = dados_clima[0]['UVIndexText']

    return temperatura, weathertext, umidade, uv


def obter_numero(numero):
    p = inflect.engine()
    numero_extenso = p.number_to_words(numero)

    return numero_extenso


def ouvir():
    try:
        with sr.Microphone(device_index=1) as source:
            print('Ouvindo...')
            voice = reconhecedor.listen(source)
            command = reconhecedor.recognize_google(voice, language='pt-br')
            print(command)
            return command

    except:
        return 'Não escutei nada :/'


cidade = obter_cidade()
chave_api = "4UzZJLjlG6jvG9z7ki2AVvjFl60IwAje"

regiao_norte = ['RO', 'AC', 'AM', 'RR', 'PA', 'AP', 'TO', 'MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']
regiao_sul = ['MG', 'ES', 'RJ', 'SP', 'PR', 'SC', 'RS', 'MS', 'MT', 'GO', 'DF']

hortalicas = ["Abobóra",
              "Abobrinha",
              "Acelga",
              "Aipó",
              "Alface de inverno",
              "Alface de verão",
              "Alho poró",
              "Berinjela",
              "Beterraba",
              "Cebola",
              "Cebolinha verde",
              "Cenoura de inverno",
              "Cenoura de verão",
              "Coentro",
              "Couve",
              "Couve-flor de inverno",
              "Couve-flor de verão",
              "Ervilha",
              "Espinafre",
              "Fava de sevilha",
              "Feijão",
              "Jiló",
              "Maxixe",
              "Melancia",
              "Melão",
              "Mostarda",
              "Nabo",
              "Pepino",
              "Pimentão",
              "Quiabo",
              "Rabanete",
              "Repolho do inverno",
              "Repolho do verão",
              "Salsa",
              "Tomate"]

sul = [[8, 9, 10, 11, 12],
       [1, 2, 8, 9, 10, 11, 12],
       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
       [2, 3, 4, 5, 6, 7],
       [2, 3, 4, 5, 6, 7, 8, 9],
       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
       [2, 3, 4, 5, 6, 7],
       [8, 9, 10, 11, 12],
       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
       [3, 4, 5, 6, 7],
       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
       [1, 2, 3, 4, 10, 11, 12],
       [1, 2, 3, 10, 11, 12],
       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
       [1, 2, 3, 4, 5, 6, 7],
       [1, 10, 11, 12],
       [2, 3, 4, 5, 6, 7, 8, 9, 10],
       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
       [3, 4, 5],
       [1, 2, 3, 8, 9, 10, 11, 12],
       [1, 2, 3, 8, 9, 10, 11, 12],
       [8, 9, 10, 11, 12],
       [8, 9, 10, 11, 12],
       [1, 8, 9, 10, 11, 12],
       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
       [1, 2, 8, 9, 10, 11, 12],
       [1, 8, 9, 10, 11, 12],
       [1, 8, 9, 10, 11, 12],
       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
       [2, 3, 4, 5, 6, 7],
       [1, 2, 8, 9, 10, 11, 12],
       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
       [8, 9, 10, 11, 12]]

norte = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         [2, 3, 4, 5, 6],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         [2, 3, 4, 5, 6, 7, 8],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         [2, 3, 4, 5, 6, 7, 8],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         [3, 4, 5, 6, 7],
         [2, 3, 4],
         [2, 3, 4, 5, 6, 7],
         [3, 4, 5, 6, 7, 8, 9],
         [1, 2, 10, 11, 12],
         [3, 4, 5, 6, 7],
         [2, 3, 4, 5, 6, 7],
         [1, 2, 3, 10, 11, 12],
         [4, 5, 6],
         [2, 3, 4, 8, 9],
         [4, 5],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         [2, 3, 4, 5, 6, 7],
         [2, 3, 4, 5, 6, 7],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         [2, 3, 4, 5, 6, 7, 8, 9],
         [2, 3, 4, 5, 6, 7],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
         [2, 3, 4, 5, 6, 7, 8, 9],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]

indices = []
regiao = ""
lista = ""
estado = obter_uf()

if estado in regiao_sul:
    regiao = sul
elif estado in regiao_norte:
    regiao = norte
else:
    print("UF Inválida")

for i, lista_secundaria in enumerate(regiao):
    if mes in lista_secundaria:
        indices.append(hortalicas[i])
temperatura, weathertext, umidade, uv = obter_clima(cidade, chave_api)

msg = "As hortaliças ideais para o seu mês são:" + ", ".join(indices)
escuta.say(msg)
escuta.runAndWait()

escuta.say("Caso queira saber informações do clima, diga CONTINUAR")
escuta.runAndWait()

with microfone as mic:
    reconhecedor.adjust_for_ambient_noise(mic)
    print("Estou ouvindo...")
    audio = reconhecedor.listen(mic)
    resposta = reconhecedor.recognize_google(audio, language='pt')
    print(resposta)
    if resposta == "continuar":
        clima = str(
            "Agora está com" + "," + str(int(temperatura)) + "graus em" + "," + str(cidade) + "e o clima está" + str(
                weathertext))
        escuta.say(clima)
        escuta.runAndWait()


@app.route('/api/hortalicas', methods=['GET'])
def obter_mensagem():
    return msg

@app.route('/api/clima', methods=['GET'])
def obter_clima():
    clima = str(
        "Agora está com " + str(int(temperatura)) + " graus em " + str(cidade) + " e o clima está " + str(
            weathertext))
    return clima


if __name__ == '__main__':
    app.run()
