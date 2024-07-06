from PIL import Image, ImageDraw, ImageFont

def get_text_width(text, font_name, font_size):
    # Create a dummy image to draw on
    img = Image.new('RGB', (1, 1), color = (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Load a font
    font = ImageFont.truetype(font_name, font_size)

    # Get text size
    text_width, _ = draw.textsize(text, font=font)

    return text_width

# # Example usage:
# text = "Ganedi Satya Harika"
# font_name = "arial.ttf"  # Replace with your font file (.ttf)
# font_size = 12

# width_pixels = get_text_width(text, font_name, font_size)
# print(f"The width of '{text}' is approximately {width_pixels} pixels.")
# value="Kallepally Sai Kiran"
# font_name="Calibri.ttf"
# font_size=12
#                 # a=width(value,"Helvetica",12)
# a=get_text_width(value,font_name,font_size)
# print(a)