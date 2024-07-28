from requests_html import HTMLSession
import os
from rich import print
from rich.prompt import Prompt
from rich.console import Console
import json
import openai
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Ottieni la chiave API di OpenAI dalle variabili d'ambiente
openai.api_key = os.getenv('OPENAI_API_KEY')

# Ottieni la variabile IMAGES dalle variabili d'ambiente e converti in booleano
Images = os.getenv('IMAGES', 'True').lower() in ('true', '1', 't')

session = HTMLSession()
extensions = ['.png', '.jpeg', '.jpg']
console = Console()

def display_logo():
    # Mostra il logo
    console.print(r"""[bold blue]
 _   _
| \ | |
|  \| | _____      _____ _ __  _   _
| . ` |/ _ \ \ /\ / / __| '_ \| | | |
| |\  |  __/\ V  V /\__ \ |_) | |_| |
\_| \_/\___| \_/\_/ |___/ .__/ \__, |
                        | |     __/ |
                        |_|    |___/
    [/bold blue]""")

def show_menu(sites):
    # Mostra il menu con le opzioni per inserire manualmente l'URL o selezionare un sito dalla lista
    console.print("1. Enter the URL manually", style="bold blue")
    for idx, site in enumerate(sites, 2):
        console.print(f"{idx}. {site['name']}", style="bold blue")

def get_summary(text):
    # Utilizza l'API di OpenAI per generare un riassunto del testo fornito
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Please summarize the following article."},
            {"role": "user", "content": text},
        ]
    )
    summary = response['choices'][0]['message']['content'].strip()
    return summary

def scrape_url(url, return_to_site_menu):
    # Esegue una richiesta HTTP all'URL fornito e stampa il contenuto dell'articolo
    response = session.get(url)
    article_text = ''
    elements = response.html.find('p, a, h1, h2, h3')
    for element in elements:
        if 'href' in element.attrs:
            link = element.attrs['href']
            if any(link.endswith(ext) for ext in extensions) and Images:
                os.system(f"kitty icat {link}")
        else:
            console.print(element.text)
            article_text += element.text + ' '

    # Mostra il menu delle opzioni per tornare al menu principale, alla selezione degli URL del sito, ottenere un riassunto o uscire
    console.print("\n[bold blue]Options:[/bold blue]")
    console.print("0. Return to main menu", style="bold blue")
    console.print("1. Return to site URL selection", style="bold blue")
    console.print("2. Get a summary of the article", style="bold blue")
    console.print("3. Exit", style="bold blue")
    option = Prompt.ask("Select an option", choices=["0", "1", "2", "3"])

    if option == "0":
        main()  # Chiama la funzione principale per tornare al menu iniziale
    elif option == "1":
        scrape_site(return_to_site_menu)  # Torna al menu degli URL del sito
    elif option == "2":
        summary = get_summary(article_text)  # Ottiene il riassunto dell'articolo
        console.print("\n[bold blue]Summary:[/bold blue]")
        console.print(summary)
        scrape_url(url, return_to_site_menu)  # Mostra nuovamente le opzioni dopo aver mostrato il riassunto
    elif option == "3":
        exit()  # Esce dal programma

def scrape_site(site):
    # Esegue una richiesta HTTP all'URL del sito e ottiene gli articoli in base all'xpath fornito
    url = site['url']
    xpath = site['xpath']
    response = session.get(url)
    articles = response.html.xpath(xpath)
    links_list = []

    for article in articles:
        links = article.xpath('.//a/@href')
        for link in links:
            if link.endswith('/'):
                link = link[:-1]
            if not link.startswith('http') and not link.startswith('https'):
                link = url + link
            if link.startswith(url):
                formatted_link = link.split('/')[-1]
                formatted_link = formatted_link.split('.')[0]
                formatted_link = formatted_link.replace('-', ' ').replace('_', ' ')
                links_list.append((link, formatted_link))

    # Aggiungi un'opzione per tornare al menu principale
    console.print("0. Go back", style="bold blue")
    for idx, (link, formatted_link) in enumerate(links_list, 1):
        console.print(f"{idx}. {formatted_link}")

    # Chiede all'utente di selezionare un link
    option = Prompt.ask("Select a link", choices=[str(i) for i in range(0, len(links_list) + 1)])
    if option == '0':
        main()  # Chiama la funzione principale per tornare al menu iniziale
    else:
        selected_link = links_list[int(option) - 1][0]
        console.print(f"You selected: {selected_link}")

        # Chiama scrape_url con il link selezionato
        scrape_url(selected_link, site)

def handle_option(option, sites):
    # Gestisce l'opzione selezionata dall'utente nel menu principale
    if option == '1':
        url = Prompt.ask("Enter the url")
        scrape_url(url, None)
    else:
        index = int(option) - 2
        if 0 <= index < len(sites):
            scrape_site(sites[index])
        else:
            console.print("Invalid option", style="bold red")

def main():
    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    # Ottieni la chiave API di OpenAI dalle variabili d'ambiente
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Ottieni la variabile IMAGES dalle variabili d'ambiente e converti in booleano
    global Images
    Images = os.getenv('IMAGES', 'True').lower() in ('true', '1', 't')

    # Carica i siti dal file JSON e mostra il menu principale
    with open('sites.json', 'r') as json_file:
        sites = json.load(json_file)

    display_logo()
    show_menu(sites)
    option = Prompt.ask("Select an option")
    handle_option(option, sites)

if __name__ == "__main__":
    main()
