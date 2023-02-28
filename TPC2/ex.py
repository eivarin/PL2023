
def areSameType(x,y):
    if x=='':return True
    if x=='=': return False
    if y=='=': return False
    return (y.isdigit() and x.isdigit()) or (not y.isdigit() and not x.isdigit())
soma=0

stringPart=""
capturing=True
while line:= input().lower():
    for c in line:
        if areSameType(stringPart,c):
            stringPart+=c
            if '=' in stringPart:
                print(soma,flush=True)
                stringPart=""
            elif 'on' in stringPart:
                capturing=True
                stringPart=""
            elif 'off' in stringPart:
                capturing=False
                stringPart=""
        else:
            if stringPart=='=':
                print(soma,flush=True)
                stringPart=""
            if capturing:
                if stringPart.isnumeric():
                    soma+=int(stringPart)
            stringPart=c

    