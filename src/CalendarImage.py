from PIL import Image, ImageDraw, ImageFont
import datetime
import json

class CalendarImage:
    def __init__(self):
        print("CalendarImage")
        self.width, self.height = 1080, 1920
        self.background_color = (33, 37, 41, 255) 
        self.eventsData = []
        self.image = None
        self.draw = None
        self.square_size = 148
        self.square_color = (43, 47, 51, 255)
        self.square_color2 = (56, 60, 63, 255)
        self.cell_spacing = 4
        self.font_path = "fonts/Roboto-Regular.ttf" 

    def generate(self):
        print("Generate")
        self.load_events()
        self.image = self.create_image()
        self.draw = self.create_draw()
        self.add_week_days()
        self.draw_calendar()
        self.save_image()


    # load json from file and parse
    def load_events(self):
        print("load_events")
        with open('events.json') as f:
            self.eventsData = json.load(f)

    # Create a new image with RGB mode
    def create_image(self):
        print("create_image")
        return Image.new('RGBA', (self.width, self.height), self.background_color)

    # Save image
    def save_image(self):
        print("save_image")
        self.image.save("images/calendar.png")


    # Initialize ImageDraw
    def create_draw(self):
        print("create_draw")
        return ImageDraw.Draw(self.image)
    
    # add week days
    def add_week_days(self):
        print("add_week_days")
        font = ImageFont.truetype(self.font_path, 16)
        text_color = (255, 255, 255, 100)

        for j in range(7): 
            top_left_corner = (10 + (self.square_size + self.cell_spacing) * j, 0 )
            bottom_right_corner = (top_left_corner[0] + self.square_size, top_left_corner[1] + 22)

            # add background color square
            self.draw.rectangle([top_left_corner, bottom_right_corner], fill=self.square_color)

            text = "DOM SEG TER QUA QUI SEX SAB"[j*4:j*4+3]
            text_width, text_height = self.draw.textsize(text, font=font)
            x = top_left_corner[0] + (self.square_size - text_width) / 2
            y = top_left_corner[1] + 2
            self.draw.text((x, y), text, font=font, fill=text_color)

    def cut_text_to_fit(self, text, font, max_width):
        draw = ImageDraw.Draw(Image.new('RGB', (1000, 1000))) 
        text_width, _ = draw.textsize(text, font=font)
        if text_width <= max_width:
            return text

        while text_width > max_width:
            text = text[:-1]
            text_width, _ = draw.textsize(text + '...', font=font)
        return text + '...'
    
    def draw_calendar(self):


        today = datetime.date.today()
        current_year = today.year
        current_month = today.month
        current_day = today.day


        # Find the first day of the current month
        first_day_of_month = datetime.date(current_year, current_month, 1)

        # Get the day of the week for the first day of the month
        start_offset = first_day_of_month.weekday() + 1  # Monday = 0, ..., Sunday = 6

        # Get the day of the week for the first day of the month
        start_offset = first_day_of_month.weekday() + 1  # Monday = 0, ..., Sunday = 6

        if(start_offset == 7):
            start_offset = 0

        day = 1
        max_days = (first_day_of_month.replace(month=(current_month % 12) + 1, day=1) - datetime.timedelta(days=1)).day
        line = 0


        fontTitle = ImageFont.truetype(self.font_path, 12)

        fontDay = ImageFont.truetype(self.font_path, 18)

        for i in range(6):
            for j in range(7): 

                top_left_corner = (10 + (self.square_size + self.cell_spacing) * j, 50 + (self.square_size + self.cell_spacing) * i)
                bottom_right_corner = (top_left_corner[0] + self.square_size, top_left_corner[1] + self.square_size )

                if i == 0 and j < start_offset:
                    self.draw.rectangle([top_left_corner, bottom_right_corner], fill=self.square_color)
                    continue  
                
                # find in eventsData if there is an event for this day
                events = []
                for e in self.eventsData:
                    if int(e['day']) == day:
                        event = e
                        # add to events
                        events.append(event)



                if day == current_day:
                    self.draw.rectangle([top_left_corner, bottom_right_corner], fill=self.square_color2)
                else:
                    self.draw.rectangle([top_left_corner, bottom_right_corner], fill=self.square_color)


                # loop through events
                eventY = 0
                for event in events:
                    # Add event text
                    if event:

                        text = self.cut_text_to_fit(event['summary'], fontTitle, self.square_size - 30)
                        text_color = event['foregroundColor']
                        x = top_left_corner[0] + 10
                        y = top_left_corner[1] + 30 + (eventY*1.3)

                        text_width, text_height = self.draw.textsize(text, font=fontTitle)

                        self.draw.rectangle([(x,y), (x + text_width + 10,y + text_height+5)], fill=event['backgroundColor'])
                        
                        self.draw.text((x+5, y+3), text, font=fontTitle, fill=text_color)
                        eventY += 16
                
                # Add text with the day of the current month
                text = str(day)
                day += 1
                text_color = (255,255,255,150)
                text_width, text_height = self.draw.textsize(text, font=fontDay)
                x = top_left_corner[0] + (self.square_size - text_width) / 2
                y = top_left_corner[1] 
                self.draw.text((x, y), text, font=fontDay, fill=text_color)

                line += 1
                
                if day > max_days:
                    break  # Stop adding days if the month ends
            if day > max_days:
                break
