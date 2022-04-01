import re

def toascii(text:str):
    return re.sub(r'[^a-zA-Z0-9]+','', text)



def speedMapper(speed:float,decimal=3):

    ref = ['B','KB','MB','GB']
    i=0
    while speed >= 1024 :
        if i > 3:
            i=3
            break
        speed = speed / 1024
        i+=1

    return f"{round(speed,decimal)} {ref[i%4]}/s"


