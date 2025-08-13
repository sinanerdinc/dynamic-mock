# Dinamik Mock

Bu proje web otomasyon testlerinde anlık olarak bazı apilerin responselarını mock başka bir response ile değiştirmeye imkan sağlayan çalışan bir örneği içerir. Bu yöntem de farklı testleri yapabilmeyi mümkün kılar. Bunun için tüm sistemin docker üzerinde çalışan bir versiyonu hazırlanmalıdır.

Bu projede test-runner klasörü, sizin testlerinizi içeren klasörü işaret eder. Bilgisayarınızda docker compose olduğunu varsayarak, çalıştırmak isterseniz aşağıdaki adımları kullananbilirsiniz.

## Çalıştırma
Mocklamak istenilen adresler config.yml içerisine eklenir. Sonrasında

```
chmod +x settings.sh
./settings.sh
```

komutu ile gerekli buildler çekilerek sistem ayağa kaldırılır. Sonrasında http://localhost:9000/docs adresinde dinamik olarak mocklamak istenilen adresin hangi path değeri ve http isteği mock klasöründeki hangi response olarak değiştirilmesi gerektiği ayarlanır. 

Bunun için POST /set_mock endpointi kullanılır, örnek bir payload:

```
{
  "host": "free.freeipapi.com",
  "path": "/api/json",
  "method": "GET",
  "active": false,
  "response_body_path": "freeipapi_mock.json",
  "status_code": 200
}
```

burada artık testlerde free.freeipapi.com/api/json adresine gidildiğinde, gateway-proxy/mock klasöründeki freeipapi_mock.json dosyasının döndürülmesi gerektiği ayarlanmıştır. Artık örnek olarak test-runner containerı içindeki run_web_test.py dosyası ile test çalıştırılabilir.

```
docker compose exec test-runner python run_web_test.py
```

Yazılan örnek test çalıştırıldığında eğer mock servis aktif ise 

```
{"result":"mocked response"}
```

şeklinde bir response dönecektir. Eğer mock servis kapalı ise o zaman gerçekten bu adresin döndüğü response dönecektir.


