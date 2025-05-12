from google.adk.agents import Agent
from google.adk.tools import google_search
import pandas as pd

# Load HSN Master Data (from Excel)
def load_hsn_master(file_path):
    """Load the Excel file with HSN master data."""
    try:
        df = pd.read_excel(file_path, dtype=str)
        df.columns = df.columns.str.strip()
        if 'HSNCode' not in df.columns or 'Description' not in df.columns:
            raise ValueError("Excel must have 'HSNCode' and 'Description' columns.")
        return df
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None

# Validate HSN Code logic
def validate_hsn_code(code, df):
    """Validates HSN code and fetches description."""
    if not code.isdigit() or not (2 <= len(code) <= 8):
        return f"Invalid format: HSN code should be numeric and between 2 to 8 digits."
    
    if code in df['HSNCode'].values:
        description = df.loc[df['HSNCode'] == code, 'Description'].values[0]
        return f"Valid HSN Code: {description}"
    else:
        return f"HSN Code '{code}' not found in the master data."

# Define the Agent with Google ADK
root_agent = Agent(
    name="hsn_code_validator",
    model="gemini-2.0-flash",  # You can replace this with your preferred model
    instruction="You are an assistant that helps users validate HSN codes. Use the provided dataset to validate the code, return a description, and report any issues.",
    description="An agent for validating HSN codes based on a given dataset.",
    tools=[google_search],  # Use google_search as a tool if needed
)

# Define the function to handle HSN code validation
def handle_hsn_code_validation(query, df):
    """Handles the HSN code validation based on the user's input."""
    hsn_code = query.strip()
    if hsn_code:
        validation_result = validate_hsn_code(hsn_code, df)
        return validation_result
    else:
        return "❌ Invalid input. Please provide a valid HSN code."

# Main logic to run the agent
def main():
    print("\n🔍 HSN Code Validation Agent using Google ADK")

    # Hardcoded file path for HSN master data Excel
    file_path = "/workspaces/HSN/HSN_SAC.xlsx" # Replace this with the actual file path
    
    # Load the HSN master data
    df = load_hsn_master(file_path)
    
    if df is None:
        return

    while True:
        # Get user input
        user_input = input("\n➡️ Enter HSN code for validation or type 'exit': ").strip()

        if user_input.lower() == 'exit':
            print("👋 Exiting the validator. Goodbye!")
            break

        # Process the query using the agent
        response = handle_hsn_code_validation(user_input, df)
        print(f"✅ {response}")

# Run the agent
if __name__ == "__main__":
    main()
