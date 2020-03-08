from PIL import Image

image = []
name = "download/35b9575e4f05df6c47e1_R.png"
t = Image.open(name)
image += [[t, t.transpose(Image.ROTATE_90), t.transpose(Image.ROTATE_180), t.transpose(Image.ROTATE_270)]]

for pos in range(8):
      for i in range(6):
        for j in range(4):
          ok = True
          for k in range(82):
            a = image[i][j].getpixel((
              [82,164,82,81,0,164,164,0][pos] +   [1,0,1,0,1,1,1,1][pos]*k,
              [81,82,164,82,81,81,164,164][pos] + [0,1,0,1,0,0,0,0][pos]*k))
            print [82,164,82,81,0,164,164,0][pos] + [1,0,1,0,1,1,1,1][pos]*k
            print [81,82,164,82,81,81,164,164][pos] + [0,1,0,1,0,0,0,0][pos]*k

            # 82,81 - 164,81; 164,82-164,164