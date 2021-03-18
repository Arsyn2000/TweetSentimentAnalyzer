create database abusiveTweetsDB;

CREATE TABLE abusiveTweetsDB.abusiveTweetsTable(
	SrNo int NOT NULL AUTO_INCREMENT,
    UserName varchar(255) NOT NULL,
    Tweet varchar(280) NOT NULL,
    Sentiment varchar(8) NOT NULL,
    Abusive varchar(5) NOT NULL,
    Count int DEFAULT 0,
    PRIMARY KEY (SrNo));
    
select * from abusiveTweetsDB.abusiveTweetsTable;

ALTER TABLE abusiveTweetsDB.abusiveTweetsTable
ADD Date varchar(50) NOT NULL;

ALTER TABLE abusiveTweetsDB.abusiveTweetsTable
RENAME COLUMN Tweet TO Latest_Abusive_Tweet_by_User;

DELETE FROM abusiveTweetsDB.abusiveTweetsTable WHERE SrNo=27;

select * from abusiveTweetsDB.abusiveTweetsTable;

ALTER TABLE abusiveTweetsDB.abusiveTweetsTable
  DROP COLUMN Date;
  
DELETE FROM abusiveTweetsDB.abusiveTweetsTable;




