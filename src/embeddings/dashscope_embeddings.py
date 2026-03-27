"""阿里云 DashScope Embeddings 适配器"""
from typing import List, Optional
import httpx


class DashScopeEmbeddings:
    """阿里云 DashScope Embeddings 适配器"""
    
    def __init__(
        self,
        model: str = "text-embedding-v2",
        api_key: Optional[str] = None,
        api_base: str = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/generation"
    ):
        self.model = model
        self.api_key = api_key
        self.api_base = api_base
        
        if not self.api_key:
            raise ValueError("API key is required")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """批量获取 embeddings"""
        import dashscope
        from dashscope import TextEmbedding
        
        dashscope.api_key = self.api_key
        
        # 阿里云要求单个或列表，但不能是空的批次
        results = []
        for text in texts:
            response = TextEmbedding.call(
                model=self.model,
                input=text
            )
            
            if response.status_code == 200:
                embedding = response.output['embeddings'][0]['embedding']
                results.append(embedding)
            else:
                raise Exception(f"Error getting embedding: {response}")
        
        return results
    
    def embed_query(self, text: str) -> List[float]:
        """获取单个查询的 embedding"""
        return self.embed_documents([text])[0]


# 使用 httpx 的简单实现（备选方案）
class SimpleDashScopeEmbeddings:
    """简单的 DashScope Embeddings 实现（使用 httpx）"""
    
    def __init__(
        self,
        model: str = "text-embedding-v2",
        api_key: Optional[str] = None,
        api_base: str = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/generation"
    ):
        self.model = model
        self.api_key = api_key
        self.api_base = api_base
        
        if not self.api_key:
            raise ValueError("API key is required")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """批量获取 embeddings"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        results = []
        for text in texts:
            payload = {
                "model": self.model,
                "input": {
                    "texts": [text]
                },
                "parameters": {}
            }
            
            response = httpx.post(self.api_base, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if data.get("output") and data["output"].get("embeddings"):
                embedding = data["output"]["embeddings"][0]["embedding"]
                results.append(embedding)
            else:
                raise Exception(f"Invalid response: {data}")
        
        return results
    
    def embed_query(self, text: str) -> List[float]:
        """获取单个查询的 embedding"""
        return self.embed_documents([text])[0]
