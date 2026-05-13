API_KEY = "AIzaSyDZnf3yvP30HHUQd8kqc_-_8abP6KVTaEk"

try:
    from google import genai
    GENAI_IMPL = "genai"
except ImportError:
    try:
        import google.generativeai as genai
        GENAI_IMPL = "generativeai"
    except ImportError as exc:
        raise ImportError(
            "Could not import google.genai or google.generativeai. "
            "Install one of these packages in the environment used to run this script."
        ) from exc

if GENAI_IMPL == "genai":
    client = genai.Client(api_key=API_KEY)
else:
    genai.configure(api_key=API_KEY)
    client = genai

try:
    # Testing with the latest available model (e.g., gemini-2.0-flash)
    if GENAI_IMPL == "genai":
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Write a 3-word slogan for a tech company."
        )
    else:
        model = client.GenerativeModel(model_name="gemini-2.5-flash")
        response = model.generate_content("Write a 3-word slogan for a tech company.")

    print(f"Model Output: {getattr(response, 'text', response)}")
    print("✅ Connection Verified.")
except Exception as e:
    print(f"❌ Connection Failed: {e}")

