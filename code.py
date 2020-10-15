#Authenticate with Twitter
import tweepy #pip install tweepy
from tweepy import OAuthHandler

consumer_key = 'tpHkVHjzU2BOlgcTazczi8XzU'
consumer_secret = 'PHd4YNV4GN6dPLCTOinpXzyEXUcFKeZfJtnOaFSOgzPU3HaiMm'
access_token = '1309925857323102209-PAE2ZVsJLKRLBTOrlnvTbBxzxUCmVD'
access_secret = 'StRb3hz98mL7FxqO8JgnTvnzBt9vHJkKxURBffHKLWZ9d'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

#Function to search tweets based on a keyword
from datetime import datetime, timedelta

def search_tweets(keyword, total_tweets):
    today_datetime = datetime.today().now()
    yesterday_datetime = today_datetime - timedelta(days=1)
    today_date = today_datetime.strftime('%Y-%m-%d')
    yesterday_date = yesterday_datetime.strftime('%Y-%m-%d')
    search_result = tweepy.Cursor(api.search,
                                  q=keyword,
                                  since=yesterday_date,
                                  result_type='recent',
                                  lang='en').items(total_tweets)
    return search_result

# Function to clean tweets by removing users, numbers and links
import re #pip install regex, pip install nltk
from nltk.tokenize import WordPunctTokenizer

def clean_tweets(tweet):
    user_removed = re.sub(r'@[A-Za-z0-9]+','',tweet.decode('utf-8'))
    link_removed = re.sub('https?://[A-Za-z0-9./]+','',user_removed)
    number_removed = re.sub('[^a-zA-Z]', ' ', link_removed)
    lower_case_tweet= number_removed.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_tweet)
    clean_tweet = (' '.join(words)).strip()
    return clean_tweet

import httplib2
import json

from oauth2client import GOOGLE_REVOKE_URI, GOOGLE_TOKEN_URI, client
from oauth2client.client import GoogleCredentials
from pydrive.auth import GoogleAuth     #pip install -U -q PyDrive
from pydrive.drive import GoogleDrive

auth_key = {
  "client_id": "32555940559.apps.googleusercontent.com",
  "client_secret": "ZmssLNjJy2998hD4CTg2ejr2",
  "refresh_token": "1//06q0OIfBTroMeCgYIARAAGAYSNwF-L9Ir6rh6u2kXWIBTvPMJF9DCi8WjS4SzgOB4N9R9mlwW_CGMxSLoWQ_-Um0eYI6DuwD48Uw"
}

credentials = client.OAuth2Credentials(
    access_token=None,
    client_id=auth_key['client_id'],
    client_secret=auth_key['client_secret'],
    refresh_token=auth_key['refresh_token'],
    token_expiry=None,
    token_uri=GOOGLE_TOKEN_URI,
    user_agent=None,
    revoke_uri=GOOGLE_REVOKE_URI)

credentials.refresh(httplib2.Http())
credentials.authorize(httplib2.Http())
cred = json.loads(credentials.to_json())
cred['type'] = 'authorized_user'

with open('adc.json', 'w') as outfile:
  json.dump(cred, outfile)

import json
my_j={"type": "service_account", "project_id": "single-arcana-291418", "private_key_id": "6a7ca374912069de248344e00940f19b1219bcb8","private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCdVlFGqftv2AKG\n39VpGVJEp9tfIgQUTAhYvy/FEMh93jw7hRwGc1RTUSUUDlT00c9q2e9JXEFO7O0x\nKyLt3LqMnfs9PAsNNzCszjYd7DAsTWzziVZmLbfU8ki4vC/aITrzeCalaskkOwTU\no8KzALNPrCoX1FGAJlDOTSzuoJ9rZGHA+mMdFdvsvtdxsN+Wz0SjWyKPLoIwN+a1\nbj688nK27+jxxQKycWeFnFzQ+sMBCrSbIq5yU9gU+gkmiP51Da9uI0XoizGngB1j\nFcKXxROrzaP6GxTSskarIXXFi/mVQY4Vd6bF+wPKD1sX8okZ00/z2Gw8IcIHXOGB\nQ1op27k/AgMBAAECggEAB5Qnqxc3W4OqBNQrA/p/xNCEbSMxfhwheiDkzKx1HoxX\na2iLLoux9VIfI/BYIEjWTGfTXRMauZIJD4lr5SLw63gVU4ryX1XCvE2HPCQV4p8X\nee2qIew0LYeUKtiJwjXqkIgU7c/kgMsaUvcmbZfsNeYYSviOX8q4sWSfSZ6mvzX4\nXxDcJxfZMM41s4Z46weEsRNf4YWevw7eKwSP/kq5fd4BSJHwhHc7G+LRPdAsvbse\nogMuqKJ+wb3U42pGgXS5RYT/ddC3POdfItGY/uPZp4jzRx+7WntQbp9S0wYN/09W\n7rAJk55h7ThD8zLCSZNerul8i+pXN0a5TT9mpE/y/QKBgQDdx8ExpdQBgix7lIDk\noi9LUOhP0q0TZscAKrzoftvjTZybYFte0wbq4zLirq8mi1/UBudFOm9pd1wHpFFj\nKreRO6xwnk6V5VUJSI2ixBuaVUZmoTAnOwAeNMW1z2GR8JhNRazMxy9htY8bNJ2j\nc94OUjFUrp3cUPD0a6Ja9tNgZQKBgQC1nRT7B1IMiItDOCybISMZLzG/s4ELzBuc\nqTS1SGxm854q4XmN8cpmwbF28nvYGS15/35oYbX15tZ9pLkQ4oR/rehoJxhlS1D1\nrZAndtJsPLRzf6AwOI8lX1WCi5rCP+bTCQwR9ufWLLSYbpfvlQmFujzH/nz67DSL\n0Iwms6rO0wKBgFFI6VIdCTsUTuFsaGFj4Bmmqb635J97x+wTvfEorcb9pyx7gIGc\nrqhgZUIX7DIgWxsG/LSu2i65hI14eCv0eBtO18DfBMaDq0sfwGmrnsJOBuOOqGt4\ngG6RwPUF8SjgGbIYm2DikEcrmCvMeQpzaSuujE4RQeKB+A5ddMAKPybRAoGBAJHK\nccc6jzEkg7cIZzZ5GXXkHumnLdbMmPXgF0HXy72xn60Ip8285iArKU01RxmozIr9\nAPrGRY4LKvBdxXq6fGcKsmC50amvFmTCWdB0YGMnMCzvrSZIoRD9QOW1MBzzs1aC\nEsBxFpcl+CvNzAY1/Bjv8k8SCj5cU6pRVdDTtjClAoGAFOztnBWBnDKARLpzjJAw\nIAqbkiNh5yNth24u8KXKPU6KjAkDgoI5R1A3PHL8tMyY6Nmh/BfU6+xsLH4epdKd\nfvIuyJYL3SqXg7mF0+trz51cbJr2a09toP0RwFREHiHv5PrZwuV9mfejlON0cCza\n4GHK5ixNL+fhDMpRhuljt0I=\n-----END PRIVATE KEY-----\n", "client_email": "twitter-analysis@single-arcana-291418.iam.gserviceaccount.com","client_id": "100834910731839937993","auth_uri": "https://accounts.google.com/o/oauth2/auth","token_uri": "https://oauth2.googleapis.com/token","auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/twitter-analysis%40single-arcana-291418.iam.gserviceaccount.com"}

with open('cred.json', 'w') as json_file:
    json.dump(my_j, json_file)

#Function to get sentiment score using Google NLP API
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file("cred.json")

def get_sentiment_score(tweet):
    client = language.LanguageServiceClient(credentials=credentials)
    document = types\
               .Document(content=tweet,
                         type=enums.Document.Type.PLAIN_TEXT)
    sentiment_score = client\
                      .analyze_sentiment(document=document)\
                      .document_sentiment\
                      .score
    return sentiment_score

# Function to search for n tweets with keyword and return T-test scores
import numpy as np
from scipy import stats

def get_stats (keyword, n):
  tweets = search_tweets(keyword, n)
  score_array = []
  for tweet in tweets:
    global cleaned_tweet
    cleaned_tweet = clean_tweets(tweet.text.encode('utf-8'))
    global sentiment_score
    sentiment_score = get_sentiment_score(cleaned_tweet)
    print('Tweet: {}'.format(cleaned_tweet))
    print('Score: {}\n'.format(sentiment_score))
    score_array = np.append(score_array, sentiment_score)

  t_score, p_value = stats.ttest_1samp(score_array, 0)
  final_tweets = 'Tweet: {}'.format(cleaned_tweet), 'Score: {}\n'.format(sentiment_score)

  return t_score, p_value
  return cleaned_tweet, sentiment_score

word = "Dak Prescott"
qty = 5
t, p = get_stats (word, qty)
print ('T-score = ' + str(t))
print ('P Value = ' + str(p))

# START OF TKINTER GUI----------------------------------------------------------------------------------
from tkinter import * #import gui tools
from PIL import ImageTk, Image # import python image library (pillow)

root = Tk()
root.title('Twitter Sentiment Analysis Application') #title of window
root.iconbitmap('c:/Users/jaygi/Downloads/birdy.ico') # path to icon

#add an image (page logo)
image_0 = ImageTk.PhotoImage(Image.open('c:/Users/jaygi/Downloads/app_banner.PNG')) # map the image
label_0 = Label(image = image_0)    # assign the image
label_0.grid(row = 0, column = 0)   # position the image

# Define Functions ------------------------------------------------------------

def button_clear():                 # function to clear text field
    e.delete(0, END)
    q.delete(0, END)

def button_submit():                # function to submit text entries
    global word                    # make the variable callable outside the function
    word = e.get()                  # define the keyword from user entry 
    global qty
    qty = q.get()                   # define the quanity of tweets analyzed 

# Define Frames ----------------------------------------------------------------

# Frame for user input section
frame_0 = LabelFrame(root,          # define frame
text = 'Get Latest Analysis',       # add frame text
padx = 10, pady = 5,                # add frame padding (empty space surrounding)
bg = 'white', fg = 'black'          # add frame color
)
frame_0.grid(row = 1, column = 0,   # position the frame
 padx = 10, pady = 10,              # frame padding
columnspan = 10                     # match widget width to window
)   

# Frame Around Results Section 
frame_1 = LabelFrame(root,            # define frame
text = 'Twitter\'s Latest Results',   # add frame text
padx = 10, pady = 5,                  # add frame padding (empty space surrounding)
bg = 'white', fg = 'black'            # add frame color
)
frame_1.grid(row = 9, column = 0,     # position the frame
 padx = 10, pady = 10,                # frame padding
sticky = E+W,                         # match widget width to window
rowspan = 55
) 

# Frame Around Information Section 
frame_2 = LabelFrame(root,          # define frame
text = 'Definitions',               # add frame text
padx = 10, pady = 5,                # add frame padding (empty space surrounding)
bg = 'white', fg = 'black'          # add frame color
)
frame_2.grid(row = 6, column = 0,   # position the frame
 padx = 10, pady = 10,              # frame padding
columnspan = 10                     # match widget width to window
) 

# User Input Widgets (text entry fields)----------------------------------------

# keyword entry wiget 
e = Entry(frame_0,                     # define text input box
width = 60,                            # text box width 
borderwidth = 10)                      # text box border 
e.grid(row = 2, column = 0             # position the text box
)
e.insert(0, "Enter your keyword here") # default text inside text box

# quanity entry wiget 
q = Entry(frame_0,                      # define text input box
width = 60,                             # text box width 
borderwidth = 10)                       # text box border 
q.grid(row = 3, column = 0              # position the text box
)                                       # default text inside text box
q.insert(0, "Enter number of tweets to retrieve (limit of 50)") 

# Buttons ----------------------------------------------------------------------

# button widget to submit user input
button_0 = Button(frame_0,           # define buton
text = 'Return Results',             # button text
command = (button_submit,
search_tweets,
clean_tweets,
get_sentiment_score,
get_stats)        # button function  
)
button_0.grid(row = 4, column = 0,   # position the button
sticky = W+E                         # match button width to frame
) 

# button widget to clear text field
button_0 = Button(frame_0,           # define buton
text = 'Clear Text Field',           # button text
command = button_clear               # button function 
)
button_0.grid(row = 5, column = 0,  # position the button
sticky = W+E                        # match button width to frame
) 

# Labels -----------------------------------------------------------------------

# Definitions of statistical scores 

label_0 = Label(frame_2,              # Lable for mean
text =                                # text for label
'Sentiment mean is the average sentiment of all tweets referenced' ,
bg = "white"                          #color of label background
)
label_0.grid(row = 7, column = 0)     # position of label

label_1 = Label(frame_2,              # Lable for T-Score defined
text =                                # text for label
'T-score is standard deviation; the average difference of each score from the mean' ,
bg = "white"                          #color of label background
)
label_1.grid(row = 8, column = 0)     # position of label

label_2 = Label(frame_2,              # Lable for P-Score defined
text =                                # text for label
'P-value details statistical significance; p-value > 0.05 = statistical significance' ,
bg = "white"                          #color of label background
)
label_2.grid(row = 9, column = 0)     # position of label

# Results from the API

label_3 = Label(frame_1,              # Lable for T-Score results
text = 'T-score = ' + str(t) ,        # text for label
bg = "white"                          # color of label background
)
label_3.grid(row = 10, column = 0)     # position of label

label_4 = Label(frame_1,              # Lable for P-Score results
text ='P Value = ' + str(p) ,         # text for label
bg = "white"                          # color of label background
)
label_4.grid(row = 11, column = 0)    # position of label

label_5 = Label(frame_1,                         # Lable for results
text = str(('Tweet: {}'.format(cleaned_tweet)) + # Print formated tweets 
(' Score: {}\n'.format(sentiment_score))),       # Print formated scores with tweet   
bg = "white",                                    # color of label background
)
label_5.grid(row = 12, column = 0,               # position the label
sticky = N+S+E+W, 
rowspan = 50                          
)     

# End of Labels ----------------------------------------------------------------

root.mainloop() #create the event loop
