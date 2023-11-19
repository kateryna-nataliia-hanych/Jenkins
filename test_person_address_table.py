"""
Contains Data Quality checks for Person.Address table of the AdventureWorks2012 DB on localhost
"""
import pytest
import pymssql

# Database variables
SERVER = '192.168.31.144' # Change this value according to your environment
DATABASE = 'AdventureWorks2012'
USERNAME = 'TestUser' # Change this value according to your environment
PASSWORD = 'password' # Change this value according to your environment


@pytest.fixture()
def db_connection():
    # Connect to the AdventureWorks2012 DB
    connection = pymssql.connect(
        server=SERVER,
        database=DATABASE,
        user=USERNAME,
        password=PASSWORD,
        port=1433,  # Adjust the port if necessary
        charset='UTF-8',  # Adjust the charset if necessary
        autocommit=True
    )

    yield connection
    connection.close()


def test_unique_constraint_on_address(db_connection):
    cursor = db_connection.cursor()

    # Execute a query to fetch duplicate addresses based on unique constraint
    cursor.execute("SELECT [AddressLine1], [AddressLine2], [City], [StateProvinceID], [PostalCode] FROM [Person].["
                   "Address] GROUP BY [AddressLine1], [AddressLine2], [City], [StateProvinceID], [PostalCode] HAVING "
                   "COUNT(*) > 1")
    duplicate_addresses = cursor.fetchall()

    if duplicate_addresses:
        # If combinations of columns [AddressLine1], [AddressLine2], [City], [StateProvinceID], [PostalCode] are
        # duplicated, fail the test
        pytest.fail(f"Duplicate addresses found: {duplicate_addresses}")

    cursor.close()


def test_validate_unique_rowguid(db_connection):
    cursor = db_connection.cursor()

    # Execute the SQL query to check for duplicate rowguid values
    cursor.execute("SELECT [rowguid] FROM [Person].[Address] GROUP BY [rowguid] HAVING count([rowguid]) <> 1")

    duplicate_rows = cursor.fetchall()

    cursor.close()
    # Assert that no records is returned
    assert not duplicate_rows, f"Duplicate rowguid values found: {duplicate_rows}"
