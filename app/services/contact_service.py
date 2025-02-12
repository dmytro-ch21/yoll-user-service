from app.repositories.contact_repository import ContactRepository

class ContactService:
    @staticmethod
    def create_contact(data):
        if not data.get("full_name") or not data.get("user_id"):
            return {"error": "Full name and user_id are required"}, 400
        try:
            contact = ContactRepository.create_contact(data)
            return contact
        except Exception as e:
            return {"error": str(e)}, 400

    @staticmethod
    def get_all_contacts():
        contacts = ContactRepository.get_all_contacts()
        if not contacts:
            return {"error": "No contacts found"}, 404
        return contacts

    @staticmethod
    def get_contact_by_id(contact_id):
        contact = ContactRepository.get_contact_by_id(contact_id)
        if not contact:
            return {"error": "Contact not found"}, 404
        return contact

    @staticmethod
    def update_contact(contact_id, data):
        updated = ContactRepository.update_contact(contact_id, data)
        if not updated:
            return {"error": "Contact not found or update failed"}, 404
        return {"message": "Contact updated successfully"}

    @staticmethod
    def delete_contact(contact_id):
        deleted = ContactRepository.delete_contact(contact_id)
        if not deleted:
            return {"error": "Contact not found"}, 404
        return {"message": "Contact deleted successfully"}