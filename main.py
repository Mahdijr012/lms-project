import tkinter as tk
from tkinter import messagebox

from src.models.book import Book
from src.models.member import Member
from src.services.book_collection import BookCollection
from src.services.member_collection import MemberCollection
from src.services.loan_service import LoanService

book_collection = BookCollection()
member_collection = MemberCollection()
loan_service = LoanService()

def add_book():
    book = Book(entry_title.get(), entry_author.get(), entry_isbn.get(), entry_year.get())
    book_collection.add_book(book)
    messagebox.showinfo("Success", "Book added")

def add_member():
    member = Member(entry_name.get(), entry_id.get(), entry_contact.get())
    member_collection.add_member(member)
    messagebox.showinfo("Success", "Member added")

def borrow_book():
    member = member_collection.find_by_id(entry_id.get())
    book = book_collection.find_by_isbn(entry_isbn.get())

    if member and book:
        if loan_service.borrow_book(member, book):
            messagebox.showinfo("Success", "Book borrowed")
        else:
            messagebox.showerror("Error", "Cannot borrow")
    else:
        messagebox.showerror("Error", "Invalid member or book")

def return_book():
    member = member_collection.find_by_id(entry_id.get())
    book = book_collection.find_by_isbn(entry_isbn.get())

    if member and book:
        fine = loan_service.return_book(member, book)
        messagebox.showinfo("Returned", f"Book returned. Fine: {fine}")
    else:
        messagebox.showerror("Error", "Invalid member or book")

root = tk.Tk()
root.title("LMS")
root.geometry("400x400")

tk.Label(root, text="Library System").pack()

entry_title = tk.Entry(root)
entry_title.pack()
entry_title.insert(0, "Title")

entry_author = tk.Entry(root)
entry_author.pack()
entry_author.insert(0, "Author")

entry_isbn = tk.Entry(root)
entry_isbn.pack()
entry_isbn.insert(0, "ISBN")

entry_year = tk.Entry(root)
entry_year.pack()
entry_year.insert(0, "Year")

entry_name = tk.Entry(root)
entry_name.pack()
entry_name.insert(0, "Member Name")

entry_id = tk.Entry(root)
entry_id.pack()
entry_id.insert(0, "Member ID")

entry_contact = tk.Entry(root)
entry_contact.pack()
entry_contact.insert(0, "Contact")

tk.Button(root, text="Add Book", command=add_book).pack()
tk.Button(root, text="Add Member", command=add_member).pack()
tk.Button(root, text="Borrow Book", command=borrow_book).pack()
tk.Button(root, text="Return Book", command=return_book).pack()

root.mainloop()