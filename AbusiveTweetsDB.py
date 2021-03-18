import mysql.connector
import re


class AbusiveTweetsDB:
    def __init__(self):
        print("In AbusiveTweetsDB constructor")

    def writeToDB(self, profaneTweet):
        # Config
        print("In writeToDB")
        config = {
            'user': 'root',
            'password': 'password',
            'host': 'localhost',
            'database': 'abusiveTweetsDB',
            'port': 3306,
            'raise_on_warnings': True,
        }

        # Connecting to DB
        conn = mysql.connector.connect(**config)

        # Create Cursor
        c = conn.cursor()

        tweet = profaneTweet['text']
        # Cleaning Tweet because the database gives error when you try to
        # insert emojis and special characters
        cleanTweet = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet)
        sentiment = profaneTweet['sentiment']
        abusive = profaneTweet['profanity']
        screenName = profaneTweet['screen_name']
        date = profaneTweet['created_at']
        print(tweet)
        print(sentiment)
        print(abusive)
        print(screenName)
        print(date)

        # Query
        print("Before Query")
        c.execute("SELECT * FROM abusiveTweetsDB.abusiveTweetsTable")
        records = c.fetchall()
        flag = 0

        # Looping through the records to find if the Name is already present
        for record in records:
            if str(record[1]) == str(screenName):
                flag = 1
                if str(record[6]) != str(date):
                    print('record[6] != date', record[6] != date)
                    print('record[6]', record[6])
                    print('date', date)
                    temp = int(record[5]) + 1
                    tempSrNo = record[0]
                    tempLatestAbusiveTweetByUser = cleanTweet
                    tempSentiment = sentiment
                    tempDate = date
                    # Change Latest_Abusive_Tweet_by_User, Sentiment, Date
                    sql = """UPDATE abusiveTweetsDB.abusiveTweetsTable
                                           SET Count= %s, Latest_Abusive_Tweet_by_User= %s, Sentiment= %s, Date= %s
                                           WHERE SrNo= %s"""
                    val = (temp, tempLatestAbusiveTweetByUser, tempSentiment, tempDate, tempSrNo)
                    c.execute(sql, val)
                    print("Updated in DB")
                    flag = 1
                    break
        if flag == 0:
            numberOfEntries = len(records)
            newSrNo = int(numberOfEntries) + 1
            sql = """INSERT INTO abusiveTweetsDB.abusiveTweetsTable
                                          (SrNo, Name, Latest_Abusive_Tweet_by_User, Sentiment, Abusive, Count, Date) 
                                          VALUES (%s, %s, %s, %s, %s, %s, %s)"""

            val = (newSrNo, screenName, cleanTweet, sentiment, abusive, '1', date)

            # Execute
            print("Before Execute")
            c.execute(sql, val)
            print("Sent to DB!")

        # Commit
        conn.commit()

        # End Session
        c.close()
        conn.close()

    def returnAllDataFromDatabase(self):
        # Config
        print("In writeToDB")
        config = {
            'user': 'root',
            'password': 'password',
            'host': 'localhost',
            'database': 'abusiveTweetsDB',
            'port': 3306,
            'raise_on_warnings': True,
        }

        # Connecting to DB
        conn = mysql.connector.connect(**config)

        # Create Cursor
        c = conn.cursor()

        # Execute fetchall()
        c.execute("SELECT * FROM abusiveTweetsDB.abusiveTweetsTable")
        records = c.fetchall()

        return records
