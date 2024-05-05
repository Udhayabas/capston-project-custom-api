import json
import openai
from collections import defaultdict

products_file = 'products.json'
categories_file = 'categories.json'

delimiter = "####"
step_2_system_message_content = f"""
You will be provided with agriculture related advisor a conversation. \
The most recent user query will be delimited with \
{delimiter} characters.
Output a python list of objects, where each object has \
the following format:
     'agriculture category':<Crops, \Livestock, \Fisheries, \Forestry,
      \Agrochemicals, \Agri-       inputs, \Agri-food processing, \
      Agro-allied products>,
OR
     'products': <a list of products that must \
     be found in the allowed products below>
     
Where the agriculture categories and products must be found in \
the formers service query.
If a product is mentioned, it must be associated with \
the correct category in the allowed products list below.
If no products or categories are found, output an \
empty list.
Only list products and categories that have not already \
been mentioned and discussed in the earlier parts of \
the conversation.    

Allowed products: 

 Crops category:
 fruits
 vegetables
 grains
 oilseeds
 pulses
 fibers 
 medicinal plants
 
 Livestock category:
 animals raised for meat
 milk
 eggs
 
 Fisheries category:
 aquatic animals such as fish
 shrimp
 other seafood
 
 Forestry category:
 timber
 pulp
 paper 
 other wood products
 
 Agrochemicals category:
 fertilizers
 pesticides
 herbicides
 fungicides
 
 Agri-inputs category:
 seeds
 seedlings
 agricultural machinery
 tools and equipment
 
 Agri-food processing category:
 milling
 canning
 packaging 
 preserving

 Agro-allied product category:
 textiles
 biofuels
 pharmaceuticals
 other industrial goods
 
 Only output the list of objects, with nothing else.
"""
step_2_system_message = {'role':'system', 'content': step_2_system_message_content}    


step_4_system_message_content = f"""
    You are a agriculture advisor assistant for a formers. \
    Respond in a friendly and helpful tone, with VERY concise answers. \
    Make sure to ask the user relevant follow-up questions.
"""
step_4_system_message = {'role':'system', 'content': step_4_system_message_content}    

step_6_system_message_content = f"""
    You are an assistant that evaluates whether \
    formers advising assistant responses sufficiently \
    answer formers questions, and also validates that \
    all the facts the assistant cites from the product \
    information are correct.
    The conversation history, product information, user and formers \
    advising agent messages will be delimited by \
    3 backticks, i.e. ```.
    Respond with a Y or N character, with no punctuation:
    Y - if the output sufficiently answers the question \
    AND the response correctly uses product information
    N - otherwise

    Output a single letter only.
"""
step_6_system_message = {'role':'system', 'content': step_6_system_message_content}    

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    return response.choices[0].message["content"]

def create_categories():
    categories_dict = {
        'Billing': [
            'Unsubscribe or upgrade',
            'Add a payment method',
            'Explanation for charge',
            'Dispute a charge'
        ],
        'Technical Support': [
            'General troubleshooting',
            'Device compatibility',
            'Software updates'
        ],
        'Account Management': [
            'Password reset',
            'Update personal information',
            'Close account',
            'Account security'
        ],
        'General Inquiry': [
            'agri Product information',
            'Pricing',
            'Feedback',
            'Speak to a human'
        ]
    }

    categories_file = 'categories.json'  # Define the filename to write the categories

    with open(categories_file, 'w') as file:
        json.dump(categories_dict, file)

    return categories_dict

def get_categories():
    with open(categories_file, 'r') as file:
            categories = json.load(file)
    return categories

def get_product_list():
    # Define the allowed products inside the function
    allowed_products = [
        "fruits",
        "vegetables",
        "grains",
        "oilseeds",
        "pulses",
        "fibers",
        "medicinal plants",
        "animals raised for meat",
        "milk",
        "eggs",
        "aquatic animals such as fish",
        "shrimp",
        "other seafood",
        "timber",
        "pulp",
        "paper",
        "other wood products",
        "fertilizers",
        "pesticides",
        "herbicides",
        "fungicides",
        "seeds",
        "seedlings",
        "agricultural machinery",
        "tools and equipment",
        "milling",
        "canning",
        "packaging",
        "preserving",
        "textiles",
        "biofuels",
        "pharmaceuticals",
        "other industrial goods"
    ]
    
    # Return the list of allowed products
    return allowed_products

def get_products_and_category():
    products_by_category = defaultdict(list)
    for product_name, product_info in products.items():
        category = product_info.get('category')
        if category:
            products_by_category[category].append(product_info.get('name'))
    
    return dict(products_by_category)

def get_products():
    with open(products_file, 'r') as file:
        products = json.load(file)
    return products

def find_category_and_product(user_input, products_and_category):
    delimiter = "####"
    system_message = f"""
    You will be provided with agriculture related advisor a conversation. \
The most recent user query will be delimited with \
{delimiter} characters.
Output a python list of objects, where each object has \
the following format:
     'agriculture category':<Crops, \Livestock, \Fisheries, \Forestry,
      \Agrochemicals, \Agri-       inputs, \Agri-food processing, \
      Agro-allied products>,
OR
     'products': <a list of products that must \
     be found in the allowed products below>
     

    Where the categories and products must be found in the formers service query.
    If a product is mentioned, it must be associated with the correct category in the allowed products list below.
    If no products or categories are found, output an empty list.

    The allowed products are provided in JSON format.
    The keys of each item represent the category.
    The values of each item is a list of products that are within that category.
    Allowed products: {products_and_category}
    """
    messages = [  
        {'role': 'system', 'content': system_message},    
        {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"},  
    ] 
    return get_completion_from_messages(messages)

def find_category_and_product_only(user_input, products_and_category):
    delimiter = "####"
    system_message = f"""
    You will be provided with former's queries. 
    The former's query will be delimited with {delimiter} characters.
    Output a Python list of objects, where each object has the following format:
        'agriculture category': <Crops, Livestock, Fisheries, Forestry, Agrochemicals, Agri-inputs, Agri-food processing, Agro-allied products>,
    OR
        'products': <a list of products that must be found in the allowed products list below>

    Where the categories and products must be found in the former's service query.
    If a product is mentioned, it must be associated with the correct category in the allowed products list below.
    If no products or categories are found, output an empty list.

    Allowed products: 

    1. Crops:
       - Cereals (e.g., rice, wheat, corn)
       - Fruits (e.g., apples, oranges, bananas)
       - Vegetables (e.g., tomatoes, potatoes, carrots)
       - Pulses (e.g., lentils, chickpeas, beans)
       - Oilseeds (e.g., soybeans, sunflower, canola)
       - Spices (e.g., pepper, cinnamon, turmeric)

    2. Livestock:
       - Dairy products (e.g., milk, cheese, yogurt)
       - Meat products (e.g., beef, pork, poultry)
       - Eggs
       - Wool and fibers (e.g., wool, silk)
       - Honey

    3. Aquaculture:
       - Fish (e.g., salmon, tilapia, trout)
       - Shrimp
       - Oysters
       - Seaweed

    4. Forestry products:
       - Timber (e.g., pine, oak, teak)
       - Pulp and paper
       - Resins and gums

    5. Horticulture products:
       - Flowers (e.g., roses, lilies, orchids)
       - Nursery plants (e.g., tree saplings, ornamental plants)
       - Medicinal plants
       - Aromatic plants
   
    Only output the list of objects, nothing else.
    """
    messages = [  
        {'role': 'system', 'content': system_message},    
        {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"},  
    ] 
    return get_completion_from_messages(messages)
def get_products_and_category(products):
    products_by_category = defaultdict(list)
    for product_name, product_info in products.items():
        category = product_info.get('category')
        if category:
            products_by_category[category].append(product_info.get('name'))
    
    return dict(products_by_category)
from collections import defaultdict

def get_products_and_category(products):
    products_by_category = defaultdict(list)
    for category, product_info in products.items():
        if isinstance(product_info, str):
            products_by_category[category].append(product_info)
        else:
            for product_name, product_detail in product_info.items():
                products_by_category[category].append(product_name)
    return dict(products_by_category)
def get_products():
    products = {
        "Crops": "This includes grains (such as wheat, corn, rice), vegetables (such as tomatoes, onions, carrots), fruits (such as apples, oranges, bananas), and other crops like cotton, coffee, and sugarcane",
        "Livestock": "This includes animals raised for meat (such as cattle, pigs, chickens), dairy (such as cows, goats, sheep), and other purposes (such as horses for riding, bees for honey production)",
        "Poultry": "This includes chickens, ducks, turkeys, and other domesticated birds raised for meat and eggs",
        "Aquaculture": "This includes fish farming, shrimp farming, and other forms of aquatic animal farming for food production",
        "Forestry products": "This includes timber, wood products, and other products derived from forests and trees",
        "Horticulture": "This includes fruits, vegetables, flowers, ornamental plants, and other crops grown in gardens or greenhouses"
    }
    return products




def get_products_from_query(user_msg):
    products_and_category = get_products_and_category()
    delimiter = "####"
    system_message = f"""
    You will be provided with former queries. 
    The most recent user query will be delimited with
    {delimiter} characters.
    Output a python list of objects, where each object has
    the following format:
        'agriculture category': <Crops, Livestock, Fisheries, Forestry,
        Agrochemicals, Agri-inputs, Agri-food processing, Agro-allied products>,
            
    OR
        'products': <a list of products that must be found in the allowed products list below>

    Where the categories and products must be found in the former's service query.
    If a product is mentioned, it must be associated with the correct category in the            allowed products list below.
    If no products or categories are found, output an empty list.

    Allowed products: {products_and_category}
    """

    messages = [
        {'role': 'system', 'content': system_message},    
        {'role': 'user', 'content': f"{delimiter}{user_msg}{delimiter}"},  
    ] 

    final_response = get_completion_from_messages(messages)
    return final_response


def generate_output_string(category_and_product_list):
    output_string = ''
    for item in category_and_product_list:
        output_string += f"{item}\n"
    return output_string

def read_string_to_list(input_string):
    result = json.loads(input_string)
    return result
import json
from collections import defaultdict

def get_products_and_category(products):
    products_by_category = defaultdict(list)
    for product_name, product_info in products.items():
        category = product_info.get('category')
        if category:
            products_by_category[category].append(product_info.get('name'))
    
    return dict(products_by_category)

def read_string_to_list(input_string):
    result = json.loads(input_string)
    return result

def find_category_and_product_only(user_input, products_and_category):
    delimiter = "####"
    system_message = f"""
    You will be provided with former's queries. 
    The former's query will be delimited with {delimiter} characters.
    Output a Python list of objects, where each object has the following format:
        'agriculture category': <Crops, Livestock, Fisheries, Forestry, Agrochemicals, Agri-inputs, Agri-food processing, Agro-allied products>,
    OR
        'products': <a list of products that must be found in the allowed products list below>

    Where the categories and products must be found in the former's service query.
    If a product is mentioned, it must be associated with the correct category in the allowed products list below.
    If no products or categories are found, output an empty list.

    Allowed products: 

    1. Crops:
       - Cereals (e.g., rice, wheat, corn)
       - Fruits (e.g., apples, oranges, bananas)
       - Vegetables (e.g., tomatoes, potatoes, carrots)
       - Pulses (e.g., lentils, chickpeas, beans)
       - Oilseeds (e.g., soybeans, sunflower, canola)
       - Spices (e.g., pepper, cinnamon, turmeric)

    2. Livestock:
       - Dairy products (e.g., milk, cheese, yogurt)
       - Meat products (e.g., beef, pork, poultry)
       - Eggs
       - Wool and fibers (e.g., wool, silk)
       - Honey

    3. Aquaculture:
       - Fish (e.g., salmon, tilapia, trout)
       - Shrimp
       - Oysters
       - Seaweed

    4. Forestry products:
       - Timber (e.g., pine, oak, teak)
       - Pulp and paper
       - Resins and gums

    5. Horticulture products:
       - Flowers (e.g., roses, lilies, orchids)
       - Nursery plants (e.g., tree saplings, ornamental plants)
       - Medicinal plants
       - Aromatic plants
   
    Only output the list of objects, nothing else.
    """
    messages = [  
        {'role': 'system', 'content': system_message},    
        {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"},  
    ] 
    return get_completion_from_messages(messages)


 