#!/bin/bash
set -e

echo ">>> Test ortamı hazırlanıyor..."
echo "Docker container'ları başlatılıyor..."
docker compose up --build -d

# Gateway-proxy'nin dinamik IP adresini öğren
GATEWAY_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker compose ps -q gateway-proxy))

if [ -z "$GATEWAY_IP" ]; then
    echo "HATA: Gateway IP adresi bulunamadı."
    docker compose down
    exit 1
fi
echo "Gateway IP adresi bulundu: $GATEWAY_IP"

# config.yml dosyasından host'ları oku
HOSTS_TO_REDIRECT=($(grep '^\s*-' config.yml | sed 's/^\s*-\s*//'))

if [ ${#HOSTS_TO_REDIRECT[@]} -eq 0 ]; then
    echo "UYARI: config.yml dosyasında yönlendirilecek host bulunamadı."
else
    echo "Konfigürasyon dosyasından şu hostlar bulundu: ${HOSTS_TO_REDIRECT[*]}"

    # /etc/hosts dosyasına eklenecek tam satırı oluştur
    HOSTS_ENTRY=$(printf "%s " "${HOSTS_TO_REDIRECT[@]}")

    # Eskiden kalma #proxied_host_entry etiketli satırı sil ve yenisini ekle
    # Bu, hosts dosyasının tekrar tekrar aynı girdilerle dolmasını engeller.
    docker compose exec -T -u root chrome sh -c "sed -i '/\s*#proxied_host_entry/d' /etc/hosts; echo '$GATEWAY_IP $HOSTS_ENTRY #proxied_host_entry' >> /etc/hosts"

    echo "Selenium Chrome container'ının hosts dosyası güncellendi."
fi

echo ""
echo ">>> Ortam hazır."