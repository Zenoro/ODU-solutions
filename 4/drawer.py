import os
import sys
from PIL import Image, ImageDraw

im = Image.new('RGB', (1800, 700), (255, 255, 255))
draw = ImageDraw.Draw(im)

axeswidth = 6
trackwidth = 2
#scale_x = 500
scale_x = 300
#scale_y = 100
scale_y = 300

with open('res.txt') as f:
    lines = f.readlines();

tls = []
d_x, d_y = lines[0].split()
x_center = 900
y_center = 350
d_x = float(d_x)
d_y = float(d_y)
num_left = 0
num_right = 0
for i in range(1, len(lines)):
    x_tl, y_tl = lines[i].split()
    tls.append((float(x_tl), -float(y_tl)));
    if float(x_tl) * scale_x < 0:
        num_left += 1
    else:
        num_right += 1

draw.line((50, y_center, 2 * x_center - 50, y_center), fill = 'blue', width = axeswidth);
draw.line((x_center, 50, x_center, 2 * y_center - 50), fill = 'blue', width = axeswidth);

for i in range(len(tls)):
	draw.rectangle((tls[i][0] * scale_x + x_center, tls[i][1] * scale_y + y_center, (tls[i][0] + d_x) * scale_x + x_center, (tls[i][1] + d_y) * scale_y + y_center), fill = 'black');
    
draw.ellipse((x_center - axeswidth, y_center - axeswidth - scale_y, x_center + axeswidth, y_center + axeswidth - scale_y), 'yellow', 'blue')
draw.ellipse((x_center - axeswidth, y_center - axeswidth + scale_y, x_center + axeswidth, y_center + axeswidth + scale_y), 'yellow', 'blue')
draw.ellipse((x_center - axeswidth - scale_x, y_center - axeswidth, x_center + axeswidth - scale_x, y_center + axeswidth), 'yellow', 'blue')
draw.ellipse((x_center - axeswidth + scale_x, y_center - axeswidth, x_center + axeswidth + scale_x, y_center + axeswidth), 'yellow', 'blue')

filename = "res"
im.save(filename + '.png')

# print(num_left, num_right)

#os.remove('res.txt')
#os.remove('a.out')
