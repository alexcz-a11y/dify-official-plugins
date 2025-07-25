import logging
import requests
from typing import List
from dify_plugin.entities.model import ModelType
from dify_plugin.errors.model import CredentialsValidateFailedError
from dify_plugin import ModelProvider
from dify_plugin.entities.model.ai_model_entity import AIModelEntity, ModelPropertyKey, FetchFrom

logger = logging.getLogger(__name__)


class OpenRouterProvider(ModelProvider):
    def validate_provider_credentials(self, credentials: dict) -> None:
        try:
            model_instance = self.get_model_instance(ModelType.LLM)
            model_instance.validate_credentials(model="openai/gpt-4o-mini", credentials=credentials)
        except CredentialsValidateFailedError as ex:
            raise ex
        except Exception as ex:
            logger.exception(f"{self.get_provider_schema().provider} credentials validate failed")
            raise ex
    
    def get_models(self, model_type: ModelType, credentials: dict) -> List[AIModelEntity]:
        """
        Get available models from OpenRouter API
        
        :param model_type: model type
        :param credentials: provider credentials
        :return: list of models
        """
        if model_type != ModelType.LLM:
            return []
            
        api_key = credentials.get('api_key')
        if not api_key:
            raise CredentialsValidateFailedError('API key is required')
            
        try:
            # Call OpenRouter API to get models
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://dify.ai',
                'X-Title': 'Dify'
            }
            
            response = requests.get(
                'https://openrouter.ai/api/v1/models',
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch models from OpenRouter: {response.status_code} {response.text}")
                return []
                
            models_data = response.json()
            models = []
            
            for model_info in models_data.get('data', []):
                model_id = model_info.get('id')
                if not model_id:
                    continue
                    
                # Parse model features
                features = []
                if model_info.get('architecture', {}).get('modality') == 'text+image->text':
                    features.append('vision')
                    
                # Check if model supports function calling
                if model_info.get('top_provider', {}).get('supports_function_calling'):
                    features.extend(['tool-call', 'multi-tool-call'])
                    
                # Get context size
                context_size = model_info.get('context_length', 4096)
                
                # Get pricing info
                pricing = model_info.get('pricing', {})
                input_price = pricing.get('prompt', '0')
                output_price = pricing.get('completion', '0')
                
                # Create model entity
                model_entity = AIModelEntity(
                    model=model_id,
                    label={
                        'en_US': model_info.get('name', model_id),
                        'zh_Hans': model_info.get('name', model_id)
                    },
                    model_type=ModelType.LLM,
                    features=features,
                    fetch_from=FetchFrom.FETCH_FROM_REMOTE,
                    model_properties={
                        ModelPropertyKey.CONTEXT_SIZE: context_size,
                        ModelPropertyKey.MODE: 'chat'
                    },
                    pricing={
                        'input': str(float(input_price) * 1000000),  # Convert to per million tokens
                        'output': str(float(output_price) * 1000000),
                        'unit': '0.000001',
                        'currency': 'USD'
                    }
                )
                
                models.append(model_entity)
                
            logger.info(f"Successfully fetched {len(models)} models from OpenRouter")
            return models
            
        except requests.RequestException as e:
            logger.error(f"Request failed when fetching models from OpenRouter: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error when fetching models from OpenRouter: {e}")
            return []
