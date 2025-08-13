from .config import OPENAI_API_KEY
import redis, hashlib, json
from openai import OpenAI

oai_client = OpenAI(api_key=OPENAI_API_KEY)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_embedding(client, text, model):
    text_hash = hashlib.sha256(text.encode()).hexdigest()
    cache_key = f"{model}_{text_hash}"
    cached_response = redis_client.get(cache_key)

    if cached_response:
        print("found response in cache")
        return json.loads(cached_response)

    print("no response in cache, obtaining embedding from LLM")
    response = client.embeddings.create(
                    input=text,
                    model=model,
                )

    embedding = response.data[0].embedding
    redis_client.set(cache_key, json.dumps(embedding))
    return embedding
