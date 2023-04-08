from mongoengine import connect, Document, StringField, disconnect

# Disconnect the existing connection (if any)
disconnect(alias='default')

# Define the MongoDB connection
connect(host="mongodb+srv://medadmin:hMna4RYKa0rIS9wp@medicalanalysissystem.mptbxix.mongodb.net/test")


# Define the schema for your MongoDB document
class MyDocument(Document):
    name = StringField(required=True)
    email = StringField(required=True)


# Define the function to create and save a new document
def create_document(name, email):
    # Create a new document with the data
    document = MyDocument(name=name, email=email)
    document.save()
    print("Document created")

    # Return the created document object
    return document

create_document("ujjawal", "ujjawalpoudel@gmail.com")
