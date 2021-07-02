from pytesseract import image_to_string
import os
import pandas
import cv2
import concurrent.futures
import time

class Converter:
    def __init__(self):
        self.main_dir = 'predictions'
        os.environ['OMP_THREAD_LIMIT'] = '1'
        # 추출한 text data를 .txt file로 저장
        self.text_dir = "category.txt"
        f = open(self.text_dir, "r")
        category_names = f.readlines()
        self.category_list=["file_name"]
        self.category_dict = {}
        del category_names[0]
        category_idx = 0
        for category_name in category_names:
            self.category_dict[category_idx] = category_name.split("\n")[0]
            category_idx += 1
        for category_idx in range(21):
            self.category_list.append(self.category_dict[category_idx])
        self.eye_dict = {}
        self.csv_total_list =[]

    def ocr(self, image_name):
        df = pandas.DataFrame(columns = self.category_list)
        #txt_file = open(main_dir+"%s/text/%s.txt"%(os.path.dirname(image_name).replace("VF", "new_VF"), image_name.split("/")[-1].split(".")[0]), 'w')
        csv_save_list=[]
        csv_save_list.append(image_name.split("/")[-1].split(".")[0])
        for category_idx in range(21):
            image_file = self.main_dir+"%s/category%02i_%s/%s"%(os.path.dirname(image_name).replace("VF", "new_VF"), category_idx, self.category_dict[category_idx], image_name.split("/")[-1])
            if os.path.exists(image_file):
                image = cv2.imread(image_file)
                resize_image = cv2.resize(image, dsize=(0,0), fx=4.3, fy=4.3, interpolation=cv2.INTER_LANCZOS4)
                gry = cv2.cvtColor(resize_image, cv2.COLOR_BGR2GRAY)
                thr = cv2.adaptiveThreshold(gry, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                            cv2.THRESH_BINARY_INV, 25, 28)
                bnt = cv2.bitwise_not(thr)
                text = image_to_string(resize_image, config="--psm 6")
                csv_save_list.append(text)
            else:
                continue
            if category_idx == 2:
                if "OD" in text:
                    self.eye_dict[image_name.split("/")[-1]] = 0
                else:
                    self.eye_dict[image_name.split("/")[-1]] = 1
        csv_save_list = [csv_save_list]
        df = pandas.DataFrame(csv_save_list, columns = self.category_list)
        df.to_csv(self.main_dir+'/dataframes/'+image_name.split('.')[0]+'.csv',index=False, encoding='utf-8')
        self.csv_total_list.append(csv_save_list)
        #txt_file.close()

    def generate_txt_data(self, image_dir):
        file_name_list = os.listdir(image_dir)
        cnt=0
        beginning_time = time.time()
        with concurrent.futures.ProcessPoolExecutor(max_workers=None) as executor:
            for image_name in zip(file_name_list,executor.map(self.ocr,file_name_list)):
                cnt+=1
                if cnt%100==0:
                    print(f'Seconds to process {cnt}/76,929 examples :{time.time() - beginning_time}')
        return self.eye_dict

    def concat_dataframes(self, df_dir):
        main_df = pandas.DataFrame(columns=self.category_list)
        df_list = os.listdir(df_dir)
        for df_name in df_list:
            df = pandas.read_csv(df_dir+'/'+df_name)
            main_df = main_df.append(df)
        main_df.to_csv(self.main_dir+"/VF_text_result.csv", index=False, encoding='utf-8')

if __name__ == '__main__':
    test_dir = "/home/ubuntu/data/Specular/Specular_new"
    #test_dir = '/home/ubuntu/data/Workspace/Yoonkyoung/sp_sample/Img_both'
    converter = Converter()
    eye_dict = converter.generate_txt_data(image_dir=test_dir)
    converter.concat_dataframes('predictions/dataframes')