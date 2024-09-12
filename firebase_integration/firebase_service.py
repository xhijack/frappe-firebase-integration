import json
from google.oauth2 import service_account
from google.cloud import firestore

credentials_path = '/Users/ramdani/Documents/code/erpnext/experiment/sopwer-c0401-firebase-adminsdk-q9wop-80e696f421.json'

credentials = service_account.Credentials.from_service_account_file(credentials_path)

def geo_point_to_dict(geo_point):
    return {
        'latitude': geo_point.latitude,
        'longitude': geo_point.longitude
    }

def handle_complex_types(data):
    # Convert GeoPoint objects to dictionaries
    for key, value in data.items():
        if isinstance(value, firestore.GeoPoint):
            data[key] = geo_point_to_dict(value)
        # Add more type handling as needed (e.g., Timestamp, Blob)
    return data

class FirebaseIntegration:
    def __init__(self):
        self.db = firestore.Client(credentials=credentials)

    def get_data(self, collection, document):
        doc_ref = self.db.collection(collection).document(document)
        doc = doc_ref.get()
        return doc.to_dict()
    
    def get_all_data(self, collection, condition=None, order_by_field=None, direction="ASCENDING"):
        try:
            query = self.db.collection(collection)
            
            # Menambahkan kondisi filter jika ada
            if condition:
                if isinstance(condition, dict):
                    for field, value in condition.items():
                        query = query.where(field, '==', value)
                else:
                    raise ValueError("Condition must be a dictionary where key is the field name and value is the value to filter.")
            
            # Menambahkan order by jika ada
            if order_by_field:
                direction = firestore.Query.ASCENDING if direction.upper() == "ASCENDING" else firestore.Query.DESCENDING
                print(order_by_field, direction)
                query = query.order_by(order_by_field, direction=direction)
            
            docs = query.stream()
            
            # Menangani tipe data kompleks seperti GeoPoint
            data = [handle_complex_types(doc.to_dict()) for doc in docs]
            return data
        except Exception as e:
            print(f'An error occurred: {e}')
            return []
