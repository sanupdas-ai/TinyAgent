from llm import LLM

llm = LLM(model="gemma3:12b", temperature=1)

prompt_example = "I saw 6 flamingos. 2 few away. 1 hid behind a tree. How many can I see?"
prompt_answer = "You saw 6 flamingos 2 flew away. 6 - 2 = 4. Then, 1 flamingo hid. You see now 4 - 1 = 3."

query = "I saw 9 penguins. 2 slid in the water and disappeared from sight while 4 waddled up from the shore. How many can I see?"

message = [
  {"role": "user", "content": prompt_example},
  {"role": "assistant", "content": prompt_answer},
  {"role": "user", "content": query}
]

response = llm.generate(message)
print(response)

# Let's thin step by step.