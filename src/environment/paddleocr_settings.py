from pydantic_settings import BaseSettings


class PaddleOcrSettings(BaseSettings):
    """Variáveis de ambiente relacionadas ao PaddleOCR."""
    PADDLE_PDX_INITIALIZED: str = "0"
    FLAGS_use_mkldnn: str = "0"
    FLAGS_call_stack_level: str = "0"
    PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK: bool = True
    FLAGS_enable_pir_api: str = "0"

    class Config:
        env_file = ".env"
        extra = "ignore"
        hide_input_in_errors = True
