import pytest

from examples import (
    find_and_replace,
    get_random_item,
    gather_input,
    get_data_from_file,
    get_user_id_1,
    some_list
)

## test for a function with side-effects (like modifying a list)
def test_find_and_replace():
    mylist = ['apples','oranges']
    find_and_replace(mylist, 'apples', 'bananas')    
    assert mylist[0] == 'bananas'

## test for a raised exception
def test_find_and_replace_error():
    mylist = ['apples','oranges']
    with pytest.raises(ValueError):
        find_and_replace(mylist, 'bananas', 'pears')

## test for a choice that falls within the list "some_list" from the example
def test_get_random_item_no_mock():
    choice = get_random_item()
    assert choice in some_list

# Test for get_random_item function
def test_get_random_item(mocker):
    # Patch the random.choice method with a specific return value "alpha"
    mock_choice = mocker.patch("random.choice",return_value="alpha")
    
    # assert that the choice returned is "alpha"
    assert get_random_item() == 'alpha'
    
    # assert that the choice method was called once
    mock_choice.assert_called_once()
    
# Test for gather_input function
def test_gather_input(mocker):
    # Mock the input function
    mock_input = mocker.patch("builtins.input", return_value="Test input")

    # Call the function under test
    result = gather_input("Enter input: ")

    # Assert the result
    assert result == "Test input"

    # Assert that the input function was called with the correct prompt
    mock_input.assert_called_once_with("Enter input: ")

# Tests getting data from a file creating a temp file for testing
def test_get_data_from_file(tmp_path):
    # Create a temporary file with test data
    test_data = "file contents"
    file_path = tmp_path / "test.txt"
    with open(file_path, "w") as f:
        f.write(test_data)

    # Call the function under test
    result = get_data_from_file(file_path)

    # Assert the result
    assert result == test_data    

# Test for get_data_from_file function
def test_get_data_from_file(mocker):
    # Mock the open function
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="file contents"))

    # Call the function under test
    result = get_data_from_file("test.txt")

    # Assert the result
    assert result == "file contents"

    # Assert that the open function was called with the correct filename
    mock_open.assert_called_once_with("test.txt")

# Set up a mock object for the database connection
@pytest.fixture
def mock_psycopg2_connect(mocker):
    # Patch the psycopg2.connect method
    mock_connect = mocker.patch('psycopg2.connect')
    
    # Return the mock object
    return mock_connect

# Test for get_user_id_1 function
def test_get_user_id_1(mock_psycopg2_connect):
    # Get a mocked version of the connection for later
    mock_connect = mock_psycopg2_connect.return_value
    
    # Mock the cursor and its methods
    mock_cursor = mock_psycopg2_connect.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = 'test_user'

    # Call the function under test
    user = get_user_id_1()

    # Assert the result
    assert user == 'test_user'

    # Assert the database connection and cursor were called as expected
    mock_psycopg2_connect.assert_called_once_with(
        dbname="mydb",
        user="username",
        password="password",
        host="127.0.0.1",
        port="5432"
    )
    
    #Asset that each of the functions below were called once as expected
    mock_cursor.execute.assert_called_once_with("SELECT * FROM USERS WHERE ID=1")    
    mock_cursor.close.assert_called_once()
    mock_connect.commit.assert_called_once()
    mock_connect.close.assert_called_once()
    
# In this test, you would call the function, then inspect the data at row 1.
# When connecting to the test database, you might have already set the expected data previously.
# Better would be to set the test data yourself, then check for it.
def test_get_user_id_1_nomock():
    pass