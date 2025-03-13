from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnableBranch
from langchain_core.runnables.base import RunnableEach, RunnableMap
from langchain_core.runnables.retry import RunnableRetry
from langchain.schema.output_parser import StrOutputParser
from langchain_ollama import ChatOllama
import random

def get_llm() -> ChatOllama:
    return ChatOllama(model="llama3.2")

def get_motivational_quote(input_text: dict) -> str:
    quotes = [
        "Believe in yourself!",
        "Keep pushing forward!",
        "Success is a journey, not a destination."
    ]
    return random.choice(quotes)


# Simulate an unreliable function
def unreliable_weather_response(input_text: dict) -> str:
    if random.random() < 0.3:  # Simulate a 30% failure rate
        raise ValueError("Weather API failed!")  
    location = input_text.get("location", "your area")
    return f"The weather in {location} is sunny with a high of 75°F."


def get_question_prompt_template(input: dict) -> ChatPromptTemplate:
    if random.random() < 0.3:  # Simulate a 30% failure rate
        print("Failed in attempt")
        raise ValueError("Weather API failed!")  
    return ChatPromptTemplate.from_template("Answer the following question: {input}")

def get_greetings_prompt_template(input: dict) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_template("Can you respond with a friendly comment to greet : {input}")

def help_with_routes(input_str: str) -> str:
    greetings = ["hello", "hi", "greetings", "hey"]
    if "?" in input_str:
        return "question"
    elif any(w in input_str.lower() for w in greetings):
        return "greetings"
    else:
        return "unknown"

def create_runnable_branch() -> RunnableBranch:
    runnable_question = RunnableLambda(get_question_prompt_template)
    runnable_retry = RunnableRetry(bound=runnable_question, max_attempt_number=3)
    return RunnableBranch(
        (lambda x: help_with_routes(x["input"]) == "question",
         runnable_retry | get_llm() | StrOutputParser()),
        (lambda x: help_with_routes(x["input"]) == "greetings",
         RunnableLambda(get_greetings_prompt_template) | get_llm() | StrOutputParser()),
        RunnableLambda(lambda x: "I'm not sure how to respond to that."),  # Default case
    )

def main():
    branch = create_runnable_branch()
    input_data = {"input": "Hi, Krishnan"}
    result = branch.invoke(input_data)
    print(result)

    input_data = {"input": "Who won wimbledon mens singles 2021?"}
    result = branch.invoke(input_data)
    print(result)


def main_runnable():
    inputs = [
        {"input": "Hi, Krishnan"},
        {"input": "Who won wimbledon mens singles 2021?"}
    ]

    runner = RunnableEach(bound=create_runnable_branch())
    responses = runner.invoke(input=inputs)
    for i, response in enumerate(responses):
      print(f"User: {inputs[i]['input']}")
      print(f"Bot: {response}\n")

def main_map():
  runnable_weather = RunnableLambda(unreliable_weather_response)
  weather_with_retry = RunnableRetry(bound=runnable_weather, max_attempt_number=3)
    # Create a parallel map that runs both functions
  parallel_tasks = RunnableMap({
      "weather": weather_with_retry,  # Weather report with retry
      "quote": RunnableLambda(get_motivational_quote)  # Motivational quote
  })

  # Test input with location
  test_input = {"message": "Give me a weather update and a quote", "location": "Los Angeles"}

  # Run the parallel tasks
  response = parallel_tasks.invoke(test_input)

  # Display results
  print(f"User: {test_input['message']}")
  print(f"Bot (Weather): {response['weather']}")
  print(f"Bot (Quote): {response['quote']}\n")

if __name__ == "__main__":
    # main()
    # main_runnable()
    main_map()