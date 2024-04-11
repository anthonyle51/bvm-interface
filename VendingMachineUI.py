import tkinter as tk
from tkinter import ttk, messagebox

class VendingMachineUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vending Machine")

        self.products = [
            {"id": "A1", "name": "Lithium AA", "price": 5.99},
            {"id": "A2", "name": "Lithium AAA", "price": 6.99},
            {"id": "B1", "name": "Alkaline AA", "price": 4.99},
            {"id": "B2", "name": "Alkaline AAA", "price": 4.49}
        ]
        self.cart = []

        self.product_frame = ttk.LabelFrame(root, text="Products")
        self.product_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        for product in self.products:
            button = ttk.Button(self.product_frame, text=f"{product['name']} - ${product['price']}", 
                                command=lambda p=product: self.add_to_cart(p))
            button.pack(fill='x', padx=5, pady=5)

        self.cart_summary = tk.StringVar(value="Cart: 0 item(s) - $0.00")
        ttk.Label(root, textvariable=self.cart_summary).grid(row=1, column=0, sticky="ew")

        ttk.Button(root, text="Clear Cart", command=self.clear_cart).grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        ttk.Button(root, text="Checkout", command=self.checkout).grid(row=3, column=0, sticky="ew", padx=10, pady=5)

    def add_to_cart(self, product):
        self.cart.append(product)
        self.update_cart_summary()

    def clear_cart(self):
        self.cart.clear()
        self.update_cart_summary()

    def update_cart_summary(self):
        total = sum(item['price'] for item in self.cart)
        summary = f"Cart: {len(self.cart)} item(s) - ${total:.2f}"
        self.cart_summary.set(summary)

    def checkout(self):
        if not self.cart:
            messagebox.showinfo("Checkout", "Your cart is empty.")
            return
        
        total = sum(item['price'] for item in self.cart)
        messagebox.showinfo("Checkout", f"Total amount: ${total:.2f}\nThank you for your purchase!")
        self.clear_cart()

if __name__ == "__main__":
    root = tk.Tk()
    app = VendingMachineUI(root)
    root.mainloop()