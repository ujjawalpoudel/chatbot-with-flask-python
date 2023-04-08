import firebase_admin
from firebase_admin import credentials

from firebase_admin import db

cred = credentials.Certificate('./medicalanalysissystem-firebase-adminsdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://medicalanalysissystem-default-rtdb.firebaseio.com/'
})


ref = db.reference("medicalanalysissystem")
ref.set({
	"Book1":
	{
		"Title": "The Fellowship of the Ring",
		"Author": "J.R.R. Tolkien",
		"Genre": "Epic fantasy",
		"Price": 100
	},
	"Book2":
	{
		"Title": "The Two Towers",
		"Author": "J.R.R. Tolkien",
		"Genre": "Epic fantasy",
		"Price": 100	
	},
	"Book3":
	{
		"Title": "The Return of the King",
		"Author": "J.R.R. Tolkien",
		"Genre": "Epic fantasy",
		"Price": 100
	},
	"Book4":
	{
		"Title": "Brida",
		"Author": "Paulo Coelho",
		"Genre": "Fiction",
		"Price": 100
	}
})