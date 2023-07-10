import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter


def parse(party, text):
    if party == "sumar":
        return SumarParser().parse(text)
    elif party == "psoe":
        return PSOEParser().parse(text)
    elif party == "pp":
        return PPParser().parse(text)
    elif party == "vox":
        return VoxParser().parse(text)
    else:
        raise Exception("Party not supported")


class SumarParser:
    def parse(self, text):
        text = self.__remove_index(text)
        text = self.__remove_page_numbers(text)
        text = self.__remove_line_breaks(text)
        text = self.__remove_footers(text)

        return text

    def __remove_index(self, text):
        lines = text.split('\n')
        filtered_lines = [line for line in lines if ". . . . . ." not in line]
        return '\n'.join(filtered_lines)

    def __remove_line_breaks(self, text):
        """Remove line breaks from text"""
        text = text.replace(' -\n', '').replace('-\n', '').replace('  ', ' ').replace('- ', '').replace(' \n', ' ')
        return re.sub(r'(?<!\.)\n', ' ', text).replace(' . ', '').replace(' ) ', '')

    def __remove_page_numbers(self, text):
        """Remove page numbers with a regex that matches  ".\n{number}." """
        return re.sub(r'(?<=\n)(?!\.)\d+', '\n', text)

    def __remove_footers(self, text):
        return text.replace('\nPODEMOS.', ' ')

    def __chunk_text(self, text):
        text_splitter = CharacterTextSplitter(
            separator='.',
            chunk_size=128,
            chunk_overlap=15,
        )

        return text_splitter.create_documents([text])


class PSOEParser:
    def parse(self, text):
        text = self.__remove_index(text)
        text = self.__remove_line_breaks(text)
        text = self.__remove_page_numbers(text)

        return text

    def __remove_index(self, text):
        lines = text.split('\n')
        filtered_lines = [line for line in lines if "......." not in line]
        return '\n'.join(filtered_lines)

    def __remove_line_breaks(self, text):
        """Remove line breaks from text"""
        text = text.replace(' -\n', '').replace('  ', ' ').replace(' \n', ' ')
        return re.sub(r'(?<!\.)\n', ' ', text).replace('• ', '')

    def __remove_page_numbers(self, text):
        """Remove page numbers with a regex that matches  ".\n{number}." """
        text = re.sub(r'\.\d+\n', '.', text)
        text = re.sub(r'\d+\n', '.', text)
        text = re.sub(r'/\d+ MADRID 7 DE JULIO 2023', '', text)
        return text.replace('Madrid 7 de julio de 2023', '')

    def __chunk_text(self, text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=128,
            chunk_overlap=15
        )

        return text_splitter.create_documents([text])
class PPParser:
    def parse(self, text):
        text = self.__remove_index(text)
        text = self.__remove_line_breaks(text)
        text = self.__remove_point_numbers(text)
        text = self.__remove_page_numbers(text)
        text = self.__remove_titles(text)
        text = self.__wrap_paragraphs(text)

        return text

    def __remove_index(self, text):
        lines = text.split('\n')
        filtered_lines = [line for line in lines if "...." not in line]
        return '\n'.join(filtered_lines)

    def __remove_titles(self, text):
        lines = text.split("\n")
        lines_without_uppercase = [
            line for line in lines if not line.isupper()]

        text = "\n".join(lines_without_uppercase[19:]).replace('RAREDIL', '').replace('RIULFNI', '')
        return re.sub(r'\d+Objetivo', '', text)

    def __remove_line_breaks(self, text):
        """Remove line breaks from text"""
        return text.replace(' -\n', '').replace('  ', ' ').replace(' \n', ' ')

    def __wrap_paragraphs(self, text):
        return re.sub(r'(?<!\.)\n', ' ', text)

    def __remove_point_numbers(self, text):
        text = re.sub(r'\d+_ ', '', text)
        text = re.sub(r'\d+ _ ', '', text)
        text = re.sub(r'\d+“', '', text)
        return text

    def __remove_page_numbers(self, text):
        """Remove page numbers with a regex that matches  ".\n{number}." """
        text = re.sub(r'\n\d+\n', '', text)
        return text

    def __chunk_text(self, text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=128,
            chunk_overlap=15
        )

        return text_splitter.create_documents([text])


class VoxParser:
    def parse(self, text):
        text = self.__remove_page_numbers(text)
        text = self.__remove_line_breaks(text)
        text = self.__remove_point_numbers(text)
        text = self.__remove_titles(text)
        text = self.__clean_chars(text)

        return text

    def __remove_line_breaks(self, text):
        """Remove line breaks from text"""
        return text.replace(' -\n', '').replace('  ', ' ').replace(' \n', ' ')

    def __remove_titles(self, text):
        lines = text.split("\n")
        lines_without_uppercase = [
            line for line in lines if not line.isupper()]
        return "\n".join(lines_without_uppercase)

    def __remove_point_numbers(self, text):
        return re.sub(r'\d+. ', '', text)

    def __remove_page_numbers(self, text):
        return re.sub(r'\n\d+\.', '', text)

    def __clean_chars(self, text):
        return text.replace('昀椀', 'fi')

    def __chunk_text(self, text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=128,
            chunk_overlap=15
        )

        return text_splitter.create_documents([text])
