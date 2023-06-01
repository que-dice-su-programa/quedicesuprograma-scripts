import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

def parse_and_chunk(party, text):
    if party == "podemos":
        return PodemosParser().parse_and_chunk(text)
    elif party == "psoe":
        return PSOEParser().parse_and_chunk(text)
    elif party == "pp":
        return PPParser().parse_and_chunk(text)
    elif party == "vox":
        return VoxParser().parse_and_chunk(text)
    else:
        raise Exception("Party not supported")


def chunk_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1024,
        chunk_overlap = 100
    )

    return text_splitter.create_documents([text])

class PodemosParser:
    def parse_and_chunk(self, text):
        text = self.__remove_index(text)
        text = self.__remove_line_breaks(text)
        text = self.__remove_page_numbers(text)
        text = self.__remove_footers(text)
        chunks = self.__chunk_text(text)
        chunks = map(lambda chunk: chunk.page_content.replace('\n', ' '), chunks)

        return list(chunks)

    def __remove_index(self, text):
        lines = text.split('\n')
        filtered_lines = [line for line in lines if ". . . . . ." not in line]
        return '\n'.join(filtered_lines)

    def __remove_line_breaks(self, text):
        """Remove line breaks from text"""
        return text.replace(' -\n', '').replace('  ', ' ').replace('- ', '').replace(' \n', ' ')

    def __remove_page_numbers(self, text):
        """Remove page numbers with a regex that matches  ".\n{number}." """
        return re.sub(r'\.\n\d+\.', '.', text)

    def __remove_footers(self, text):
        return text.replace('\nPODEMOS.', ' ')

    def __chunk_text(self, text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1024,
            chunk_overlap = 20
        )

        return text_splitter.create_documents([text])


class PSOEParser:
    def parse_and_chunk(self, text):
        text = self.__remove_line_breaks(text)
        text = self.__remove_page_numbers(text)
        chunks = self.__chunk_text(text)
        chunks = map(lambda chunk: chunk.page_content.replace('\n', ' '), chunks)

        return list(chunks)[6::][:-2]

    def __remove_line_breaks(self, text):
        """Remove line breaks from text"""
        return text.replace(' -\n', '').replace('  ', ' ').replace(' \n', ' ')

    def __remove_page_numbers(self, text):
        """Remove page numbers with a regex that matches  ".\n{number}." """
        text = re.sub(r'\.\d+\n', '.', text)
        text = re.sub(r'\d+\n', '.', text)
        return text

    def __chunk_text(self, text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1024,
            chunk_overlap = 20
        )

        return text_splitter.create_documents([text])


class PPParser:
    def parse_and_chunk(self, text):
        text = self.__remove_line_breaks(text)
        text = self.__remove_point_numbers(text)
        text = self.__remove_page_numbers(text)
        text = self.__remove_titles(text)
        chunks = self.__chunk_text(text)
        chunks = map(lambda chunk: chunk.page_content.replace('\n', ' '), chunks)

        return list(chunks)[6::][:-2]

    def __remove_titles(self, text):
        lines = text.split("\n")
        lines_without_uppercase = [line for line in lines if not line.isupper()]
        return "\n".join(lines_without_uppercase)

    def __remove_line_breaks(self, text):
        """Remove line breaks from text"""
        return text.replace(' -\n', '').replace('  ', ' ').replace(' \n', ' ')

    def __remove_point_numbers(self, text):
        text = re.sub(r'\d+_ ', '', text)
        text = re.sub(r'\d+ _ ', '', text)
        return text

    def __remove_page_numbers(self, text):
        """Remove page numbers with a regex that matches  ".\n{number}." """
        text = re.sub(r'\d+PROGRAMA ELECTORAL ', '', text)
        text = re.sub(r'\d+ \. ', '', text)
        return text

    def __chunk_text(self, text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1024,
            chunk_overlap = 20
        )

        return text_splitter.create_documents([text])


class VoxParser:
    def parse_and_chunk(self, text):
        text = self.__remove_line_breaks(text)
        text = self.__remove_point_numbers(text)
        text = self.__remove_titles(text)
        chunks = self.__chunk_text(text)
        chunks = map(lambda chunk: chunk.page_content.replace('\n', ' '), chunks)

        return list(chunks)[6::][:-2]

    def __remove_line_breaks(self, text):
        """Remove line breaks from text"""
        return text.replace(' -\n', '').replace('  ', ' ').replace(' \n', ' ')

    def __remove_titles(self, text):
        lines = text.split("\n")
        lines_without_uppercase = [line for line in lines if not line.isupper()]
        return "\n".join(lines_without_uppercase)

    def __remove_point_numbers(self, text):
        return re.sub(r'\d+. ', '', text)

    def __remove_page_numbers(self, text):
        """Remove page numbers with a regex that matches  ".\n{number}." """
        return re.sub(r'\.\d+\n', '', text)

    def __chunk_text(self, text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1024,
            chunk_overlap = 20
        )

        return text_splitter.create_documents([text])

