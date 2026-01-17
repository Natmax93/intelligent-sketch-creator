from assistant.suggestions import CAT_EARS, ROOF_TRIANGLE

SUGG_CAT_EARS_ID = "CAT_EARS"
SUGG_ROOF_ID = "ROOF_TRIANGLE"


def propose_suggestion(context: dict):
    trigger = context.get("trigger", "manual")
    created_kind = context.get("created_kind")
    auto_suppressed = context.get("auto_suppressed", set())

    # --- Candidate 1 : oreilles ---
    has_ellipse = bool(context.get("has_ellipse", False))
    has_cat_ears = bool(context.get("has_cat_ears", False))

    can_cat_ears = has_ellipse and not has_cat_ears
    if trigger == "auto":
        can_cat_ears = can_cat_ears and (created_kind == "QGraphicsEllipseItem")
        can_cat_ears = can_cat_ears and (SUGG_CAT_EARS_ID not in auto_suppressed)

    if can_cat_ears:
        return {
            "suggestion_id": SUGG_CAT_EARS_ID,
            "suggestion": CAT_EARS,
            "uncertainty_pct": 70,
            "explanation": [
                "Une ellipse est détectée (tête possible).",
                "Aucune oreille détectée pour l'instant.",
                "Suggestion optionnelle.",
            ],
            "what_to_do": "Appliquez si vous dessinez un chat, sinon ignorez.",
        }

    # --- Candidate 2 : toit ---
    has_rect = bool(context.get("has_rect", False))
    has_roof = bool(context.get("has_roof_triangle", False))

    can_roof = has_rect and not has_roof
    if trigger == "auto":
        can_roof = can_roof and (created_kind == "QGraphicsRectItem")
        can_roof = can_roof and (SUGG_ROOF_ID not in auto_suppressed)

    if can_roof:
        return {
            "suggestion_id": SUGG_ROOF_ID,
            "suggestion": ROOF_TRIANGLE,
            "uncertainty_pct": 65,
            "explanation": [
                "Un rectangle est détecté (mur/façade possible).",
                "Aucun toit détecté pour l'instant.",
                "Ajout d'un triangle au-dessus pour former un toit.",
            ],
            "what_to_do": "Appliquez si vous dessinez une maison, sinon ignorez.",
        }

    return None
