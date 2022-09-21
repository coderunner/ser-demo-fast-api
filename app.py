from fastapi import FastAPI, Header, HTTPException, Response, Request

from book import *
import uuid


CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_XML = "application/xml"

BOOKS = [
  Book(id = str(uuid.uuid4()), title = 'Le bon livre', author = 'H. Lebon'),
  Book(id = str(uuid.uuid4()), title = 'Un autre bon livre', author = "B. LeBonAussi")
 ]

app = FastAPI()


@app.get("/books")
async def get_books(accept: str | None = Header(default=None)):
    if accept == None or CONTENT_TYPE_JSON in accept:
      return BOOKS

    elif CONTENT_TYPE_XML in accept:
      element = books_to_xml_element(BOOKS)
      xml = ET.tostring(element, encoding='utf8', method='xml')
      return Response(content=xml, media_type="application/xml")
    
    else:
      raise HTTPException(status_code=415, detail="Unsupported media type")


@app.post("/books")
async def post_book(request: Request, content_type: str | None = Header(default=None)):

    if content_type == None or CONTENT_TYPE_JSON in content_type:
      body = await request.body()
      new_book = create_new_book(Book.parse_raw(body))
      BOOKS.append(new_book)
      return new_book

    elif CONTENT_TYPE_XML in content_type:
      body = await request.body()
      new_book_data = from_xml_data(body)
      new_book = create_new_book(new_book_data)
      BOOKS.append(new_book)

      xml = ET.tostring(book_to_xml_element(new_book), encoding='utf8', method='xml')
      return Response(content=xml, media_type="application/xml")
    
    else:
      raise HTTPException(status_code=415, detail="Unsupported media type")

def create_new_book(book_data):
    id = str(uuid.uuid4())
    return Book(id = id, title = book_data.title, author = book_data.author)
    
    
