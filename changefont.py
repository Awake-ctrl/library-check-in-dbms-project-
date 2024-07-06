
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def change_font_size(data, font_name="Calibri.ttf", font_size=12):
    # Register the font (although not used directly in the data processing, it's here for completeness)
    pdfmetrics.registerFont(TTFont("CustomFont", font_name))
    
    # Create a list to hold the processed data
    processed_data = []
    DATA=""
    # Process each line of data
    for line in data:
        # Add a tuple with the line and the font size
        processed_data.append((line, font_size))
    for line,font_size in processed_data:
        DATA+=str(line)
        
    
    return DATA

        
        
       
