import tkinter as tk
from gui import LibraryGUI
from src.services.member_collection import MemberCollection
from src.services.book_collection import BookCollection
from src.services.loan_service import LoanService

def main():
    # 1. Initialize the root window
    root = tk.Tk()

    # 2. Initialize the Backend Services
    book_system = BookCollection()
    member_system = MemberCollection()
    loan_system = LoanService(book_system, member_system)

    # 3. Launch the GUI, passing the backend services to it
    app = LibraryGUI(root, book_system, member_system, loan_system)

    # 4. Start the program loop
    root.mainloop()

if __name__ == "__main__":
    main()