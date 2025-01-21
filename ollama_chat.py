import ollama

def main():
  stream = True
  response = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "Why is cricket famous in India?"}],
    stream=stream
  )

  if stream == False:
    print(response["message"]["content"])
  else:
    for chunk in response:
      print(chunk["message"]["content"], end="", flush=True)

if __name__ == "__main__":
  main()