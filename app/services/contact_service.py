from app.repositories.contact_repository import ContactRepository


class ContactService:
    @staticmethod
    def get_all_contacts():
        contacts = ContactRepository.get_all_contacts()
        if not contacts:
            return {"error": "No contacts found"}, 404
        return contacts

    @staticmethod
    def create_contact(data):
        if not data.get("full_name") or not data.get("user_id"):
            return {"error": "Full name and user_id are required"}, 400
        try:
            contact = ContactRepository.create_contact(data)
            return contact
        except Exception as e:
            return {"error": f"There was an error: {e}"}, 400

    @staticmethod
    def get_all_contacts_by_user(user_id):
        contacts = ContactRepository.get_all_contacts_by_user(user_id)
        if not contacts:
            return {"error": "No contacts found for this user"}, 404
        return contacts

    @staticmethod
    def get_contact_by_id_and_user(contact_id, user_id):
        contact = ContactRepository.get_contact_by_id_and_user(contact_id, user_id)
        if not contact:
            return {"error": "Contact not found or does not belong to this user"}, 404
        return contact

    @staticmethod
    def update_contact(contact_id, data, user_id):
        existing = ContactRepository.get_contact_by_id_and_user(contact_id, user_id)
        if not existing:
            return {"error": "Contact not found or does not belong to this user"}, 404

        merged_data = {
            "full_name": data.get("full_name", existing["full_name"]),
            "phone_number": data.get("phone_number", existing["phone_number"]),
            "email": data.get("email", existing["email"]),
            "street": data.get("street", existing["street"]),
            "city": data.get("city", existing["city"]),
            "state": data.get("state", existing["state"]),
            "postal_code": data.get("postal_code", existing["postal_code"]),
            "country": data.get("country", existing["country"]),
            "additional_info": data.get("additional_info", existing["additional_info"]),
            "base64_image": data.get("base64_image", existing["base64_image"]),
            "is_favorite": data.get("is_favorite", existing["is_favorite"]),
        }

        updated_id = ContactRepository.update_contact(contact_id, merged_data)
        if not updated_id:
            return {"error": "Contact update failed"}, 400

        return {"message": "Contact updated successfully"}

    @staticmethod
    def delete_contact(contact_id, user_id):
        contact = ContactRepository.get_contact_by_id_and_user(contact_id, user_id)
        if not contact:
            return {"error": "Contact not found or does not belong to this user"}, 404
        deleted = ContactRepository.delete_contact(contact_id)
        if not deleted:
            return {"error": "Contact deletion failed"}, 404
        return {"message": "Contact deleted successfully"}
