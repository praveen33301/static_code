"""
Inventory management system for tracking stock items.

This module provides functions to add, remove, query, and persist inventory data.
"""
import json
from datetime import datetime

# Global variable
stock_data = {}

def add_item(item="default", qty=0, logs=None):
    """
    Add an item to the inventory or increase its quantity.
    
    Args:
        item: The name of the item to add (str or int)
        qty: The quantity to add (int)
        logs: Optional list to append log messages to
        
    Returns:
        None
    """
    if logs is None:
        logs = []
    if not item:
        return
    # Validate types
    if not isinstance(qty, int):
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")

def remove_item(item, qty):
    """
    Remove an item from inventory or decrease its quantity.
    
    Args:
        item: The name of the item to remove
        qty: The quantity to remove (int)
        
    Returns:
        None
    """
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except (KeyError, TypeError):
        pass

def get_qty(item):
    """
    Get the quantity of an item in inventory.
    
    Args:
        item: The name of the item
        
    Returns:
        int: The quantity of the item
    """
    return stock_data[item]

def load_data(file="inventory.json"):
    """
    Load inventory data from a JSON file.
    
    Args:
        file: The path to the JSON file (default: "inventory.json")
        
    Returns:
        None
    """
    global stock_data  # pylint: disable=global-statement
    with open(file, "r", encoding="utf-8") as f:
        stock_data = json.loads(f.read())

def save_data(file="inventory.json"):
    """
    Save inventory data to a JSON file.
    
    Args:
        file: The path to the JSON file (default: "inventory.json")
        
    Returns:
        None
    """
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(stock_data))

def print_data():
    """
    Print a report of all items in inventory.
    
    Returns:
        None
    """
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])

def check_low_items(threshold=5):
    """
    Check for items with quantity below a threshold.
    
    Args:
        threshold: The minimum quantity threshold (default: 5)
        
    Returns:
        list: A list of item names below the threshold
    """
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result

def main():
    """
    Main function to demonstrate inventory system functionality.
    
    Returns:
        None
    """
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")  # invalid types, will be ignored due to validation
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()
    # Removed dangerous eval() usage
    print("Inventory system demo completed")

if __name__ == "__main__":
    main()
