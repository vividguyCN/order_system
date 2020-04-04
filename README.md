<<<<<<< HEAD
# order_system

run login.py
=======
# 订单管理后台

### 安装相关依赖
```
pip install -r requirements.txt
```

### 运行服务
```
python3 runserver.py
```

### 访问API
```
/apidocs
```

### 创建数据表
```
CREATE TABLE `login` (
        `uid` int(11) unsigned NOT NULL AUTO_INCREMENT,
        `username` tinytext NOT NULL,
        `password` tinytext NOT NULL,
        `email` tinytext,
	    `isActive` bit NOT NULL DEFAULT 1,
         PRIMARY KEY (`uid`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `info`(
		`id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
		`userId` int(11) UNSIGNED NOT NULL,
        `dateTime` TIMESTAMP NOT NULL,
		`productType` TINYTEXT NOT NULL,
		`productName` TINYTEXT NOT NULL,
		`productDescription` TINYTEXT,
		`withAccessories` bit NOT NULL DEFAULT 0,
        `accessories` TINYTEXT,
		`platform` TINYTEXT NOT NULL,
		`note` TINYTEXT,
		`isActive` bit NOT NULL DEFAULT 1,
		PRIMARY KEY (`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `money`(
		`id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
		`purchasePrice` int(11) UNSIGNED NOT NULL,
		`soldPrice` int(11) UNSIGNED NOT NULL,
		`postPrice` int(11) UNSIGNED DEFAULT 0,
		`profit` int(11) NOT NULL,
		PRIMARY KEY (`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `purchaser`(
		`id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
		`purchaser` TINYTEXT NOT NULL,
		`contact` TINYTEXT,
		PRIMARY KEY (`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 配置信息
连接数据库，更改config文件中的以下属性
```
HOSTNAME
PORT
DATABASE
USERNAME
PASSWORD
```
>>>>>>> dev
