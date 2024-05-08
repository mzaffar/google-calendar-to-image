from src.GoogleCalendar import GoogleCalendar
from src.CalendarImage import CalendarImage

googleCalendar = GoogleCalendar()
googleCalendar.export_to_json()

calendarImage = CalendarImage()
calendarImage.generate()