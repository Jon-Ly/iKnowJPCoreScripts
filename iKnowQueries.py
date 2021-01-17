from bs4 import BeautifulSoup
import os 
import lxml, urllib.request, time

ids = [
        '566921', '566922', '566924', '566925', '566926', '566927', '566928', '566929', '566930', '566932', # Japanese Core 1000
        '594768', '594770', '594771', '594772', '594773', '594774', '594775', '594777', '594778', '594780', # Japanese Core 2000
        '615865', '615866', '615867', '615869', '615871', '615872', '615873', '615874', '615876', '615877', # Japanese Core 3000
        '615947', '615949', '615950', '615951', '615953', '615954', '615955', '615957', '615958', '615959', # Japanese Core 4000
        '616077', '616078', '616079', '616080', '616081', '616082', '616083', '616084', '616085', '616086', # Japanese Core 5000
        '598434', '598432', '598431', '598430', '598427', '598426', '598425', '598424', '598423', '598422'  # Japanese Core 6000
    ]

core_counter = 1
step_counter = 1

try:
    os.mkdir('jcoreJson')
except OSError as error:  
    print(error)


for id in ids:
    request = urllib.request.Request(
        'https://iknow.jp/api/v2/goals/' + id + '?')
    words_and_sentences = urllib.request.urlopen(request)
    soup = BeautifulSoup(words_and_sentences, 'lxml')

    try:
        new_file = open(f'jcoreJson/Japanese_Core_{str(core_counter)}_{str(step_counter)}.txt', 'w+', encoding='utf-8')
        new_file.write(soup.prettify().split('<p>')[1].strip().split('</p>')[0].strip())
        if step_counter == 10:
            step_counter = 1
            core_counter += 1
        else:
            step_counter += 1

            new_file.close()
    except OSError as error:  
        print(error)
