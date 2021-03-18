from flask import Flask, flash, redirect, render_template, request, session, abort
import AbusiveTweetsDB
import Analysis

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('FrontEnd.html')


@app.route("/find-sentiment", methods=['POST'])
def findSentiment():
    print("In findSentiment")

    name = request.form['name']
    print("Name:" + name)

    sentiment = request.form.getlist('sentiment')
    print(sentiment)

    # Getting Tweets
    twitterClient = Analysis.TwitterClient()
    tweets = twitterClient.get_tweets(query=name, count=200)
    pTweets = []
    nTweets = []
    neuTweets = []
    profaneTweets = []

    for tweet in tweets:
        if tweet['profanity']:
            profaneTweets.append(tweet)
            obj = AbusiveTweetsDB.AbusiveTweetsDB()
            obj.writeToDB(tweet)
        if tweet['sentiment'] == 'positive':
            pTweets.append(tweet)
        elif tweet['sentiment'] == 'negative':
            nTweets.append(tweet)
        else:
            neuTweets.append(tweet)

    print("Length of the profaneTweets list:", len(profaneTweets))
    print(profaneTweets)

    posPercentage = 100 * len(pTweets) / len(tweets)
    negPercentage = 100 * len(nTweets) / len(tweets)
    neuPercentage = 100 * len(neuTweets) / len(tweets)
    print("Positive tweets percentage: {} %".format(posPercentage))
    print("Negative tweets percentage: {} %".format(negPercentage))
    print("Neutral tweets percentage: {} %".format(neuPercentage))

    # ___________________________________________________________________________________

    resList = []
    if 'positiveFalse' not in sentiment:
        posNo = request.form['posNo']
        print("posNo:", posNo)
        count = 1
        print("\nPositive tweets:")
        for tweet in pTweets[:int(posNo)]:
            resList.append(tweet)
            print(str(count) + ") " + tweet['text'])
            count = count + 1
    else:
        posNo = 0
    print("Length of the list after adding positive tweets:", len(resList))

    if 'negativeFalse' not in sentiment:
        negNo = request.form['negNo']
        print('negNo:', negNo)
        count = 1
        print("\nNegative tweets:")
        for tweet in nTweets[:int(negNo)]:
            resList.append(tweet)
            print(str(count) + ") " + tweet['text'])
            count = count + 1
    else:
        negNo = 0
    print("Length of the list after adding negative tweets:", len(resList))

    if 'neutralFalse' not in sentiment:
        neuNo = request.form['neuNo']
        print('neuNo:', neuNo)
        count = 1
        print("\nNeutral tweets:")
        for tweet in neuTweets[:int(neuNo)]:
            resList.append(tweet)
            print(str(count) + ") " + tweet['text'])
            count = count + 1
    else:
        neuNo = 0
    print("Length of the list after adding neutral tweets:", len(resList))
    print(resList)

    obj = AbusiveTweetsDB.AbusiveTweetsDB()
    records = obj.returnAllDataFromDatabase()
    print(records)

    data = {'Task': 'Tweet Classification', 'Positive': posPercentage, 'Negative': negPercentage,
            'Neutral': neuPercentage}

    return render_template('DisplayResult.html', resList=resList, data=data, records=records)


if __name__ == "__main__":
    app.run()
