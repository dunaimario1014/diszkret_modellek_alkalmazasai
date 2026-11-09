def add_code(a,b):
    ret=''
    for char1, char2 in zip(a,b):
        if char1 == char2:
            ret += '0'
        else:
            ret += '1'

    return ret

def is_linear_code(code_words: list[str]) -> bool:
    for i in code_words:
        for j in code_words:
            if add_code(i,j) not in code_words:
                return False
    return True

assert is_linear_code(['000', '110', '011', '101']) == True, "is_linear_code(['000', '110', '011', '101']) eredménye hibás"
assert is_linear_code(['000', '100', '010']) == False, "is_linear_code(['000', '100', '010']) eredménye hibás"
assert is_linear_code(['0000', '0011', '0101', '0110', '1001', '1010', '1100', '1111']) == True, 'a párosra kiegészítés kódja lineáris'
assert is_linear_code(['001', '010', '100', '111']) == False, 'a páratlanra kiegészítés kódja nem lineáris'
assert is_linear_code(['0000', '1111']) == True, "is_linear_code(['0000', '1111']) eredménye hibás"
print("OK!")