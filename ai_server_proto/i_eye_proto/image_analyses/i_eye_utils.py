def collect_diagnosis(user_id, labels, best_guess, web_entities, diagnosis):
    return {
        "user_id": user_id,
        "label": labels,
        "best_guess": best_guess,
        "web_entities": web_entities,
        "diagnosis": diagnosis
    }
