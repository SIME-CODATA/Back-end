import ssl

import httpx

from Back_end.access_api.smae.config import SmaeConfig, get_smae_config


def create_smae_ssl_context() -> ssl.SSLContext:
    """
    Cria o contexto SSL necessário para compatibilidade com a API do SMAE.

    O servidor do SMAE exige TLS 1.2 e atualmente necessita de
    SECLEVEL=1 para comunicação com versões modernas do OpenSSL.
    """

    ssl_context = ssl.create_default_context()

    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
    ssl_context.maximum_version = ssl.TLSVersion.TLSv1_2

    ssl_context.set_ciphers("DEFAULT:@SECLEVEL=1")

    return ssl_context


class SmaeClient:
    """Cliente HTTP responsável pela comunicação com a API do SMAE."""

    def __init__(self, config: SmaeConfig | None = None):
        self.config = config or get_smae_config()
        self._access_token: str | None = None

        ssl_context = create_smae_ssl_context()

        self._client = httpx.Client(
            base_url=self.config.base_url,
            timeout=30.0,
            verify=ssl_context,
            headers={
                "Accept": "application/json",
                "smae-sistemas": self.config.systems,
            },
        )

    def login(self) -> None:
        """Autentica no SMAE e mantém o token apenas em memória."""

        response = self._client.post(
            "/login",
            json={
                "email": self.config.email,
                "senha": self.config.password,
            },
        )

        response.raise_for_status()

        data = response.json()

        access_token = data.get("access_token")

        if not access_token:
            raise RuntimeError(
                "O SMAE não retornou access_token após o login."
            )

        self._access_token = access_token

    def get(self, endpoint: str, params: dict | None = None) -> dict:
        """Executa uma requisição GET autenticada no SMAE."""

        if self._access_token is None:
            self.login()

        response = self._client.get(
            endpoint,
            params=params,
            headers={
                "Authorization": f"Bearer {self._access_token}",
            },
        )

        if response.status_code == 401:
            self.login()

            response = self._client.get(
                endpoint,
                params=params,
                headers={
                    "Authorization": f"Bearer {self._access_token}",
                },
            )

        response.raise_for_status()

        return response.json()

    def close(self) -> None:
        """Fecha o cliente HTTP."""

        self._client.close()