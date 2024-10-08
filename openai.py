import openai

# Replace this with your valid OpenAI API key
openai.api_key = "sk--LPxS0sU7T-cKLHyCCpP4EBJGnbglnbDAQSgU2JCWNT3BlbkFJkGEp7qzJfr6JATanf1EUizl2YxkV9UA5izPOL0CY8A"

def nong_khao(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
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
