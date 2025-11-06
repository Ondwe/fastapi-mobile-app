# Read the file
with open('working_app.py', 'r') as f:
    content = f.read()

# Replace ANY API key with the new one
import re

# This will replace any API key pattern with the new one
content = re.sub(
    r'GEMINI_API_KEY\s*=\s*["\'][^"\']*["\']',
    'GEMINI_API_KEY = "AIzaSyA5CuKcnLaosr7NEMn9e75VxUGdz5XcoT4"',
    content
)

# Write back
with open('working_app.py', 'w') as f:
    f.write(content)

print("✅ API Key updated successfully!")
print("New key: AIzaSyA5CuKcnLaosr7NEMn9e75VxUGdz5XcoT4")
