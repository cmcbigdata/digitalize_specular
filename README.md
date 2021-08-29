# Digitalize_specular

crop.py is used to crop the image into different image segments (based on xy pixel coordinates). Run the following code to run crop.py

```
python crop.py --image_dir [크롭할 이미지 폴더] --output_dir [크롭된 이미지 저장할 폴더] --label_dir [UI 를 통해 얻은 xy coordinate CSV 파일]
```

image_to_txt.py is used to convert the different segments into text and save to csv file. Run the following code to run image_to_txt.py

```
python image_to_txt.py --test_dir [OCR 할 이미지 폴더] 
*crop.py 할때 [크롭할 이미지 폴더] 와 동일*
```

front_UI.py is simple UI code using PyQt5 for user to provide the xy-coordinates of the label to extract from the image. (provides the csv file for input to --label_dir used in crop.py). However, current code does not support which variable name the xy coordinate is labeled for. Needs additional code.

*Make sure to use python 3.6 for compatibility with opencv*
