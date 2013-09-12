import re

def next_version_number():
    setup_py_lines = open('setup.py', encoding='utf-8').readlines()

    with open('setup.py', 'w', encoding='utf-8') as f:
        for line in setup_py_lines:
            if 'version = "' in line:
                digits = re.findall('\d+', line) # find version
                if len(digits) != 3:
                    raise ValueError("bad setup py, in line '%s'" % line)

                digits[-1] = str(int(digits[-1]) + 1) # increment last version number

                parts = line.split('"') # find what inside parenteses
                if len(parts) != 3:
                    raise ValueError("bad setup py, in line '%s'" % line)

                parts[1] = '.'.join(digits) # replace version

                f.write('"'.join(parts))
            else:
                f.write(line)

if __name__ == '__main__':
    next_version_number()
