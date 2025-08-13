# Dinamik Mock

Bu proje web otomasyon testlerinde anlık olarak bazı apilerin responselarını mock başka bir response ile değiştirmeye imkan sağlayan çalışan bir örneği içerir. Bu yöntem de farklı testleri yapabilmeyi mümkün kılar. Bunun için tüm sistemin docker üzerinde çalışan bir versiyonu hazırlanmalıdır.

Bu projede test-runner klasörü, sizin testlerinizi içeren klasörü işaret eder. Bilgisayarınızda docker compose olduğunu varsayarak, çalıştırmak isterseniz aşağıdaki adımları kullananbilirsiniz.

## Çalıştırma
Mocklamak istenilen adresler config.yml içerisine eklenir. Sonrasında

```
chmod +x settings.sh
```
ile çalıştırma izni verildikten sonra

```
./settings.sh
```

komutu ile gerekli ayarların otomatik yapılması sağlanır, bu aşamada buildler çekilecek gerekli network ayarları yapılarak sistem ayağa kaldırılacaktır. 

Sonrasında http://localhost:9000/docs adresinde ayarları yapabileceğiniz bir api sizi karşılayacak, dinamik olarak mocklamak istenilen adresin hangi path değeri ve http isteği mock klasöründeki hangi response olarak değiştirilmesi gerektiğini buradan ayarlayabilirsiniz.

Bunun için POST /set_mock endpointi kullanılmalıdır, örnek bir payload:

```
{
  "host": "free.freeipapi.com",
  "path": "/api/json",
  "method": "GET",
  "active": true,
  "response_body_path": "freeipapi_mock.json",
  "status_code": 200
}
```

burada artık testlerde free.freeipapi.com/api/json adresine gidildiğinde, gateway-proxy/mock klasöründeki freeipapi_mock.json dosyasının döndürülmesi gerektiği ayarlanmıştır. Bu ayarı iptal ederek tekrar orjinal response döndürülmesini isterseniz de 

**"active": false**

olarak yeni bir istek atabilirsiniz.

Artık chrome containerı içerisinden geçen tüm network trafiğinde bu adres mocklanmıştır. run_web_test.py dosyası ile örnek verilen testi çalıştırabilirsiniz.

```
docker compose exec test-runner python run_web_test.py
```

Yazılan örnek test çalıştırıldığında eğer mock servis aktif ise 

```
{"result":"mocked response"}
```

şeklinde bir response dönecektir. Eğer mock servis kapalı ise o zaman gerçekten bu adresin döndüğü response ekrana gelecektir.


