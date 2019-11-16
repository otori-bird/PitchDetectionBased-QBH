import os
import codecs
from pydub import AudioSegment


# with open("temp.txt","rb") as f:
#     u = f.read().decode("utf-16")
#     t = u.encode("utf-8")
#     c = 5
with open("./data/Pray.wav","wb") as f:
    f.close()
sound = AudioSegment.from_mp3("Pray.mp3")
sound.export("./data/Pray.wav", format="wav")