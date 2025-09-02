# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Optional
# import groq
# import os
# import re

# app = FastAPI(
#     title="T-Shirt Color Detection API",
#     description="API to detect t-shirt colors from text using Llama 3 via Groq",
#     version="1.0.0"
# )

# # Initialize Groq client
# try:
#     # Get API key from environment variable
#     os.environ["GROQ_API_KEY"] = ""
#     api_key = os.getenv("GROQ_API_KEY")
#     if not api_key:
#         raise ValueError("GROQ_API_KEY environment variable not set")
    
#     client = groq.Groq(api_key=api_key)
# except Exception as e:
#     print(f"Error initializing Groq client: {e}")
#     client = None

# class TextRequest(BaseModel):
#     text: str

# class ColorResponse(BaseModel):
#     original_text: str
#     detected_color: Optional[str] = None
#     confidence: Optional[str] = None
#     error: Optional[str] = None

# def extract_color_from_response(response_text):
#     """
#     Extract color information from the model response.
#     This function tries to parse the response to find the color.
#     """
#     # Look for patterns that might indicate a color in the response
#     color_patterns = [
#         r'color[:\s]+([a-zA-Z\s]+)',
#         r'([a-zA-Z\s]+)(?=\s*color)',
#         r'is\s+([a-zA-Z\s]+)',
#         r'([a-zA-Z\s]+)(?=\s*shirt)',
#     ]
    
#     # Common color list to validate against
#     common_colors = [
#         "red", "blue", "green", "yellow", "black", "white", 
#         "gray", "grey", "orange", "purple", "pink", "brown",
#         "navy", "maroon", "teal", "olive", "cyan", "magenta",
#         "lavender", "turquoise", "beige", "cream", "gold", "silver"
#     ]
    
#     # First, try to find any color mentioned in the response
#     for color in common_colors:
#         if color in response_text.lower():
#             return color.capitalize(), "high"
    
#     # If no direct color match, try patterns
#     for pattern in color_patterns:
#         match = re.search(pattern, response_text, re.IGNORECASE)
#         if match:
#             potential_color = match.group(1).strip().lower()
#             if any(color in potential_color for color in common_colors):
#                 for color in common_colors:
#                     if color in potential_color:
#                         return color.capitalize(), "medium"
    
#     return None, "low"

# @app.post("/detect-color", response_model=ColorResponse)
# async def detect_color(request: TextRequest):
#     """
#     Detect t-shirt color from text description using Llama 3 via Groq
#     """
#     if client is None:
#         raise HTTPException(status_code=500, detail="Groq client not initialized")
    
#     try:
#         # Create a prompt for the LLM
#         prompt = f"""
#         Analyze the following text and identify the color of the t-shirt mentioned.
#         If no t-shirt color is mentioned, respond with "No color detected".
#         Text: "{request.text}"
        
#         Please provide only the color name in your response, or "No color detected".
#         """
        
#         # Call Groq API
#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "You are a helpful assistant that detects clothing colors from text descriptions. Your responses should be concise and only include the color name or 'No color detected'."
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             model="llama-3.1-8b-instant",  # Using Llama 3 8B model
#             temperature=0.1,  # Low temperature for more deterministic responses
#             max_tokens=10
#         )
        
#         # Get the response
#         response_text = chat_completion.choices[0].message.content.strip()
        
#         # Check if no color was detected
#         if "no color detected" in response_text.lower():
#             return ColorResponse(
#                 original_text=request.text,
#                 detected_color=None,
#                 confidence=None,
#                 error="No color detected in the text"
#             )
        
#         # Extract color from the response
#         detected_color, confidence = extract_color_from_response(response_text)
        
#         if detected_color:
#             return ColorResponse(
#                 original_text=request.text,
#                 detected_color=detected_color,
#                 confidence=confidence
#             )
#         else:
#             return ColorResponse(
#                 original_text=request.text,
#                 detected_color=None,
#                 confidence=None,
#                 error="Could not determine color from the response"
#             )
            
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# @app.get("/")
# async def root():
#     return {"message": "T-Shirt Color Detection API. Use POST /detect-color with text to detect colors."}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)



# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Optional, Dict, Any
# import groq
# import os
# import re
# import json

# app = FastAPI(
#     title="Dynamic Product Type Detection API",
#     description="API to detect product niche and specific types from text using Llama 3 via Groq",
#     version="1.0.0"
# )

# # Initialize Groq client
# try:
#     os.environ["GROQ_API_KEY"] = ""
#     api_key = os.getenv("GROQ_API_KEY")
#     if not api_key:
#         raise ValueError("GROQ_API_KEY environment variable not set")
    
#     client = groq.Groq(api_key=api_key)
# except Exception as e:
#     print(f"Error initializing Groq client: {e}")
#     client = None

# class TextRequest(BaseModel):
#     text: str

# class ProductResponse(BaseModel):
#     original_text: str
#     detected_niche: Optional[str] = None
#     detected_product_type: Optional[str] = None
#     confidence: Optional[str] = None
#     error: Optional[str] = None

# # Define common niches and their product types
# PRODUCT_CATEGORIES = {
#     "shoe": ["sneakers", "runners", "joggers", "sports shoes", "athletic shoes", 
#              "boots", "sandals", "flip flops", "loafers", "formal shoes", "heels"],
#     "shirt": ["t-shirt", "polo", "polo shirt", "full sleeves", "long sleeves",
#               "short sleeves", "button-down", "dress shirt", "casual shirt", "formal shirt"],
#     "vape": ["watermelon lime", "fresh mint", "passionfruit orange guava", "menthol",
#              "tobacco", "berry blast", "mango", "strawberry", "vanilla", "coffee"],
#     "pants": ["jeans", "trousers", "chinos", "sweatpants", "leggings", "shorts",
#               "cargo pants", "formal pants", "track pants", "yoga pants"],
#     "electronics": ["smartphone", "laptop", "tablet", "headphones", "earbuds",
#                     "smartwatch", "camera", "gaming console", "tv", "monitor"],
#     "cosmetics": ["lipstick", "foundation", "mascara", "eyeliner", "blush",
#                   "moisturizer", "serum", "sunscreen", "perfume", "nail polish"]
# }

# def detect_niche_and_product(text: str, model_response: str) -> tuple:
#     """
#     Detect niche and product type from the model response and original text
#     """
#     # Convert to lowercase for easier matching
#     text_lower = text.lower()
#     response_lower = model_response.lower()
    
#     # First, try to detect the niche
#     detected_niche = None
#     detected_product = None
#     confidence = "low"
    
#     # Check for each niche in the text and response
#     for niche, products in PRODUCT_CATEGORIES.items():
#         # Check if niche is mentioned
#         if niche in text_lower or niche in response_lower:
#             detected_niche = niche
#             confidence = "medium"
            
#             # Now try to detect specific product type
#             for product in products:
#                 if product in text_lower or product in response_lower:
#                     detected_product = product
#                     confidence = "high"
#                     break
            
#             # If no specific product found but niche is detected
#             if not detected_product:
#                 # Try to extract product from response using patterns
#                 product_patterns = [
#                     r'product[:\s]+([a-zA-Z\s]+)',
#                     r'type[:\s]+([a-zA-Z\s]+)',
#                     r'is\s+([a-zA-Z\s]+)',
#                     r'([a-zA-Z\s]+)(?=\s*(shoe|shirt|vape|pants|electronics|cosmetics))',
#                 ]
                
#                 for pattern in product_patterns:
#                     match = re.search(pattern, response_lower)
#                     if match:
#                         potential_product = match.group(1).strip()
#                         # Check if this matches any known product type
#                         for product in products:
#                             if product in potential_product:
#                                 detected_product = product
#                                 confidence = "medium"
#                                 break
#                         if detected_product:
#                             break
            
#             break
    
#     return detected_niche, detected_product, confidence

# @app.post("/detect-product", response_model=ProductResponse)
# async def detect_product(request: TextRequest):
#     """
#     Detect product niche and type from text description using Llama 3 via Groq
#     """
#     if client is None:
#         raise HTTPException(status_code=500, detail="Groq client not initialized")
    
#     try:
#         # Create a more sophisticated prompt for the LLM
#         prompt = f"""
#         Analyze the following text and identify:
#         1. The product niche/category (shoe, shirt, vape, pants, electronics, cosmetics, or other)
#         2. The specific product type within that niche
        
#         Text: "{request.text}"
        
#         Respond in JSON format with the following structure:
#         {{
#             "niche": "detected niche or null",
#             "product_type": "detected product type or null",
#             "explanation": "brief explanation of your analysis"
#         }}
        
#         If you cannot determine either, use null values.
#         """
        
#         # Call Groq API
#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "system",
#                     "content": """You are a product classification expert. Analyze text to identify 
#                     product categories and specific types. Always respond with valid JSON in the 
#                     specified format. Be concise and accurate."""
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             model="llama-3.1-8b-instant",
#             temperature=0.1,
#             max_tokens=150
#         )
        
#         # Get the response
#         response_text = chat_completion.choices[0].message.content.strip()
        
#         # Try to parse JSON response
#         try:
#             # Extract JSON from response (in case there's additional text)
#             json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
#             if json_match:
#                 response_data = json.loads(json_match.group())
#             else:
#                 response_data = {"niche": None, "product_type": None}
#         except json.JSONDecodeError:
#             # If JSON parsing fails, fall back to text analysis
#             response_data = {"niche": None, "product_type": None}
        
#         # Extract from JSON response or fall back to text analysis
#         if response_data.get("niche") and response_data.get("product_type"):
#             detected_niche = response_data["niche"]
#             detected_product = response_data["product_type"]
#             confidence = "high"
#         else:
#             # Fallback: Use our pattern matching approach
#             detected_niche, detected_product, confidence = detect_niche_and_product(
#                 request.text, response_text
#             )
        
#         if detected_niche:
#             return ProductResponse(
#                 original_text=request.text,
#                 detected_niche=detected_niche,
#                 detected_product_type=detected_product,
#                 confidence=confidence
#             )
#         else:
#             return ProductResponse(
#                 original_text=request.text,
#                 detected_niche=None,
#                 detected_product_type=None,
#                 confidence=None,
#                 error="No product niche detected in the text"
#             )
            
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# @app.get("/categories")
# async def get_categories():
#     """
#     Get available product categories and their types
#     """
#     return PRODUCT_CATEGORIES

# @app.post("/add-category")
# async def add_category(category_data: Dict[str, Any]):
#     """
#     Add a new product category or update existing one
#     """
#     try:
#         category = category_data.get("category")
#         products = category_data.get("products", [])
        
#         if not category or not products:
#             raise HTTPException(status_code=400, detail="Category and products are required")
        
#         PRODUCT_CATEGORIES[category.lower()] = [p.lower() for p in products]
#         return {"message": f"Category '{category}' added/updated successfully"}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/")
# async def root():
#     return {
#         "message": "Dynamic Product Type Detection API",
#         "endpoints": {
#             "POST /detect-product": "Detect product niche and type from text",
#             "GET /categories": "View available product categories",
#             "POST /add-category": "Add new product category"
#         }
#     }

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)



############## v3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import groq
import os
import re
import json

app = FastAPI(
    title="Dynamic Product Type Detection API",
    description="API to detect product niche and specific types from text using Llama 3 via Groq",
    version="2.0.0"
)

# Initialize Groq client
try:
    os.environ["GROQ_API_KEY"] = ""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")
    
    client = groq.Groq(api_key=api_key)
except Exception as e:
    print(f"Error initializing Groq client: {e}")
    client = None

class TextRequest(BaseModel):
    text: str

class ProductResponse(BaseModel):
    original_text: str
    detected_niche: Optional[str] = None
    detected_product_type: Optional[str] = None
    confidence: Optional[str] = None
    error: Optional[str] = None

# Enhanced product categories with context clues
PRODUCT_CATEGORIES = {
    "vape": {
        "products": ["watermelon lime", "fresh mint", "passionfruit orange guava", "menthol",
                    "tobacco", "berry blast", "mango", "strawberry", "vanilla", "coffee",
                    "ice mint", "cool mint", "fruit", "dessert", "beverage"],
        "context_clues": ["flavour", "flavor", "juice", "vape", "e-liquid", "e-juice", 
                         "disposable", "pod", "nicotine", "mg/ml", "puff", "vaping"]
    },
    "shoe": {
        "products": ["sneakers", "runners", "joggers", "sports shoes", "athletic shoes", 
                    "boots", "sandals", "flip flops", "loafers", "formal shoes", "heels"],
        "context_clues": ["shoe", "footwear", "sneaker", "running", "walking", "comfort"]
    },
    "shirt": {
        "products": ["t-shirt", "polo", "polo shirt", "full sleeves", "long sleeves",
                    "short sleeves", "button-down", "dress shirt", "casual shirt", "formal shirt"],
        "context_clues": ["shirt", "tee", "t-shirt", "polo", "sleeve", "cotton", "size"]
    },
    "pants": {
        "products": ["jeans", "trousers", "chinos", "sweatpants", "leggings", "shorts",
                    "cargo pants", "formal pants", "track pants", "yoga pants"],
        "context_clues": ["pants", "trousers", "jeans", "leggings", "waist", "fit"]
    }
}

def detect_from_context(text: str) -> tuple:
    """
    Detect niche and product using context clues and pattern matching
    """
    text_lower = text.lower()
    
    # Check for each niche and its context clues
    for niche, data in PRODUCT_CATEGORIES.items():
        products = data["products"]
        context_clues = data["context_clues"]
        
        # Check if any context clue is present
        has_context = any(clue in text_lower for clue in context_clues)
        
        if has_context:
            # Now look for specific products
            for product in products:
                if product in text_lower:
                    return niche, product, "high"
            
            # If no specific product found, return the niche
            return niche, None, "medium"
    
    # Special case for vape flavors without explicit vape context
    if not any(clue in text_lower for clue in ["vape", "e-liquid", "e-juice", "disposable"]):
        # Check if it's likely a vape flavor question
        flavor_related = any(word in text_lower for word in ["flavour", "flavor", "taste", "puff"])
        has_known_flavor = any(flavor in text_lower for flavor in PRODUCT_CATEGORIES["vape"]["products"])
        
        if flavor_related and has_known_flavor:
            # Find which flavor is mentioned
            for flavor in PRODUCT_CATEGORIES["vape"]["products"]:
                if flavor in text_lower:
                    return "vape", flavor, "medium"
    
    return None, None, "low"

@app.post("/detect-product", response_model=ProductResponse)
async def detect_product(request: TextRequest):
    """
    Detect product niche and type from text description using Llama 3 via Groq
    """
    if client is None:
        raise HTTPException(status_code=500, detail="Groq client not initialized")
    
    try:
        # First, try context-based detection
        niche, product, confidence = detect_from_context(request.text)
        
        if niche == "vape" and product:
            return ProductResponse(
                original_text=request.text,
                detected_niche=niche,
                detected_product_type=product,
                confidence=confidence
            )
        
        # If context detection didn't work well, use LLM
        prompt = f"""
        Analyze this text to identify the product being discussed: "{request.text}"
        
        Focus on detecting:
        1. Product niche/category (vape, shoe, shirt, pants, or other)
        2. Specific product type or flavor within that niche
        
        For vape products, common flavors include: fresh mint, watermelon lime, passionfruit orange guava, etc.
        
        Respond with JSON format:
        {{
            "niche": "detected niche or null",
            "product_type": "detected product type or null",
            "confidence": "high/medium/low"
        }}
        
        Be specific about flavors and product types.
        """
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """You are a product detection expert. Analyze text to identify 
                    products and their specific types/flavors. Always respond with valid JSON.
                    Pay special attention to vape flavors even when the word "vape" isn't explicitly mentioned."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.1-8b-instant", 
            temperature=0.1,
            max_tokens=150,
            response_format={"type": "json_object"}
        )
        
        response_text = chat_completion.choices[0].message.content.strip()
        
        try:
            response_data = json.loads(response_text)
            detected_niche = response_data.get("niche")
            detected_product = response_data.get("product_type")
            confidence = response_data.get("confidence", "medium")
            
            # Clean up the response
            if detected_niche and detected_niche.lower() == "null":
                detected_niche = None
            if detected_product and detected_product.lower() == "null":
                detected_product = None
            
        except json.JSONDecodeError:
            detected_niche, detected_product, confidence = None, None, "low"
        
        if detected_niche:
            return ProductResponse(
                original_text=request.text,
                detected_niche=detected_niche,
                detected_product_type=detected_product,
                confidence=confidence
            )
        else:
            return ProductResponse(
                original_text=request.text,
                detected_niche=None,
                detected_product_type=None,
                confidence=None,
                error="No product detected in the text"
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/categories")
async def get_categories():
    """
    Get available product categories and their types
    """
    return {k: v["products"] for k, v in PRODUCT_CATEGORIES.items()}

@app.post("/add-category")
async def add_category(category_data: Dict[str, Any]):
    """
    Add a new product category or update existing one
    """
    try:
        category = category_data.get("category")
        products = category_data.get("products", [])
        context_clues = category_data.get("context_clues", [])
        
        if not category or not products:
            raise HTTPException(status_code=400, detail="Category and products are required")
        
        PRODUCT_CATEGORIES[category.lower()] = {
            "products": [p.lower() for p in products],
            "context_clues": [c.lower() for c in context_clues]
        }
        return {"message": f"Category '{category}' added/updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vape-flavors")
async def get_vape_flavors():
    """
    Get specifically vape flavors
    """
    return PRODUCT_CATEGORIES["vape"]["products"]

@app.get("/")
async def root():
    return {
        "message": "Enhanced Product Detection API",
        "endpoints": {
            "POST /detect-product": "Detect product niche and type from text",
            "GET /categories": "View available product categories",
            "GET /vape-flavors": "View vape flavors",
            "POST /add-category": "Add new product category"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)