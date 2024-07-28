from requests_html import HTMLSession
import os
from rich import print
from rich.prompt import Prompt
from rich.console import Console

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
    [/bold blue]""", justify="left")

def show_menu():
    console.print("1. Inserisci manualmente l'URL", style="bold blue")
    console.print("2. Altra opzione", style="bold blue")

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

def handle_option(option):
    if option == '1':
        url = Prompt.ask("Enter the url")
        scrape_url(url)
    elif option == '2':
        console.print("Altra opzione selezionata", style="bold green")
    else:
        console.print("Opzione non valida", style="bold red")

def main():
    display_logo()
    show_menu()
    option = Prompt.ask("Seleziona un'opzione")
    handle_option(option)

if __name__ == "__main__":
    main()
