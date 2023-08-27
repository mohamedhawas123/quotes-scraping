from fastapi import FastAPI, Depends, HTTPException
import psycopg2 
from typing import List
from scraper import DATEBASE_URL


app = FastAPI();


def get_db():

    conn = psycopg2.connect(DATEBASE_URL)
    try:
        yield conn 
    finally:
        conn.close();


@app.get('/quotes', response_model=List[dict])
def read_quotes(author: str = None, db: psycopg2.extensions.connection=Depends(get_db)):
    with db.cursor() as cursor:
        if author:
            cursor.execute("SELECT * FROM quotes WHERE author=%s", (author, ))
        else:
            cursor.execute("SELECT * FROM quotes")
        
        results = [
            {   "id": id,
                "quote": quote,
                "author": author
            } for id, quote, author in cursor.fetchall()
        ]
        return results
    








