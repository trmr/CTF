import urllib
from PIL import Image

def solve(id):
  image = []
  for a in "LRUDFB":
    img = urllib.urlopen("http://qubicrube.pwn.seccon.jp:33654/images/"+id+"_"+a+".png").read()
    name = "download/"+id+"_"+a+".png"
    open(name, "wb").write(img)
    t = Image.open(name)
    image += [[t, t.transpose(Image.ROTATE_90), t.transpose(Image.ROTATE_180), t.transpose(Image.ROTATE_270)]]
  for bb in "LRUDFB":
    base = Image.open("download/"+id+"_"+bb+".png")
    for pos in range(8):
      for i in range(6):
        for j in range(4):
          ok = True
          for k in range(82):
            a = image[i][j].getpixel((
              [82,164,82,81,0,164,164,0][pos] + [1,0,1,0,1,1,1,1][pos]*k,
              [81,82,164,82,81,81,164,164][pos] + [0,1,0,1,0,0,0,0][pos]*k))
            b = base.getpixel((
              [82,163,82,82,0,164,164,0][pos] + [1,0,1,0,1,1,1,1][pos]*k,
              [82,82,163,82,82,82,163,163][pos] + [0,1,0,1,0,0,0,0][pos]*k))
            if a!=b:
              ok = False
          if ok:
            ox = [82,164,82,0,0,164,164,0][pos]
            oy = [0,82,164,82,0,0,164,164][pos]
            for y in range(82):
              for x in range(82):
                base.putpixel((ox+x,oy+y), image[i][j].getpixel((ox+x,oy+y)))
    base.save(id[:2]+"_"+bb+".png")

import subprocess

id = "01000000000000000000"
while True:
  print id[:2]
  solve(id)
  nextid = ""
  for a in "LRUDFB":
    res = subprocess.check_output((r"zbarimg", "-q", id[:2]+"_"+a+".png"))
    print a, res[:-1]
    if "http" in res:
      nextid = res[len("QR-Code:http://qubicrube.pwn.seccon.jp:33654/"):-1]
  if nextid=="":
    break
  id = nextid