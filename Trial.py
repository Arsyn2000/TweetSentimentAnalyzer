from textblob import TextBlob

testimonial = TextBlob("I am neutral.")
print(testimonial.sentiment)