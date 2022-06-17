import requests
import shutil
import time
import os
import random
from PIL import Image

'''
pip3 install requests
pip3 install Pillow
'''

'''
// copy this code snippet to the console of the orders.flashphotography.com website that has all your images
// (website ex: https://orders.flashphotography.com/Orders/Packages.aspx?...&GroupImage=#)
// this will get all the images from the magnifier. You can also manually copy the images from the magnifier for pictures you want to use.
const AId = $(".Qty > select").attr("name").split("_")[1]
const arr = []
$('.ProofInfo > a').each(function (i, e) {
    const link = $(e).attr("href")
    const sub = link.substring(link.indexOf("?") + 1, link.indexOf('&ViewID'))
    arr.push(`${sub}&A=${AId}`)
})
// copy this array output and replace it with photos
console.log(JSON.stringify(arr))
'''

IMG_HOST = 'http://magnifier.flashphotography.com/MagnifyRender.ashx'

# paste the output from the above code snippet here
# sometimes the picture download errors, if so just go http://magnifier.flashphotography.com/Magnify.aspx?<metadata> and click on one section and try the script again.
PHOTO_LINKS = [
    # "O=27148873&R=00102&F=1049&A=71992",
]

def download_chunks(photo_link, path):
    print('Download image')
    for X in range(-50, 501, 50):
        for Y in range(-50, 701, 50):
            print('Downloading image at X: {} Y: {}'.format(X, Y))
            time.sleep(0.2)
            output_path = path + str(X) + '_' + str(Y) + '.jpg'
            url_path = IMG_HOST + '?X=' + str(X) + '&Y=' + str(Y) + '&' + photo_link + '&rand=' + str(random.random())
            print(url_path)
            r = requests.get(url_path, stream=True)
            if r.status_code == 200:
                with open(output_path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

def combine_chunks(photo_link, path):
    print('Combine image')
    combined_img = Image.new('RGB', (550, 750))
    for X in range(-50, 501, 50):
        for Y in range(-50, 701, 50):
            input_path = path + str(X) + '_' + str(Y) + '.jpg'
            img = Image.open(input_path)
            img_crop = img.crop((40, 40, 90, 90))
            combined_img.paste(img_crop, (X,Y))
    combined_img.save('final/{}.jpg'.format(photo_link))

def crop_photo(photo_link):
    print('Crop image')
    img = Image.open('final/{}.jpg'.format(photo_link))
    img_crop = img.crop((54, 54, 532, 682))
    img_crop.save('final/{}.jpg'.format(photo_link))

for photo_link in PHOTO_LINKS:
    try:
        path = r'data_{}/'.format(photo_link)
        print(path)
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            shutil.rmtree(path)
            os.makedirs(path)
        
        if not os.path.exists('final'):
            os.makedirs('final')

        download_chunks(photo_link, path)
        combine_chunks(photo_link, path)
        crop_photo(photo_link)

        shutil.rmtree(path)
        time.sleep(30)
    except Exception as e:
        print('Error: ' + str(e))
