import re
from langchain.text_splitter import NLTKTextSplitter

def parse_and_chunk(party, text):
    if party == "podemos":
        return PodemosParser().parse_and_chunk(text)
    else:
        raise Exception("Party not supported")

class PodemosParser:
    def parse_and_chunk(self, text):
        text = self.__remove_index(text)
        text = self.__remove_line_breaks(text)
        text = self.__remove_page_numbers(text)
        text = self.__remove_footers(text)
        text_splitter = NLTKTextSplitter()
        chunks = text_splitter.split_text(text)
        chunks = map(lambda chunk: chunk.replace('\n', ' '), chunks)

        return list(chunks)

    def __remove_index(self, text):
        lines = text.split('\n')
        filtered_lines = [line for line in lines if ". . . . . ." not in line]
        return '\n'.join(filtered_lines)

    def __remove_line_breaks(self, text):
        """Remove line breaks from text"""
        return text.replace(' -\n', '').replace('  ', ' ').replace(' \n', ' ')

    def __remove_page_numbers(self, text):
        """Remove page numbers with a regex that matches  ".\n{number}." """
        return re.sub(r'\.\n\d+\.', '.', text)

    def __remove_footers(self, text):
        return text.replace('\nPODEMOS.', ' ')


