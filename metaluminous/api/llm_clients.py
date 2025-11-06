"""
Metaluminous Engine - LLM Client Abstractions
"""
import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from loguru import logger

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import settings


class LLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate text from prompt"""
        pass


class OllamaClient(LLMClient):
    """Client for Ollama local inference"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or settings.ollama_host
        self.client = httpx.AsyncClient(timeout=300.0)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def generate(
        self,
        prompt: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate text using Ollama"""
        logger.debug(f"Generating with Ollama model: {model}")
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
            }
        }
        
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except httpx.HTTPError as e:
            logger.error(f"Ollama API error: {e}")
            raise
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


class OpenAIClient(LLMClient):
    """Client for OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.openai_api_key
        if not self.api_key:
            logger.warning("OpenAI API key not configured")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def generate(
        self,
        prompt: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate text using OpenAI API"""
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")
        
        logger.debug(f"Generating with OpenAI model: {model}")
        
        # Use openai library
        try:
            from openai import AsyncOpenAI
            
            client = AsyncOpenAI(api_key=self.api_key)
            
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            return response.choices[0].message.content
        except ImportError:
            logger.error("OpenAI library not installed")
            raise
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise


class AnthropicClient(LLMClient):
    """Client for Anthropic Claude API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.anthropic_api_key
        if not self.api_key:
            logger.warning("Anthropic API key not configured")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def generate(
        self,
        prompt: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate text using Anthropic API"""
        if not self.api_key:
            raise ValueError("Anthropic API key not configured")
        
        logger.debug(f"Generating with Anthropic model: {model}")
        
        try:
            from anthropic import AsyncAnthropic
            
            client = AsyncAnthropic(api_key=self.api_key)
            
            response = await client.messages.create(
                model=model,
                max_tokens=max_tokens or 4096,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
        except ImportError:
            logger.error("Anthropic library not installed")
            raise
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise


class GoogleClient(LLMClient):
    """Client for Google Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.google_api_key
        if not self.api_key:
            logger.warning("Google API key not configured")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def generate(
        self,
        prompt: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate text using Google Gemini API"""
        if not self.api_key:
            raise ValueError("Google API key not configured")
        
        logger.debug(f"Generating with Google model: {model}")
        
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model_obj = genai.GenerativeModel(model)
            
            generation_config = {
                "temperature": temperature,
            }
            if max_tokens:
                generation_config["max_output_tokens"] = max_tokens
            
            response = await asyncio.to_thread(
                model_obj.generate_content,
                prompt,
                generation_config=generation_config
            )
            
            return response.text
        except ImportError:
            logger.error("Google generativeai library not installed")
            raise
        except Exception as e:
            logger.error(f"Google API error: {e}")
            raise
