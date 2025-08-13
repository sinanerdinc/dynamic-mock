import time
from selenium import webdriver
from selenium.webdriver.common.by import By

SELENIUM_URL = "http://chrome:4444/wd/hub"
TARGET_URL = "http://free.freeipapi.com/api/json"


# --- Ana Fonksiyon ---
def run_test():
    """Sadece tarayıcıyı açar, hedef URL'e gider ve sayfa içeriğini yazdırır."""

    print(">>> Selenium test betiği başlatıldı.")
    options = webdriver.ChromeOptions()
    driver = None  # Hata durumunda quit çağırabilmek için dışarıda tanımla

    try:
        print(f"Selenium Chrome'a bağlanılıyor: {SELENIUM_URL}")
        driver = webdriver.Remote(
            command_executor=SELENIUM_URL,
            options=options
        )
        print("Bağlantı başarılı.")

        print(f"Sayfa açılıyor: {TARGET_URL}")
        driver.get(TARGET_URL)

        # Sayfanın yüklenmesi için kısa bir bekleme
        time.sleep(2)

        # Sayfanın içeriğini al ve yazdır
        body_text = driver.find_element(By.TAG_NAME, "body").text
        print("\n--- SAYFA İÇERİĞİ ---\n")
        print(body_text)
        print("\n----------------------\n")

        print(">>> Test başarıyla tamamlandı.")

    except Exception as e:
        print(f"\n!!! BİR HATA OLUŞTU !!!\n{e}\n")
    finally:
        if driver:
            print("Tarayıcı kapatılıyor.")
            driver.quit()


if __name__ == "__main__":
    run_test()