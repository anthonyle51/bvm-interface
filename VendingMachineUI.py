import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class VendingMachineUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vending Machine")
        
        # Set the window size and prevent resizing
        # root.overrideredirect(True)
        self.root.geometry('800x480')
        # self.root.resizable(False, False)

        # Main frame configuration
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(pady=10, fill='both', expand=True)
        
        self.left_header = ttk.Frame(self.main_frame)
        self.left_header.grid(row=0, column=0)

        self.right_header = ttk.Frame(self.main_frame)
        self.right_header.grid(row=0, column=1)

        # Left side frame for products
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.grid(row=1, column=0, sticky='ns')

        # Right side frame for cart or additional info
        self.right_frame = ttk.Frame(self.main_frame, width=400)
        self.right_frame.grid(row=1, column=1, sticky='nsew')

        # Configure column configuration in main_frame for resizing behavior
        self.main_frame.columnconfigure(0, weight=2)  # Let the left frame expand more
        self.main_frame.columnconfigure(1, weight=1)  # Fixed width for the right frame

        # Sample products in the vending machine with images
        self.products = [
            {"id": "A1", "name": "Lithium AA", "price": 5.99, "image_path": "batteries/energizer-lithium-AA.jpg"},
            # {"id": "A2", "name": "Lithium AAA", "price": 6.99, "image_path": "batteries/energizer-lithium-AAA.webp"},
            {"id": "B1", "name": "Alkaline AA", "price": 4.99, "image_path": "batteries/duracell-alkaline-AA.jpg"},
            {"id": "B2", "name": "Alkaline AAA", "price": 4.49, "image_path": "batteries/energizer-alkaline-AAA.jpg"}
        ]

        self.setup_header()
        self.setup_products_panel()

        self.cart_items = []
        self.setup_checkout_panel()

    def setup_header(self):
        ttk.Label(self.left_header, text="PlusMinus", font=('Arial', 16)).pack(pady=20)
        ttk.Label(self.right_header, text="Cart Summary", font=('Arial', 16)).pack(pady=20)

    def setup_products_panel(self):
        self.images = {}
        self.product = ""

        # Creating product display with images
        self.products_frame = tk.LabelFrame(self.left_frame, text="Products")
        self.products_frame.pack(fill='x', expand=True)

        for product in self.products:
            # Container frame for each product
            product_frame = tk.Frame(self.products_frame, bg='white', highlightthickness=2)
            product_frame.pack(padx=5, pady=5, fill='x')

            # self.product = product

            original_image = Image.open(product['image_path'])
            resized_image = original_image.resize((50, 50), Image.LANCZOS) 
            photo = ImageTk.PhotoImage(resized_image)
            self.images[product['id']] = photo 

            # Image label
            image_label = tk.Label(product_frame, image=photo)
            image_label.pack(side='top', padx=10)
            image_label.bind("<Button-1>", lambda event, p=product: self.add_to_cart(event, p))

            # Text label for the name and price, and button for adding to cart
            text = f"{product['name']} - ${product['price']}"
            text_label = tk.Label(product_frame, text=text)
            text_label.pack(side='bottom')
            #text_label.bind("<Button-1>", self.on_product_click) 

            # product_frame.bind("<Button-1>", self.on_product_click) 

            # button = ttk.Button(product_frame, text="Add to Cart", command=lambda p=product: self.add_to_cart(p))
            # button.pack(side='bottom', padx=10)

    def setup_checkout_panel(self):
        ttk.Label(self.right_frame, text="Cart Summary", font=('Arial', 16)).pack(pady=20)
        self.cart_listbox = tk.Listbox(self.right_frame)
        self.cart_listbox.pack(fill='both', expand=True)
        ttk.Button(self.right_frame, text="Clear Cart", command=self.clear_cart).pack(fill='x', pady=5)
        ttk.Button(self.right_frame, text="Checkout", command=self.checkout).pack(fill='x', pady=5)

    def add_to_cart(self, event, product):
        start_color = (173, 216, 230)
        end_color = (255, 255, 255)
        self.fade_border_color(event.widget.master, start_color, end_color, 10)

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

    def fade_border_color(self, frame, start_rgb, end_rgb, steps):
        delta = [(end - start) / steps for start, end in zip(start_rgb, end_rgb)]

        def fade(step):
            new_color = '#%02x%02x%02x' % (
                int(start_rgb[0] + delta[0] * step),
                int(start_rgb[1] + delta[1] * step),
                int(start_rgb[2] + delta[2] * step)
            )
            frame.config(highlightbackground=new_color)

            if step < steps:
                frame.after(20, lambda: fade(step + 1))

        fade(0)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = VendingMachineUI(root)
    root.mainloop()