import openai
openai.api_key = "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"

def nong_khao(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit"]:
            print("Exiting chatbot. Goodbye!")
            break
        response = nong_khao(user_input)
        print("NongKhao:", response)
