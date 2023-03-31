import discord
import requests
from bs4 import BeautifulSoup


intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
TOKEN = 'Token'

def get_nerdin_vagas(cargo):
    url = f'https://nerdin.com.br/vagas?CodigoCidade=5570&CodigoCargo=8&CodigoVaga=&CodigoEmpresa=0&q={cargo}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    vagas = soup.find_all('div', class_='card-body')
    return vagas

def get_linkedin_vagas(cargo):
    url = f'https://www.linkedin.com/jobs/search/?keywords={cargo}&location=Trabalho%20remoto'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    vagas = soup.find_all('li', class_='result-card')
    return vagas

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/vagas'):
        cargo = message.content.split(' ')[1]
        nerdin_vagas = get_nerdin_vagas(cargo)
        linkedin_vagas = get_linkedin_vagas(cargo)
        response = ''
        for vaga in nerdin_vagas:
            response += f'Nerdin: {vaga.find("a").text}\n{vaga.find("a").get("href")}\n\n'
        for vaga in linkedin_vagas:
            response += f'LinkedIn: {vaga.find("h3").text}\n{vaga.find("a").get("href")}\n\n'
        await message.reply(response)


client.run(TOKEN)
