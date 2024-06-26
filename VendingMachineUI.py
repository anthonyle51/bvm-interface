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
        self.dark_color = '#5c7068'
        self.neutral_color = '#c3d4cd'

        # Main frame configuration
        self.main_frame = tk.Frame(root, highlightbackground=self.dark_color, highlightthickness=2)
        self.main_frame.pack_propagate(0)
        self.main_frame.pack(fill='both', expand=True)

        
        self.left_header = tk.Frame(self.main_frame, bg='#90ee90', width=450, height=80)
        self.left_header.pack_propagate(0)
        self.left_header.grid(row=0, column=0, sticky='nesw')


        self.right_header = tk.Frame(self.main_frame, bg=self.dark_color, width=325)
        self.right_header.pack_propagate(0)
        self.right_header.grid(row=0, column=2, sticky='nesw')

        # Left side frame for products
        self.left_frame = tk.Frame(self.main_frame, width=450, bg='blue')
        self.left_frame.pack_propagate(0)
        self.left_frame.grid(row=1, column=0, columnspan=1, sticky='nesw')

        # Right side frame for cart or additional info
        self.right_frame = tk.Frame(self.main_frame, bg='lime', width=325, height=400)
        self.right_frame.pack_propagate(0)
        self.right_frame.grid(row=1, column=2, columnspan=1, sticky='nsew')

        self.divider_frame = tk.Frame(self.main_frame, bg=self.dark_color, width=2)
        self.divider_frame.pack_propagate(0)
        self.divider_frame.grid(row=0, column=1, rowspan=2, columnspan=1, sticky='nsew')

        # Configure column configuration in main_frame for resizing behavior
        self.main_frame.columnconfigure(0, weight=18)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=13) 

        self.main_frame.rowconfigure(0, weight=1)  
        self.main_frame.rowconfigure(1, weight=5) 

        self.alkaline_inserted = 0
        self.lithium_inserted = 0
        self.alkaline_discount = 0
        self.lithium_dicount = 0

        self.subtotal = 0

        self.products = {
            "A1":{"id": "A1", "name": "Duracell CR2032", "price": 2.45, "image_path": "batteries/duracell_cr2032.png"},
            "A2":{"id": "A2", "name": "Hi-Watt CR2032", "price": 2.45, "image_path": "batteries/hiwatt_cr2032.png"},
            "A3":{"id": "A3", "name": "Toshiba CR2032", "price": 2.45, "image_path": "batteries/toshiba_cr2032.jpg"},
            "B1":{"id": "B1", "name": "Energizer Alkaline-AA", "price": 1.25, "image_path": "batteries/energizer-alkaline-AA.jpg"},
            "B2":{"id": "B2", "name": "Diehard Alkaline-AA", "price": 1.25, "image_path": "batteries/diehard_alkaline_AA.jpg"},
            "B3":{"id": "B3", "name": "Duracell Alkaline-AA", "price": 1.25, "image_path": "batteries/duracell-alkaline-AA.jpg"},
            "C1":{"id": "C1", "name": "Energizer Lithium-AA", "price": 2.95, "image_path": "batteries/energizer-lithium-AA.jpg"},
            "C2":{"id": "C2", "name": "EBL Lithium-AA", "price": 2.95, "image_path": "batteries/ebl_li_AA.jpg"},
            "C3":{"id": "C3", "name": "Duracell Lithium-AA", "price": 2.95, "image_path": "batteries/duracell_li_AA.png"}
        }

        self.products_keys = [key for key in self.products]

        self.setup_header()
        self.setup_products_panel()

        self.cart_items = {}
        self.cart_images = {}
        self.checkout_image= None
        self.clear_cart_image= None
        self.x_image = None

        self.setup_checkout_panel()

    def setup_header(self):
        tk.Label(self.left_header, text="PlusMinus", font=('Arial', 16), bg='#90ee90').pack(pady=20)
        tk.Label(self.right_header, text="Your Cart", font=('Arial', 16), bg=self.dark_color, fg='white').pack(pady=20)

    def setup_products_panel(self):
        self.images = {}
        self.product = ""

        # Creating product display with images
        self.products_frame = tk.Frame(self.left_frame, background='#ededed')
        self.products_frame.pack_propagate(0)
        self.products_frame.pack(fill='both', expand=True)

        #self.products_frame.grid(row=0, column=0, sticky='nsew')

        count = 0
        for i in range(3):
            for j in range(3):
                if count < len(self.products):
                    product = self.products[self.products_keys[count]]
                    # Container frame for each product
                    product_frame = tk.Frame(self.products_frame, background='white', highlightbackground='white', highlightthickness=2)
                    product_frame.grid(row=i, column=j, sticky='ew')

                    original_image = Image.open(product['image_path'])
                    resized_image = original_image.resize((111, 111), Image.LANCZOS) 
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

    def setup_checkout_panel(self):
        self.right_frame.rowconfigure(0, weight=3)  
        self.right_frame.rowconfigure(1, weight=2) 
        self.right_frame.columnconfigure(0, weight=1)

        self.parent_cart = tk.Frame(self.right_frame, bg='white', height=240, highlightthickness=2, highlightbackground=self.dark_color)
        self.parent_cart.pack_propagate(0)
        self.parent_cart.grid(row=0, sticky='nesw')

        self.cart_canvas = tk.Canvas(self.parent_cart, width=25, bg ='white')
        #self.cart_canvas.pack_propagate(0)
        self.cart_scrollbar = tk.Scrollbar(self.parent_cart, bg='white', orient='vertical', command=self.cart_canvas.yview)


        self.cart_canvas.pack(side="left", fill="both", expand=True)
        self.cart_scrollbar.pack(side="right", fill="y")


        self.scrollable_frame = tk.Frame(self.cart_canvas, bg='white')
        self.scrollable_frame.pack(side='top', fill='x', expand=True)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.cart_canvas.configure(
                scrollregion=self.cart_canvas.bbox("all")
            )
        )

        self.cart_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")
        self.cart_canvas.configure(yscrollcommand=self.cart_scrollbar.set)

        # self.add_button = tk.Button(self.scrollable_frame, text="Add Frame", width=30, command=self.add_frame)
        # self.add_button.pack(side='top', fill='x', expand=True)

        self.cart_canvas.bind("<ButtonPress-1>", self.start_scroll)
        self.cart_canvas.bind("<B1-Motion>", self.do_scroll)

        self.orig_x = 0

        self.update_checkout_frame()

    def update_checkout_frame(self):
        self.checkout_frame = tk.Frame(self.right_frame, bg=self.neutral_color, height=160)
        self.checkout_frame.pack_propagate(0)
        self.checkout_frame.grid(row=1, sticky='nsew')
        print("Checkout Frame Subtotal: ", self.subtotal)

        bufferRow1 = tk.Label(self.checkout_frame, text=" ", background=self.neutral_color)
        bufferRow1.grid(row=0)
        bufferRow2 = tk.Label(self.checkout_frame, text=" ", background=self.neutral_color)
        bufferRow2.grid(row=1)

        self.buffer_frame = tk.Frame(self.checkout_frame, bg=self.dark_color, height=25)
        self.buffer_frame.pack(side='top', fill='x', expand=False)

        subtotal = f"Subtotal: ${self.subtotal:.2f}"
        subtotal_label = tk.Label(self.checkout_frame, text=subtotal, background=self.neutral_color)
        subtotal_label.grid(row=2)

        lithium_inserted_text = f"Lithium Inserted: {self.lithium_inserted}"
        lithium_inserted_label = tk.Label(self.checkout_frame, text=lithium_inserted_text, background=self.neutral_color)
        lithium_inserted_label.grid(row=3)

        alkaline_inserted_text = f"Alkaline Inserted: {self.alkaline_inserted}"
        alkaline_inserted_label = tk.Label(self.checkout_frame, text=alkaline_inserted_text, background=self.neutral_color)
        alkaline_inserted_label.grid(row=4)

        discount_text = f"Discount: ${self.alkaline_discount * self.alkaline_inserted + self.lithium_dicount * self.lithium_inserted}"
        discount_label = tk.Label(self.checkout_frame, text=discount_text, background=self.neutral_color)
        discount_label.grid(row=5)

        total = f"Total: ${self.subtotal - (self.alkaline_discount * self.alkaline_inserted + self.lithium_dicount * self.lithium_inserted):.2f}"
        total_label = tk.Label(self.checkout_frame, text=total, background=self.neutral_color)
        total_label.grid(row=6)

        checkout_icon = Image.open("assets/checkout.png")
        resized_icon = checkout_icon.resize((130, 45), Image.LANCZOS)
        checkout_photo = ImageTk.PhotoImage(resized_icon)
        self.checkout_image = checkout_photo 

        clear_cart_icon = Image.open("assets/clear-cart.png")
        resized_clear_cart = clear_cart_icon.resize((130, 45), Image.LANCZOS) 
        clear_cart_photo = ImageTk.PhotoImage(resized_clear_cart)
        self.clear_cart_image = clear_cart_photo 

        checkout_button_frame = tk.Frame(self.checkout_frame, bg=self.neutral_color)
        checkout_button_frame.pack(side='right', padx=5, expand=False)

        # Image label

        image_cc_label = tk.Label(checkout_button_frame, image=clear_cart_photo, bg=self.neutral_color)
        image_cc_label.grid(row=0, column=0)

        bufferRow = tk.Label(checkout_button_frame, text=" ", background=self.neutral_color)
        bufferRow.grid(row=1, column=0)
        
        image_label = tk.Label(checkout_button_frame, image=checkout_photo, bg=self.neutral_color)
        image_label.grid(row=2, column=0)
        
        
        bufferCol = tk.Label(checkout_button_frame, text=" ", background=self.neutral_color)
        bufferCol.grid(row=0, column=1)

        image_label.bind("<Button-1>", lambda event, self=self: self.checkout())
        image_cc_label.bind("<Button-1>", lambda event, self=self: self.clear_cart())
        

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
            self.subtotal += product['price']
        else:
            self.cart_items[product['id']] += 1
            self.subtotal += product['price']
            
        self.update_cart_view()
        self.update_checkout_frame()
        print("Subtotal:", self.subtotal)

    def update_cart_view(self):
        self.clear_frame(self.scrollable_frame)
        x_image = Image.open('assets/x.png')
        x_resized_image = x_image.resize((25, 25), Image.LANCZOS) 
        x_image_photo = ImageTk.PhotoImage(x_resized_image)
        self.x_image = x_image_photo
    
        for item in self.cart_items:
            # frame = tk.Frame(self.scrollable_frame, width=50, highlightbackground='green', highlightthickness=2)
            # frame.pack(side='top', pady=2, fill="x", expand=True)

            # product = self.products[item]
                        
            # original_image = Image.open(product['image_path'])
            # resized_image = original_image.resize((50, 50), Image.LANCZOS) 
            # photo = ImageTk.PhotoImage(resized_image)
            # self.cart_images[product['id']] = photo 

            # # Image label
            # image_label = tk.Label(frame, image=photo, bg='white')
            # image_label.pack(side='left', padx=10)


            # # Text label for the name and price, and button for adding to cart
            # text = f"{product['name']} - ${product['price'] * self.cart_items[item]:.2f}"
            # text_label = tk.Label(frame, text=text, background='white')
            # text_label.pack(side='left')

            frame = tk.Frame(self.scrollable_frame, width=50, background='white', highlightthickness=2, highlightbackground='black')
            frame.pack(side='top', pady=2, fill="x", expand=True)
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)

            product = self.products[item]
                        
            original_image = Image.open(product['image_path'])
            resized_image = original_image.resize((50, 50), Image.LANCZOS) 
            photo = ImageTk.PhotoImage(resized_image)
            self.cart_images[product['id']] = photo 

            # Image label
            image_label = tk.Label(frame, image=photo, background='white')
            image_label.grid(column=0, row=0)

            info_frame = tk.Frame(frame, bg='white')
            info_frame.grid(column=1, row=0)

            # Text label for the name and price, and button for adding to cart
            name_text = f"{product['name']}"
            name_label = tk.Label(info_frame, text=name_text, background='white')
            name_label.grid(row=0, column=0)


            quantity_frame = tk.Frame(info_frame, bg='white')
            quantity_frame.grid(row=1, column=0)

            quantity_frame.columnconfigure(0, weight=1)
            quantity_frame.columnconfigure(1, weight=2)
            quantity_frame.columnconfigure(2, weight=1)

            qty_text = f"QTY: {self.cart_items[item]}"
            qty__label = tk.Label(quantity_frame, text=qty_text, background='black', fg='white')
            qty__label.grid(column=0, row=0)

            margin_frame = tk.Frame(quantity_frame)
            margin_frame.grid(column=1, row=0)

            price_text = f"${product['price'] * self.cart_items[item]:.2f}"
            price_label = tk.Label(quantity_frame, text=price_text, background='white', highlightthickness=1, highlightbackground='black')
            price_label.grid(column=2, row=0)

            # x_image = Image.open('assets/x.png')
            # x_resized_image = x_image.resize((50, 50), Image.LANCZOS) 
            # x_image_photo = ImageTk.PhotoImage(x_resized_image)
            # self.x_image = x_image_photo

            x_image_label = tk.Label(frame, image=self.x_image, background='white', width=40)
            x_image_label.grid(column=2, row=0)
            x_image_label.bind("<Button-1>", lambda event, p=product: self.remove_from_cart(event, p))

    def remove_from_cart(self, event, product):
        self.cart_items.pop(product['id'])
        self.update_cart_view()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def clear_cart(self):
        self.cart_items.clear()
        self.alkaline_inserted = 0
        self.lithium_inserted = 0
        self.alkaline_discount = 0
        self.lithium_dicount = 0

        self.subtotal = 0
        self.update_cart_view()
        self.update_checkout_frame()


    def checkout(self):
        if not self.cart_items:
            messagebox.showinfo("Checkout", "Your cart is empty.")
            return
        total = sum(self.products[item]['price'] for item in self.cart_items)
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