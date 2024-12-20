class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.addresses = []
        self.shopping_cart = ShoppingCart()
        self.orders_history = []
        self.is_logged_in = False

    def login(self, password):
        if self.password == password:
            self.is_logged_in = True
            print(f"Welcome, {self.username}! You are now logged in.")
        else:
            print("Incorrect password.")

    def logout(self):
        self.is_logged_in = False
        print(f"Goodbye, {self.username}. You are now logged out.")

    def add_address(self, street, city, zip_code):
        address = Address(street, city, zip_code)
        self.addresses.append(address)
        print("Address added.")

    def search_product(self, product_name, products_list):
        results = [product for product in products_list if product_name.lower() in product.name.lower()]
        return results

    def sort_products_by_price(self, products_list):
        return sorted(products_list, key=lambda product: product.price)

    def add_to_shopping_cart(self, product, quantity):
        if not self.is_logged_in:
            print("You must log in to add items to your shopping cart.")
            return

        if product.stock < quantity:
            print(f"Insufficient stock for '{product.name}'. Available: {product.stock}.")
        else:
            self.shopping_cart.add_product(product, quantity)
            product.stock -= quantity

    def view_shopping_cart(self):
        if not self.is_logged_in:
            print("Log in to view your shopping cart.")
        else:
            self.shopping_cart.show_cart()

    def finalize_order(self):
        if not self.is_logged_in:
            print("You need to log in to complete your order.")
            return

        total = self.shopping_cart.calculate_total()
        confirmation = input(f"The total cost is {total}. Would you like to complete the purchase? (yes/no): ")

        if confirmation.lower() == "yes":
            self.orders_history.append(self.shopping_cart.items)
            self.shopping_cart = ShoppingCart()
            print("Your purchase has been completed.")
        else:
            print("Your purchase was canceled.")


class Admin:
    def __init__(self):
        self.products = []

    def add_product(self, name, price, description, stock):
        product = Product(name, price, description, stock)
        self.products.append(product)
        print(f"Product '{name}' added.")

    def delete_product(self, product_name):
        self.products = [product for product in self.products if product.name != product_name]
        print(f"Product '{product_name}' deleted.")

    def update_product(self, product_name, new_name=None, new_price=None, new_description=None, new_stock=None):
        for product in self.products:
            if product.name == product_name:
                if new_name:
                    product.name = new_name
                if new_price:
                    product.price = new_price
                if new_description:
                    product.description = new_description
                if new_stock is not None:
                    product.stock = new_stock
                print(f"Product '{product_name}' updated.")
                return
        print(f"Product '{product_name}' not found.")


class Product:
    def __init__(self, name, price, description, stock):
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock


class Address:
    def __init__(self, street, city, zip_code):
        self.street = street
        self.city = city
        self.zip_code = zip_code


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_product(self, product, quantity):
        self.items.append((product, quantity))
        print(f"Added {quantity} unit(s) of '{product.name}' to your shopping cart.")

    def calculate_total(self):
        total = sum(product.price * quantity for product, quantity in self.items)
        return total

    def show_cart(self):
        print("Items in your shopping cart:")
        for product, quantity in self.items:
            print(f"- {product.name} (Quantity: {quantity}, Unit Price: {product.price})")
        print(f"Total cost: {self.calculate_total()}")


if __name__ == "__main__":
    admin = Admin()
    admin.add_product("Smartphone", 800, "Latest smartphone model.", 10)
    admin.add_product("Headphones", 50, "High-quality headphones.", 20)

    print("\nAvailable products:")
    for product in admin.products:
        print(f"{product.name} - ${product.price} - Stock: {product.stock}")

    user = User("sepideh", "password123")
    user.login("password123")
    user.add_address("Hojrat Street", "Jahrom", "741819")

    results = user.search_product("Smartphone", admin.products)
    print("\nSearch results for 'Smartphone':")
    for product in results:
        print(f"{product.name} - ${product.price} - {product.description}")

    user.add_to_shopping_cart(admin.products[0], 2)
    user.view_shopping_cart()
    user.finalize_order()

    print("\nOrder history:")
    for order in user.orders_history:   
        for product, quantity in order:
            print(f"{product.name} - Quantity: {quantity}")
