from pydantic import BaseModel
import xml.etree.ElementTree as ET

class Book(BaseModel):
    id: str | None = None
    title: str
    author: str

def book_to_xml_element(book): 
    b = ET.Element('Book')
    ET.SubElement(b, 'Id').text = book.id
    ET.SubElement(b, 'Title').text = book.title
    ET.SubElement(b, 'Author').text = book.author
    return b

def books_to_xml_element(books):
    b = ET.Element('Books')
    for book in books :
      b.append(book_to_xml_element(book))
    return b

def from_xml_data(data):
    book = ET.fromstring(data)
    return Book(id = None, title = book.find('Title').text, author = book.find('Author').text)