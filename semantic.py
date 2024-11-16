import streamlit as st
import requests
import json

# Function to call OpenAI API
def get_semantic_score(blog_content, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are an assistant who helps evaluate the semantic quality of blog content."
            },
            {
                "role": "user",
                "content": f"Please analyze the semantic quality of the following blog content:\n\n{blog_content}"
            }
        ],
        "temperature": 0.7,
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    
    if response.status_code == 200:
        # Extract the model's response
        score_response = response_data["choices"][0]["message"]["content"]
        return score_response
    else:
        return f"Error: {response_data.get('error', {}).get('message', 'Unknown error')}"

# Streamlit UI
def main():
    st.title("Semantic Score Evaluation for Blog Post")
    
    # Input: OpenAI API Key
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    
    if not api_key:
        st.warning("Please enter your OpenAI API key to proceed.")
        return
    
    # Input: Blog content
    blog_content = st.text_area("Insert your blog content here", height=300)
    
    if st.button("Evaluate Semantic Score"):
        if blog_content:
            with st.spinner("Analyzing..."):
                result = get_semantic_score(blog_content, api_key)
            st.subheader("Analysis Result:")
            st.write(result)
        else:
            st.warning("Please provide some blog content to analyze.")
    
if __name__ == "__main__":
    main()
