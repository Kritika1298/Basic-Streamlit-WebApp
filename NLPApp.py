import streamlit as st

#NLP Pakages
import spacy
from textblob import TextBlob
from gensim.summarization import summarize

#Sumy packages
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

#Summary Function
def sumy_summarizer(docx):
    parser=PlaintextParser.from_string(docx,Tokenizer("english"))
    lex_summarizer=LexRankSummarizer()
    summary=lex_summarizer(parser.document,3)
    summary_list=[str(sentence) for sentence in summary]
    result=' '.join(summary_list)
    return result

def text_analyzer(my_text):
    nlp=spacy.load('en')
    docx=nlp(my_text)
    tokens=[token.text for token in docx]
    allData=[('"Tokens":{},\n"Lemma":{}'.format(token.text,token.lemma_))for token in docx]
    return allData

def entity_analyzer(my_text):
    nlp=spacy.load('en')
    docx=nlp(my_text)
    tokens=[token.text for token in docx]
    entities = [(entity.text,entity.label_) for entity in docx.ents]
    allData=['"Tokens":{},\n"Entities":{}'.format(tokens,entities)]
    return allData

def main():
    """NLP App with Streamlit """
    st.title("NLPifyy with Streamlit")
    st.subheader("Natural Language Processing on the Go")

    #Tokenization

    value="Type Here"
    if st.checkbox("Show Tokens and Lemma"):
        st.subheader("Tokenizer Your Text")
        message = st.text_area("Enter Your Text",value)
        if st.button("Analyze"):
            nlp_result=text_analyzer(message)
            st.json(nlp_result)

    #Named Entity
    if st.checkbox("Show Named Entities"):
        st.subheader("Extract Entities From Your Text")
        message = st.text_area("Enter Your Text",value)
        if st.button("Extract"):
            nlp_result=entity_analyzer(message)
            st.json(nlp_result)

    #Sentimental Analysis

    if st.checkbox("Show Sentiment Analysis"):
        st.subheader("Sentiment of Your Text")
        message=st.text_area("Enter Your Text",value)
        if st.button("Analyze"):
            blob=TextBlob(message)
            result_sentiment=blob.sentiment
            st.success(result_sentiment)

    #Text Summarization
    if st.checkbox("Show Text Summarization"):
        st.subheader("Summarize Your Text")
        message=st.text_area("Enter Your Text",value)
        summary_options=st.selectbox("Choose Your Summarizer",['gensim','sumy'])
        if st.button("Summarize"):
            if summary_options=="genism":
                st.text("Using Gensim Summazier..")
                summary_result=summarize(message)
            elif summary_options=='sumy':
                st.text("Using Sumy Summarizer..")
                summary_result=sumy_summarizer(message)
            else:
                st.warning("Using Default Summarizer")
                st.text("Using Gensim")
                summary_result=summarize(message)

            st.success(summary_result)

        st.sidebar.subheader("About App")
        st.sidebar.text("NLP WebApp With Streamlit")


if __name__ == '__main__':
    main()
