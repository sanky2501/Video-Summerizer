from flask import Flask
from flask import request 
from flask import render_template
from flask import abort
from flask_cors import CORS

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.utils import get_stop_words

import nltk
nltk.download('punkt')

def Summarize(text):

    
    LANGUAGE = "english"
    SENTENCES_COUNT = 20
    
    summarizer = LexRankSummarizer()
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))

    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    
    summary = summarizer(parser.document, SENTENCES_COUNT)
    
    segment = []
    result = ""
    
    for sentence in summary:
      result += (str)(sentence)

    sentencesArray = result.split('.')
    formattedSentences = ' '.join(sentencesArray)
    
    return formattedSentences

# define a variable to hold you app
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return ('You have hit our API, it is up and running');

@app.route('/api/summarize', methods=['GET'])
def GetUrl():
    """
    Called as /api/summarize?youtube_url='url'
    """
    # if user sends payload to variable name, get it. Else empty string
    video_url = request.args.get('youtube_url', '') 

    text = ""
    try:
      
      video_id = video_url.split('=')[1]

      transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
      english = transcript_list.find_manually_created_transcript(['en', 'en-US', 'en-UK'])
      transcript = english.fetch()

      formatter = TextFormatter()
      text = formatter.format_transcript(transcript)
      
      summarized = Summarize(text)

      return summarized
    
    except:
      print("in exception")


# server the app when this file is run
if __name__ == '__main__': 
  app.run()
