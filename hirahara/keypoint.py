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
        #res = [[0 for i in range(width)] for j in range(height)]
        s = set()
        for x in range(1, width-1):
            for y in range(1, height-1):
                check_pos = []
                x_min = x - 1
                x_max = x + 1
                y_min = y - 1
                y_max = y + 1
                values = []
                for xx in range(x_min, x_max):
                    for yy in range(y_min, y_max):
                        values.append(img[xx][yy])
                max_val = max(values)
                min_val = min(values)
                val = img[x][y]
                #print(max_val - min_val)
                if ((max_val - min_val) > threshold and
                    (min_val == val or max_val == val)):
                    s.add((x, y))
                """
                else:
                    res[x][y] = False
                """
                    
        minmax_list.append(s)
    # octave間の判定
    for i in range(1, len(minmax_list)-2):
        for x in range(width):
            for y in range(height):
                if ((x, y) in minmax_list[i-1] and
                    (x, y) in minmax_list[i  ] and
                    (x, y) in minmax_list[i+1]):
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
        #r += 5

    plt.show()

# end of file
