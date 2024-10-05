from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def generate_pet_name(animal_type, pet_color):
    llm = Ollama(model="phi3", temperature=0.01)
    prompt_template_name = PromptTemplate(
        input_variables= ['animal_type', 'pet_color'], 
        template = "I have a cute {pet_color} {animal_type} as a pet. Suggest 5 names for him, list only."
    )
    # prompt = "I have a cute eagle as a pet. Suggest 5 names for him, list only."
    
    name_chain = prompt_template_name | llm
    response = name_chain.invoke({'animal_type': animal_type, "pet_color":pet_color})
    return response


if __name__ == "__main__":
    print(generate_pet_name("eagle"))