from typing import Any, Dict
from repositories.request_repository import RequestRepository


class ApiService:
    def __init__(self, repository: RequestRepository):
        self.repository = repository

    def create_thread(self, assistant_id: str, message_content: str) -> Dict[str, Any]:
        endpoint = "/v1/threads/runs"
        data = {
            "assistant_id": assistant_id,
            "thread": {
                "messages": [
                    {"role": "user", "content": message_content}
                ]
            }
        }
        response = self.repository.post(endpoint, data)
        return response
    
    def delete_thread(self,thread_id:str)->Dict[str,Any]:
        endpoint =f"/v1/threads/{thread_id}"
        response = self.repository.delete(endpoint)
    
        return response

    def get_thread_status(self, thread_id: str,run_id: str) -> Dict[str, Any]:
        endpoint = f"/v1/threads/{thread_id}/runs/{run_id}"
        response = self.repository.get(endpoint)
        return response
    
    def get_thread_run_list(self,thread_id:str,run_id:str)->Dict[str,Any]:
        endpoint = f"/v1/threads/{thread_id}/runs/{run_id}"
        response = self.repository.get(endpoint)
        return response
    
    def get_thread_messages(self, thread_id:str)->Dict[str,Any]:
        endpoint = f"/v1/threads/{thread_id}/messages"
        response = self.repository.get(endpoint)
        return response
    
    def get_thread_message_by_id(self, thread_id:str,message_id:str)->Dict[str,Any]:
        endpoint = f"/v1/threads/{thread_id}/messages/{message_id}"
        response = self.repository.get(endpoint)
        return response
    
    def send_message_to_thread(self, thread_id: str, message_content: str) -> Dict[str, Any]:
        endpoint = f"/v1/threads/{thread_id}/messages"
        data = {
            "messages": [
                {"role": "user", "content": message_content}
            ]
        }
        response = self.repository.post(endpoint, data)
        return response