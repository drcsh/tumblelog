from mongoengine import Document, StringField, ReferenceField, ListField, EmbeddedDocument, EmbeddedDocumentField, \
    CASCADE, ValidationError
from .utils import security


class User(Document):
    email = StringField(required=True, unique=True)
    password = StringField(required=True)  # It would be nice if there's was an out of the box hashed field.
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

    def clean(self):
        # The password will be unhashed the first time the User is saved, we want to catch this and hash the password
        # before saving
        if not security.password_is_hashed(self.password):

            # This is a belts & braces check, the view should have already determined this.
            try:
                security.password_is_secure_enough(self.password)
            except Exception as e:
                raise ValidationError(str(e))

            # We only want to save the password hash, not the string password.
            self.password = security.hash_password_string(self.password)


class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)


class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))

    meta = {'allow_inheritance': True}


class TextPost(Post):
    content = StringField()


class ImagePost(Post):
    image_path = StringField()


class LinkPost(Post):
    link_url = StringField()
