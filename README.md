# order_system

### Setup
```
pip install -r requirements.txt
```

### Runserver
```
python3 login.py
```

### visit API
```
/apidocs
```

### create table 
```
CREATE TABLE `login` (
    `uid` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `username` tinytext,
    `password` tinytext,
    `email` tinytext,
    PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

```

### config 
change attributes in config.py
```
HOSTNAME
PORT
DATABASE
USERNAME
PASSWORD
```