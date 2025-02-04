from  models import *

class Products():

    def all_products(self):
        all_products = Manufacturer.objects.all()
        return products
    
    def purchase(self, product, quantity):
        product = Manufacturer.objects.get(item=product)
        product.quantity -= quantity
        product.save()
    

if __name__ == "__main__":
    print("""
    
    1 - List All Products
    2 - Purchase Product
    

    """)

    Product = Products()
    products = Product.all_products()
    choice = int(input(">:"))
    if choice == 1:
        for product in products:
            print("{}, Quantity Left : {}".format(product.item, product.quantity))
    
    elif choice == 2:
        item = input("> Item:")
        quantity = int(input("> Quantity: "))
        Product.purchase(item, quantity)
        print("You purchased {} from {}".format(item, quantity))


