HOST = '127.0.0.1'
PORT = 5000

# default page size of accounts
PAGE_SIZE = 10

config_mysql = {
	"host": "127.0.0.1",
	"port": 3306,
	"db": "flexisip",
	"username": "root",
	"password": "1234"
}

config_query = {
	"create_accounts": "INSERT INTO accounts(login, password, phone) values('{}', '{}', '{}');",
	"get_accounts": "SELECT * FROM accounts WHERE registerID = {}",
	"get_all_accounts": "SELECT * FROM accounts;",
	"get_accounts_with_page": "SELECT * FROM accounts LIMIT {} OFFSET {};",
	"update_accounts": "UPDATE accounts SET {} WHERE registerID = {};",
	"delete_accounts": "DELETE FROM accounts WHERE registerID = {};",
}