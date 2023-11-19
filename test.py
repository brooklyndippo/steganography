"""
[Day 7] Assignment: Steganography
    - Turn in on Gradescope (https://make.sc/bew2.3-gradescope)
    - Lesson Plan: https://tech-at-du.github.io/ACS-3230-Web-Security/#/Lessons/Steganography

Deliverables:
    1. All TODOs in this file.
    2. Decoded sample image with secret text revealed
    3. Your own image encoded with hidden secret text!
"""
# TODO: Run `pip3 install Pillow` before running the code.
from PIL import Image, ImageDraw, ImageFont


def decode_image(path_to_png):
    # Open the image using PIL:
    encoded_image = Image.open(path_to_png)

    # Separate the red channel from the rest of the image:
    red_channel = encoded_image.split()[0]

    # Create a new PIL image with the same size as the encoded image:
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    x_size, y_size = encoded_image.size

    # TODO: Using the variables declared above, replace `print(red_channel)` with a complete implementation:
    # print(red_channel)  # Start coding here!
    
    for column in range(y_size):
      for row in range(x_size):
        if red_channel.getpixel((row, column)) % 2 == 1:
        #if str(red_channel.getpixel((row, column)))[-1] == '1':
          pixels[row, column] = (0, 0, 0) #if it ends in a 1, make it black
        else:
          pixels[row, column] = (255, 255, 255) #if it ends in a 0, make it white

    # DO NOT MODIFY. Save the decoded image to disk:
    decoded_image.save(f'{path_to_png[:-4]}_decoded.png')


def encode_image(path_to_png, secret_message):
    #define the starting image
    starting_image = Image.open(path_to_png)
    starting_image_pixels = starting_image.load()
    
    secret_image = write_text(path_to_png, secret_message)
    secret_image_pixels = secret_image.load()
    
    #create a new PIL image with the same size as the starting image
    encoded_image = Image.new("RGB", starting_image.size)
    pixels = encoded_image.load()
        
    for x in range(encoded_image.width):
      for y in range(encoded_image.height):
        
        # initialize the red, green, and blue pixels
        ir, ig, ib = starting_image_pixels[x, y]
        
        # if the secret image pixel is black
        if secret_image_pixels[x, y] == (0, 0, 0):
          nr = int(f'{ir:08b}'[:7] + '1', 2) # update the lsb to end in 1 in red channel of encoded image      
          pixels[x, y] = (nr, ig, ib)   
        else:
          nr = int(f'{ir:08b}'[:7] + '0', 2)         # otherwise, make the lsb 0
          pixels[x, y] = (nr, ig, ib)

    encoded_image.save(f'{path_to_png[:-4]}_encoded.png')



def write_text(path_to_png, secret_message):
    
  decoded_image = Image.open(path_to_png)
      
  encoded_image = Image.new("RGB", decoded_image.size)
  
  #save the image to disk
  draw = ImageDraw.Draw(encoded_image)
  
  # use a truetype font
  font = ImageFont.truetype("cookiemonster.ttf", 240)

  draw.text((200, 250), secret_message, font=font)

  return encoded_image


# decode the sample image
# decode_image('encoded_sample.png')


# image to encode secret message in
image_to_encode = 'chocolate_chip_cookies.png'
secret_message = 'Home is where heart is. Heart where cookie is.'

# encode the secret message in the image
encode_image(image_to_encode, secret_message)

# decode the secret message from the image
decode_image(f'{image_to_encode[:-4]}_encoded.png')





#  encode_image('chocolate_chip_cookies.png', 'Home is where heart is. Heart where cookie is.')



#  secret_image = write_text('chocolate_chip_cookies.png', 'Home is where heart is. Heart where cookie is.')