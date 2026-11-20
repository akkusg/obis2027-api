# obis2027-api

Öğrenci Bilgi Sistemi için basit bir Flask API örneği. Kullanıcı bilgileri
ortam değişkenlerinden alınır; ders listesi örnek veridir ve gerçek bir öğrenci
bilgi sistemine bağlı değildir.

## Kurulum ve çalıştırma

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export API_USERNAME="ogrenci"
export API_PASSWORD="kendi-parolaniz"
flask --app app run
```

`SECRET_KEY`, `API_USERNAME` ve `API_PASSWORD` zorunludur. Sunucuyu yeniden
başlatırken oturumların geçerli kalması için aynı gizli anahtarı kullanın.
HTTPS ile dağıtımda `SESSION_COOKIE_SECURE=true` ayarlayın. Flask'ın geliştirme
sunucusu üretim için uygun değildir.

## Uç noktalar

Giriş yapın ve oturum çerezini kaydedin:

```sh
curl -c cookies.txt -H 'Content-Type: application/json' \
  -d '{"username":"ogrenci","password":"kendi-parolaniz"}' \
  http://127.0.0.1:5000/api/login
```

Girişten sonra örnek dersleri listeleyin:

```sh
curl -b cookies.txt http://127.0.0.1:5000/api/list-courses
```

Giriş hatalı bilgiler için `401`, geçersiz istek için `400` ve eksik sunucu
yapılandırması için `503` döndürür. Ders listesi için giriş zorunludur; oturum
olmadığında `401` döner.

Testleri çalıştırmak için `python -m unittest` kullanın.