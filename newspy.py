from requests_html import HTMLSession
import os
from rich import print
from rich.prompt import Prompt
from rich.console import Console
import json

session = HTMLSession()
extensions = ['.png', '.jpeg', '.jpg']
console = Console()

def display_logo():
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
    console.print("1. Inserisci manualmente l'URL", style="bold blue")
    for idx, site in enumerate(sites, 2):
        console.print(f"{idx}. {site['name']}", style="bold blue")

def scrape_url(url):
    response = session.get(url)
    elements = response.html.find('p, a, h1, h2, h3')
    for element in elements:
        if 'href' in element.attrs:
            link = element.attrs['href']
            if any(link.endswith(ext) for ext in extensions):
                os.system(f"kitty icat {link}")
        else:
            console.print(element.text)

def scrape_site(site):
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
            if not link.startswith('http') or not link.startswith('https'):
                link = url + link
            if link.startswith(url):
                formatted_link = link.split('/')[-1]
                formatted_link = formatted_link.split('.')[0]
                formatted_link = formatted_link.replace('-', ' ').replace('_', ' ')
                links_list.append((link, formatted_link))

    for idx, (link, formatted_link) in enumerate(links_list, 1):
        console.print(f"{idx}. {formatted_link}")

    # Prompt user to select a link
    option = Prompt.ask("Seleziona un link", choices=[str(i) for i in range(1, len(links_list) + 1)])
    selected_link = links_list[int(option) - 1][0]
    console.print(f"Hai selezionato: {selected_link}")

    # Call scrape_url with the selected link
    scrape_url(selected_link)

def handle_option(option, sites):
    if option == '1':
        url = Prompt.ask("Enter the url")
        scrape_url(url)
    else:
        index = int(option) - 2
        if 0 <= index < len(sites):
            scrape_site(sites[index])
        else:
            console.print("Opzione non valida", style="bold red")

def main():
    with open('sites.json', 'r') as json_file:
        sites = json.load(json_file)

    display_logo()
    show_menu(sites)
    option = Prompt.ask("Seleziona un'opzione")
    handle_option(option, sites)

if __name__ == "__main__":
    main()
