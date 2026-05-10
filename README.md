# Django Quiz App

Django ile geliştirilmiş çok kullanıcılı bir quiz/test uygulaması.

## Özellikler

- Kullanıcı kayıt ve giriş sistemi
- Test oluşturma (kayıtlı kullanıcılar)
- Sorulara görsel ekleme
- Çoktan seçmeli sorular (A/B/C/D)
- Puan sistemi ve sonuç değerlendirmesi
- Kayıtsız kullanıcılar testleri çözebilir
- Kategori sistemi
- Modern ve responsive tasarım

## Puan Skalası

| Yüzde | Değerlendirme |
|-------|--------------|
| %85 ve üzeri | Mükemmel |
| %70 - %84 | Çok İyi |
| %50 - %69 | İyi |
| %30 - %49 | Orta |
| %30 altı | Yetersiz |

## Kullanılan Teknolojiler

- Python 3.13
- Django 6.0
- Bootstrap 5.3
- SQLite

## Kurulum

```bash
git clone https://github.com/SemihYakup/Quiz-app.git
cd Quiz-app
pip install django pillow
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Geliştirici

Semih Yakup  
GitHub: https://github.com/SemihYakup
