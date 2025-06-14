import streamlit as st
import openai
import os

st.set_page_config(page_title="CodyOS Assistant", layout="wide")

st.title("🤖 CodyOS Assistant")
st.markdown("Ask questions and receive responses using embedded vault logic.")

# Load OpenAI API key
api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# Load vault context
with open("vault_context.md", "r") as file:
    vault_context = file.read()

mode = st.selectbox("Mode", ["🔌 Live (OpenAI API)", "🧪 Mock (Offline Testing)"])

question = st.text_input("Ask CodyOS a question:")
submit = st.button("Submit")

if submit and question:
    st.markdown("### 💬 Response")
    if mode == "🧪 Mock (Offline Testing)":
        st.markdown("_This is a simulated response based on your logic vault._")
        st.info(f"Question: {question}\n\nAnswer: (Placeholder) Based on CodyOS logic, the correct action is to...")
    else:
        if not api_key:
            st.error("API key not found. Please set it in .env or Streamlit secrets.")
        else:
            try:
                openai.api_key = api_key
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": f"You are CodyOS, a domain-aware assistant with the following context:
{vault_context}"},
                        {"role": "user", "content": question}
                    ]
                )
                st.success(response.choices[0].message.content)
            except Exception as e:
                st.error(f"API Error: {e}")
