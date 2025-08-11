# IP2Location IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE-AREACODE-ELEVATION [DB21] Sample Database and Codes

Web Site  : https://www.ip2location.com
Email     : support@ip2location.com

© Copyright IP2Location.com. All Rights Reserved.



## Introduction

Welcome to IP2Location.com. This package consists of sample data and sample codes for IP2Location database.

IP2Location IP-Country-Region-City-Latitude-Longitude-ZIPCode-TimeZone-AreaCode-Elevation Database [DB21] provides a solution to determine the country, region or state, city, latitude and longitude, ZIP/Postal code, time zone, area code, and elevation of origin for any IP address in a few simple steps.

IP2Location has been used in many types of projects such as:

1. select the geographically closest mirror
2. analyze your web server logs to determine the countries
3. credit card fraud detection
4. software export controls
5. display native language and currency
6. prevent password sharing and abuse of service
7. geotargeting in advertisement

The database will be updated in monthly basis for greater accuracy.

Enjoy the products!



*~The* IP2Location.com Team



## IP2Location Database Setup Guide

#### MySQL Server

1. Create a new IP2Location database.

   ```mysql
   CREATE DATABASE ip2location;
   USE ip2location;
   ```

   

2. Create IP2Location table.

   ##### IPv4

   ```mysql
   CREATE TABLE `ip2location_db21`(
       `ip_from` INT(10) UNSIGNED,
       `ip_to` INT(10) UNSIGNED,
       `country_code` CHAR(2),
       `country_name` VARCHAR(64),
       `region_name` VARCHAR(128),
       `city_name` VARCHAR(128),
       `latitude` DOUBLE,
       `longitude` DOUBLE,
       `zip_code` VARCHAR(30),
       `time_zone` VARCHAR(8),
       `idd_code` VARCHAR(5),
       `area_code` VARCHAR(30),
       `elevation` INT(10),
       PRIMARY KEY (`ip_to`)
   ) CHARSET=utf8 COLLATE=utf8_bin;
   ```

   

   ##### IPv6

   ```mysql
   CREATE TABLE `ip2location_db21_ipv6`(
       `ip_from` DECIMAL(39,0),
       `ip_to` DECIMAL(39,0),
       `country_code` CHAR(2),
       `country_name` VARCHAR(64),
       `region_name` VARCHAR(128),
       `city_name` VARCHAR(128),
       `latitude` DOUBLE,
       `longitude` DOUBLE,
       `zip_code` VARCHAR(30),
       `time_zone` VARCHAR(8),
       `idd_code` VARCHAR(5),
       `area_code` VARCHAR(30),
       `elevation` INT(10),
       PRIMARY KEY (`ip_to`)
   ) CHARSET=utf8 COLLATE=utf8_bin;
   ```

   

3. Import IP2Location CSV data into the database.

   ##### IPv4

   ```mysql
   LOAD DATA LOCAL INFILE 'IP2LOCATION-IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE-AREACODE-ELEVATION.SAMPLE.CSV'
   INTO TABLE `ip2location_db21` FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n';
   ```

   

   ##### IPv6

   ```mysql
   LOAD DATA LOCAL INFILE 'IP2LOCATION-IPV6-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE-AREACODE-ELEVATION.SAMPLE.CSV'
   INTO TABLE `ip2location_db21_ipv6` FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n';
   ```

   

#### MS-SQL Server

1. Create a new IP2Location database.

   ```mssql
   CREATE DATABASE ip2location
   GO
    
   USE ip2location
   GO
   ```

   

2. Create IP2Location table.

   ##### IPv4

   ```mssql
   CREATE TABLE [ip2location].[dbo].[ip2location_db21](
       [ip_from] bigint NOT NULL,
       [ip_to] bigint NOT NULL,
       [country_code] char(2) NOT NULL,
       [country_name] nvarchar(64) NOT NULL,
       [region_name] nvarchar(128) NOT NULL,
       [city_name] nvarchar(128) NOT NULL,
       [latitude] float NOT NULL,
       [longitude] float NOT NULL,
       [zip_code] nvarchar(30) NOT NULL,
       [time_zone] nvarchar(8) NOT NULL,
       [idd_code] nvarchar(5) NOT NULL,
       [area_code] nvarchar(30) NOT NULL,
       [elevation] int(10) NOT NULL
   ) ON [PRIMARY]
   GO
    
   CREATE CLUSTERED INDEX [ip_to] ON [ip2location].[dbo].[ip2location_db21]([ip_to]) ON [PRIMARY]
   GO
   ```

   

   ##### IPv6

   ```mssql
   CREATE TABLE [ip2location].[dbo].[ip2location_db21_ipv6](
       [ip_from] char(39) NOT NULL,
       [ip_to] char(39) NOT NULL,
       [country_code] char(2) NOT NULL,
       [country_name] nvarchar(64) NOT NULL,
       [region_name] nvarchar(128) NOT NULL,
       [city_name] nvarchar(128) NOT NULL,
       [latitude] float NOT NULL,
       [longitude] float NOT NULL,
       [zip_code] nvarchar(30) NOT NULL,
       [time_zone] nvarchar(8) NOT NULL,
       [idd_code] nvarchar(5) NOT NULL,
       [area_code] nvarchar(30) NOT NULL,
       [elevation] int(10) NOT NULL
   ) ON [PRIMARY]
   GO
    
   CREATE CLUSTERED INDEX [ip_to] ON [ip2location].[dbo].[ip2location_db21_ipv6]([ip_to]) ON [PRIMARY]
   GO
   ```

   

3. Import IP2Location CSV  data into the database.

   ##### IPv4

   ```mssql
   BULK INSERT ip2location_db21
   FROM 'IP2LOCATION-IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE-AREACODE-ELEVATION.SAMPLE.CSV'
   WITH
   (
   	FORMAT = 'CSV', 
   	FIELDQUOTE = '"',
   	FIELDTERMINATOR = ',',
   	ROWTERMINATOR = '0x0D0A',
   	TABLOCK
   )
   ```

   
   
   ##### IPv6
   
   ```mssql
   BULK INSERT ip2location_db21_ipv6
   FROM 'IP2LOCATION-IPV6-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE-AREACODE-ELEVATION.SAMPLE.CSV'
   WITH
   (
   	FORMAT = 'CSV', 
   	FIELDQUOTE = '"',
   	FIELDTERMINATOR = ',',
   	ROWTERMINATOR = '0x0D0A',
   	TABLOCK
   )
   GO
   
   update ip2location_db21_ipv6 set
   ip_from = (SUBSTRING(REPLICATE('0', 39), 1, 39 - LEN(ip_from)) + ip_from),
   ip_to = (SUBSTRING(REPLICATE('0', 39), 1, 39 - LEN(ip_to)) + ip_to)
   GO
   ```
   
   
   



## Technical Support

Any other problem and bugs please report at support@ip2location.com.