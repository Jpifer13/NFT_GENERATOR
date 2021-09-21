import os
import random
import time
from PIL import Image
import itertools
import threading
import sys


class ImageCollection:
    def __init__(self, image_collection_directory: str) -> None:
        self.image_collection_directory = image_collection_directory
        self.layers = {}
    
    def populate_collection_layers(self) -> None:
        path = self.image_collection_directory
        for directory in os.scandir(path):
            if directory.is_dir():
                self.layers[directory.name] = []
                for filename in os.scandir(directory.path):
                    if filename.is_file():
                        self.layers[directory.name].append(filename.path)
    
    def generate_random_order(self):
        for layer_key in self.layers.keys():
            random.shuffle(self.layers[layer_key])
    
    def _squish(self, background: str, base: str, eye: str, hair: str, accessory: str) -> Image:
        base = Image.open(base)
        background_image = Image.open(background)
        if base.size != background_image.size:
            background_image = background_image.resize(base.size)
        eyes = Image.open(eye)
        hair = Image.open(hair)
        accessories = Image.open(accessory)
        background_image.paste(base, (0,0), base)
        background_image.paste(eyes, (0,0), eyes)
        background_image.paste(hair, (0,0), hair)
        background_image.paste(accessories, (0,0), accessories)
        
        return background_image
    
    def combine_layers(self, counter=0):
        try:
            os.makedirs(f'{os.getcwd()}/output')
        except Exception as err:
            print(err)
        for background in self.layers['background']:
            for eye in self.layers['eyes']:
                for hair in self.layers['hair']:
                    for accessory in self.layers['accessories']:
                        self._squish(background, self.layers['base'][0], eye, hair, accessory).save(f'{os.getcwd()}/output/image{counter}.png')
                        if counter%50 == 0:
                            print(f"Image {counter} complete!")
                        counter+=1
                        

PROCESS_COMPLETE = False
#here is the animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if PROCESS_COMPLETE:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')


if __name__ == '__main__':
    print("Enter the path to the folder containing your assets input.")
    print(f"Here is an example path: {os.getcwd()}")
    image_collection_input_directory = input('Enter folder path here: ')
    collection = ImageCollection(image_collection_directory=image_collection_input_directory)
    collection.populate_collection_layers()
    collection.generate_random_order()
    print('Glueing layers... This can take up to an hour depending on the amount of features and layers.')
    t = threading.Thread(target=animate, daemon=True)
    t.start()
    start = time.perf_counter()
    collection.combine_layers()
    finish = time.perf_counter()
    PROCESS_COMPLETE = True
    print(f'Glueing complete in: {finish - start} seconds...')
    input('Press ENTER or RETURN to exit.')
