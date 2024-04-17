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
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill='both', expand=True)

        
        self.left_header = tk.Frame(self.main_frame, bg='#90ee90')
        self.left_header.pack_propagate(0)
        self.left_header.grid(row=0, column=0, sticky='nsew')


        self.right_header = tk.Frame(self.main_frame, bg='white')
        self.right_header.pack_propagate(0)
        self.right_header.grid(row=0, column=2, sticky='nsew')

        # Left side frame for products
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack_propagate(0)
        self.left_frame.grid(row=1, column=0, columnspan=1, sticky='nsew')

        # Right side frame for cart or additional info
        self.right_frame = tk.Frame(self.main_frame, bg='white')
        self.right_frame.pack_propagate(0)
        self.right_frame.grid(row=1, column=2, columnspan=1, sticky='nsew')

        self.divider_frame = tk.Frame(self.main_frame, bg='#001a01')
        self.divider_frame.pack_propagate(0)
        self.divider_frame.grid(row=0, column=1, rowspan=2, columnspan=1, sticky='nsew')

        # Configure column configuration in main_frame for resizing behavior
        self.main_frame.columnconfigure(0, weight=15)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=9) 

        self.main_frame.rowconfigure(0, weight=1)  
        self.main_frame.rowconfigure(1, weight=5) 

        self.products = {
            "A1":{"id": "A1", "name": "Engergizer Lithium AA", "price": 5.99, "image_path": "batteries/energizer-lithium-AA.jpg"},
            # {"id": "A2", "name": "Lithium AAA", "price": 6.99, "image_path": "batteries/energizer-lithium-AAA.webp"},
            "B1":{"id": "B1", "name": "Duracell Alkaline AA", "price": 4.99, "image_path": "batteries/duracell-alkaline-AA.jpg"},
            "B2":{"id": "B2", "name": "Alkaline AAA", "price": 4.49, "image_path": "batteries/energizer-alkaline-AAA.jpg"},

            "C1":{"id": "C1", "name": "Lithium AA", "price": 5.99, "image_path": "batteries/energizer-lithium-AA.jpg"},
            "C2":{"id": "C2", "name": "Alkaline AA", "price": 4.99, "image_path": "batteries/duracell-alkaline-AA.jpg"},
            "C3":{"id": "C3", "name": "Alkaline AAA", "price": 4.49, "image_path": "batteries/energizer-alkaline-AAA.jpg"},
            "C4":{"id": "C4", "name": "Lithium AA", "price": 5.99, "image_path": "batteries/energizer-lithium-AA.jpg"},
            "C5":{"id": "C5", "name": "Alkaline AA", "price": 4.99, "image_path": "batteries/duracell-alkaline-AA.jpg"},
            "C6":{"id": "C6", "name": "Alkaline AAA", "price": 4.49, "image_path": "batteries/energizer-alkaline-AAA.jpg"}
        }

        self.products_keys = [key for key in self.products]

        self.setup_header()
        self.setup_products_panel()

        self.cart_items = {}
        self.cart_images = {}
        self.setup_checkout_panel()

    def setup_header(self):
        tk.Label(self.left_header, text="PlusMinus", font=('Arial', 16), bg='#90ee90').pack(pady=20)
        tk.Label(self.right_header, text="Cart Summary", font=('Arial', 16), bg='white').pack(pady=20)

    def setup_products_panel(self):
        self.images = {}
        self.product = ""

        # Creating product display with images
        self.products_frame = tk.Frame(self.left_frame, background='#ededed')
        self.products_frame.pack(fill='both', expand=True)

        #self.products_frame.grid(row=0, column=0, sticky='nsew')

        count = 0
        for i in range(3):
            for j in range(3):
                if count < len(self.products):
                    print(self.products_keys)
                    print(self.products_keys[count])
                    product = self.products[self.products_keys[count]]
                    # Container frame for each product
                    product_frame = tk.Frame(self.products_frame, background='white', highlightbackground='blue', highlightthickness=2)
                    product_frame.grid(row=i, column=j, sticky='ew')

                    original_image = Image.open(product['image_path'])
                    resized_image = original_image.resize((125, 125), Image.LANCZOS) 
                    photo = ImageTk.PhotoImage(resized_image)
                    self.images[product['id']] = photo 

                    # Image label
                    image_label = tk.Label(product_frame, image=photo, bg='white')
                    image_label.pack(side='top', padx=10)
                    image_label.bind("<Button-1>", lambda event, p=product: self.add_to_cart(event, p))

                    # Text label for the name and price, and button for adding to cart
                    text = f"{product['name']} - ${product['price']}"
                    text_label = tk.Label(product_frame, text=text, background='white')
                    text_label.pack(side='bottom')

                    count += 1
                
        # for product_dict in self.products:
        #     product = self.products[product_dict]
        #     # Container frame for each product
        #     product_frame = tk.Frame(self.products_frame, background='white', highlightbackground='blue', highlightthickness=2)
        #     product_frame.pack(padx=5, pady=5)

        #     original_image = Image.open(product['image_path'])
        #     resized_image = original_image.resize((100, 100), Image.LANCZOS) 
        #     photo = ImageTk.PhotoImage(resized_image)
        #     self.images[product['id']] = photo 

        #     # Image label
        #     image_label = tk.Label(product_frame, image=photo, bg='white')
        #     image_label.pack(side='top', padx=10)
        #     image_label.bind("<Button-1>", lambda event, p=product: self.add_to_cart(event, p))

        #     # Text label for the name and price, and button for adding to cart
        #     text = f"{product['name']} - ${product['price']}"
        #     text_label = tk.Label(product_frame, text=text, background='white')
        #     text_label.pack(side='bottom')

    def setup_checkout_panel(self):
        # self.cart_listbox = tk.Listbox(self.right_frame, bg='white', borderwidth=0)
        # self.cart_listbox.pack(fill='both', expand=True)
        # tk.Button(self.right_frame, text="Clear Cart", bg='white', command=self.clear_cart).pack(fill='x', pady=5)
        # tk.Button(self.right_frame, text="Checkout", bg='white', command=self.checkout).pack(fill='x', pady=5)

        self.cart_canvas = tk.Canvas(self.right_frame, width=25, bg ='purple', highlightbackground='blue', highlightthickness=2)
        self.cart_canvas.pack_propagate(0)
        self.cart_scrollbar = tk.Scrollbar(self.right_frame, bg='yellow', orient='vertical', command=self.cart_canvas.yview)
        self.scrollable_frame = tk.Frame(self.cart_canvas, bg='pink', highlightbackground='red', highlightthickness=2)

        self.scrollable_frame.pack(side='top', fill='both', expand='True')

        # self.scrollable_frame.grid(row=0, column=0, columnspan= 1, rowspan=1, sticky='nsew')

        # self.canvas_frame = self.canvas.create_window((0,0),
        #     window=self.mailbox_frame, anchor = NW)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.cart_canvas.configure(
                scrollregion=self.cart_canvas.bbox("all")
            )
        )

        # self.cart_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        # self.cart_canvas.configure(yscrollcommand=self.cart_scrollbar.set)

        self.cart_canvas.pack(side="left", fill="both", expand=True)
        self.cart_scrollbar.pack(side="right", fill="y")

        self.add_button = tk.Button(self.scrollable_frame, text="Add Frame", width=30, command=self.add_frame)
        self.add_button.pack(side='top', fill='x', expand=True)

        self.cart_canvas.bind("<ButtonPress-1>", self.start_scroll)
        self.cart_canvas.bind("<B1-Motion>", self.do_scroll)

        self.orig_x = 0

    def start_scroll(self, event):
        self.orig_x = event.x
        self.cart_canvas.scan_mark(event.x, event.y)

    def do_scroll(self, event):
        self.cart_canvas.scan_dragto(self.orig_x, event.y, gain=1)

    def add_frame(self):
        frame = tk.Frame(self.scrollable_frame, relief=tk.RAISED, borderwidth=1, highlightbackground='green', highlightthickness=2)
        frame.pack(pady=10, fill="x", expand=True)

        remove_button = ttk.Button(frame, text="Remove Frame", command=lambda: self.remove_frame(frame))
        remove_button.pack()

        text = "testing"
        text_label = tk.Label(frame, text=text, background='white')
        text_label.pack()

        for item in self.cart_items:
            text2 = "testing"
            text2_label = tk.Label(frame, text=text2, background='white')
            text2_label.pack()
            product = self.products[item]
                        
            original_image = Image.open(product['image_path'])
            resized_image = original_image.resize((50, 50), Image.LANCZOS) 
            photo = ImageTk.PhotoImage(resized_image)
            self.cart_images[product['id']] = photo 

            # Image label
            image_label = tk.Label(frame, image=photo, bg='white')
            image_label.pack(side='left', padx=10)

            # Text label for the name and price, and button for adding to cart
            text1 = f"{product['name']} - ${product['price'] * self.cart_items[item]}"
            text1_label = tk.Label(frame, text=text1, background='white')
            text1_label.pack()
    # def add_product_to_cart(self.scrollable_frame, ):
    #     frame = tk.Frame(s)

    def remove_frame(self, frame):
        frame.destroy()

    def add_to_cart(self, event, product):
        start_color = (173, 216, 230)
        end_color = (255, 255, 255)
        self.fade_border_color(event.widget.master, start_color, end_color, 10)

        if product['id'] not in self.cart_items:
            self.cart_items[product['id']] = 1
        else:
            self.cart_items[product['id']] += 1
            
        self.update_cart_view()
        print(self.cart_items)

    def update_cart_view(self):
        self.clear_frame(self.scrollable_frame)

    
        for item in self.cart_items:
            frame = tk.Frame(self.scrollable_frame, width=50, highlightbackground='green', highlightthickness=2)
            frame.pack(side='top', pady=2, fill="x", expand=True)
            product = self.products[item]
                        
            original_image = Image.open(product['image_path'])
            resized_image = original_image.resize((25, 25), Image.LANCZOS) 
            photo = ImageTk.PhotoImage(resized_image)
            self.cart_images[product['id']] = photo 

            # Image label
            image_label = tk.Label(frame, image=photo, bg='white')
            image_label.pack(side='left', padx=10)
            image_label.bind("<Button-1>", lambda event, p=product: self.add_to_cart(event, p))

            # Text label for the name and price, and button for adding to cart
            text = f"{product['name']} - ${product['price'] * self.cart_items[item]}"
            text_label = tk.Label(frame, text=text, background='white')
            text_label.pack(side='left')



    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

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