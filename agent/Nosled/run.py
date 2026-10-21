import json
import ollama
import pyautogui
import time
import pyperclip

task = input("What task should the agent perform? ")

prompt = f"""You are the task planner for a desktop AI agent. Convert the user's request into a sequence of actions. 

Available actions:
1. open_website (Required parameter: url, Optional: query)
2. open_application (Required parameter: name)
3. search_web (Required parameter: query)

Rules:
* Return valid JSON only.
* Do not use Markdown code fences.
* Do not invent new action types.
* Use a maximum of 10 steps.
* Do not claim that an action has been executed.
* If the task requires an unavailable capability, return an error explaining what is missing.
* When the user wants to open a website and search for something on it, use one open_website action containing both url and query.

Use this JSON structure:
{{
    "task": "Short description",
    "steps": [
        {{
            "action": "open_website",
            "url": "https://youtube.com",
            "query": "Search Term"
        }}
    ]
}}

User's task: {task}"""

# 3. Calls the Ollama API using Gemma 3.
try:
    response = ollama.chat(
        model="gemma3:4b",
        messages=[{"role": "user", "content": prompt}],
        format="json",  # Forces the model to respond in valid JSON
    )

    # 4. Extract the content from the response
    result = response["message"]["content"]

    # 5. Parse and print the valid JSON plan
    plan = json.loads(result)
    print("\n--- AI GENERATED PLAN ---\n") 
    print(json.dumps(plan, indent=4))

except json.JSONDecodeError:
    print("\n[Error] The model did not return valid JSON.")
    print("Raw output:")
    print(result)
except Exception as e:
    print(f"\n[An error occurred]: {e}")


for step in plan["steps"]:
    action = step.get("action")
    query = step.get("query")
    url = step.get("url")
    name = step.get("name")

    if(action == "open_website"):
        query = step.get("query")

        pyautogui.press("win")
        time.sleep(2)

        pyautogui.write("chrome")
        pyautogui.press("enter")

        time.sleep(2)

        pyautogui.write(url)
        pyautogui.press("enter")

        time.sleep(4)
        pyautogui.hotkey("/")

        pyautogui.write(query)
        pyautogui.press("enter")

        time.sleep(20)

   
    elif (action == "open_application"):
        pyautogui.press("win")
        time.sleep(2)
        
        pyautogui.write(name)
        pyautogui.press("enter")
        
    elif (action == "search_web"):

        user = (
                f"Research this topic in detail: {query}. "
                "Use web search if available. Prioritize current, reliable sources. "
                "Include key findings, relevant dates, and source links. "
                "Clearly distinguish verified facts from analysis."
            )
        
        pyautogui.press("win")
        time.sleep(2)
    
        pyautogui.write("chrome")
        pyautogui.press("enter")
    
        time.sleep(2)
    
        pyautogui.write("https://chatgpt.com/?temporary-chat=true")
        pyautogui.press("enter")
    
        time.sleep(4)
    
        pyautogui.write(user)
        pyautogui.press("enter")
    
        time.sleep(20)
    
        pyautogui.click(x=500, y=500) 
        time.sleep(1)
    
        # 2. Press Ctrl + A (Select All)
        pyautogui.hotkey("ctrl", "a")
        time.sleep(1)
    
        # 3. Press Ctrl + C (Copy)
        pyautogui.hotkey("ctrl", "c")
        time.sleep(2)
    
        pyautogui.hotkey("alt", "F4")
        time.sleep(2)
    
        # 4. Pull the text from your system clipboard into Python
        '''search_results_text = pyperclip.paste()
    
        print("--- Extracted Text ---")
        print(search_results_text[:1000000])'''
    
        pyautogui.press("win")
        time.sleep(2)
    
        pyautogui.write("notepad.exe")
        pyautogui.press("enter")
    
        time.sleep(5)
    
        pyautogui.click(x=500, y=500) 
        time.sleep(3)
    
        pyautogui.hotkey("ctrl", "v")
        time.sleep(5)
    
        pyautogui.hotkey("ctrl", "shift", "s")
        time.sleep(2)
    
        pyautogui.write("query")
        pyautogui.press("enter")
else:
     print("unknown")


