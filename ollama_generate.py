import ollama

modelfile = """
FROM llama3.2
SYSTEM you are very smart assistant who knows everything about cricket who answers questions succincty and informatively
PARAMETER temperature 0.1
"""

def main():
  ollama.create(model='cricketllm', from_ ='llama3.2', system="you are very smart assistant who knows everything about cricket who answers questions succincty and informatively")
  # ollama.create(model="cricketllm", modelfile=modelfile)
  response = ollama.generate(
    model="cricketllm",
    prompt="How to get a batsman out LBW?"
  )


  print(response["response"])

if __name__ == "__main__":
  main()