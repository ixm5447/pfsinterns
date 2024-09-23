import json

# Dictionary to store inventory and sales data
inventory = {}
sales = {}

def savedata(): # Saves inventory data to a file
    with open("inventory.json", "w") as file:
        json.dump(inventory, file) # Converts inventory to JSON and saves it
    with open("sales.json", "w") as file:
        json.dump(sales, file) # Converts sales data to JSON and saves it

def loaddata(): # Loads saved inventory and sales data
    global inventory, sales
    try:
        with open("inventory.json", "r") as file:
            inventory = json.load(file) # Loads inventory from JSON
    except (FileNotFoundError, json.JSONDecodeError):
        inventory = {}

    try:
        with open("sales.json", "r") as file:
            sales = json.load(file) # Loads sales data from JSON
    except (FileNotFoundError, json.JSONDecodeError):
        sales = {}

# Dictionary of text colors
colors = {
    "black": '\033[30m',
    "red": '\033[31m',
    "green": '\033[32m',
    "orange": '\033[33m',
    "blue": '\033[34m',
    "reset colors": '\033[1;m'
}

clear = '\x1b[2J\x1b[H' # Clear output variable

# Menu options for user to choose from  
def menu_options():
    print("Menu: ")
    print("    View inventory [1]")
    print("    Add new product [2]")
    print("    Update product quantity [3]")
    print("    Delete product [4]")
    print("    Make a sale [5]")
    print("    View sales report [6]")
    print("    Quit [7]")

print(colors["blue"] + "Welcome to the Inventory Management System.")  

# Main function with while loop
loaddata() # Load data at the start

while True:
    print(colors["blue"]) 
    menu_options()
    
    try:
        main_q = int(input("\nPlease input a selection: "))

        if main_q == 1: # View inventory
            print(clear) # Clears previous output
            print(colors["green"]) # Green color for inventory

            print("Inventory: ")
            for product, details in inventory.items():
                quantity = details['quantity']
                price = details['price']
                print(f"{colors['green']}{product}: {colors['blue']}Quantity: {quantity}, Price: ${price:.2f}")
     
        elif main_q == 2: # Add a new product
            try:
                print(colors["green"])
                print(clear)
                
                product_name = input("Enter the product name: ")
                product_quantity = int(input("Enter the quantity: "))
                product_price = float(input("Enter the price per unit: "))
                
                inventory[product_name] = {"quantity": product_quantity, "price": product_price}
                savedata()
            except:
                print(colors["red"] + "One or more of your inputs are invalid.")
                
        elif main_q == 3: # Update product quantity
            try:
                print(clear)
                print(colors["green"])
                
                product_name = input("Which product do you want to update?: ")
                if product_name in inventory:
                    new_quantity = int(input(f"Enter the new quantity for {product_name}: "))
                    inventory[product_name]["quantity"] = new_quantity
                    savedata()
                    print(f"{product_name}'s quantity updated to {new_quantity}.")
                else:
                    print(colors["red"] + "Product not found.")
            except:
                print(colors["red"] + "Invalid input.")
                
        elif main_q == 4: # Delete a product
            try:
                print(clear)
                print(colors["green"])
                
                product_remove = input("Which product do you want to delete?: ")
                if product_remove in inventory:
                    inventory.pop(product_remove) # Removes product from inventory
                    print(f"{product_remove} has been removed from the inventory.")
                    savedata()
                else:
                    print(colors["red"] + "Product not found.")
            except:
                print(colors["red"] + "Invalid input.")
                
        elif main_q == 5: # Make a sale
            try:
                print(clear)
                print(colors["green"])

                product_name = input("What is the product sold?: ") 
                if product_name in inventory:
                    sale_quantity = int(input(f"How many {product_name}(s) were sold?: "))
                    if sale_quantity <= inventory[product_name]["quantity"]:
                        inventory[product_name]["quantity"] -= sale_quantity

                        sale_amount = sale_quantity * inventory[product_name]["price"]
                        if product_name in sales:
                            sales[product_name] += sale_amount
                        else:
                            sales[product_name] = sale_amount

                        savedata()
                        print(f"Sale recorded: {sale_quantity} {product_name}(s) sold for ${sale_amount:.2f}.")
                    else:
                        print(colors["red"] + "Not enough stock.")
                else:
                    print(colors["red"] + "Product not found.")
            except:
                print(colors["red"] + "Invalid input.")
                
        elif main_q == 6: # View sales report
            print(clear)
            print(colors["green"])

            print("Sales Report: ")
            for product, total_sales in sales.items():
                print(f"{colors['green']}{product}: {colors['blue']}Total sales: ${total_sales:.2f}")
                
        elif main_q == 7: # Quit the program
            print(clear)
            print(colors["green"])
            print("Thank you for using the Inventory Management System.")
            break
    except:
        print(colors["red"])
        print("Please input a valid selection.")
