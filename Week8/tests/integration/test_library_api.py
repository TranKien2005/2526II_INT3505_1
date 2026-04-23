def test_library_borrow_return_flow(client):
    create_book_resp = client.post(
        "/books",
        json={"title": "The Pragmatic Programmer", "author": "Andy Hunt", "total_quantity": 1},
    )
    assert create_book_resp.status_code == 200
    book = create_book_resp.json()
    assert book["available_quantity"] == 1

    borrow_resp = client.post(
        "/borrows",
        json={"book_id": book["id"], "borrower_name": "Kien"},
    )
    assert borrow_resp.status_code == 200
    borrow = borrow_resp.json()
    assert borrow["status"] == "BORROWED"

    borrow_again_resp = client.post(
        "/borrows",
        json={"book_id": book["id"], "borrower_name": "Another"},
    )
    assert borrow_again_resp.status_code == 400
    assert borrow_again_resp.json()["detail"] == "Book is out of stock"

    return_resp = client.post(f"/borrows/{borrow['id']}/return")
    assert return_resp.status_code == 200
    returned = return_resp.json()
    assert returned["status"] == "RETURNED"

    books_resp = client.get("/books")
    assert books_resp.status_code == 200
    books = books_resp.json()
    assert len(books) == 1
    assert books[0]["available_quantity"] == 1

    borrows_resp = client.get("/borrows")
    assert borrows_resp.status_code == 200
    borrows = borrows_resp.json()
    assert len(borrows) == 1
    assert borrows[0]["status"] == "RETURNED"
