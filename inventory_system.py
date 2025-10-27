"""
Inventory Management System

This module provides functions to manage inventory items including adding,
removing, loading, saving, and checking stock quantities.
"""
import json
import logging
from datetime import datetime

# Global variable
stock_data = {}

def addItem(item="default", qty=0, logs=None):
    """
    Add an item to the inventory.
    
    Args:
        item: The item name (string)
        qty: The quantity to add (integer)
        logs: Optional list to append log messages
    """
    if logs is None:
        logs = []
    # Validate input types
    if not isinstance(item, str):
        logging.warning("Invalid item type: %s. Item must be a string.",
                        type(item).__name__)
        return
    if not isinstance(qty, int):
        logging.warning("Invalid quantity type: %s. Quantity must be an integer.",
                        type(qty).__name__)
        return
    if not item:
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")

def removeItem(item, qty):
    """
    Remove an item from the inventory.
    
    Args:
        item: The item name (string)
        qty: The quantity to remove (integer)
    """
    # Validate input types
    if not isinstance(item, str):
        logging.warning("Invalid item type: %s. Item must be a string.",
                        type(item).__name__)
        return
    if not isinstance(qty, int):
        logging.warning("Invalid quantity type: %s. Quantity must be an integer.",
                        type(qty).__name__)
        return

    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        logging.warning("Item '%s' not found in inventory.", item)

def getQty(item):
    """
    Get the quantity of an item in the inventory.
    
    Args:
        item: The item name (string)
    
    Returns:
        The quantity of the item (integer), or 0 if not found
    """
    # Validate input type
    if not isinstance(item, str):
        logging.warning("Invalid item type: %s. Item must be a string.",
                        type(item).__name__)
        return 0

    if item not in stock_data:
        logging.warning("Item '%s' not found in inventory.", item)
        return 0
    return stock_data[item]

def loadData(file="inventory.json"):
    """
    Load inventory data from a JSON file.
    
    Args:
        file: The file path to load from (string)
    """
    global stock_data  # pylint: disable=global-statement
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.loads(f.read())
    except FileNotFoundError:
        logging.warning("File '%s' not found. Starting with empty inventory.", file)
        stock_data = {}
    except json.JSONDecodeError:
        logging.error("Invalid JSON in file '%s'. Starting with empty inventory.", file)
        stock_data = {}

def saveData(file="inventory.json"):
    """
    Save inventory data to a JSON file.
    
    Args:
        file: The file path to save to (string)
    """
    try:
        with open(file, "w", encoding="utf-8") as f:
            f.write(json.dumps(stock_data))
    except IOError as e:
        logging.error("Error saving data to file '%s': %s", file, str(e))

def printData():
    """
    Print all items and their quantities in the inventory.
    """
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])

def checkLowItems(threshold=5):
    """
    Check for items with quantity below the specified threshold.
    
    Args:
        threshold: The minimum quantity threshold (integer, default=5)
    
    Returns:
        A list of item names with quantity below the threshold
    """
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result

def main():
    """
    Main function to demonstrate the inventory system functionality.
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    addItem("apple", 10)
    addItem("banana", -2)
    addItem(123, "ten")  # invalid types, now properly validated
    removeItem("apple", 3)
    removeItem("orange", 1)
    print("Apple stock:", getQty("apple"))
    print("Low items:", checkLowItems())
    saveData()
    loadData()
    printData()
    # Removed dangerous eval() usage
    print('eval removed for security')

main()
