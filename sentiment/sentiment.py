from transformers import pipeline
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv
load_dotenv()

prompt = input("Hey! How can I help you today? -> ")

def get_reply(prompt):

    zeroshot_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    # zeroshot_classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-basic-zeroshot-v2.0")


    sentiment_labels = [
        # Basic Sentiment Labels
        "Positive", "Negative", "Neutral",
        
        # Extended Sentiment Labels
        "Very Positive", "Positive", "Neutral", "Negative", "Very Negative",
        
        # Emotion-Based Sentiment Labels
        "Happy", "Sad", "Angry", "Surprised", "Fearful", "Disgusted", "Neutral",
        
        # Product/Service Feedback Labels
        "Highly Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Highly Dissatisfied",
        
        # Customer Service Sentiment Labels
        "Praise", "Complaint", "Suggestion", "Query",
        
        # Social Media Sentiment Labels
        "Love", "Like", "Neutral", "Dislike", "Hate"
    ]


    results = zeroshot_classifier(
        sequences = prompt,
        candidate_labels = sentiment_labels,
        multi_label = True
        )

    filtered_results = {label: score for label, score in zip(results['labels'], results['scores'])}
    labels = list(filtered_results.keys())[:5]
    scores = list(filtered_results.values())[:5]
    # print(filtered_results)


    os.environ["LANGCHAIN_TRACING_V2"]="true"
    os.environ["LANGCHAIN_API_KEY"]="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"
    #prompt template 
    prompt=ChatPromptTemplate.from_messages(
        [
            ("system","chat with the user keeping in mind the sentiment scores of the user's input"),
            ("user","Question:{question}")
        ]
    )

    llm=Ollama(model="phi3")
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser

    result_string = f"Question:{prompt}, 'Emotions':{labels}, 'Scores':{scores}"
    return {
        'reply': chain.invoke({"question":result_string}),
        'sentiment': {label: score for label, score in zip(labels, scores)}
    } 
    



