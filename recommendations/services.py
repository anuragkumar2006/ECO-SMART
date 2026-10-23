from .models import RecommendationRule

DEFAULT_RULES = {
    'organic': {
        'bin_type': 'Green (Wet Waste Bin)',
        'bin_color_code': '#2E8B57',
        'biodegradable': True,
        'suggestion': 'Place the waste in the designated organic/wet-waste stream. Where appropriate, organic waste can be composted for soil enrichment.'
    },
    'recyclable': {
        'bin_type': 'Blue (Dry Recyclable Bin)',
        'bin_color_code': '#3B82F6',
        'biodegradable': False,
        'suggestion': 'Rinse or clean container residues if necessary. Place the item in the designated blue dry-recyclable waste stream for reprocessing.'
    },
    'hazardous': {
        'bin_type': 'Red / Yellow (Hazardous Waste Bin)',
        'bin_color_code': '#B45309',
        'biodegradable': False,
        'suggestion': 'Do NOT mix with ordinary municipal waste. Deposit at a designated hazardous waste drop-off point or specialized collection bin.'
    }
}

def get_recommendation_for_category(category_name):
    cat_clean = category_name.lower().strip()
    rule = RecommendationRule.objects.filter(category=cat_clean, active=True).first()
    if rule:
        return {
            'bin_type': rule.bin_type,
            'bin_color_code': rule.bin_color_code,
            'biodegradable': rule.biodegradable,
            'suggestion': rule.suggestion
        }
    
    # Fallback to defaults
    if cat_clean in DEFAULT_RULES:
        return DEFAULT_RULES[cat_clean]
    
    return {
        'bin_type': 'General Waste Bin',
        'bin_color_code': '#6B7280',
        'biodegradable': False,
        'suggestion': 'Follow local waste segregation guidelines for unclassified items.'
    }
