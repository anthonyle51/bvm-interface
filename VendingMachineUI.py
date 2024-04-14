import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class VendingMachineUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vending Machine")
        
        # Set the window size and prevent resizing
        # root.overrideredirect(True)
        self.root.geometry('800x400')
        # self.root.resizable(False, False)

        # Main frame configuration
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Left side frame for products
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=0, sticky='ns')

        # Right side frame for cart or additional info
        self.right_frame = ttk.Frame(self.main_frame, width=200)
        self.right_frame.grid(row=0, column=1, sticky='nsew', padx=10)

        # Configure column configuration in main_frame for resizing behavior
        self.main_frame.columnconfigure(0, weight=1)  # Let the left frame expand more
        self.main_frame.columnconfigure(1, weight=0)  # Fixed width for the right frame

        # Sample products in the vending machine with images
        self.products = [
            {"id": "A1", "name": "Lithium AA", "price": 5.99, "image_path": "batteries\energizer-lithium-AA.jpg"},
            # {"id": "A2", "name": "Lithium AAA", "price": 6.99, "image_path": "batteries\energizer-lithium-AAA.webp"},
            {"id": "B1", "name": "Alkaline AA", "price": 4.99, "image_path": "batteries\duracell-alkaline-AA.jpg"},
            {"id": "B2", "name": "Alkaline AAA", "price": 4.49, "image_path": "batteries\energizer-alkaline-AAA.jpg"}
        ]

        self.setup_products_panel()

        self.cart_items = []
        self.setup_checkout_panel()

    def setup_products_panel(self):
        self.images = {}

        # Creating product display with images
        self.product_frame = ttk.LabelFrame(self.left_frame, text="Products")
        self.product_frame.pack(fill='x', expand=True)

        for product in self.products:
            # Container frame for each product
            product_frame = ttk.Frame(self.product_frame)
            product_frame.pack(padx=5, pady=5, fill='x')

            # Load and resize the image using Pillow
            original_image = Image.open(product['image_path'])
            resized_image = original_image.resize((50, 50), Image.LANCZOS)  # Resize the image to 50x50 pixels
            photo = ImageTk.PhotoImage(resized_image)
            self.images[product['id']] = photo  # Store it in the dictionary to prevent garbage collection

            # Image label
            image_label = ttk.Label(product_frame, image=photo)
            image_label.pack(side='left', padx=10)

            # Text label for the name and price, and button for adding to cart
            text = f"{product['name']} - ${product['price']}"
            label = ttk.Label(product_frame, text=text)
            label.pack(side='left')

            button = ttk.Button(product_frame, text="Add to Cart", command=lambda p=product: self.add_to_cart(p))
            button.pack(side='left', padx=10)

    def setup_checkout_panel(self):
        ttk.Label(self.right_frame, text="Cart Summary", font=('Arial', 16)).pack(pady=20)
        self.cart_listbox = tk.Listbox(self.right_frame)
        self.cart_listbox.pack(fill='both', expand=True)
        ttk.Button(self.right_frame, text="Clear Cart", command=self.clear_cart).pack(fill='x', pady=5)
        ttk.Button(self.right_frame, text="Checkout", command=self.checkout).pack(fill='x', pady=5)

    def add_to_cart(self, product):
        self.cart_items.append(product)
        self.update_cart_view()

    def update_cart_view(self):
        self.cart_listbox.delete(0, tk.END)
        for item in self.cart_items:
            self.cart_listbox.insert(tk.END, f"{item['name']} - ${item['price']}")
        total = sum(item['price'] for item in self.cart_items)
        self.cart_listbox.insert(tk.END, f"Total: ${total:.2f}")

    def clear_cart(self):
        self.cart_items.clear()
        self.update_cart_view()

    def checkout(self):
        if not self.cart_items:
            messagebox.showinfo("Checkout", "Your cart is empty.")
            return
        total = sum(item['price'] for item in self.cart_items)
        messagebox.showinfo("Checkout", f"Total amount: ${total:.2f}\nThank you for your purchase!")
        self.clear_cart()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = VendingMachineUI(root)
    root.mainloop()