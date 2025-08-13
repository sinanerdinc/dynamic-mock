import httpx
import json
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

app = FastAPI(
    title="Dosya Tabanlı Mock Proxy",
    version="5.0",
    description="Tüm mock yanıtlarını dosyalardan okuyan, sadeleştirilmiş proxy."
)

class MockConfig(BaseModel):
    host: str
    path: str
    method: Optional[str] = Field(
        default=None,
        description="Hedeflenen HTTP metodu (GET, POST vb.). Belirtilmezse tüm metodlar için geçerli olur."
    )
    active: bool
    response_body_path: Optional[str] = Field(
        default=None,
        description="Kullanılacak mock JSON dosyasının /app/mocks/ içindeki yolu."
    )
    status_code: Optional[int] = Field(
        default=200,
        description="Mock aktifken dönecek HTTP durum kodu."
    )


MOCK_CONFIGS: Dict[str, Dict] = {}

@app.post("/set_mock", tags=["Kontrol"])
def set_mock(config: MockConfig):
    key_method_prefix = f"{config.method.upper()} " if config.method else ""
    key = f"{key_method_prefix}{config.host}{config.path}"

    MOCK_CONFIGS[key] = {
        "active": config.active,
        "response_body_path": config.response_body_path,
        "status_code": config.status_code
    }
    print(f"[Gateway] Ayarlar güncellendi: '{key}' -> {MOCK_CONFIGS[key]}")
    return {"message": f"'{key}' için ayarlar başarıyla güncellendi."}


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], tags=["Proxy"])
async def proxy(request: Request, path: str):
    target_host = request.headers.get('host')
    if not target_host:
        return JSONResponse(status_code=400, content={"error": "Host başlığı bulunamadı."})

    full_path = f"/{path}"

    method_specific_key = f"{request.method.upper()} {target_host}{full_path}"
    generic_key = f"{target_host}{full_path}"
    key_to_use = method_specific_key if method_specific_key in MOCK_CONFIGS else generic_key

    host_mock_config = MOCK_CONFIGS.get(key_to_use)

    if host_mock_config and host_mock_config.get("active"):
        print(f"[Gateway] MOCK MODU AKTİF: '{key_to_use}' kuralı kullanılarak yanıt işleniyor.")

        status_code = host_mock_config.get("status_code", 200)
        file_path_suffix = host_mock_config.get("response_body_path")

        if file_path_suffix:
            file_path = f"/app/mocks/{file_path_suffix}"
            print(f"[Gateway] Dosya okunuyor: {file_path}")
            try:
                with open(file_path, "r") as f:
                    content = json.load(f)
                return JSONResponse(status_code=status_code, content=content)
            except FileNotFoundError:
                print(f"[Gateway] HATA: Mock dosyası bulunamadı: {file_path}")
                return JSONResponse(status_code=500, content={"error": "Mock dosyası sunucuda bulunamadı."})

        else:
            print("[Gateway] Dosya yolu belirtilmedi, boş yanıt dönülüyor.")
            return Response(status_code=status_code)

    print(f"[Gateway] PROXY MODU: İstek https://{target_host}/{path} adresine yönlendiriliyor.")
    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=f"https://{target_host}/{path}",
            params=request.query_params,
            headers=request.headers,
            content=await request.body(),
            cookies=request.cookies
        )
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = {name: value for (name, value) in resp.headers.items() if name.lower() not in excluded_headers}
    return Response(content=resp.content, status_code=resp.status_code, headers=headers)