# utils/emotion_response.py

# utils/emotion_responses.py

def generate_companion_response(predicted_emotions):
    # Theme mapping based on your 28-emotion list
    emotion_themes = {
        "Warmth": {"joy", "gratitude", "love", "pride", "optimism", "admiration", "approval", "caring"},
        "Anxiety": {"nervousness", "fear", "confusion", "surprise"},
        "Grief": {"sadness", "disappointment", "remorse", "grief", "loneliness"},
        "Frustration": {"anger", "frustration", "annoyance", "disgust", "disapproval"},
        "Reflection": {"realization", "curiosity", "relief", "desire", "embarrassment"},
        "Amusement": {"amusement", "excitement"},
        "Neutral": {"neutral"}
    }

    theme_messages = {
        "Warmth": "Your words radiate warmth and light. It's wonderful to feel those moments of joy, love, or pride within you.",
        "Anxiety": "It sounds like you're navigating something uncertain. It’s okay to feel unsettled—I'm here with you in the unknown.",
        "Grief": "There’s a quiet weight behind your words. Whether it's sadness, loss, or just a heavy heart—I’m here with compassion.",
        "Frustration": "You sound emotionally charged, and that’s okay. Sometimes our strongest feelings just need to be heard, without judgment.",
        "Reflection": "You seem to be processing a lot right now. That’s a powerful thing—realizations and curiosity show growth.",
        "Amusement": "I can sense your playful energy. Laughter and excitement add beautiful color to our day—thank you for sharing that.",
        "Neutral": "Not every day is heavy or bright. Sometimes, just feeling neutral is valid and worth honoring too."
    }

    # Identify emotion themes present
    detected_themes = set()
    for emotion in predicted_emotions:
        for theme, emotions in emotion_themes.items():
            if emotion in emotions:
                detected_themes.add(theme)

    if not detected_themes:
        return (
            "I sense you're feeling a mix of things right now. Whatever it is, I'm here to sit with you through it all. "
            "You don’t have to have it all figured out. Just keep talking—I’m listening, every step of the way."
        )

    # Count and sort themes by frequency of matching emotions
    theme_counts = {theme: 0 for theme in detected_themes}
    for emotion in predicted_emotions:
        for theme in detected_themes:
            if emotion in emotion_themes[theme]:
                theme_counts[theme] += 1

    sorted_themes = sorted(theme_counts.items(), key=lambda x: -x[1])
    primary_theme = sorted_themes[0][0]
    secondary_themes = [t[0] for t in sorted_themes[1:]]

    message = theme_messages[primary_theme]

    if secondary_themes:
        message += " And I also sense hints of " + ", ".join(secondary_themes[:-1])
        if len(secondary_themes) > 1:
            message += f", and {secondary_themes[-1]}."
        else:
            message += f" {secondary_themes[-1]}."
        message += " It's okay to feel many things at once—I'm here to hold that space for you."

    return message
