# Краткое описание
Устройство представляет собой крупногабаритную подзорную трубу, которая обладает возможностью фокусироваться на объекты, находящиеся в диапазоне расстояний 3-10000 метров.

# Команда
Кулаев Фёдор, группа Б04-303 

Ветров Алексей, группа Б04-303


# Цель проекта
Все сталкивались с проблемой, что при использовании бинокля при перенаведении его на более или менее удалённый предмет приходится двигать колёсико регулировки. Мы поставили перед собой задачу собрать устройство, которое сможет перефокусироваться автоматически. 


# Подробное описание устройства
Оптическая схема состоит из схемы Кеплера, где объектив - линза на 3 дптр, окуляр - линза на 16 дптр(Теоретическое увеличение такой схемы 5.33). В конце схемы мы добавили делитель луча. Одна половина луча попадает на камеру, с помощью которой мы понимаем, в фокусе находятся объекты или нет. Моторчиком двигаем одну линзу относительно другой до того момента, пока изображение не окажется сфокусированным. Моторчиком и состоянием фокусировки управляет микрокомпьютер. Питание за счёт powerbank.


# Компоненты
Объектив - линза для очков на 3 дптр (https://market.yandex.ru/product--linza-dlia-ochkov-sfericheskaia-1sht-ice-maker-d-65-index-1-70/1884922652?sku=102071359570&uniqueId=964545&showOriginalKmEmptyOffer=1)

Окуляр - линза для очков на 16 дптр (https://market.yandex.ru/product--linza-dlia-ochkov-sfericheskaia-1sht-ice-maker-d-60-index-1-70/1884926108?sku=102071359528&uniqueId=964545&showOriginalKmEmptyOffer=1)

Мотор DC205 RPM 

Драйвер к мотору TB6612FNG

Камера Pi-camera module 3

Микрокомпьютер Raspberry Pi Zero v1.3 (в процессе настройки использовалась Raspberry Pi 4 model B)

PD-триггер для получения нужного напряжения с powerbank (https://www.ozon.ru/product/trigger-modul-fastcharge-9v-12v-15v-20v-1156203022/?reviewsVariantMode=2)

powerbank


# Трудности 
Наше устройство получилось довольно большим ввиду того, что мы не имеем возможности обрезать под нужный диаметр линзы, и поэтому в процессе разработки было принято решение вместо бинокля сделать подзорную трубу.

Мы хотели всё запитать с помощью одного powerbank, поэтому нам пришлось дополнительно приобрести PD-триггер для получения нужного напряжения на моторах


# Существующие аналоги
<([https://www.amazon.com/s?k=autofocus+binoculars)](https://www.amazon.com/Bushnell-Waterproof-Spectator-Binocular-10x50mm/dp/B07353SGQG/ref=sr_1_2?dib=eyJ2IjoiMSJ9.P-iXW86EkNQRRb_yhQdGQklRsZmOZBnbjMBHXZ-HVRhW5Rf-N8rl2i5FDKiHmXHR20MRqxE30GU0fvmaiHydaFRAsWpPJ_s9l78y7PAjW7kg4rbgBmaHCn5x6uvtdMW-w1fjW0iNGG-HielwBWobSbSN34vpxXrCPYL49aFq8YKl9eZ1dcsXSahYJdS2GgbsKflhcc_d7e4hytqYKhzRZeX8bGFT0TDznpCeqbJtUCc.bEGMcOQOpADVm-uDvyADaEo49JktgrikeFhsy2YIh9o&dib_tag=se&keywords=autofocus%2Bbinoculars&qid=1747322670&sr=8-2&th=1)>

<<https://binokl.shop/product/free-focus-bpsh-8x40>>


# Фото
![photo_2025-05-16 11 59 47](https://github.com/user-attachments/assets/795c9990-0035-4cd6-ba6d-69b25dae7228)


# Видео


https://github.com/user-attachments/assets/4ccdcfca-6943-4ccf-b469-e8c1348ee5a3




