import inspect
import sys

def is_string(code: str):
    end_idx = 0
    tmp_idx = 1

    if code[0] == '"':
        code = code[1:]
        for ch in code:
            if ch == '"':
                end_idx += tmp_idx
                break
            tmp_idx += 1
    
    return end_idx != 0 and end_idx == len(code)

def print_error(line: int):
    print(f'[makelog] error : {line}')
    # print(f'[makelog] error {inspect.currentframe().f_back.f_lineno}') # 디버그 용

def execute(code: str, line: int):
    tokens = code.split()
    filename = str()
    text = str()

    if len(tokens) == 0:
        return 0
    elif len(tokens) != 4:
        print_error(line)
    elif len(tokens) == 4:
        if tokens[0] == 'out':
            # tokens[1] == string
            if is_string(tokens[1]):
                text = tokens[1][1:-1]
            else:
                print_error(line)
                return 1
            
            # tokens[3] == string
            if is_string(tokens[3]):
                filename = tokens[3][1:-1]
            else:
                print_error(line)
                return 1

            # tokens[2] == redirection
            if tokens[2] == '>':
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
            elif tokens[2] == '>>':
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(text)
            else:
                print_error(line)
                return 1
        else:
            print_error(line)
            return 1
        
    return 0

def interpreter(code: str):
    code = code.splitlines()
    line = 1

    for c in code:
        if execute(c, line) == 0:
            line += 1
        else:
            break

def main():
    args = sys.argv
    code = ''

    if len(args) == 1:
        try:
            with open(args[0], 'r', encoding='utf-8') as f:
                code = f.read()
            interpreter(code)
        except:
            print('There is no such file')
        return
    
if __name__ == '__main__':
    main()