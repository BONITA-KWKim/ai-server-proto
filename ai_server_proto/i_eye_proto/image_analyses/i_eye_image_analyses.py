from ..custom_utils.whitelist_for_labels import get_whitelist_value
from ..custom_utils.whitelist_for_labels import get_refusal_value
from ..custom_utils.whitelist_for_labels import get_whitelist_score_value
from ..custom_utils.eye_disease import get_disease_value


def recognize_human_eye(labels):
    label_score = 0

    for l in labels:
        print("[DEB] desc:", l.description)
        print("[DEB] score:", l.score)
        if 0.9 > l.score:
            break

        first_char = l.description[0]
        whitelist_by_index = get_whitelist_value(first_char.lower())
        refusal_list_by_index = get_refusal_value(first_char.lower())

        if l.description.lower() in whitelist_by_index:
            print(l.description.lower())
            print(whitelist_by_index)
            label_score += 1

        if any(l.description.lower() is s for s in refusal_list_by_index):
            print(l.description.lower())
            print(refusal_list_by_index)
            return False

    if get_whitelist_score_value() > label_score:
        print("[DEB] not enough score: %d" % label_score)
        return False

    print("[DEB] score value: ", label_score)

    return True


def analysis_eyes(web_detections):
    best_guess = web_detections.best_guess_labels
    web_entities = web_detections.web_entities
    print("[DEB] best guess: ", best_guess)
    print("[DEB] web entities: ", web_entities)

    # best guess
    for b in best_guess:
        first_char = b.label[0]
        disease_list_by_index = get_disease_value(first_char.lower())
        if b.label.lower() in disease_list_by_index:
            print("Success: Disease[%s]" % b.label.lower())

    # web entities
    for w in web_entities:
        print("[DEB] desc: ", w.description)
        print("[DEB] score: ", w.score)
        first_char = w.description[0]
        disease_list_by_index = get_disease_value(first_char.lower())

        if w.description.lower() in disease_list_by_index:
            print("Success: Disease[%s]" % w.description.lower())

    print("[DEB] end of the image analysis")

    diagnosis = "conjunctivitis"
    return diagnosis
