from pathlib import Path
import re
import string
import shutil 


class sortkey(str):
    def __lt__(s1, s2):        
        pattern = 'lc([0-9]*)_.*\.py'
        num1 = int(re.match(pattern, s1).groups()[0])
        num2 = int(re.match(pattern, s2).groups()[0])
        return num1 < num2

def process_and_copy(source_dir, output_dir):
    main_block = 'def main'
    for pth in source_dir.glob('*.py'):
        print(f'cleaning {pth}')
        with pth.open() as f:
            code = f.read()
        idx = code.find(main_block)
        if idx > -1:
            code = code[:idx]

        new_file = output_dir/pth.name
        with new_file.open('w') as f:
            f.write(code)

def get_number_and_title(filename):
    pattern = 'lc([0-9]*)_(.*)\.py'
    # from IPython import embed; embed(); exit(0)    
    number, title = re.match(pattern, filename).groups()

    titlewords = title.split('_')
    if titlewords[0] in ['e', 'm', 'h']:
        titlewords = titlewords[1:]

    return number, string.capwords(' '.join(titlewords))

def main():
    source_dir = Path('../code')
    output_dir = Path('_code')
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()
    process_and_copy(source_dir, output_dir)

    root = output_dir
    codefiles = list([p.name for p in root.glob('*.py') if p.name != 'utils.py'])
    codefiles.sort(key=sortkey)

    include_code = ''
    for cf in codefiles:
        filename = output_dir/cf
        number, title = get_number_and_title(filename.name)
        section_name = f'Leetcode {number}: {title}'
        sectionline = f'\\section*{{{section_name}}}'
        includeline = f'\\lstinputlisting[language=Python]{{{filename}}}'
        pagebreak = '\\pagebreak \n\n'
        line = f'{sectionline}\n{includeline}\n{pagebreak}'
        include_code += line

    template_path = Path('template.tex')
    with template_path.open() as tmp:
        template = tmp.read()

    latex = template.replace('%%!', include_code)
    outfile = Path('leetcode.tex')
    with outfile.open('w') as f:
        f.write(latex)


if __name__ == '__main__':
    main()    