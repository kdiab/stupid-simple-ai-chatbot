import json
from difflib import get_close_matches

def load_kb(path: str) -> dict:
    with open(path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_kb(path: str, data: dict):
    with open(path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_q: str, q: list[str]) -> str | None:
    match: list = get_close_matches(user_q, q, n=1, cutoff=0.7)
    return match[0] if match else None

def get_answer(q: str, kb: dict) -> str | None:
    for k in kb["questions"]:
        if k["question"] == q:
            return k["answer"]

def bot():
    kb: dict = load_kb('./kb.json')

    while True:
        user_input: str = input('User:')
        if user_input.lower() == 'q':
            break
        
        best_match: str | None = find_best_match(user_input, [q["question"] for q in kb["questions"]])
        if best_match:
            ans: str = get_answer(best_match, kb)
            print(f'Bot: {ans}')
        else:
            print('Bot: IDK, PLEASE TEACH ME')
            new_ans: str = input('Type expected answer: ')
            if new_ans.lower() != 'skip':
                kb["questions"].append({"question": user_input, "answer": new_ans})
                save_kb('kb.json', kb)
                print('Knowledge aquired!')

if __name__ == '__main__':
    bot()
