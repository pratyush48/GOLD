'''This code is written by @Pratyush Nandi-Research Assistant at IIIT Bangalore
   Functionality of this code is to implement a extraction of area and delay from results of VTR'''
class extract():
    def __init__(self,filename):
        print("reached extraction script")
        self.my_file = open(filename,"r+")
        self.my_file.seek(0)

    def __del__(self):
        print("deleted extraction script object")

    def main(self):
        cont = self.my_file.readlines()
        headings = cont[0]
        values = cont[1]
        hwords = []
        vwords = []

        j = ''
        for i in headings:
            if(i !='\t'):
                j = j+i
            if(i =='\t'):
                hwords.append(j)
                j = ''
        j = ''
        for i in values:
            if(i !='\t'):
                j = j+i
            if(i =='\t'):
                vwords.append(j)
                j = ''

        area = -1
        delay = 0
        for i in range(0,len(hwords)):
            if(hwords[i] == 'logic_block_area_total'):
                area = float(vwords[i])
                print(area)
            if(hwords[i] == 'crit_path_total_sta_time'):
                delay = float(vwords[i])
                print(delay)
        self.my_file.close()
        print(len(hwords))
        print(len(vwords))
        return area*delay