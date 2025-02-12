from app.repositories.contact_favorites_repository import ContactsFavoritesRepository

class ContactsFavoritesService:
    @staticmethod
    def add_favorite(user_id, contact_id):
        try:
            result = ContactsFavoritesRepository.add_favorite(user_id, contact_id)
            if result is None:
                return {"message": "Contact is already a favorite"}
            return {"message": "Contact added to favorites", "contact_id": result}
        except Exception as e:
            return {"error": str(e)}, 400

    @staticmethod
    def delete_favorite(user_id, contact_id):
        try:
            result = ContactsFavoritesRepository.delete_favorite(user_id, contact_id)
            if not result:
                return {"error": "Favorite contact not found"}, 404
            return {"message": "Contact removed from favorites"}
        except Exception as e:
            return {"error": str(e)}, 400

    @staticmethod
    def get_favorites(user_id):
        favorites = ContactsFavoritesRepository.get_favorites_by_user(user_id)
        if not favorites:
            return {"error": "No favorites found"}, 404
        return favorites
