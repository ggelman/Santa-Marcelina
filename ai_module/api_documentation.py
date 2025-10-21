#!/usr/bin/env python3
"""
Documentação API Simples com Flasgger
=====================================

Documentação interativa das APIs usando Flasgger (Swagger UI)
sem dependências complexas.
"""

from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from flask_cors import CORS
import json
import os

# Configuração do Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Sistema AI da Padaria - API Documentation",
        "description": """
# 🍞 Sistema AI da Padaria

## Visão Geral
Sistema de Inteligência Artificial completo para predição de demanda, 
geração de insights e análise de dados de vendas de uma padaria.

## Funcionalidades Principais
- 📊 **Predição de Demanda**: Algoritmos ML para previsão de vendas
- 🧠 **Geração de Insights**: IA para análise estratégica  
- 🗄️ **Cache Inteligente**: Sistema Redis com fallback graceful
- 📈 **Monitoramento**: Logging estruturado e métricas em tempo real
- 🛡️ **Tratamento de Erros**: Framework robusto com retry logic
- ⚡ **Health Checks**: Verificação avançada de componentes

## Arquitetura
- **Framework**: Flask + Redis + MySQL
- **ML**: Prophet + Scikit-learn
- **IA**: Google Gemini + OpenAI
- **Monitoramento**: Structured Logging + psutil
- **Cache**: Redis com fallback para arquivos locais

## Códigos de Status
- `200` - Sucesso
- `400` - Requisição inválida
- `401` - Não autorizado
- `404` - Recurso não encontrado
- `429` - Rate limit excedido
- `500` - Erro interno do servidor
- `503` - Serviço indisponível
        """,
        "version": "1.0.0",
        "termsOfService": "",
        "contact": {
            "name": "Sistema AI Padaria",
            "email": "support@padaria-ai.com"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    },
    "host": "localhost:5001",
    "basePath": "/",
    "schemes": ["http", "https"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "securityDefinitions": {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-KEY"
        }
    },
    "tags": [
        {
            "name": "AI",
            "description": "APIs de Inteligência Artificial"
        },
        {
            "name": "Data", 
            "description": "APIs de Dados e Coleta"
        },
        {
            "name": "Monitoring",
            "description": "APIs de Monitoramento" 
        },
        {
            "name": "Health",
            "description": "APIs de Health Check"
        },
        {
            "name": "Cache",
            "description": "APIs de Cache"
        }
    ]
}

def create_swagger_specs():
    """Cria especificações Swagger para cada endpoint."""
    
    # Especificações para cada endpoint
    specs = {
        'predict': {
            "tags": ["AI"],
            "summary": "Prediz demanda de um produto",
            "description": """
Prediz a demanda de vendas para um produto específico usando modelos Prophet.

**Produtos disponíveis:**
- Bolo_de_Chocolate
- Brigadeiro_Gourmet  
- Cafe_Expresso
- Pao_Frances
- Croissant

**Exemplo de uso:**
```python
import requests

response = requests.post('/api/ai/predict', json={
    'product_name': 'Bolo_de_Chocolate',
    'days': 7,
    'confidence_interval': 0.95
})
```
            """,
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "required": ["product_name", "days"],
                        "properties": {
                            "product_name": {
                                "type": "string",
                                "description": "Nome do produto",
                                "example": "Bolo_de_Chocolate"
                            },
                            "days": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 30,
                                "description": "Número de dias para predição",
                                "example": 7
                            },
                            "confidence_interval": {
                                "type": "number",
                                "minimum": 0.8,
                                "maximum": 0.99,
                                "description": "Intervalo de confiança",
                                "example": 0.95
                            }
                        }
                    }
                }
            ],
            "responses": {
                "200": {
                    "description": "Predição realizada com sucesso",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "example": "success"},
                            "product_name": {"type": "string", "example": "Bolo_de_Chocolate"},
                            "prediction": {
                                "type": "array",
                                "items": {"type": "number"},
                                "example": [65.2, 68.1, 72.3, 70.5, 73.8, 75.2, 69.1]
                            },
                            "confidence_intervals": {"type": "object"},
                            "model_info": {"type": "object"},
                            "prediction_date": {"type": "string", "format": "date-time"},
                            "cache_hit": {"type": "boolean", "example": False}
                        }
                    }
                },
                "400": {
                    "description": "Parâmetros inválidos",
                    "schema": {"$ref": "#/definitions/Error"}
                },
                "404": {
                    "description": "Produto não encontrado",
                    "schema": {"$ref": "#/definitions/Error"}
                },
                "500": {
                    "description": "Erro interno",
                    "schema": {"$ref": "#/definitions/Error"}
                }
            }
        },
        
        'generate_insight': {
            "tags": ["AI"],
            "summary": "Gera insights usando IA",
            "description": """
Gera insights estratégicos usando IA baseado em prompts e dados de contexto.

**Modelos suportados:**
- Google Gemini (recomendado)
- OpenAI GPT

**Exemplos de prompts:**
- "Analise o padrão de vendas de bolos nos finais de semana"
- "Sugira estratégias para aumentar vendas de café"
- "Identifique produtos com maior potencial de crescimento"
            """,
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "required": True,
                    "schema": {
                        "type": "object",
                        "required": ["prompt"],
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "Prompt para geração de insight",
                                "example": "Analise as vendas de bolo de chocolate dos últimos 7 dias"
                            },
                            "context_data": {
                                "type": "object",
                                "description": "Dados de contexto para análise"
                            },
                            "max_tokens": {
                                "type": "integer",
                                "minimum": 100,
                                "maximum": 2000,
                                "description": "Máximo de tokens na resposta",
                                "example": 500
                            },
                            "model": {
                                "type": "string",
                                "enum": ["gemini", "openai"],
                                "description": "Modelo de IA a usar",
                                "example": "gemini"
                            }
                        }
                    }
                }
            ],
            "responses": {
                "200": {
                    "description": "Insight gerado com sucesso",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "example": "success"},
                            "insight": {"type": "string", "description": "Insight gerado pela IA"},
                            "model_used": {"type": "string", "example": "gemini"},
                            "token_count": {"type": "integer", "example": 234},
                            "generation_time": {"type": "number", "example": 1.45},
                            "cache_hit": {"type": "boolean", "example": False}
                        }
                    }
                },
                "400": {"description": "Prompt inválido", "schema": {"$ref": "#/definitions/Error"}},
                "401": {"description": "API key inválida", "schema": {"$ref": "#/definitions/Error"}},
                "429": {"description": "Rate limit excedido", "schema": {"$ref": "#/definitions/Error"}},
                "500": {"description": "Erro interno", "schema": {"$ref": "#/definitions/Error"}}
            }
        },
        
        'products': {
            "tags": ["Data"],
            "summary": "Lista produtos disponíveis",
            "description": "Retorna lista completa de produtos cadastrados no sistema. Os dados são automaticamente cacheados para melhor performance.",
            "responses": {
                "200": {
                    "description": "Produtos listados com sucesso",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "example": "success"},
                            "products": {
                                "type": "array",
                                "items": {"type": "string"},
                                "example": ["Bolo_de_Chocolate", "Brigadeiro_Gourmet", "Cafe_Expresso"]
                            },
                            "count": {"type": "integer", "example": 10},
                            "cache_hit": {"type": "boolean", "example": True}
                        }
                    }
                },
                "500": {"description": "Erro interno", "schema": {"$ref": "#/definitions/Error"}}
            }
        },
        
        'health_robust': {
            "tags": ["Health"],
            "summary": "Health check robusto completo",
            "description": """
Executa verificação completa da saúde do sistema incluindo todos os componentes.

**Componentes verificados:**
- Database (MySQL)
- Cache (Redis) 
- Modelos ML
- APIs externas (Gemini, OpenAI)
- Recursos do sistema (CPU, memória, disco)

**Métricas coletadas:**
- Tempo de resposta
- Disponibilidade
- Performance
- Uso de recursos
- Taxa de erro
- Uptime percentage
            """,
            "responses": {
                "200": {
                    "description": "Health check executado com sucesso",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "example": "success"},
                            "overall_status": {
                                "type": "string",
                                "enum": ["healthy", "warning", "critical", "unknown"],
                                "example": "healthy"
                            },
                            "components": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "example": "MySQL Database"},
                                        "type": {"type": "string", "example": "database"},
                                        "status": {"type": "string", "example": "healthy"},
                                        "response_time": {"type": "number", "example": 0.123},
                                        "uptime_percentage": {"type": "number", "example": 99.5},
                                        "error_message": {"type": "string"}
                                    }
                                }
                            },
                            "summary": {
                                "type": "object",
                                "properties": {
                                    "total_components": {"type": "integer", "example": 5},
                                    "healthy_components": {"type": "integer", "example": 4},
                                    "warning_components": {"type": "integer", "example": 1},
                                    "critical_components": {"type": "integer", "example": 0}
                                }
                            },
                            "alerts": {
                                "type": "array",
                                "items": {"type": "string"},
                                "example": ["WARNING: Redis Cache - Performance degraded"]
                            },
                            "timestamp": {"type": "string", "format": "date-time"}
                        }
                    }
                },
                "500": {"description": "Erro no health check", "schema": {"$ref": "#/definitions/Error"}}
            }
        },
        
        'cache_status': {
            "tags": ["Cache"],
            "summary": "Status do cache Redis",
            "description": """
Retorna status atual e estatísticas detalhadas do sistema de cache Redis.

**Informações incluídas:**
- Taxa de hit/miss
- Número de chaves armazenadas
- Uso de memória
- Tempo de uptime
- Performance metrics
            """,
            "responses": {
                "200": {
                    "description": "Status obtido com sucesso",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "example": "success"},
                            "cache_status": {"type": "string", "example": "available"},
                            "stats": {
                                "type": "object",
                                "properties": {
                                    "total_requests": {"type": "integer", "example": 1500},
                                    "cache_hits": {"type": "integer", "example": 1200},
                                    "cache_misses": {"type": "integer", "example": 300},
                                    "hit_rate": {"type": "number", "example": 80.0},
                                    "total_keys": {"type": "integer", "example": 45},
                                    "memory_usage": {"type": "string", "example": "12.5MB"},
                                    "uptime": {"type": "string", "example": "2h 30m"}
                                }
                            },
                            "timestamp": {"type": "string", "format": "date-time"}
                        }
                    }
                },
                "500": {"description": "Erro ao acessar cache", "schema": {"$ref": "#/definitions/Error"}}
            }
        }
    }
    
    # Definições comuns
    definitions = {
        "Error": {
            "type": "object",
            "required": ["status", "message"],
            "properties": {
                "status": {"type": "string", "example": "error"},
                "message": {"type": "string", "example": "Erro interno do servidor"},
                "error_code": {"type": "string", "example": "INTERNAL_ERROR"},
                "timestamp": {"type": "string", "format": "date-time"}
            }
        },
        "Success": {
            "type": "object",
            "required": ["status"],
            "properties": {
                "status": {"type": "string", "example": "success"},
                "message": {"type": "string", "example": "Operação executada com sucesso"},
                "timestamp": {"type": "string", "format": "date-time"}
            }
        }
    }
    
    return specs, definitions

def create_documented_app():
    """Cria aplicação Flask com documentação Swagger."""
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    
    CORS(app)
    
    # Adiciona definições ao template
    specs, definitions = create_swagger_specs()
    swagger_template["definitions"] = definitions
    
    # Inicializa Swagger
    swagger = Swagger(app, config=swagger_config, template=swagger_template)
    
    # ==================== ROTAS DOCUMENTADAS ====================
    
    @app.route('/api/ai/predict', methods=['POST'])
    @swag_from({
        'tags': ['AI'],
        'summary': 'Prediz demanda de um produto',
        'description': specs['predict']['description'],
        'parameters': specs['predict']['parameters'],
        'responses': specs['predict']['responses']
    })
    def predict_demand_doc():
        """Endpoint documentado para predição de demanda."""
        return jsonify({
            "message": "Esta é a documentação. Acesse http://localhost:5001/api/ai/predict para usar a API real.",
            "real_endpoint": "http://localhost:5001/api/ai/predict",
            "method": "POST"
        })
    
    @app.route('/api/ai/generate-insight', methods=['POST'])
    @swag_from({
        'tags': ['AI'],
        'summary': 'Gera insights usando IA',
        'description': specs['generate_insight']['description'],
        'parameters': specs['generate_insight']['parameters'],
        'responses': specs['generate_insight']['responses']
    })
    def generate_insight_doc():
        """Endpoint documentado para geração de insights."""
        return jsonify({
            "message": "Esta é a documentação. Acesse http://localhost:5001/api/ai/generate-insight para usar a API real.",
            "real_endpoint": "http://localhost:5001/api/ai/generate-insight",
            "method": "POST"
        })
    
    @app.route('/api/data/products', methods=['GET'])
    @swag_from({
        'tags': ['Data'],
        'summary': 'Lista produtos disponíveis',
        'description': specs['products']['description'],
        'responses': specs['products']['responses']
    })
    def products_doc():
        """Endpoint documentado para listagem de produtos."""
        return jsonify({
            "message": "Esta é a documentação. Acesse http://localhost:5001/api/data/products para usar a API real.",
            "real_endpoint": "http://localhost:5001/api/data/products",
            "method": "GET"
        })
    
    @app.route('/api/health/robust', methods=['GET'])
    @swag_from({
        'tags': ['Health'],
        'summary': 'Health check robusto completo',
        'description': specs['health_robust']['description'],
        'responses': specs['health_robust']['responses']
    })
    def health_robust_doc():
        """Endpoint documentado para health check robusto."""
        return jsonify({
            "message": "Esta é a documentação. Acesse http://localhost:5001/api/health/robust para usar a API real.",
            "real_endpoint": "http://localhost:5001/api/health/robust",
            "method": "GET"
        })
    
    @app.route('/api/cache/status', methods=['GET'])
    @swag_from({
        'tags': ['Cache'],
        'summary': 'Status do cache Redis',
        'description': specs['cache_status']['description'],
        'responses': specs['cache_status']['responses']
    })
    def cache_status_doc():
        """Endpoint documentado para status do cache."""
        return jsonify({
            "message": "Esta é a documentação. Acesse http://localhost:5001/api/cache/status para usar a API real.",
            "real_endpoint": "http://localhost:5001/api/cache/status",
            "method": "GET"
        })
    
    # ==================== ROTAS ADICIONAIS ====================
    
    @app.route('/')
    def index():
        """Página inicial com links para documentação."""
        return jsonify({
            "message": "Sistema AI da Padaria - Documentação",
            "documentation": {
                "swagger_ui": "/docs/",
                "api_spec": "/apispec.json",
                "real_api": "http://localhost:5001"
            },
            "endpoints": {
                "ai_predict": "/api/ai/predict",
                "ai_insights": "/api/ai/generate-insight", 
                "data_products": "/api/data/products",
                "health_check": "/api/health/robust",
                "cache_status": "/api/cache/status"
            },
            "version": "1.0.0"
        })
    
    @app.route('/api/endpoints', methods=['GET'])
    def list_endpoints():
        """Lista todos os endpoints disponíveis."""
        endpoints = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                endpoints.append({
                    'endpoint': rule.rule,
                    'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
                    'function': rule.endpoint
                })
        
        return jsonify({
            "status": "success",
            "endpoints": endpoints,
            "count": len(endpoints),
            "documentation_url": "/docs/"
        })
    
    return app

if __name__ == '__main__':
    # Verifica se flasgger está disponível
    try:
        import flasgger
        print("✅ Flasgger disponível")
    except ImportError:
        print("❌ Flasgger não encontrado. Instale com: pip install flasgger")
        exit(1)
    
    # Cria app com documentação
    app = create_documented_app()
    
    print("\n🚀 Documentação API Swagger ativa!")
    print("=" * 50)
    print("📖 Swagger UI: http://localhost:5002/docs/")
    print("📄 API Spec: http://localhost:5002/apispec.json")
    print("🌐 Endpoints: http://localhost:5002/api/endpoints")
    print("🔗 API Real: http://localhost:5001")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5002, debug=True)