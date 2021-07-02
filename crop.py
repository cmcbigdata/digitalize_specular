from PIL import Image
import os

LABELS = {
    'Laterality_OD': (45,107,84,130),
    'Laterality_OS': (548,106,586,130),
    'CD_OD': (240,140,276,157),
    'CD_OS': (357,138,391,156),
    'CV_OD': (240,157,276,172),
    'CV_OS': (355,155,395,173),
    'HEX_OD': (241,173,276,189),
    'HEX_OS': (357,171,392,188),
    'CellNum_OD': (240,188,277,204),
    'CellNum_OS': (363,187,392,205),
    'Pachy_OD': (240,203,277,220),
    'Pachy_OS': (356,206,392,222),
    'AVE_OD': (241,234,276,251),
    'AVE_OS': (357,234,391,251),
    'MAX_OD': (239,252,277,267),
    'MAX_OS': (356,251,392,267),
    'MIN_OD': (241,268,277,283),
    'MIN_OS': (357,268,393,284),
    'SD_OD': (241,284,277,300),
    'SD_OS': (356,284,393,301),
    'Specular_OD': (145,143,234,276),
    'Specular_OS': (401,143,491,276),
}

def save_label(out_dir,category,label_name, image, image_name):
    croped = image.crop(LABELS[label_name])
    if category<10:
        folder = f'{out_dir}/category0{category}_{label_name}'
    else:
        folder = f'{out_dir}/category{category}_{label_name}'
    if not os.path.exists(folder):
        os.makedirs(folder)
    croped.save(folder+'/'+image_name)

out_dir = 'predictions'
main_dir = "/home/ubuntu/data/Specular/Specular_new"
#main_dir = '/home/ubuntu/data/Workspace/Yoonkyoung/sp_sample/Img_both'
image_lst = os.listdir(main_dir)

cnt=0
for image_name in image_lst:
    print(cnt)
    cnt+=1
    img = Image.open(main_dir+'/'+image_name)
    category=0
    for label in LABELS:
        save_label(out_dir,category,label,img,image_name)
        category+=1