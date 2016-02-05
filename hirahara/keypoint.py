from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from scale_space import ScaleSpace
from dog import dog

def extract_keypoints(octave, threshold):
    ## ここに処理を書く
    keypoints = []
    minmax_list = []
    # 各イメージの最大値、最小値の判定
    (width, height) = octave[0].shape
    for img in octave:
        res = [[0 for i in range(width)] for j in range(height)]
        for x in range(width):
            for y in range(height):
                check_pos = []
                x_min = x - 1
                x_max = x + 1
                y_min = y - 1
                y_max = y + 1
                if x == 0:
                    x_min = 0
                elif x == width-1:
                    x_max = x
                if y == 0:
                    y_min = 0
                elif y == height-1:
                    y_max = y
                min_val = 0
                max_val = 255
                for xx in range(x_min, x_max):
                    for yy in range(y_min, y_max):
                        if min_val < img[xx][yy]:
                            min_val = img[xx][yy]
                        if max_val > img[xx][yy]:
                            max_val = img[xx][yy]
                res[x][y] = 0
                #print(max_val - min_val)
                if (abs(max_val - min_val) > threshold and
                    (min_val == img[x][y] or
                     max_val == img[x][y])):
                    res[x][y] = 1
        minmax_list.append(res)
    # octave間の判定
    for i in range(1, len(minmax_list)-2):
        for x in range(width):
            for y in range(height):
                if (minmax_list[i-1][x][y] == 1 and
                    minmax_list[i  ][x][y] == 1 and
                    minmax_list[i+1][x][y] == 1):
                    keypoints.append([x, y])
    print('point num = %d' % len(keypoints))
    return keypoints


if __name__ == '__main__':
    lena_img = Image.open('img/lena.jpg').convert('L')
    lena_img = np.array(lena_img, dtype=np.float) / 255

    print('Create Scale-space')
    scale_space = ScaleSpace(lena_img)
    scale_space.create()

    print('Apply DoG to Scale-space')
    dog_space = dog(scale_space)

    keypoint_space = []
    for octave in dog_space:
        keypoint_space.append([])
        keypoint_space[-1].append(extract_keypoints(octave, 0.01))

    print('Draw keypoints')
    plt.imshow(lena_img, cmap='Greys_r')
    fig = plt.gcf()
    r = 1
    for n, octave in enumerate(keypoint_space):
        for l, layer in enumerate(octave):
            for p in layer:
                m = np.power(2, n)
                fig.gca().add_artist(plt.Circle((p[1]*m, p[0]*m), r, color='r', fill=False))
        r += 5

    plt.show()

# end of file
