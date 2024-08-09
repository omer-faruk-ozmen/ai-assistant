# Triage Assistant

**Hastane Triaj Asistanı**, acil servislerde çalışan doktorlar ve sağlık personeli için geliştirilmiş bir yapay zeka destekli uygulamadır. Bu uygulama, özellikle yeni atanan doktorların tanı koyma ve müdahale süreçlerinde karşılaştıkları zorlukları azaltmayı amaçlar. Yapay zeka, hastaların anamnez bilgilerini analiz ederek olası hastalıkları belirler ve doktorlara tanı ve tedavi süreçlerinde rehberlik eder. Bu sayede, hastalara daha hızlı, etkili ve güvenli sağlık hizmetleri sunulması sağlanır.

## Özellikler

- **Yapay Zeka Destekli Tanı:** Hastaların anamnez bilgilerini analiz ederek olası hastalıkları ve gerekli müdahaleleri önerir.
- **Rehberlik:** Kritik kararlar alırken doktorlara rehberlik eder, iş yükünü hafifletir.
- **Verimlilik:** Tanı ve tedavi süreçlerini hızlandırarak sağlık hizmetlerinin kalitesini artırır.

## Kurulum

Projenin çalıştırılması için gerekli adımlar aşağıda listelenmiştir. 

### 1. Depoyu Klonlayın

Öncelikle, projeyi yerel makinenize klonlayın:

```bash
git clone https://github.com/kullanici_adi/proje_adi.git
cd proje_adi
```
### 2. Sanal Ortamı Oluşturun ve Gerekli Paketleri Yükleyin

Proje için bağımlılıkları izole etmek adına bir Python sanal ortamı oluşturun ve gerekli paketleri yükleyin:

```bash
python -m venv myenv
source myenv/bin/activate  # Windows için: myenv\Scripts\activate
pip install -r requirements.txt
```

### 3. Ortam Değişkenlerini Ayarlayın

Uygulamanın düzgün çalışabilmesi için bazı ortam değişkenlerini ayarlamanız gerekiyor. Aşağıdaki değişkenleri .env dosyasına ekleyin veya terminalde tanımlayın:

```bash
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
OPENAI_API_KEY=your-api-key
OPENAI_ASSISTANT_ID=assistant-key
DATABASE_URI=postgresql+psycopg2://username:password@host/database-name
```

### 4. Veritabanını Başlatın

Uygulamanın kullanacağı veritabanını oluşturmak için aşağıdaki komutları çalıştırın. (Bu uygulamada veritabanı olarak PostgreSQL kullanılmıştır.):

```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

### 5. Uygulamayı Çalıştırın

Artık uygulamayı çalıştırabilirsiniz:

```bash
flask run
```
Uygulama, varsayılan olarak http://localhost:5000 veya :8080 adresinde çalışacaktır.
