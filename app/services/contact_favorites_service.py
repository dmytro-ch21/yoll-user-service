from app.repositories.contact_favorites_repository import ContactsFavoritesRepository
from app.repositories.contact_repository import ContactRepository

class ContactsFavoritesService:
    @staticmethod
    def add_favorite(user_id, contact_id):
        try:
            # Mark the contact as favorite.
            updated = ContactRepository.update_favorite_status(contact_id, True)
            if not updated:
                return {"error": "Contact not found"}, 404

            # Insert the favorite record.
            result = ContactsFavoritesRepository.add_favorite(user_id, contact_id)
            if result is None:
                # If the record already exists, provide a message about that
                return {"message": "Contact is already marked as favorite"}
            return {"message": "Contact added to favorites", "contact_id": result}
        except Exception as e:
            return {"error": str(e)}, 400

    @staticmethod
    def delete_favorite(user_id, contact_id):
        try:
            # Mark the contact as not favorite.
            updated = ContactRepository.update_favorite_status(contact_id, False)
            if not updated:
                return {"error": "Contact not found"}, 404

            # Remove the favorite record.
            result = ContactsFavoritesRepository.delete_favorite(user_id, contact_id)
            if not result:
                return {"error": "Favorite contact not found"}, 404
            return {"message": "Contact removed from favorites"}
        except Exception as e:
            return {"error": str(e)}, 400

    @staticmethod
    def get_favorites(user_id):
        try:
            favorites = ContactsFavoritesRepository.get_favorites_by_user(user_id)
            if not favorites:
                return {"error": "No favorites found"}, 404
            return favorites
        except Exception as e:
            return {"error": str(e)}, 400
