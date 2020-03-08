import jpeg4py as jpeg
import matplotlib.pyplot as pp


if __name__ == "__main__":
    pp.imshow(jpeg.JPEG("test.jpg").decode())
    pp.show()