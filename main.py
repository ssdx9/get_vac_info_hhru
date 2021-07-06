import requests
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

#Запрос объема пагинации
def req_pag(kword,per_page):    
    r=requests.get('https://api.hh.ru/vacancies', 
        params={'text':kword, 'per_page':per_page})      
    pages=r.json()['pages']    
    return pages

#Получение вакансий
def req_vacs(kword,per_page,pages):    
    vacs=[]
    #Пагинация:
    for p in range(pages):    
        r=requests.get('https://api.hh.ru/vacancies',
                params={'text':kword, 
                        'per_page':per_page,
                        'page':p}).json()['items']                
        print(f"Reading page {p} of {pages}")
        #Сохранение ссылок на каждую вакансию:
        for i in range(len(r)): 
            vacs.append(r[i]['url']) 
    return vacs

#Извлечение "Ключевых навыков" и запись в файл:
def file_kskills(vacs):
    with open("Outputtext.txt", "w", encoding="utf-8") as text_file:        
        for vac in range(len(vacs)):
            det_vac=requests.get(vacs[vac]).json()
            kskills=det_vac['key_skills']            
            for index in range(len(kskills)):            
                for key in kskills[index]:
                    strraw = f"{kskills[index][key]}\n" 
                    strprep = strraw.replace(" ","_") #приведение каждой записи к n-грамме                    
                    text_file.write(strprep)
        print(f"Retrieving key skills from from vacancy {vac}")

#Вывод из файла в WordCloud:
def wc_kskills(kword):
    wctext = open('Outputtext.txt', encoding='utf-8').read()
    sw = set(STOPWORDS)
    sw.add(kword) #исключение из WC самого запроса
    wc = WordCloud(background_color="black", stopwords=sw,                    
                    contour_width=3, contour_color='steelblue', scale=15, 
                    collocations=False) #отключения поиска коллокаций для избежания ложного срабатывания
    wc.generate(wctext)
    
    plt.title(f'"{kword}" - сопутствующие ключевые навыки')
    plt.axis("off")
    plt.imshow(wc, interpolation="bilinear") 
    plt.show()

#Набор функций:
def getvacs():
    per_page = 100        
    kword = input ('Введите ключевое слово для поиска сопутствующих навыков:')
    pages = req_pag(kword,per_page)
    vacs = req_vacs(kword,per_page,pages)    
    file_kskills(vacs)
    print(f"Preparing wordcloud...")
    wc_kskills(kword)

getvacs()