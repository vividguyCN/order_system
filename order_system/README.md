# 订单管理后台

### 安装相关依赖
```
pip install -r requirements.txt
```

### 运行服务
```
python3 main.py
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
        `role` int(11) NOT NULL DEFAULT 2,
         PRIMARY KEY (`uid`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `order_info`(
		`id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
		`userId` int(11) UNSIGNED NOT NULL,
        `dateTime` TIMESTAMP NOT NULL,
		`productType` TINYTEXT NOT NULL,
		`productName` TINYTEXT NOT NULL,
		`productDescription` TINYTEXT,
		`platform` TINYTEXT NOT NULL,
		`note` TINYTEXT,
		`isActive` bit NOT NULL DEFAULT 1,
		PRIMARY KEY (`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `order_money`(
		`id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
		`purchasePrice` int(11) UNSIGNED NOT NULL,
		`soldPrice` int(11) UNSIGNED NOT NULL,
		`postPrice` int(11) UNSIGNED DEFAULT 0,
		`profit` int(11) NOT NULL,
		PRIMARY KEY (`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `order_purchaser`(
		`id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
		`purchaser` TINYTEXT NOT NULL,
		`contact` TINYTEXT,
		PRIMARY KEY (`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `stock_info`(
		`id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
		`userId` int(11) UNSIGNED NOT NULL,
        `dateTime` TIMESTAMP NOT NULL,
		`productType` TINYTEXT NOT NULL,
		`productName` TINYTEXT NOT NULL,
		`productDescription` TINYTEXT,
		`platform` TINYTEXT NOT NULL,
		`note` TINYTEXT,
		`isSold` bit NOT NULL DEFAULT 0,
		PRIMARY KEY (`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `stock_money`(
		`id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
		`price` int(11) UNSIGNED NOT NULL,
		`num` int(11) UNSIGNED NOT NULL,
		`total` int(11) UNSIGNED
		PRIMARY KEY (`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `stock_creator`(
		`id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
		`creator` TINYTEXT NOT NULL,
		`contact` TINYTEXT,
		PRIMARY KEY (`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 配置信息
连接数据库，更改config文件中的测试环境