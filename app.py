from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables
import streamlit as st
import os
import google.generativeai as genai
import streamlit_authenticator as stauth
import pickle
from pathlib import Path
import razorpay
import stripe

st.set_page_config(page_title="Q&A Demo")
# Load Environment Variable
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Razorpay Configuration
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

#Initialize Razorpay Client
client = razorpay.Client(auth=(RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET))

## function to load Gemini Pro model and get repsonses
model=genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])

#Authentication
# --- USER AUTHENTICATION ----

names = ["Arun","Tanzeem"]
usernames = ["arun","tanzeem"]

#Load Hashed Password
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

#Initialize the authenticator

authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    'Q&A Demo',
    'abcdef',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login("Login","main")

def create_order(amount):
    order = client.order.create({
        'amount': amount * 100,
        'currency': 'INR',
        'payment_capture': '1'
    })
    return order

# Payment Status
def check_payment():
    return st.session_state.get("payment verifier", False)

if authentication_status:
    if not check_payment():
        st.warning("complete the payment to access the feature")
        amount = 10
        order = create_order(amount)
        # Display Payment button using Razorpay Checkout Form
        checkout_code = f"""
        <form action="/app" method="POST">
            <script
                src="https://checkout.razorpay.com/v1/checkout.js"
                data-key="{RAZORPAY_KEY_ID}"
                data-amount="{order['amount']}"
                data-currency="INR"
                data-order_id="{order['id']}"
                data-buttontext="Pay with Razorpay"
                data-name="Q&A Service Subscription"
                data-description="Payment for Q&A Service Subscription"
                data-image="https://your-logo-url.com/logo.png"
                data-prefill.name="{name}"
                data-theme.color="#F37254"
            ></script>
            <input type="hidden" custom="Hidden Element" name="hidden">
        </form>
        """
        st.components.v1.html(checkout_code, height=800, width=600)        
        # # Create a Checkout Session
        # session = stripe.checkout.Session.create(
        #     payment_method_types=['card'],
        #     line_items=[{
        #         'price_data':{
        #             'currency':'inr',
        #             'product_data':{
        #                 'name': 'Q&A Service Subscription',
        #             },
        #             'unit_amount': 500,
        #         },
        #         'quantity': 1,
        #     }],
        #     mode='payment',
        #     success_url="http://localhost:8501/?session_id={CHECKOUT_SESSION_ID}",
        #     cancel_url="http://localhost:8501/",
        # )
        # st.write(f"[Pay Now]({session.url})")
        #Mock Setting Payment_verified to True after redirect
        if st.button("Mock Payment Verification"):
            st.session_state.payment_verified = True
            st.experimental_rerun()
    else:
        st.success("Payment verified. You can now use the features.")
        st.write("Please select a feature from the sidebar")

        #Sidebar for feature selection
        st.sidebar.title("Features")
        feature = st.sidebar.radio("Select a Feature", ["Email_Extraction","Health", "Medical","Multiple_Pdf"])
        if feature == "1_🌍_Email_Extraction":
            import Email_Extractionas as e
            e.show()
        elif feature == "2_👨‍🎓_Health":
            import Health as health
            health.show()
        elif feature == "3_💉_Medical":
            import Medical as medical
            medical.show()
        elif feature == "4_📕_multiple_pdf":
            import Multiple_Pdf as pdf
            pdf.main()
elif authentication_status == False:
    st.error("Username/Password is Incorrect")
elif authentication_status == None:
    st.error("Please enter your username and password")
elif authentication_status:
    st.header("Gemini LLM Application")

    #Initialize session state for chat histroy if it doesnt exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    @st.cache
    def get_gemini_response(question):
        response=chat.send_message(question,stream=True)
        return response

    ##initialize our streamlit app
    input=st.text_input("Input: ",key="input")
    submit=st.button("Ask the question")

    if submit and input:
        response=get_gemini_response(input)
        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", input))
        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))
    st.subheader("The Chat History is")
        
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

    authenticator.logout("Logout","sidebar")
    st.sidebar.title(f"welcome {name}")
        