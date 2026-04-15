# main.py
import json
from tkinter import messagebox
from gui import LibraryApp
from src.services.book_collection import BookCollection
from src.services.member_collection import MemberCollection
from src.services.loan_service import LoanService
from src.utils.constants import DATA_FILE

def save_all_data(services):
    """A central function to save data from all services."""
    # Start with a clean slate to represent the current state
    full_data = {}
    
    # Each service adds its data to the dictionary
    services['books'].save_data(DATA_FILE, full_data)
    services['members'].save_data(DATA_FILE, full_data)
    services['loans'].save_data(DATA_FILE, full_data)
    
    # Write the combined data to the file once
    with open(DATA_FILE, 'w') as f:
        json.dump(full_data, f, indent=4)

if __name__ == "__main__":
    # 1. Initialize all backend services
    book_service = BookCollection()
    member_service = MemberCollection()
    loan_service = LoanService(book_service, member_service)

    # 2. Load data from the JSON file into each service
    book_service.load_data(DATA_FILE)
    member_service.load_data(DATA_FILE)
    loan_service.load_data(DATA_FILE)
    
    # 3. Bundle services into a dictionary to pass to the GUI
    services = {
        'books': book_service,
        'members': member_service,
        'loans': loan_service
    }

    # 4. Create and run the GUI
    app = LibraryApp(services)
    
    # 5. Set the closing protocol to save data
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to save changes and quit?"):
            save_all_data(services)
            app.destroy()
            
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()