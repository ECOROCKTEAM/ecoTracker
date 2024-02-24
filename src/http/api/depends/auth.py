from fastapi.security import APIKeyHeader

token_header = APIKeyHeader(name="Authorization", scheme_name="Authorization", auto_error=True)
