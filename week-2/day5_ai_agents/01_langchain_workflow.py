# 01_langchain_workflow.py
from langchain_core.prompts import PromptTemplate

def test_langchain_prompts():
    print("--- 1. LangChain Prompt Templates ---")
    
    # LangChain allows us to create reusable templates with variables
    template = "You are an expert on {topic}. Explain {concept} in 2 simple sentences."
    
    prompt_template = PromptTemplate(
        input_variables=["topic", "concept"],
        template=template
    )
    
    # Fill the variables
    formatted_prompt = prompt_template.format(
        topic="Astronomy", 
        concept="Black Holes"
    )
    
    print("\n✅ Formatted Prompt ready for LLM:")
    print(f"'{formatted_prompt}'")
    
    print("\n(In a full LangChain app, this prompt is piped directly into the LLM using the '|' operator).")

if __name__ == "__main__":
    test_langchain_prompts()