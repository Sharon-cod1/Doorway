# properties/recommendations.py
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from properties.models import Property, UserInteraction

def get_recommendations(user_id, num_recommendations=5):
    # Get user's interaction history
    user_interactions = UserInteraction.objects.filter(user_id=user_id)
    
    # Get all properties
    properties = Property.objects.all().values('id', 'price', 'bedrooms', 'bathrooms', 'property_type')
    df = pd.DataFrame(list(properties))
    
    # Train KNN model
    knn = NearestNeighbors(n_neighbors=num_recommendations)
    knn.fit(df[['price', 'bedrooms', 'bathrooms']])
    
    # Get recommendations based on last interaction
    last_interaction = user_interactions.last()
    _, indices = knn.kneighbors([[last_interaction.property.price, 
                                 last_interaction.property.bedrooms,
                                 last_interaction.property.bathrooms]])
    
    return Property.objects.filter(id__in=df.iloc[indices[0]]['id'])