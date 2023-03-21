import ply.lex as lex

states = (
    ('levantado', 'exclusive'),
    ('moedas', 'exclusive'),
)

tokens = (
    "LEVANTAR",
    "POUSAR",
    "ABORTAR",
    "MOEDAS",
    "MOEDA",
    "FIM_MOEDAS",
    "BLOQUEAR",
    "INTERNACIONAL",
    "NACIONAL",
    "VERDE",
    "AZUL"
)

moedas = [
    200,
    100,
    50,
    20,
    10,
    5,
    2,
    1
]

def t_LEVANTAR(t: lex.LexToken):
    r"LEVANTAR"
    t.lexer.begin('levantado')
    return t

def t_levantado_POUSAR(t: lex.LexToken):
    r"POUSAR"
    t.lexer.begin('INITIAL')
    return t

def t_levantado_MOEDAS(t: lex.LexToken):
    r"MOEDA"
    t.lexer.begin('moedas')
    return t

t_levantado_BLOQUEAR = r"T=6(?:0|4)1\d{6}"
t_levantado_INTERNACIONAL = r"T=00\d{9}"
t_levantado_NACIONAL = r"T=2\d{8}"
t_levantado_VERDE = r"T=800\d{6}"
t_levantado_AZUL = r"T=808\d{6}"
t_levantado_ABORTAR = r"ABORTAR"

t_moedas_MOEDA = r"\d{1,2}(?:c|e)"

def t_moedas_FIM_MOEDAS(t: lex.LexToken):
    r"\.|\n"
    t.lexer.begin('levantado')
    return t

t_ignore = ' \t\n'

t_levantado_ignore = ' \t\n'

t_moedas_ignore = ' \t,'

def t_levantado_error(t):
    print(type(t))
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)


def t_moedas_error(t):
    print(type(t))
    print(f"Moeda invalida {t.value[0]}")
    t.lexer.skip(1)

def t_error(t):
    print(type(t))
    print(f"Levante o telefone primeiro. Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

def getSaldoStrFromInt(i: int):
    euros = i // 100
    cents = i%100
    return f"{euros}e{cents}c"

def getCoinsStrFromInt(i:int):
    result = "troco = "
    moedasTroco = []
    for coin in moedas:
        x = 0
        while i >= coin:
            i -= coin
            x += 1
        if x > 0:
            moedaString = f"{coin//100}e" if coin >= 100 else f"{coin}c"
            moedasTroco.append(f"{x}x{moedaString}")
    result+= ", ".join(moedasTroco) + "; Volte sempre!"
    return result

def parseMoedas(x):
    feedback = 'maq: "'
    tok = lexer.token()
    while tok.type != "FIM_MOEDAS":
        match tok.value:
            case "1c":
                x += 1
            case "2c":
                x += 2
            case "5c":
                x += 5
            case "10c":
                x += 10
            case "20c":
                x += 20
            case "50c":
                x += 50
            case "1e":
                x += 100
            case "2e":
                x += 200
            case _:
                feedback += f"{tok.value} - moeda inválida; "
        tok = lexer.token()
        if not tok:
            break
    print(feedback + f'saldo = {getSaldoStrFromInt(x)}"')
    return x

def handleChamada(call_type, curr_saldo):
    price = -1
    match call_type:
        case "BLOQUEAR":
            print('maq: "Esse número não é permitido neste telefone. Queira discar novo número!"')
        case "INTERNACIONAL":
            price = 150
        case "NACIONAL":
            price = 25
        case "VERDE":
            price = 0
        case "AZUL":
            price = 10
    if price != -1:
        next_saldo = curr_saldo - price
        if next_saldo >= 0:
            print(f'maq: "saldo = {getSaldoStrFromInt(next_saldo)}"')
            return next_saldo
        else:
            print(f'maq: "Saldo insuficiente"')
            return curr_saldo
saldo = 0
while x := input():
    lexer.input(x)
    while tok := lexer.token():
        match tok.type:
            case "LEVANTAR":
                print('maq: "Introduza moedas."')
            case "POUSAR":
                print(getCoinsStrFromInt(saldo))
                saldo = 0
            case "MOEDAS":
                saldo = parseMoedas(saldo)
            case "BLOQUEAR" | "INTERNACIONAL" | "NACIONAL" | "VERDE" | "AZUL":
                saldo = handleChamada(tok.type, saldo)
            case "ABORTAR":
                print(f'maq: "{getCoinsStrFromInt(saldo)}')
                saldo = 0

