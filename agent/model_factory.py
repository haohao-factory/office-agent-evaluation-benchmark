import os
def model_config(): return {"model":os.getenv("OPENAI_MODEL"),"base_url":os.getenv("OPENAI_BASE_URL"),"api_key_configured":bool(os.getenv("OPENAI_API_KEY"))}
