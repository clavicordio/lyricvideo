<b>A little program for making pixel art lyric videos.</b>

I wrote this project to make 8bit lyric videos for my music project <i>Flying Salmon</i>.
 
Then, some people were curious to see the source code and asked me to share it. Well, here it is! The code is a bit messy and not very user-friendly for customization, because I didn't expect anyone to ever see it. 
Here's an example of what you can make:
 
https://youtu.be/uMxgx-nJi9o

So basically a program takes:
1) a gif animation
2) a lyric text file with timecodes (see ```lyrics``` folder for examples)
3) an audio file

and combines it into a pixel perfect aesthetic lyric video.



Requirements:
1) ```ffmpeg``` (https://www.ffmpeg.org)
2) ```pip3 install numpy pillow sk-video opencv-python``` (or simply ```pip3 install -r requirements.txt```)

Running:
1) ```setup.py``` - downloads data
2) ```main.py``` - creates a lyric video.


To configure it, you should create a configuration file (see ```config_dailyjourney.py``` or ```config_underwatercity.py``` as an example) and specify it in ```main.py``` as follows:

```from config_dailyjourney import *```

Enjoy! 

Please let me know if this code helps you create a lyric video of your own, I'd really love to see it! 

________________________

Contact me on social media or check out my music: https://linktr.ee/FlyingSalmon

Shoutout to Alena for drawing the GIFs! https://www.instagram.com/alena_alien_art/

Also thanks to  <i>Codeman38 (cody@zone38.net)</i> for creating the <b>PressStart2P</b> font!


