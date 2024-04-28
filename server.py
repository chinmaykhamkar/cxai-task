import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from decouple import config
from langchain.memory import ConversationBufferWindowMemory

def generate_final_response(ai_response):
    result_dict = eval(f'{{ {ai_response} }}')
    print(result_dict)
    return result_dict

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


st.set_page_config(
    page_title="CXApp",
    page_icon="🤖"
)


st.title("CXApp")


# check for messages in session and create if not exists
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello there, am CXApp assistant. How can I help you?"},
    ]


# Display all messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)


if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            ai_response = llm_chain.predict(question=user_prompt)
            final_response = generate_final_response(ai_response)
            st.write(final_response)
    new_ai_message = {"role": "assistant", "content": final_response}
    st.session_state.messages.append(new_ai_message)