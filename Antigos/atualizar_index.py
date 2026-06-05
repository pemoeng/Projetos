import openpyxl, json, datetime, re

# Mapeamento para normalizar valores (sem acento → com acento, minúsculo → correto)
NORMALIZAR = {
    "em analise":  "Em Análise",
    "aprovado":    "Aprovado",
    "aprovado ar": "Aprovado AR",
    "reprovado":   "Reprovado",
    "obra":        "Obra",
    "cancelado":   "Cancelado",
}

def normalizar(valor):
    v = valor.strip()
    return NORMALIZAR.get(v.lower(), v)

wb = openpyxl.load_workbook("Projetos100125-Paulo.xlsx")
ws = wb["Plan1"]

rows = []
for row in ws.iter_rows(min_row=2, values_only=False):
    protocolo_cell  = row[0]
    cliente_cell    = row[1]
    projeto_cell    = row[2]
    vistoria_cell   = row[3]
    inversores_cell = row[4]
    marca_cell      = row[5]

    protocolo = protocolo_cell.value
    cliente   = cliente_cell.value

    # Ignora linhas sem protocolo ou sem cliente
    if not protocolo or not cliente:
        continue

    # Ignora linhas riscadas (strikethrough)
    if (protocolo_cell.font and protocolo_cell.font.strike) or \
       (cliente_cell.font and cliente_cell.font.strike):
        continue

    def cv(cell):
        v = cell.value
        return "" if v is None else str(v).strip()

    proj = normalizar(cv(projeto_cell))
    inv  = cv(inversores_cell)
    marc = cv(marca_cell)

    # Vistoria: converte datas para dd/mm/aaaa
    if isinstance(vistoria_cell.value, datetime.datetime):
        vist = vistoria_cell.value.strftime("%d/%m/%Y")
    elif isinstance(vistoria_cell.value, (int, float)):
        try:
            d = datetime.datetime(1899, 12, 30) + datetime.timedelta(days=int(vistoria_cell.value))
            vist = d.strftime("%d/%m/%Y")
        except:
            vist = str(vistoria_cell.value)
    else:
        vist = normalizar(cv(vistoria_cell))

    # Vistoria vazia → "Sem Status" (necessário para o filtro "Não Instalado" funcionar)
    if vist == "":
        vist = "Sem Status"

    rows.append({
        "protocolo": str(protocolo).strip(),
        "cliente":   str(cliente).strip(),
        "projeto":   proj,
        "vistoria":  vist,
        "inversores":inv,
        "marca":     marc
    })

# Substitui apenas o bloco DATA no HTML, mantendo todo o layout intacto
new_data = json.dumps(rows, ensure_ascii=False)

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

html_new = re.sub(
    r'const DATA = \[.*?\];',
    f'const DATA = {new_data};',
    html,
    flags=re.DOTALL
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_new)

print(f"Feito! {len(rows)} registros atualizados.")