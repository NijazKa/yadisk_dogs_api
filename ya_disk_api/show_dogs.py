import requests


TOKEN = input('Введите ваш токен от я.диска: ')
BREED = input('Введите название породы: ')
BREED_URL = 'https://dog.ceo/api/breeds/list/all'
DISK_URL = 'https://cloud-api.yandex.net/v1/disk/resources'
headers = {'Authorization': TOKEN}


def create_folder(folder: str) -> None: # Функция создает папку на я.диске 
    if len(folder.split('/')) == 3:
        folder_main = folder.split('/')[-2]
        print(folder_main)
        path_main = {'path': f'Dogs/{folder_main}'}
        create_main_folder = requests.put(DISK_URL, params=path_main, headers=headers)
        print(f'Первая папка из 3 создана {create_main_folder.status_code}')
        
        path_second = {'path': folder}
        create_second_folder = requests.put(DISK_URL, params=path_second, headers=headers)
        print(f'вторая папка из 3 создана {create_second_folder.status_code}')

    elif len(folder.split('/')) == 2:
        path = {'path': folder}
        create_folder = requests.put(DISK_URL, params=path, headers=headers)
        print(f'Создана папка из двух {create_folder.status_code}')
    else:
        path = {'path': folder}
        create_folder = requests.put(DISK_URL, params=path, headers=headers)
        print(f'создана папка из одной {create_folder.status_code}')
        

# функция safe_picture не сохраняет подпапки, разобраться
def safe_picture(picture_url:str, folder: str) -> None: # Функция закачивает фаил по ссылке
    file_name = picture_url.split('/')[-1]
    create_folder(f'Dogs/{folder}')
    sub_breed = '/'
    if sub_breed in folder:
        path = {'path': f'Dogs/{folder}/{folder.split('/')[-1]}_{file_name}', 'url': picture_url}
        file = requests.post(f'{DISK_URL}/upload', params=path, headers=headers)
        print(f'статус сохранения картинки субпороды {file.status_code}')
    else:
        path = {'path': f'Dogs/{folder}/{folder}_{file_name}', 'url': picture_url}
        file = requests.post(f'{DISK_URL}/upload', params=path, headers=headers)
        print(f'статус сохранения картинки обычной породы {file.status_code}')
    
def generate_dog_url(breed: str) -> str: # Функция преобразования породы в ссылку получения картинки
    url = f'https://dog.ceo/api/breed/{breed}/images/random'
    link = requests.get(url)
    link = link.json()['message']
    return link

def breed_list() -> list: # Сбор пород в список
    response = requests.get(BREED_URL)
    list = response.json()['message']
    breed_list = []
    for k, m in list.items():
        if len(m) == 0:
            breed_list.append(k)
        else:
            for sub in m:
                str = f'{k}/{sub}'
                breed_list.append(str)
    print(breed_list)
    return breed_list


def get_dog(breed:str) -> None: # Функция возвращает имена файлов 
    breed_list = []
    path = {'path': f'Dogs/{breed}'}
    response = requests.get(DISK_URL, params=path, headers=headers)
    for i in range(len(response.json()['_embedded']['items'])):
        breed_dict = {}
        #print(response.json()['_embedded']['items'][i-1]['name'])
        breed_dict['file_name'] = response.json()['_embedded']['items'][i-1]['name']
        breed_list.append(breed_dict)

    return breed_list


print(get_dog('african'))

