# Dinamik Mock

Docker ile araya bir gateway ekleyerek, docker chrome üzerinde çalıştırdığımız bir test için istediğimiz bir adresi, kendi yaptığımız bir mock servis ile değiştirmenize imkan sağlar. 

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





