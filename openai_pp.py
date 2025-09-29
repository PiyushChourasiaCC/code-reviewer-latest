import openai
import glob
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Path to your directory containing class files
cls_dir = 'force-app/main/default/classes'

# Gather all .cls files in the specified directory
cls_files = glob.glob(os.path.join(cls_dir, '*.cls'))

# File to store the review results
output_file = 'ai_code_reviews.txt'

all_reviews = []

for cls_file in cls_files:
    with open(cls_file, 'r') as file:
        code = file.read()
    
    prompt = f"""
    Review the following Salesforce Apex code and provide me a summary table with few columns describing risk count, notes, potential fix, and checks. Check for:
    - Exception logging with add to ExceptionLog
    - Exception handling best practices
    - Global interface classes
    - Presence of Jira numbers in comments
    - Salesforce coding standards (no hardcoded IDs, bulkification, etc.)
    - Anything that could indicate tech debt or security risk
    File: {os.path.basename(cls_file)}
    Code:
    {code}

    """
    
    response = openai.responses.create(
        model="gpt-4.1",
        input=[{"role": "user", "content": prompt}]
    )
    review = f"\n=== Review: {os.path.basename(cls_file)} ===\n{response.output[0].content[0].text}\n"
    all_reviews.append(review)

# Write all reviews to the output file
with open(output_file, 'w') as out:
    out.writelines(all_reviews)

