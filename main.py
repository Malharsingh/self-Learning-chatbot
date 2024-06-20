# first import the required libraries for json
import json

# To get the closest match from the json file
from difflib import get_close_matches


# Load the json file
def load_json(file_name: str):
    with open(file_name, 'r') as file:
        data: dict = json.load(file)
    return data


# Update the json file
def update_json(file_name: str, data: dict):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


# Find the best match for the word
def find_best_match(question: str, questions: list[str]) -> str | None:
    match: list[str] = get_close_matches(question, questions, n=1, cutoff=0.6)
    return match[0] if match else None


def answer_question(question: str, data: dict) -> str | None:
    for q in data["questions"]:
        if q["question"] in question:
            return q["answer"]
    return None


def chat_bot():
    data: dict = load_json('Database.json')

    while True:
        user_input: str = input("You: ")

        if user_input.lower() == "exit":
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in data["questions"]])

        if best_match:
            answer: str | None = answer_question(best_match, data)
            if answer:
                print(f"Bot: {answer}")
            else:
                print("Bot: I am sorry, I do not know the answer to that question.")
        else:
            print("Bot: I am sorry, I do not know the answer to that question.")

            print("Bot: Can you help me learn?")
            new_answer: str = input("Type the answer to the question or exit to exit: ")

            if new_answer.lower() != 'exit':
                data["questions"].append({"question": user_input, "answer": new_answer})
                update_json('Database.json', data)

            print("Bot: Thank you for teaching me something new.")


if __name__ == "__main__":
    chat_bot()
