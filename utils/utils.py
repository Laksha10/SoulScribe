def generate_companion_response(predicted_emotions):
    emotion_set = set(predicted_emotions)
    for emotion in emotion_set:
        if emotion in emotion_groups_response:
            return emotion_groups_response[emotion]

    # Fallback message if no known emotion detected
    return (
        "I sense you're feeling a mix of things right now. Whatever it is, I'm here to sit with you through it all. "
        "You don’t have to have it all figured out. Just keep talking—I’m listening, every step of the way."
    )
