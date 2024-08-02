# API Test
This API manager data in MySQL

setup database:
```bash
CREATE DATABASE IF NOT EXISTS flexisip CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE accounts (
    registerID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    login VARCHAR(20) NOT NULL,
    password VARCHAR(40) NOT NULL,
    phone VARCHAR(20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```


## Test 1: API CRUD accounts
### The code is contained in the file app.py

#### get all
default page size is 10
```bash
curl --location --request GET 'http://127.0.0.1:5000/get_accounts_all' \
--header 'page: 1'
```
or
```bash
curl --location --request GET 'http://127.0.0.1:5000/get_accounts_all'
```


#### get
```bash
curl --location --request GET 'http://127.0.0.1:5000/get_accounts/3'
```

#### create
```bash
curl --location --request POST 'http://127.0.0.1:5000/create_accounts' \
--header 'Content-Type: application/json' \
--data-raw '{
    "login": "nguyen_van_b",
    "password": "nguyanvanb",
    "phone": "035749534"
}'
```

#### update
```bash
curl --location --request POST 'http://127.0.0.1:5000/update_accounts/3' \
--header 'Content-Type: application/json' \
--data-raw '{
    "login": "nguyen_a",
    "password": "nguyenapro",
    "phone": "09000000"
}'
```

#### delete
```bash
curl --location --request DELETE 'http://127.0.0.1:5000/delete_accounts/1'
```

## Test 2: API Show serialpaso
Check file name matches the system, and get content it
### The code is contained in the file app.py

```bash
curl --location --request POST 'http://127.0.0.1:5000/api/showSerialpaso' \
--header 'Content-Type: application/json' \
--data-raw '{
    "file": "index",
    "app_env": 0,
    "contract_app": 0,
    "contract_server": 0
}'
```

## Test 3: Get same files name
get the same file name in two folders, when you provide two path folders

### The code is contained in the file scripts.py