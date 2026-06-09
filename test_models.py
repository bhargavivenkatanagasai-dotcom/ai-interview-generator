from google import genai

client = genai.Client(
    api_key=""
)

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello"
    )
    print(response.text)
except Exception as e:
    print("ERROR:", e)