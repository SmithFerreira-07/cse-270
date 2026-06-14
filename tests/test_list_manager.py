from list_manager import (initialize_list, get_list, add_to_list, remove_from_list, replace_item_in_list, get_item_at_position)
import pytest

## Ensures the we can get the list
def test_get_list():
    # Arrange
    initialize_list()
    # Act
    result = get_list()
    # Assert
    assert isinstance(result, list), "Variable is not a list"

## Ensures the list is empty at the beginning
def test_initialize_list():
    # Arrange
    initialize_list()
    # Act
    result = get_list()
    # Assert
    assert len(result) == 0, "Length of list was not 0"
    
## Ensures one item only was added to the list
def test_add_to_list():
    # Arrange
    initialize_list()
    add_to_list("12345")
    # Act
    result = get_list()
    # Assert
    assert len(result) == 1, "The list was not 1 item long."
    assert result[0] == "12345", "The list does not have 12345."
    
## Allows you to remove an item from the list 
def test_remove_from_list():
    # Arrange    
    initialize_list()
    add_to_list("12345")
    # Act
    remove_from_list("12345")
    result = get_list()
    # Assert
    assert len(result) == 0, "Item was not removed from the list"  
    
## Tests raising a value error when the item to remove is not found in the list
def test_remove_from_list_missing_value():
    # Arrange    
    initialize_list()
    add_to_list("12345")
    # Act
    # Assert
    with pytest.raises(ValueError):
        remove_from_list("23456")


## Tests replacing an item in the list successfully         
def test_replace_item():
    # Arrange    
    initialize_list()
    add_to_list("12345")
    # Act
    replace_item_in_list("12345", "23456")
    result = get_list()
    # Assert
    assert len(result) == 1, "Result length was not 1"
    assert result[0] == "23456", "Item was not replaced as expected."
    
## Tests raising a value error when the item to replace is not found
def test_replace_item_missing_value():
    # Arrange    
    initialize_list()
    add_to_list("12345")
    # Act
    # Assert
    with pytest.raises(ValueError):
        replace_item_in_list("23456", "34567")

## Tests getting the item at the first position in the list. This is 1-based instead of 0-based
def test_get_item_at_position():
    # Arrange    
    initialize_list()
    add_to_list("12345")
    # Act
    result = get_item_at_position(1)
    # Assert
    assert result == "12345", "Result was not 12345 as expected."
    
## Tests getting the item at a given position in the list. This is 1-based instead of 0-based
def test_get_item_at_position_5():
    # Arrange    
    initialize_list()
    add_to_list("12345")
    add_to_list("23456")
    add_to_list("34567")
    add_to_list("45678")
    add_to_list("56789")
    # Act
    result = get_item_at_position(5)
    # Assert
    assert result == "56789", "Result was not 56789 as expected."

## Tests raising a value error when a bad position is indicated
def test_get_item_at_bad_position():
    # Arrange    
    initialize_list()
    add_to_list("12345")
    add_to_list("23456")
    add_to_list("34567")
    add_to_list("45678")
    add_to_list("56789")
    # Act    
    # Assert
    with pytest.raises(ValueError):
        result = get_item_at_position(-1)
        result = get_item_at_position(0)    
        result = get_item_at_position(6)

if __name__ == '__main__':
    pytest.main([__file__])