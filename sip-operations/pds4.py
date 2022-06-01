import os
import itertools
from typing import Iterable

from bs4 import BeautifulSoup
from bs4.element import Tag


class Product:
    '''
    Represents a product label.
    '''
    def __init__(self, label_file:str, lid:str, version:tuple, data_files:list[str]):
        '''
        Create a product label
        '''
        self.label_file = label_file
        self.lid = lid
        self.version = version
        self.data_files = data_files

    def lidvid(self):
        '''
        Combine the LID and VID into a LIDVID
        '''
        return f"{self.lid}::{self.vid()}"

    def vid(self):
        '''
        Combine major and minor version numbers into a VID
        '''
        major, minor = self.version
        return f"{str(major)}.{str(minor)}"

    def supersede_dir(self):
        '''
        Combine major and minor version numbers into a VID
        '''
        major, minor = self.version
        return f"v{str(major)}_{str(minor)}"

def create_product(label_file:str) -> Product:
    '''
    Parses a label file into a Label object.
    '''
    with open(label_file) as f:
        doc = BeautifulSoup(f, 'lxml-xml')
    product_element = doc.find(['Product_Observational', 'Product_Document', 'Product_Collection', 'Product_Bundle', 'Product_Context', 'Product_Browse'])
    identification_area = product_element.Identification_Area

    return Product(
        label_file=label_file,
        lid=identification_area.logical_identifier.text,
        version=tuple(int(x) for x in identification_area.version_id.text.split(".")),
        data_files=find_referenced_files(product_element)
    )


def find_referenced_files(product:Tag)->Iterable[str]:
    '''
    Finds all of the files references in a label.
    '''
    element_names=['File', 'Document_File']
    files = product.find_all(element_names)
    return set(x.file_name.text for x in files)

def find_all_labels(directory:str, include_supereded=False)->Iterable[str]:
    '''
    Finds all of the label files in a directory
    '''
    return (x for x in find_all_files(directory, include_supereded) if x.endswith(".xml"))

def find_all_files(directory:str, include_superseded=False)->Iterable[str]:
    '''
    Finds all of the files in a directory, except for already-superseded files.
    '''
    return itertools.chain.from_iterable((os.path.join(dirname, filename) for filename in filenames) 
        for (dirname, _,  filenames) 
        in os.walk(directory) if filenames
        if include_superseded or not 'SUPERSEDED' in dirname)
