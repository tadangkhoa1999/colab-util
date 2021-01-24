import os
import io
from datetime import datetime
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML, Audio
from google.colab.output import eval_js
from base64 import b64decode


class ColabPhoto():

    @staticmethod
    def take_photo(folder, quality=1.0, size=(800, 600)):
        if folder[-1] != '/':
            folder += '/'
        VIDEO_HTML = """
        <video autoplay
         width=%d height=%d style='cursor: pointer;'></video>
        <script>

        var video = document.querySelector('video')

        navigator.mediaDevices.getUserMedia({ video: true })
          .then(stream=> video.srcObject = stream)

        var data = new Promise(resolve=>{
          video.onclick = ()=>{
            var canvas = document.createElement('canvas')
            var [w,h] = [video.offsetWidth, video.offsetHeight]
            canvas.width = w
            canvas.height = h
            canvas.getContext('2d')
                  .drawImage(video, 0, 0, w, h)
            video.srcObject.getVideoTracks()[0].stop()
            video.replaceWith(canvas)
            resolve(canvas.toDataURL('image/jpeg', %f))
          }
        })
        </script>
        """
        display(HTML(VIDEO_HTML % (size[0], size[1], quality)))
        data = eval_js("data")
        binary = b64decode(data.split(',')[1])
        f = io.BytesIO(binary)
        img = np.asarray(Image.open(f))
        timestampStr = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
        filename = '%sphoto_%s.jpeg' % (folder, timestampStr)
        Image.fromarray(img).save(filename)
        print('Image captured and saved to %s' % filename)

    @staticmethod
    def display_folder_content(folder, res=256):
        if folder[-1] != '/':
            folder += '/'
        for i, img_path in enumerate(sorted(os.listdir(folder))):
            if '.png' in img_path:
                display(Image.open(folder+img_path).resize((res, res)),
                        'img %d: %s' % (i, img_path))
                print('\n')

    @staticmethod
    def display_sbs(folder1, folder2, res=256, fs=12):
        if folder1[-1] != '/':
            folder1 += '/'
        if folder2[-1] != '/':
            folder2 += '/'

        imgs1 = sorted([f for f in os.listdir(folder1) if '.png' in f])
        imgs2 = sorted([f for f in os.listdir(folder2) if '.png' in f])
        if len(imgs1) != len(imgs2):
            print("Found different amount of images in %s vs %s directories. That's not supposed to happen..." % (
                folder1[:-1], folder2[:-1]))

        for i in range(len(imgs1)):
            img1 = Image.open(folder1+imgs1[i]).resize((res, res))
            img2 = Image.open(folder2+imgs2[i]).resize((res, res))
            f, axarr = plt.subplots(1, 2, figsize=(fs, fs))
            axarr[0].imshow(img1)
            axarr[0].title.set_text('%s %d' % (folder1[:-1], i))
            axarr[1].imshow(img2)
            axarr[1].title.set_text('%s %d' % (folder2[:-1], i))
            plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[])
            plt.show()
            print("")
