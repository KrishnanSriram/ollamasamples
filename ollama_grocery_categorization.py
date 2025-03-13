import ollama

# Global variables. They can be moved into some configuration or env variables
prompt = """
You are an assistant that categorizes and sorts grocery items.
Here is the list of items: 
{items}
Plese: 
1. Categorize them intp appropriate categories such as Meat & Fish, Tinned & Dried Produce, Grains & Bread, Condiments, Dairy & Eggs, and Oil & Fat
2. Please sort the items alphabetically within each category
3. Present the organized list in a clear and organized them using bullet points and numbering
"""
model = "llama3.2"

def get_items(input_file):
  with open(input_file, "r") as f:
    items = f.read().strip()

  return items

def persist_content(output_file, text):
  with open(output_file, "w") as f:
      f.write(text.strip())

  return True
    
def main():
  input_file = "grocery_list.txt"
  output_file = "categorized_list.txt"

  items = get_items(input_file=input_file)
  

  try:
    response = ollama.generate(model=model, prompt=prompt)
    generated_text = response.get("response", "")

    persist_content(output_file=output_file, text=generated_text)
    
    print(f'Completed categorization. Check - {output_file} for results')
  except Exception as e:
    print("Error: ", str(e))

if __name__ == "__main__":
  main()