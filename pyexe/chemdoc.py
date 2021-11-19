# Parsing chemical formulas in doc files
# Working in an extremely low-efficient approach (just like Microsoft Word itself)

from docx import Document
from pyvalem.formula import Formula, FormulaParseError

def main():
    input_file_path = input('Input file (e.g. test.docx): ')
    output_file_path = input('Output filename (e.g. result.docx): ')

    doc = Document(input_file_path)

    # Here comes the nesting loops!
    for paragraph in doc.paragraphs:
        for word in paragraph.text.split():
            try:
                replace_text_in_paragraph(paragraph, word, Formula(word).html)
            except FormulaParseError:
                continue

    doc.save(output_file_path)

def replace_text_in_paragraph(paragraph, key, value):
    inline = paragraph.runs
    for item in inline:
        if key in item.text:
            item.text = item.text.replace(key, value)

if __name__ == '__main__':
    main()