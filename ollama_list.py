import ollama

def ollama_list():
  response = ollama.list()
  print(response)
  


if __name__ == "__main__":
  ollama_list()