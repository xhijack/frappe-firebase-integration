from firebase_integration.firebase_integration import FirebaseIntegration

def get_driver_locations(delivery_trip_id):
    firebase_integration = FirebaseIntegration()
    return firebase_integration.get_all_data('delivery_trip', delivery_trip_id)