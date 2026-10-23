from predictions.models import Prediction
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
import pandas as pd

def get_analytics_summary(user):
    qs = Prediction.objects.filter(user=user)
    total_scans = qs.count()
    
    if total_scans == 0:
        return {
            'total_scans': 0,
            'organic_count': 0,
            'recyclable_count': 0,
            'hazardous_count': 0,
            'biodegradable_count': 0,
            'non_biodegradable_count': 0,
            'biodegradable_percentage': 0,
            'non_biodegradable_percentage': 0,
            'top_category': 'None',
            'eco_insight': 'Scan your first waste item to start building your waste profile.'
        }

    counts = qs.aggregate(
        organic=Count('id', filter=Q(category='organic')),
        recyclable=Count('id', filter=Q(category='recyclable')),
        hazardous=Count('id', filter=Q(category='hazardous')),
        bio=Count('id', filter=Q(biodegradable=True)),
        non_bio=Count('id', filter=Q(biodegradable=False)),
    )

    organic_c = counts['organic'] or 0
    recyclable_c = counts['recyclable'] or 0
    hazardous_c = counts['hazardous'] or 0
    bio_c = counts['bio'] or 0
    non_bio_c = counts['non_bio'] or 0

    bio_pct = round((bio_c / total_scans) * 100, 1)
    non_bio_pct = round((non_bio_c / total_scans) * 100, 1)

    # Determine top category
    cat_map = {'Organic': organic_c, 'Recyclable': recyclable_c, 'Hazardous': hazardous_c}
    top_cat = max(cat_map, key=cat_map.get)

    if top_cat == 'Recyclable':
        insight = f"Recyclable is your most frequently detected category ({recyclable_c} items, {round(recyclable_c/total_scans*100,1)}%). Remember to clean plastic and paper items before placing them in the Blue bin!"
    elif top_cat == 'Organic':
        insight = f"Organic waste leads your scans ({organic_c} items, {round(organic_c/total_scans*100,1)}%). Consider composting your kitchen waste for eco-friendly fertilizer!"
    else:
        insight = f"Hazardous waste detected in your activity ({hazardous_c} items). Ensure proper disposal at official E-waste or red bin centers."

    return {
        'total_scans': total_scans,
        'organic_count': organic_c,
        'recyclable_count': recyclable_c,
        'hazardous_count': hazardous_c,
        'biodegradable_count': bio_c,
        'non_biodegradable_count': non_bio_c,
        'biodegradable_percentage': bio_pct,
        'non_biodegradable_percentage': non_bio_pct,
        'top_category': top_cat,
        'eco_insight': insight
    }

def get_category_distribution(user):
    qs = Prediction.objects.filter(user=user).values('category').annotate(count=Count('id'))
    res = {'organic': 0, 'recyclable': 0, 'hazardous': 0}
    for item in qs:
        cat = item['category'].lower()
        if cat in res:
            res[cat] = item['count']
    return res

def get_biodegradability_split(user):
    qs = Prediction.objects.filter(user=user)
    bio_count = qs.filter(biodegradable=True).count()
    non_bio_count = qs.filter(biodegradable=False).count()
    return {
        'biodegradable': bio_count,
        'non_biodegradable': non_bio_count
    }

def get_bin_usage_analytics(user):
    qs = Prediction.objects.filter(user=user).values('bin_type', 'bin_color_code').annotate(count=Count('id'))
    return list(qs)

def get_trends_analytics(user, days=30):
    start_date = timezone.now() - timedelta(days=days)
    predictions = list(Prediction.objects.filter(user=user, created_at__gte=start_date).values('created_at', 'category'))
    
    if not predictions:
        return {'dates': [], 'organic': [], 'recyclable': [], 'hazardous': [], 'total': []}

    df = pd.DataFrame(predictions)
    df['date'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d')
    
    pivot = df.pivot_table(index='date', columns='category', aggfunc='size', fill_value=0)
    
    dates = list(pivot.index)
    organic_counts = list(pivot.get('organic', [0]*len(dates)))
    recyclable_counts = list(pivot.get('recyclable', [0]*len(dates)))
    hazardous_counts = list(pivot.get('hazardous', [0]*len(dates)))
    total_counts = [int(o + r + h) for o, r, h in zip(organic_counts, recyclable_counts, hazardous_counts)]

    return {
        'dates': dates,
        'organic': [int(x) for x in organic_counts],
        'recyclable': [int(x) for x in recyclable_counts],
        'hazardous': [int(x) for x in hazardous_counts],
        'total': total_counts
    }
