def syntactic_analysis(tokens):
    index = 0
    print(tokens)

    def parse_expression(tokens):
        nonlocal index
        if tokens[index][0] == 'STRING':
            index += 1
            if tokens[index][0] == 'OP':
                index += 1
                if tokens[index][0] == 'NUM':
                    index += 1
                    return True
        return False

    def parse_print(tokens):
        nonlocal index
        if tokens[index][0] == 'SYSTEM':
            index += 1
            if tokens[index][0] == 'PARENIZQ':
                index += 1
                if parse_expression(tokens):
                    if tokens[index][0] == 'PARENDER':
                        index += 1
                        if tokens[index][0] == 'PUNTOCOMA':
                            index += 1
                            return True
        return False

    def parse_for(tokens):
        nonlocal index
        if tokens[index][0] == 'FOR':
            index += 1
            if tokens[index][0] == 'PARENIZQ':
                index += 1
                if tokens[index][0] == 'INT':
                    index += 1
                    if tokens[index][0] == 'ID':
                        index += 1
                        if tokens[index][0] == 'EQ':
                            index += 1
                            if tokens[index][0] == 'NUM':
                                index += 1
                                if tokens[index][0] == 'PUNTOCOMA':
                                    index += 1
                                    if tokens[index][0] == 'ID':
                                        index += 1
                                        if tokens[index][0] == 'OP':
                                            index += 1
                                            if tokens[index][0] == 'NUM':
                                                index += 1
                                                if tokens[index][0] == 'PUNTOCOMA':
                                                    index += 1
                                                    if tokens[index][0] == 'ID':
                                                        index += 1
                                                        if tokens[index][0] == 'OP':
                                                            index += 1
                                                            if tokens[index][0] == 'PARENDER':
                                                                index += 1
                                                                if tokens[index][0] == 'LLAVEIZQ':
                                                                    index += 1
                                                                    if parse_print(tokens):
                                                                        if tokens[index][0] == 'LLAVEDER':
                                                                            return "Estructura FOR correcta"
        return "Error linea: " + str(index) + " con el token: " + str(tokens[index])

    return parse_for(tokens)