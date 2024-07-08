#clean csv data for the format you want 
import csv

def scrub_to_csv():
    cleaned_data=[]
    # we are adding the brackets cause some of the elements further on in the periodic table have theoretical weights and the . is to include the decimal point
    numbers=['0','1','2','3','4','5','6','7','8','9','0','[',']','.']
    
    def clean_data(element,colnum,rownum):
        index=0
        name=''
        number=''
        symbol=''
        weight=''

        while index<len(element) and element[index] not in numbers:
            if element[index]=='Â':  # \xad is new line dash which appears after this special charatcer so we use +2 
                index+=2
            else:
                name+=element[index]
                index+=1
        
        while index<len(element) and element[index] in numbers:
            number+=element[index]
            index+=1

        while index<len(element) and element[index] not in numbers:
            if element[index]=='â':  # â€‹ indicates difference between weigth and symbol of the element hence we skip three characters
                index+=3
            else:
                symbol+=element[index]
                index+=1
        
        while index<len(element) :
            if element[index] in numbers:
                weight+=element[index]
            index+=1

        return [name,number,symbol,weight,colnum,rownum]


    with open('Periodic Data.csv',newline='') as csvfile :
        reader = csv.reader(csvfile)
        count=0
        # skip row 1 and 2 since they are headers 
        for row in reader:
            # +print(row)
            if count>1:
                for i in range(len(row)):
                    if len(row[i])>1 and row[i]!='Period 1': 
                        #since the periodic table is not a perfect rectangle we will get some empty strings so to prevent that we are adding this 
                        #also the first element in the cleaned data is something called period 1 so we add the second condition to manually clean out the data 
                        cleaned_data.append(clean_data(row[i],i,count))
            count+=1

    # print(cleaned_data)
    return cleaned_data


                    


scrub_to_csv()