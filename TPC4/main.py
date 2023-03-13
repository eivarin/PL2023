import re

f = open("example.csv", "r")
lines = f.read().splitlines()

header = lines.pop(0)
print(header)
print(lines)

fields = re.split(r"(?<!\{\d),(?!\d+\})", header)

class campo:
    def __init__(self, matches):
        self.name = matches[0]
        self.isList = False
        if (matches[1]):
            self.isList = True
            self.minimum_e = int(matches[1])
            self.maximum_e =  int(matches[2]) if matches[2] else ""
            self.agregation_fun = matches[3]
    def get_regex(self):
        r = r"((?:\w|\s)+)"
        if self.isList:
            for _ in range(self.minimum_e-1):
                r += r",((?:\w|\s)+)"
            for _ in range(self.maximum_e-self.minimum_e):
                r += r",((?:\w|\s)+)?"
        return r


class row:
    def __init__(self, line, campos, regex: re.Pattern):
        self.dict = {}
        grs = regex.match(line).groups()
        indice_campos = 0
        indice_grupos = 0
        while indice_campos < len(campos):
            c = campos[indice_campos]
            if c:
                if (c.isList):
                    self.dict[c.name] = []
                    for x in grs[indice_grupos:c.minimum_e+indice_grupos]:
                        self.dict[c.name].append(int(x))
                        indice_grupos += 1
                    for x in grs[indice_grupos: (c.maximum_e - c.minimum_e)+indice_grupos]:
                        if(x):
                            self.dict[c.name].append(int(x))
                            indice_grupos += 1
                    if c.agregation_fun:
                        match(c.agregation_fun):
                            case "sum":
                                self.dict["sum" + c.name] = sum(self.dict[c.name])
                                del self.dict[c.name]
                                break
                            case "media":
                                self.dict["media" + c.name] = sum(self.dict[c.name]) / len(self.dict[c.name])
                                del self.dict[c.name]
                                break
                            case _:
                                break
                else:
                    self.dict[c.name] = grs[indice_grupos]
                    indice_grupos += 1
            indice_campos += 1
    def __str__(self):
        r = "  { \n    "
        lis = []
        for key,value in self.dict.items():
            if type(value) == type([]):
                lis.append(f'"{key}": {value}')
            else:
                lis.append(f'"{key}": "{value}"')
        r += ", \n    ".join(lis)
        return r + " \n  }"

parsed_fields = []
for field in fields:
    m = re.match(r"(\w+)(?:\{(\d+)(?:,(\d+))\})?(?:\:\:(\w+))?", field)
    if m:
        parsed_fields.append(campo(m.groups()))

regex_str=parsed_fields[0].get_regex()
for c in parsed_fields[1:]:
    regex_str += "," + c.get_regex()
print(regex_str)
regex = re.compile(regex_str)
data = [row(line, parsed_fields, regex) for line in lines]
result = "[ \n" + ", \n".join([str(l) for l in data]) + " \n]"
print(result)