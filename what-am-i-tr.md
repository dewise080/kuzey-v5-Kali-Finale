# 🏠 Kuzey-emlak Gayrimenkul Platformu

> Django tabanlı, çok dilli destek, interaktif haritalar, blog sistemi, statik site oluşturma ve gelişmiş yönetici özellikleri sunan modern ve zengin özellikli bir gayrimenkul web uygulaması.

🌐 **Canlı Demo:** [https://kuzey-emlak.lotfinity.tech](https://kuzey-emlak.lotfinity.tech)

---

## 📋 İçindekiler

- [Genel Bakış](#-genel-bakış)
- [Temel Uygulamalar ve Modüller](#-temel-uygulamalar-ve-modüller)
- [Temel Özellikler](#-temel-özellikler)
- [Teknoloji Altyapısı](#-teknoloji-altyapısı)
- [Kullanıcı Özellikleri](#-kullanıcı-özellikleri)
- [Yönetici Özellikleri](#-yönetici-özellikleri)
- [API ve Entegrasyon](#-api-ve-entegrasyon)
- [Statik Site Oluşturma](#-statik-site-oluşturma)
- [Çoklu Dil Desteği](#-çoklu-dil-desteği)

---

## 🎯 Genel Bakış

**Kuzey-emlak**, Django üzerine inşa edilmiş sofistike ve tam özellikli bir gayrimenkul yönetim platformudur. Gayrimenkul ajanslarının mülk ilanlarını, emlakçıları, müşteri taleplerini ve blog içeriklerini şık bir yönetici arayüzü üzerinden yönetmesini sağlarken, kullanıcılara interaktif haritalar, mülk arama ve iletişim özellikleri sunan modern bir ön yüz deneyimi sağlar.

Platform **13 dil** destekler, CDN dağıtımı için **statik site oluşturma** sunar ve mülk fotoğraflarını filigran ekleme ve düzenleme için gelişmiş **görüntü işleme araçları** içerir.

### 🚀 Hızlı Bağlantılar - Şimdi Deneyin!

| Sayfa | Bağlantı |
|-------|----------|
| 🏠 **Ana Sayfa** | [https://kuzey-emlak.lotfinity.tech/tr/](https://kuzey-emlak.lotfinity.tech/tr/) |
| 🏢 **Tüm Mülkler** | [https://kuzey-emlak.lotfinity.tech/tr/properties/](https://kuzey-emlak.lotfinity.tech/tr/properties/) |
| 🗺️ **İnteraktif Harita** | [https://kuzey-emlak.lotfinity.tech/tr/map/](https://kuzey-emlak.lotfinity.tech/tr/map/) |
| 💳 **Finansman** | [https://kuzey-emlak.lotfinity.tech/tr/financing/](https://kuzey-emlak.lotfinity.tech/tr/financing/) |
| 📧 **İletişim** | [https://kuzey-emlak.lotfinity.tech/tr/contact/](https://kuzey-emlak.lotfinity.tech/tr/contact/) |
| 📡 **API İlanları** | [https://kuzey-emlak.lotfinity.tech/api/listings](https://kuzey-emlak.lotfinity.tech/api/listings) |
| 📖 **OpenAPI Spesifikasyonu** | [https://kuzey-emlak.lotfinity.tech/api/openapi.json](https://kuzey-emlak.lotfinity.tech/api/openapi.json) |

---

## 📦 Temel Uygulamalar ve Modüller

### 1. **İlanlar** (`listings/`)
Platformun kalbi - tüm mülk ilanlarını yönetir.

| Bileşen | Açıklama |
|---------|----------|
| `Listing` modeli | Tam mülk verileri: başlık, adres, fiyat, yatak odası, banyo, metrekare, işlem türü (kiralık/satılık), mülk tipi, GPS koordinatları, bina detayları (yaş, kat, ısıtma, asansör, eşyalı durumu), site bilgisi, aidatlar ve daha fazlası |
| `ListingImage` modeli | İlan başına birden fazla görsel, sıralama, görünürlük, kırpma desteği ve ana görsel işareti |
| `ListingImportJob` modeli | Harici emlak sitelerinden otomatik web kazıma içe aktarma işleri |
| Coğrafi Kodlama | Nominatim/Geopy kullanarak otomatik adres-koordinat dönüşümü |
| İşlem Türleri | "Kiralık" ve "Satılık" desteği |

### 2. **Emlakçılar** (`realtors/`)
Danışman/emlakçı yönetimi.

| Özellik | Açıklama |
|---------|----------|
| Emlakçı profilleri | İsim, fotoğraf, açıklama, telefon, e-posta |
| MVP belirleme | En iyi performans gösteren danışmanları öne çıkarma |
| İşe başlama tarihi takibi | Danışman kıdemi yönetimi |

### 3. **İletişim** (`contacts/`)
Talep ve müşteri adayı yönetim sistemi.

| Özellik | Açıklama |
|---------|----------|
| Mülk talepleri | Kullanıcılar belirli ilanlar hakkında soru gönderebilir |
| Kullanıcı takibi | Talepleri kayıtlı kullanıcılara bağlar |
| Tekrar önleme | Aynı kullanıcının aynı ilana birden fazla talep göndermesini engeller |

### 4. **Hesaplar** (`accounts/`)
Kullanıcı kimlik doğrulama ve kontrol paneli.

| Özellik | Açıklama |
|---------|----------|
| Kayıt | Doğrulama ile tam kullanıcı kaydı |
| Giriş/Çıkış | Güvenli oturum yönetimi |
| Kullanıcı Paneli | Gönderilen talepleri ve durumlarını görüntüleme |
| Şifre güvenliği | Hashlenmiş şifre depolama |

### 5. **Blog** (`blog/`)
Tam özellikli blog sistemi.

| Özellik | Açıklama |
|---------|----------|
| Yazılar | Başlık, içerik, öne çıkan görsel, yazar, kategoriler |
| Kategoriler | Yazıları konuya göre düzenleme |
| Yorumlar | Kayıtlı kullanıcılar yorum yapabilir |
| Otomatik slug | SEO dostu URL oluşturma |
| Arama | Yazılarda tam metin arama |
| Sayfalama | Sayfalanmış yazı listeleri |
| GraphQL API | GraphQL üzerinden yazıları ve kategorileri sorgulama |

### 6. **Sayfalar** (`pages/`)
Statik sayfa yönetimi ve tema.

| Özellik | Açıklama |
|---------|----------|
| Tema Ayarları | Özelleştirilebilir renkler (ana, vurgu, arka plan, metin) |
| Yazı Tipi Yapılandırması | Özel yazı tipi içe aktarma ile Google Fonts entegrasyonu |
| Özel CSS | Ek stil enjeksiyonu |
| Statik sayfalar | Hakkında, Finansman, özel açılış sayfaları |

### 7. **Baton** (`baton/`)
Özel yönetici teması ve geliştirmeler.

| Özellik | Açıklama |
|---------|----------|
| Yönetici Temaları | Özelleştirilebilir yönetici paneli görünümü |
| Filtre geliştirmeleri | Açılır menü, giriş ve çoklu seçim filtreleri |
| Modern Arayüz | Şık, duyarlı yönetici arayüzü |

### 8. **Görüntü Araçları** (`imagetools/`)
Gelişmiş görüntü işleme yardımcıları.

| Özellik | Açıklama |
|---------|----------|
| Filigran | Konum, opaklık, ölçek kontrolü ile logo ekleme |
| Kırpma | En-boy oranına duyarlı kırpma |
| Çerçeveleme | Yuvarlatılmış köşelerle kenarlık ekleme |
| Köşe üçgenleri | Eski logoları renkli üçgenlerle kapatma |
| Yedekleme sistemi | İşlemeden önce otomatik yedekleme |

### 9. **API** (`api/`)
RESTful API uç noktaları.

| Uç Nokta | Açıklama | Canlı Deneyin |
|----------|----------|---------------|
| `/api/listings` | Koordinatlı GeoJSON ilan verileri | [🔗 Görüntüle](https://kuzey-emlak.lotfinity.tech/api/listings) |
| `/api/listings/<id>` | Tekil ilan coğrafi detayları | [🔗 Örnek](https://kuzey-emlak.lotfinity.tech/api/listings/1) |
| `/api/openapi.json` | OpenAPI 3.1 spesifikasyonu | [🔗 Spec](https://kuzey-emlak.lotfinity.tech/api/openapi.json) |
| Mekansal filtreleme | Sınırlayıcı kutu (bbox) sorgu desteği | - |
| CORS etkin | Çapraz kaynak erişimi izinli | - |

### 10. **Yaş** (`Ages/`)
Kısıtlı içerik için yaş doğrulama modülü.

---

## ✨ Temel Özellikler

### 🗺️ İnteraktif Haritalar

👉 **[Canlı Haritayı Görüntüle](https://kuzey-emlak.lotfinity.tech/tr/map/)** | **[Basitleştirilmiş Harita](https://kuzey-emlak.lotfinity.tech/tr/map-simplified/)**

- Özel işaretçilerle **Leaflet.js entegrasyonu**
- Fotoğraflı işaretçilerle **mülk konum haritalama**
- **Yakın çevre olanakları gösterimi**:
  - 🚌 Metrobüs durakları
  - 🚏 Otobüs durakları
  - 🛒 Marketler
  - 👕 Giyim mağazaları
  - 🚕 Taksi durakları
  - 🚐 Minibüs hatları
  - 🚴 Bisiklet yolları
- En yakın hizmetlere **mesafe hesaplamaları**
- Gösterge için **harita kılavuzu geçişi**
- Her ilan için **önceden oluşturulmuş harita HTML'i**

### 🔍 Gelişmiş Mülk Arama

👉 **[Tüm Mülklere Göz Atın](https://kuzey-emlak.lotfinity.tech/tr/properties/)**

- Açıklamalarda anahtar kelime arama
- Şehir/İl filtreleme
- Yatak odası sayısı filtresi
- Fiyat aralığı filtresi
- Mülk tipi filtreleme
- İşlem türü (kiralık/satılık) filtresi

### 📸 Görüntü Yönetimi
- Sıralama ile **ilan başına birden fazla görsel**
- **Ana görsel belirleme**
- **Görünürlük kontrolü**
- **Yerleşik görüntü düzenleyiciler**:
  - Toast UI Görüntü Düzenleyici
  - Filerobot Görüntü Düzenleyici
- **Toplu işlemler**:
  - Filigran uygulama
  - Logo yerleştirme (tek tıkla veya özel)
  - Eski logolar için köşe kapatma
  - Görünürlük değiştirme
- Duyarlı görseller için **Easy Thumbnails** entegrasyonu

### 📥 Otomatik İçe Aktarma Sistemi
- Playwright ile **web kazıma entegrasyonu**
- **CSV veya tekli URL içe aktarma**
- Kimlik doğrulamalı kazıma için **çerez dosyası desteği**
- **Yapılandırılabilir seçenekler**:
  - İstekler arası gecikme
  - Hata ayıklama modu
  - Görünür/görünmez tarayıcı
  - Coğrafi kodlamayı atla
  - Görsel limiti kontrolü
- **Gerçek zamanlı ilerleme günlüğü**
- **Asenkron iş yürütme**

### 📊 GraphQL API
```graphql
query {
  posts { title, body, author { username } }
  categories { categoryname }
  post(id: 1) { title, slug, comments { message } }
}
```
- Yazılar ve kategoriler için tam CRUD mutasyonları
- GraphiQL arayüzü üzerinden inceleme etkin

---

## 🛠️ Teknoloji Altyapısı

| Kategori | Teknolojiler |
|----------|--------------|
| **Backend** | Django 4.2, Python 3 |
| **Veritabanı** | SQLite3 (geliştirme), dj-database-url ile PostgreSQL-hazır |
| **Frontend** | HTML5, CSS3, JavaScript, Tailwind CSS |
| **Haritalar** | Leaflet.js |
| **Görüntü İşleme** | Pillow, easy-thumbnails |
| **İçe/Dışa Aktarma** | django-import-export, tablib |
| **API'ler** | Graphene-Django (GraphQL), REST |
| **Web Kazıma** | Playwright, BeautifulSoup4, Requests |
| **Coğrafi Kodlama** | Geopy (Nominatim) |
| **Statik Oluşturma** | django-distill |
| **Yönetici Teması** | django-baton |
| **Çeviri** | django-rosetta |
| **Statik Dosyalar** | Whitenoise |
| **Hata Ayıklama** | Django Debug Toolbar |

---

## 👤 Kullanıcı Özellikleri

### Herkese Açık Kullanıcılar (Giriş Gerekmez)
| İşlem | Açıklama | Deneyin |
|-------|----------|---------|
| 🏠 İlanlara göz atma | Sayfalama ile tüm yayınlanmış mülkleri görüntüleme | [Mülkler →](https://kuzey-emlak.lotfinity.tech/tr/properties/) |
| 🔍 Mülk arama | Anahtar kelime, konum, fiyat, yatak odasına göre filtreleme | [Mülkler →](https://kuzey-emlak.lotfinity.tech/tr/properties/) |
| 📍 Haritada görüntüleme | Tüm ilan konumlarıyla interaktif harita | [Harita →](https://kuzey-emlak.lotfinity.tech/tr/map/) |
| 📄 Mülk detayları | Fotoğraf galerisi ile tam mülk bilgisi | [Örnek →](https://kuzey-emlak.lotfinity.tech/tr/listing/1/) |
| 🗺️ Yakın çevre olanakları | Mülk yakınındaki ulaşım, mağazalar, hizmetleri görme | [Harita →](https://kuzey-emlak.lotfinity.tech/tr/map/) |
| 📰 Blog okuma | Kategoriye göre makalelere göz atma | Yakında |
| 🌐 Dil değiştirme | 13 desteklenen dil arasında geçiş yapma | [🇬🇧 İngilizce](https://kuzey-emlak.lotfinity.tech/en/) \| [🇩🇪 Almanca](https://kuzey-emlak.lotfinity.tech/de/) |
| 💰 Finansman bilgisi | Finansman/kredi bilgi sayfasını görüntüleme | [Finansman →](https://kuzey-emlak.lotfinity.tech/tr/financing/) |

### Kayıtlı Kullanıcılar
| İşlem | Açıklama |
|-------|----------|
| 📝 Hesap oluşturma | Kullanıcı profili oluşturma |
| 🔐 Giriş/Çıkış | Güvenli kimlik doğrulama |
| 📧 Talep gönderme | İlanlar hakkında emlakçılarla iletişim |
| 📊 Kontrol paneli | Talep durumunu takip etme |
| 💬 Blog yorumu | Blog yazılarıyla etkileşim |

---

## 👨‍💼 Yönetici Özellikleri

### İlan Yönetimi
| İşlem | Açıklama |
|-------|----------|
| ➕ İlan oluşturma | Tam mülk veri girişi |
| ✏️ İlan düzenleme | Herhangi bir mülk alanını değiştirme |
| 🗑️ İlan silme | Mülkleri kaldırma |
| 📸 Görsel yönetimi | Fotoğraf ekleme, sıralama, gizleme, düzenleme |
| ✅ Yayınla/Yayından Kaldır | İlan görünürlüğünü kontrol etme |
| 📤 İçe/Dışa Aktarma | CSV, XLSX, JSON ile toplu veri işlemleri |
| 🤖 Otomatik içe aktarma | Harici sitelerden web kazıma ile içe aktarma |

### Görüntü İşleme (Yönetici İşlemleri)
| İşlem | Açıklama |
|-------|----------|
| 🖼️ Toplu görsel düzenleme | Birden fazla görsele filigran, kırpma, çerçeve uygulama |
| 🏷️ Logo uygulama | Şirket logosu filigranı ekleme |
| 🔺 Eski logo kapatma | Önceki markayı gizlemek için üçgen yerleştirme |
| ✂️ Orana göre kırpma | Tutarlı en-boy oranları uygulama |
| 🎨 Tarayıcı içi düzenleme | Toast UI ve Filerobot düzenleyiciler |

### Emlakçı Yönetimi
| İşlem | Açıklama |
|-------|----------|
| 👤 Emlakçı ekleme | Danışman profilleri oluşturma |
| ⭐ MVP durumu belirleme | En iyi danışmanları öne çıkarma |
| 📞 İletişim bilgileri | Telefon/e-posta yönetimi |

### İçerik Yönetimi
| İşlem | Açıklama |
|-------|----------|
| 📝 Blog yazıları | Makale oluşturma, düzenleme, kategorilendirme |
| 🏷️ Kategoriler | Blog kategorilerini yönetme |
| 🎨 Tema ayarları | Site renklerini ve yazı tiplerini özelleştirme |
| 🌐 Çeviriler | Rosetta ile çevirileri yönetme |

### Kullanıcı ve Talep Yönetimi
| İşlem | Açıklama |
|-------|----------|
| 👥 Kullanıcı yönetimi | Kullanıcıları görüntüleme, düzenleme, silme |
| 📩 Talepleri görüntüleme | Tüm mülk taleplerini izleme |
| 📈 Panel analitiği | Site aktivitesine genel bakış |

---

## 🔗 API ve Entegrasyon

### REST API Uç Noktaları

| Uç Nokta | Canlı Bağlantı |
|----------|----------------|
| `GET /api/listings` | [https://kuzey-emlak.lotfinity.tech/api/listings](https://kuzey-emlak.lotfinity.tech/api/listings) |
| `GET /api/listings?limit=10` | [https://kuzey-emlak.lotfinity.tech/api/listings?limit=10](https://kuzey-emlak.lotfinity.tech/api/listings?limit=10) |
| `GET /api/openapi.json` | [https://kuzey-emlak.lotfinity.tech/api/openapi.json](https://kuzey-emlak.lotfinity.tech/api/openapi.json) |

```
GET /api/listings
    ?limit=1000         # Maksimum sonuç (varsayılan 1000, maks 5000)
    ?bbox=minLon,minLat,maxLon,maxLat   # Mekansal filtre

GET /api/listings/<id>  # Tekil ilan coğrafi verisi

GET /api/openapi.json   # OpenAPI spesifikasyonu
```

### Yanıt Formatı (GeoJSON)
```json
{
  "count": 150,
  "results": [
    {
      "id": 1,
      "title": "İstanbul'da Modern Daire",
      "lat": 41.0082,
      "lng": 28.9784,
      "url": "/tr/listing/1/",
      "city": "İstanbul",
      "deal_type": "kiralik",
      "price": 15000,
      "original_url": "https://kaynak-site.com/ilan"
    }
  ]
}
```

### GraphQL Uç Noktası
```
POST /graphql/
```
- Keşif için tam GraphiQL arayüzü
- Yazıları, kategorileri ve ilgili verileri sorgulama

---

## 📦 Statik Site Oluşturma

Platform, CDN/statik hosting'e dağıtım için django-distill kullanarak **tam statik site dışa aktarımını** destekler.

### Derleme Komutu
```bash
bash scripts/build_static.sh [--zip]
```

### Oluşturulanlar
| Çıktı | Konum |
|-------|-------|
| Tüm sayfalar | `distill_output/<dil>/...` |
| Statik varlıklar | `distill_output/static/` |
| Medya dosyaları | `distill_output/media/` |
| Harita verisi JSON | `distill_output/listings/map-data/` |

### Dil Başına Oluşturulan Sayfalar
- Ana sayfa
- Mülkler listesi (sayfalama ile)
- Bireysel mülk detayları
- Harita görünümü
- İletişim sayfası
- Finansman sayfası
- 404 sayfası

### Dağıtım Hedefleri
- Netlify
- GitHub Pages
- AWS S3
- Herhangi bir statik dosya barındırıcısı

---

## 🌐 Çoklu Dil Desteği

### Desteklenen Diller (13)

| Kod | Dil | Canlı Bağlantı |
|-----|-----|----------------|
| 🇬🇧 `en` | English | [→ Ziyaret Et](https://kuzey-emlak.lotfinity.tech/en/) |
| 🇹🇷 `tr` | Türkçe | [→ Ziyaret Et](https://kuzey-emlak.lotfinity.tech/tr/) |
| 🇫🇷 `fr` | Français | [→ Ziyaret Et](https://kuzey-emlak.lotfinity.tech/fr/) |
| 🇪🇸 `es` | Español | [→ Ziyaret Et](https://kuzey-emlak.lotfinity.tech/es/) |
| 🇮🇹 `it` | Italiano | [→ Ziyaret Et](https://kuzey-emlak.lotfinity.tech/it/) |
| 🇵🇱 `pl` | Polski | [→ Ziyaret Et](https://kuzey-emlak.lotfinity.tech/pl/) |
| 🇵🇹 `pt` | Português | [→ Ziyaret Et](https://kuzey-emlak.lotfinity.tech/pt/) |
| 🇭🇺 `hu` | Magyar | [→ Ziyaret Et](https://kuzey-emlak.lotfinity.tech/hu/) |
| 🇷🇺 `ru` | Русский | [→ Ziyaret Et](https://kuzey-emlak.lotfinity.tech/ru/) |
| 🇸🇦 `ar` | العربية | [→ Ziyaret Et](https://kuzey-emlak.lotfinity.tech/ar/) |
| 🇩🇪 `de` | Deutsch | [→ Ziyaret Et](https://kuzey-emlak.lotfinity.tech/de/) |
| 🇧🇬 `bg` | български | [→ Ziyaret Et](https://kuzey-emlak.lotfinity.tech/bg/) |
| 🇳🇱 `nl` | Nederlands | [→ Ziyaret Et](https://kuzey-emlak.lotfinity.tech/nl/) |

### Özellikler
- **Dil başına URL öneki** (`/en/`, `/tr/`, `/fr/`, vb.)
- Tarayıcı içi çeviri yönetimi için **Django Rosetta**
- **Otomatik derleme** `.po`'dan `.mo` dosyalarına
- Ön yüzde **dil değiştirici**

---

## 🏗️ Proje Yapısı

```
coralcity/
├── accounts/          # Kullanıcı kimlik doğrulama ve panel
├── Ages/              # Yaş doğrulama
├── api/               # REST API uç noktaları
├── baton/             # Yönetici teması ve geliştirmeler
├── blog/              # Blog sistemi + GraphQL
├── contacts/          # Talep yönetimi
├── coralcity/         # Proje ayarları ve URL'ler
├── distill_output/    # Statik site çıktısı
├── imagetools/        # Görüntü işleme yardımcıları
├── listings/          # Temel mülk yönetimi
├── locale/            # Çeviri dosyaları
├── maps/              # Harita ile ilgili varlıklar
├── media/             # Yüklenen dosyalar
├── pages/             # Statik sayfalar ve tema
├── realtors/          # Danışman yönetimi
├── scripts/           # Derleme ve yardımcı scriptler
├── staticfiles/       # Toplanan statik dosyalar
└── templates/         # HTML şablonları
    ├── admin/         # Özel yönetici şablonları
    ├── newfrontend/   # Modern ön yüz şablonları
    └── partials/      # Yeniden kullanılabilir şablon parçaları
```

---

## 🚀 Hızlı Başlangıç

```bash
# Sanal ortam oluştur
python -m venv venv
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Veritabanı migrasyonlarını çalıştır
python manage.py migrate

# Süper kullanıcı oluştur
python manage.py createsuperuser

# Geliştirme sunucusunu çalıştır
python manage.py runserver

# Statik site derle
bash scripts/build_static.sh
```

---

## 📝 Özet

**Kuzey-emlak** aşağıdakileri bir araya getiren kapsamlı bir gayrimenkul platformudur:

- ✅ **Mülk Yönetimi** - Gelişmiş filtreleme ile tam CRUD
- ✅ **İnteraktif Haritalar** - Olanak mesafe hesaplamaları ile Leaflet
- ✅ **Görüntü İşleme** - Filigran, kırpma, düzenleme
- ✅ **Çoklu Dil** - Kolay çeviri yönetimi ile 13 dil
- ✅ **Blog Sistemi** - Kategoriler, yorumlar, GraphQL API
- ✅ **Kullanıcı Sistemi** - Kayıt, panel, talep takibi
- ✅ **İçe Aktarma Otomasyonu** - Playwright ile web kazıma
- ✅ **Statik Oluşturma** - Herhangi bir CDN'e dağıtım
- ✅ **Modern Yönetici** - Toplu işlemlerle Baton teması
- ✅ **REST ve GraphQL API'ler** - Esnek veri erişimi

Bu, modern ve tam özellikli bir web varlığı arayan gayrimenkul ajansları için üretime hazır, ölçeklenebilir bir çözümdür.

---

*2 Aralık 2025 tarihinde oluşturuldu*
