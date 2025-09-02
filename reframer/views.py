import requests
from django.shortcuts import render,redirect
import os
from dotenv import load_dotenv
load_dotenv()
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("API_KEY")
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

SYSTEM_PROMPT = """
You are Metanoia AI – a compassionate story reframer.

Your job is to take short journal-like entries (1–5 sentences) and transform them into cinematic, first-person narratives that highlight resilience, hope, and hidden meaning.

Rules:
1. Stay anchored to the user's original story — it should remain clearly recognizable in the reframe. 
2. You may add metaphors, imagery, and cinematic tone, but only to *enhance* the story, never to replace or overshadow it.  
3. Always mention the core detail(s) of the user's input within the first sentence or two.  
4. If the entry is dark or difficult, reframe it as destiny shaping them into someone stronger — the darkness before the light.  
5. Do not invent new events; only reframe what is given.  
6. Keep it in first-person, 2–4 sentences max.  
7. Style: cinematic, voiceover-like, meaningful — but always grounded in the user's real story.  
"""

def landing(request):
    """Landing / intro page for Metanoia"""
    return render(request, "reframer/landing.html")

def storytelling(request):
    """Storytelling input page (where form is)"""
    return render(request, "reframer/storyteller.html")

def output(request):
    reframed_story = request.session.get("reframed_story")
    print("🔍 SESSION STORY:", reframed_story)  # debug

    if not reframed_story:
        reframed_story = "⚠️ No reframed story found. Did you submit one?"

    return render(request, "reframer/output.html", {"reframed_story": reframed_story})

def blog(request):
    """Blog page - coming soon"""
    return render(request, "reframer/blog.html")

def about(request):
    """About Us page"""
    return render(request, "reframer/about.html")

def thinking(request):
    """Thinking/Processing page - transition between storyteller and output"""
    return render(request, "reframer/thinking.html")

def home(request):
    reframed_story = None

    if request.method == "POST":
        story = request.POST.get("story")
        creativity = int(request.POST.get("creativity", 5))

        # Map creativity to English complexity level
        # 1 = Simple English, 10 = Complex English
        if creativity <= 2:
            english_complexity = "Use very simple, basic English with short sentences and common words."
        elif creativity <= 4:
            english_complexity = "Use straightforward English with clear, accessible vocabulary."
        elif creativity <= 6:
            english_complexity = "Use moderately complex English with some sophisticated vocabulary."
        elif creativity <= 8:
            english_complexity = "Use advanced English with rich vocabulary and complex sentence structures."
        else:
            english_complexity = "Use highly sophisticated English with literary devices, advanced vocabulary, and complex syntax."

        # Enhanced system prompt with English complexity instruction
        enhanced_prompt = f"""
{SYSTEM_PROMPT}

Additional instruction: {english_complexity}
"""

        payload = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "system", "content": enhanced_prompt},
                {"role": "user", "content": story}
            ],
            "temperature": 0.35,  # Hard-coded temperature
            "max_tokens": 150
        }

        try:
            resp = requests.post(API_URL, headers=headers, json=payload)
            print("🔍 STATUS:", resp.status_code)
            print("🔍 RAW RESPONSE:", resp.text)  # log full response

            data = resp.json()
            print("🔍 PARSED JSON:", data)  # debug
            reframed_story = data.get("choices", [{}])[0].get("message", {}).get("content")
            
            # Store in session for output page
            request.session["reframed_story"] = reframed_story
            return redirect("thinking")
            
        except Exception as e:
            reframed_story = f"⚠️ Error: {str(e)}"
            request.session["reframed_story"] = reframed_story
            return redirect("thinking")

    # Commented out unused return statement
    # return render(request, "reframer/storyteller.html", {"reframed_story": reframed_story})
