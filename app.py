from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from decouple import config
from langchain.memory import ConversationBufferWindowMemory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""
    I'm going to ask you some questions and your response should be in the format of
    "intentRecognised": "", "exchangeReply": ""
  And the response should be based on this data:
Booking:
- createBooking: Initiate or request to set up a new booking.
- readBooking: Inquiries about retrieving details of existing bookings, specific or general.
- updateBooking: Modify existing bookings (participants, time, topic, space, notes).
- deleteBooking: Handle the cancellation or removal of existing bookings.
Inquiries:
- inquireSpaceAvailability: Check when specific spaces are free or inquire about their details.
- inquirePeopleAvailability: Check the availability of a specific person or group at a given time.
- searchInquiry (CXAI Search): Search for specific work documents, files, or folders.
- analyticsInquiry: Provide statistical or analytical information about the workplace.
Delegation:
- createDelegationRule
- readDelegationRule
- updateDelegationRule
- deleteDelegationRule
User Persona:
- createUserAttribute
- readUserAttribute
- updateUserAttribute
- deleteUserAttribute
Food:
- createFoodOrder
- readFoodOrder
- updateFoodOrder
- deleteFoodOrder
Miscellaneous:
-helpAndSupport: Provide technical support or emergency assistance.
-greeting: Handle various forms of greetings.
-farewell: Manage farewell expressions and closing conversations.
-gratitude: Address various forms of gratitude.
-feedback: Manage user feedback.
-other: Handle uncategorized requests.

if the question is "give me all the booking details for tomorrow" then the response should be
  "intentRecognised": "Booking: readBooking",  "exchangeReply": "Yes, I will get those results right away".  
  
If the question is "give me the availability of John at 10am" then the response should be
"intentRecognised": "Inquiries: inquirePeopleAvailability", "exchangeReply": "Let me check John's availability for you at 10 am."

keep the "exchangeReply" value short and don't ask follow up question

If you don't understand the question, just respond with "intentionRecognised": "Miscellaneous: other", "exchangeReply": "Please ask me a follow up question"
    chat_history: {chat_history},
    Human: {question}
    AI:"""
)

llm = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"))
memory = ConversationBufferWindowMemory(memory_key="chat_history", k=4)
llm_chain = LLMChain(
    llm=llm,
    memory=memory,
    prompt=prompt
)

def generate_final_response(ai_response):
    result_dict = eval(f'{{ {ai_response} }}')
    print(result_dict)
    return result_dict


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_prompt = data.get('question')
    ai_response = llm_chain.predict(question=user_prompt)
    final_response = generate_final_response(ai_response)
    print(final_response)
    return jsonify(final_response)


if __name__ == '__main__':
    app.run(debug=True)






