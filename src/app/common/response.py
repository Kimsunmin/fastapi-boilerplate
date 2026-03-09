def success_response(data: dict = None, message: str = "Success", status_code: int = 200) -> dict:
    return {
        "status": "success",
        "message": message,
        "data": data,
        "status_code": status_code,
    }
    
def error_response(data: dict = None, message: str = "Error", status_code: int = 400) -> dict:
    return {
        "status": "error",
        "message": message,
        "data": data,
        "status_code": status_code,
    }