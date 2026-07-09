# Setup

1. Install dependencies

pip install -r requirements.txt


2. Add your API key

Open the project files and replace:

api_key="YOUR_API_KEY"

with your own Anthropic API key.


3. Run the project

python main.py

Sequence Of Events
User
   |
   v
main.py
   |
   v
ai_agent()
   |
   +----------------------+
   | Store Conversation   |
   +----------------------+
   |
   v
Claude API
   |
   | Chooses Tool
   v
Tool Dispatcher
   |
   +----------------------+
   | search_flights()     |
   | book_flight()        |
   | cancel_flight()      |
   +----------------------+
   |
   v
tools.py
   |
   v
Tool Result
   |
   v
Conversation History Updated
   |
   v
current_flight Updated
   |
   v
Formatted Response
   |
   v
main.py
   |
   v
User