import re
from tkinter import filedialog
from tkinter import Tk

def find_html_references(html_content):
    pattern = re.compile(r'\b(\w+\.html)\b')
    matches = list()
    for i in html_content:
        matches.append(pattern.findall(i))
    return matches

def find_media_references(html_content):
    pattern = re.compile(r'\b(\w+\.(?:png|jpg|css|js|jpeg|mp4|ogg|gif))\b')
    matches = list()
    for i in html_content:
        matches.append(pattern.findall(i))
    return matches

def main(conteudo_html, archives):
    matches_found = find_html_references(conteudo_html)

    set_matches = [set(archive) for archive in matches_found]
    
    nova_string = []
    for index, archive in enumerate(set_matches):
        string_processada = conteudo_html[index]
        for referencia in archive:
            variavel = r'{{ url_for(REPLACE) }}'.replace('REPLACE', f"'{referencia.replace('.html','')}'")
            string_processada = string_processada.replace(referencia, variavel)
        nova_string.append(string_processada)
        
    return [nova_string, archives]

def main2(texto_base, nomes_archives):
    matches_found = find_media_references(texto_base)

    set_matches = [set(archive) for archive in matches_found]

    nova_string = []
    for index, archive in enumerate(set_matches):
        string_processada = texto_base[index]
        for referencia in archive:
            variavel = r"{{ url_for('static', filename='images/REPLACE') }}".replace("REPLACE", f"{referencia}")
            
            if referencia.endswith("css") or referencia.endswith("js"):
                variavel = variavel.replace("images/", "")
                string_processada = string_processada.replace(f"""{referencia}""", variavel)
            else: # jpeg, jpg, png, mp4, ogg, gif
                string_processada = string_processada.replace(f"""images/{referencia}""", variavel)
        nova_string.append(string_processada)
        
    
    for index,item in enumerate(nomes_archives):
        nome_archive = item.replace('.html','')
        with open(f'{nome_archive}.html', 'w', encoding='utf-8') as archive_html:
            archive_html.write(nova_string[index])

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)

    archives = filedialog.askopenfilenames(filetypes=[('archives HTML', '*.html'), ('archives CSS', '*.css'), ('archives JS', '*.js'), ('Todos os archives', '*.*')])
    conteudo_html = list()
    for item in archives:
        with open(item, 'r', encoding='utf-8') as archive:
            conteudo_html.append(archive.read())
        
    html_mudado, nomes_archives = main(conteudo_html, archives)
    main2(html_mudado, nomes_archives)
