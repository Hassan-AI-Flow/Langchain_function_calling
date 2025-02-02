from dotenv import load_dotenv
import os 



load_dotenv()


Google_Api_Key = os.environ.get("Gemini_Api_Key")

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.tools import Tool
import requests
import yfinance as yf
from langchain.agents import initialize_agent , AgentType
import streamlit as st


llm = ChatGoogleGenerativeAI(
    model= "gemini-1.5-flash",
    api_key = Google_Api_Key
)

@tool
def get_current_weather(location = "Pakistan", api_key = "8525663aca9a9324818d30b00267c3c1")-> dict:
    """
    Fetches the current weather for a given location.

    Parameters:
        location (str): The location for which weather data is to be fetched (city name or coordinates).
        api_key (str): Your OpenWeatherMap API key.

    Returns:
        dict: A dictionary containing weather information or an error message.
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q":location ,  # Query location
        "appid": api_key,  # Your API key
        "units": "metric"  # Temperature in Celsius
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        data = response.json()

        # Parse important data
        weather_info = {
            "location": data.get("name"), 
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
        return weather_info

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}




@tool
def get_stock_price(stock_symbol: str) -> str:
    """
    Function to fetch the latest stock price using Yahoo Finance.

    Parameters:
    stock_symbol (str): The symbol of the stock whose price needs to be fetched (e.g., 'AAPL' for Apple, 'TSLA' for Tesla).

    Returns:
    str: The latest stock price or an error message if the stock cannot be found.

    Example:
    >>> get_stock_price("AAPL")
    "The latest price for AAPL is $175.30."
    """
    print("function is called")

    try:
        # Fetch stock data using Yahoo Finance
        stock = yf.Ticker(stock_symbol)
        stock_info = stock.history(period="1d")  # Get the most recent stock price

        if stock_info.empty:
            return f"Error: No data available for stock symbol {stock_symbol}."

        # Extract the latest closing price
        latest_price = stock_info['Close'].iloc[0]

        # Format the result
        return f"The latest price for {stock_symbol} is ${latest_price:.2f}."

    except Exception as e:
        return f"Error fetching stock price: {str(e)}"


@tool
def calculator(expression):
  "this is calculator for evaluate any math expression"
  def add(a: float, b: float) -> float:
      """
      Adds two numbers and returns the result.

      Args:
          a (float): The first number.
          b (float): The second number.

      Returns:
          float: The sum of `a` and `b`.

      Examples:
          >>> add(3, 5)
          8
      """
      return a + b


  def subtract(a: float, b: float) -> float:
      """
      Subtracts the second number from the first and returns the result.

      Args:
          a (float): The first number.
          b (float): The second number.

      Returns:
          float: The difference of `a` and `b`.

      Examples:
          >>> subtract(10, 4)
          6
      """
      return a - b


  def multiply(a: float, b: float) -> float:
      """
      Multiplies two numbers and returns the result.

      Args:
          a (float): The first number.
          b (float): The second number.

      Returns:
          float: The product of `a` and `b`.

      Examples:
          >>> multiply(2, 3)
          6
      """
      return a * b


  def divide(a: float, b: float) -> float:
      """
      Divides the first number by the second and returns the result.

      Args:
          a (float): The numerator.
          b (float): The denominator.

      Returns:
          float: The quotient of `a` and `b`.

      Raises:
          ValueError: If `b` is zero.

      Examples:
          >>> divide(10, 2)
          5.0
      """
      if b == 0:
          raise ValueError("Division by zero is not allowed.")
      return a / b


  def power(base: float, exponent: float) -> float:
      """
      Raises a number to a specified power.

      Args:
          base (float): The base number.
          exponent (float): The exponent.

      Returns:
          float: `base` raised to the power of `exponent`.

      Examples:
          >>> power(2, 3)
          8
      """
      return math.pow(base, exponent)


  def square_root(number: float) -> float:
      """
      Calculates the square root of a number.

      Args:
          number (float): The number to find the square root of.

      Returns:
          float: The square root of `number`.

      Raises:
          ValueError: If `number` is negative.

      Examples:
          >>> square_root(16)
          4.0
      """
      if number < 0:
          raise ValueError("Cannot calculate the square root of a negative number.")
      return math.sqrt(number)


  def calculator():
      """
      A simple calculator that lets users perform basic math operations.
      """
      print("Welcome to the Calculator!")
      print("Operations:")
      print("1. Addition (+)")
      print("2. Subtraction (-)")
      print("3. Multiplication (*)")
      print("4. Division (/)")
      print("5. Power (^)")
      print("6. Square Root (√)")
      print("Type 'exit' to quit.")

      while True:
          operation = input("\nEnter the operation you want to perform: ").strip().lower()

          if operation == "exit":
              print("Thank you for using the Calculator. Goodbye!")
              break

          try:
              if operation in ['+', '1', 'addition']:
                  a = float(input("Enter the first number: "))
                  b = float(input("Enter the second number: "))
                  print(f"Result: {add(a, b)}")

              elif operation in ['-', '2', 'subtraction']:
                  a = float(input("Enter the first number: "))
                  b = float(input("Enter the second number: "))
                  print(f"Result: {subtract(a, b)}")

              elif operation in ['*', '3', 'multiplication']:
                  a = float(input("Enter the first number: "))
                  b = float(input("Enter the second number: "))
                  print(f"Result: {multiply(a, b)}")

              elif operation in ['/', '4', 'division']:
                  a = float(input("Enter the numerator: "))
                  b = float(input("Enter the denominator: "))
                  print(f"Result: {divide(a, b)}")

              elif operation in ['^', '5', 'power']:
                  base = float(input("Enter the base number: "))
                  exponent = float(input("Enter the exponent: "))
                  print(f"Result: {power(base, exponent)}")

              elif operation in ['√', '6', 'square root']:
                  number = float(input("Enter the number: "))
                  print(f"Result: {square_root(number)}")

              else:
                  print("Invalid operation. Please try again.")
          except ValueError as e:
              print(f"Error: {e}")


@tool
def news(api_key = "39f54e1bc5cd444d960059aa227a0b77", country='us', category=None):
    """
    Fetches the latest news headlines from a specified country and category using the NewsAPI.

    Parameters:
        api_key (str): Your API key for accessing the NewsAPI.
        country (str): The country code for the news (default is 'us').
                      Example: 'us' for United States, 'in' for India.
        category (str): The news category to filter by (default is None).
                        Example categories: 'business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology'.

    Returns:
        dict: A dictionary containing the status, total results, and a list of articles.
              Each article includes keys like 'source', 'author', 'title', 'description', 'url', 'publishedAt', etc.

    Raises:
        ValueError: If the API response indicates an error or invalid parameters.

    Example:
        >>> api_key = 'api_ley'
        >>> headlines = news(api_key, country='us', category='technology')
        >>> for article in headlines['articles']:
        ...     print(article['title'])
    """
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'apiKey': api_key,
        'country': country,
        'category': category
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200 or data.get('status') != 'ok':
        raise ValueError(f"Error fetching news: {data.get('message', 'Unknown error')}")

    return data


@tool
def biryani_recipe():
    """
    This function interacts with the LLM to fetch a detailed recipe for making Biryani in a structured document format.
    It returns the recipe in a professional and clear format, using a step-by-step approach.
    """
    # Prompt for the LLM to generate the Biryani recipe in document style
    prompt = """
    Provide a detailed step-by-step recipe for making a traditional Biryani, formatted in a document style. 
    Include the following sections: Ingredients, Preparation Time, Cooking Instructions, and Tips for Perfection. 
    The recipe should be easy to follow and include common variations.
    """
    # Format the recipe into a clean, document-style format
    formatted_recipe = f"""
    Biryani Recipe:
    
    1. Ingredients:
    - Basmati Rice (2 cups)
    - Chicken (500g, cut into pieces)
    - Onion (2, thinly sliced)
    - Tomatoes (2, chopped)
    - Ginger-Garlic Paste (2 tbsp)
    - Biryani Masala (2 tbsp)
    - Yogurt (1 cup)
    - Fresh Coriander and Mint Leaves (chopped)
    - Whole Spices: Cinnamon, Cloves, Cardamom, Bay Leaf
    - Ghee (2 tbsp)
    - Salt to taste
    - Water (4 cups for cooking rice)

    2. Preparation Time: 1 Hour 30 Minutes

    3. Cooking Instructions:
    a. Rinse the basmati rice and soak for 30 minutes.
    b. In a large pot, heat ghee and sauté the whole spices.
    c. Add onions and sauté until golden brown. Remove half for garnishing.
    d. Add ginger-garlic paste and cook for 2 minutes.
    e. Add chicken pieces and cook until they turn white.
    f. Add chopped tomatoes and cook until soft. Add biryani masala and yogurt. Stir well.
    g. Add fresh coriander and mint leaves. Cook for 5 minutes.
    h. Add water, bring to a boil, then reduce heat to simmer for 20 minutes.
    i. In another pot, boil water with salt and cook the soaked rice until 70% done.
    j. Layer the partially cooked rice on top of the chicken. Cover with a lid, seal the edges with dough, and cook on low heat (Dum) for 20-25 minutes.

    4. Tips for Perfection:
    - Always use high-quality basmati rice for best aroma and texture.
    - Let the biryani rest for 10 minutes after cooking before serving.
    - Garnish with fried onions, fresh coriander, and mint for extra flavor.

    Enjoy your homemade Biryani!

    """
    
    return formatted_recipe



tools = [get_current_weather , news , calculator , get_stock_price , biryani_recipe]

agent = initialize_agent(tools , llm , agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION )


# App title with emojis and custom styling
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(to right, #FFB6C1, #FF6347);
            font-family: 'Arial', sans-serif;
            animation: gradient 6s ease infinite;
        }

        @keyframes gradient {
            0% { background: linear-gradient(to right, #FFB6C1, #FF6347); }
            50% { background: linear-gradient(to right, #FF6347, #FFD700); }
            100% { background: linear-gradient(to right, #FFB6C1, #FF6347); }
        }

        .title {
            font-size: 45px;
            color: #FF1493;
            font-weight: bold;
            text-align: center;
            text-shadow: 3px 3px 10px rgba(0, 0, 0, 0.3);
            animation: bounce 1s infinite alternate;
        }

        @keyframes bounce {
            0% { transform: translateY(0); }
            100% { transform: translateY(-10px); }
        }

        .subtitle {
            font-size: 20px;
            text-align: center;
            color: #800080;
            font-style: italic;
            margin-top: 10px;
        }

        .welcome-note {
            font-size: 22px;
            color: #008080;
            text-align: center;
            font-style: italic;
            margin-top: 30px;
            font-weight: 500;
        }

        .sidebar-title {
            font-size: 22px;
            color: #FFFFFF;
            background-color: #4B0082;
            padding: 12px;
            border-radius: 10px;
        }

        .sidebar {
            background-color: #F0F8FF;
        }

        .button {
            background-color: #FF4500;
            color: white;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 20px;
            margin-top: 20px;
            transition: transform 0.3s ease-in-out;
        }

        .button:hover {
            transform: scale(1.1);
        }

        .input {
            width: 100%;
            padding: 12px;
            font-size: 18px;
            border-radius: 10px;
            margin-top: 20px;
            border: 2px solid #4B0082;
        }

        .tools-list {
            font-size: 18px;
            color: #4B0082;
            padding: 10px;
            background-color: #F5F5F5;
            margin-bottom: 10px;
            border-radius: 8px;
            transition: background-color 0.3s ease;
            cursor: pointer;
        }

        .tools-list:hover {
            background-color: #FFD700;
        }

        .tools-icon {
            font-size: 24px;
            color: #FF6347;
            margin-right: 10px;
        }

        .tooltip {
            visibility: hidden;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 5px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 150%;
            left: 50%;
            margin-left: -60px;
        }

        .tools-list:hover .tooltip {
            visibility: visible;
        }
    </style>
    """, unsafe_allow_html=True
)

# App title with emojis
st.markdown('<div class="title">Tool Calling App✨😊</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">✨Include LLM and some extra tools for resolving your queries✨</div>', unsafe_allow_html=True)

# Welcome Note with emojis
st.markdown('<div class="welcome-note">👋 Welcome to the Tool Calling App! Ask me anything, and I’ll help you with your queries😊</div>', unsafe_allow_html=True)

# Sidebar with tools menu and emojis
st.sidebar.markdown('<div class="sidebar-title">Tools🛠️</div>', unsafe_allow_html=True)
tools = [
    ("1️⃣ Get Current Weather 🌤️", "Find the current weather information for your location."),
    ("2️⃣ News 📰", "Stay up-to-date with the latest news headlines."),
    ("3️⃣ Calculator 🧮", "Perform simple mathematical operations."),
    ("4️⃣ Get Stock Price 📈", "Check the current stock prices of your favorite companies."),
    ("5️⃣ Biryani Recipe 🍛🍴", "Learn how to make delicious biryani from scratch!")
]

# Loop over tools and display each one
for tool, description in tools:
    st.sidebar.markdown(f'<div class="tools-list">{tool}<span class="tooltip">{description}</span></div>', unsafe_allow_html=True)

# Main input area with emoji hint
user_input = st.text_input("Ask anything ✨💬", key="user_input", label_visibility="hidden")

# Submit button with emojis and hover effect
if st.button("Submit✨😊", key="submit", help="Click to get the response", use_container_width=True):
    # Call your agent to process the input
    result = agent.invoke(user_input)
    st.write(result["output"])

# Footer with lighthearted message
st.markdown('<div class="footer">Made with ❤️ by your friendly assistant! ✨</div>', unsafe_allow_html=True)


