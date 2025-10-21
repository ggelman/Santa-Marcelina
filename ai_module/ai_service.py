from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime, timedelta
import subprocess
import openai
import sys
import tempfile
import logging
import time
import json
from product_name_utils import normalize_product_name, get_normalized_filename, reverse_normalize_for_display
from redis_cache import cached_model, cached_prediction, ModelCache, get_cache_info, health_check, warm_up_cache

# Sistema de monitoramento
from monitoring_system import (
    StructuredLogger, PerformanceMetrics, HealthChecker, 
    get_enhanced_monitoring_data, integrate_robust_health_checks,
    performance_monitor, log_model_load, get_monitoring_data
)

# Sistema de tratamento de erros
from error_handling import (
    error_handler, BaseAIException, ErrorSeverity, ErrorCategory,
    NetworkError, DatabaseError, AIAPIError, ValidationError, ModelLoadError,
    retry_with_fallback, AI_API_RETRY_CONFIG, DATABASE_RETRY_CONFIG, safe_execute
)
from flask_error_middleware import (
    FlaskErrorHandler, handle_api_errors, with_database_retry, 
    with_ai_api_retry, validate_request_data, CriticalOperation
)
from fallback_service import (
    get_sales_data_with_fallback, get_products_with_fallback,
    generate_insight_with_fallback, predict_with_fallback
)

# Sistema de monitoramento de segurança
from security_monitor import security_monitor

# Tenta importar gemini_service; se não disponível, usamos OpenAI como fallback
try:
    from gemini_service import generate_insights as gemini_generate_insights
    _GEMINI_AVAILABLE = True
except Exception:
    gemini_generate_insights = None
    _GEMINI_AVAILABLE = False

app = Flask(__name__)
CORS(app)  

# Rate Limiting Configuration
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
limiter.init_app(app)

# Inicializa sistema de tratamento de erros
error_middleware = FlaskErrorHandler(app)

# Middleware de monitoramento de segurança
@app.before_request
def log_request_security():
    """Registra requisições para monitoramento de segurança"""
    if request.endpoint and not request.endpoint.startswith('static'):
        ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        if ip and ',' in ip:
            ip = ip.split(',')[0].strip()
        
        user_agent = request.headers.get('User-Agent', '')
        
        # Registra a requisição
        security_monitor.log_request(
            ip=ip or 'unknown',
            endpoint=request.path,
            status_code=0,  # Será atualizado no after_request
            user_agent=user_agent
        )

@app.after_request  
def log_response_security(response):
    """Atualiza o log com o código de resposta"""
    if request.endpoint and not request.endpoint.startswith('static'):
        ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        if ip and ',' in ip:
            ip = ip.split(',')[0].strip()
            
        # Atualiza o último registro com o status code real
        if ip and hasattr(security_monitor.request_log[ip or 'unknown'], '__len__'):
            if len(security_monitor.request_log[ip or 'unknown']) > 0:
                last_request = security_monitor.request_log[ip or 'unknown'][-1]
                last_request['status_code'] = response.status_code
    
    return response

# Inicializa sistema de monitoramento e logging
metrics = PerformanceMetrics()
health_checker = HealthChecker()
logger = StructuredLogger(__name__)

# O logging agora é gerenciado pelo monitoring_system
# logging.basicConfig foi removido em favor do structured logging

openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_base = os.environ.get("OPENAI_API_BASE")

# Caminhos usando o diretório atual do script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(SCRIPT_DIR, 'trained_models')
DATA_FILE = os.path.join(SCRIPT_DIR, 'processed_sales_data.csv')
RETRAINER_SCRIPT = os.path.join(SCRIPT_DIR, 'model_retrainer.py')

@cached_model()  
def load_model(product_name):
    """Carrega modelo com tratamento de erro robusto."""
    normalized_name = normalize_product_name(product_name)
    model_filename = os.path.join(MODELS_DIR, f"prophet_model_{normalized_name}.pkl")
    
    # Log de debug para mostrar caminhos
    logger.info(f"Tentando carregar modelo: {model_filename}")
    logger.info(f"MODELS_DIR: {MODELS_DIR}")
    logger.info(f"Arquivo existe: {os.path.exists(model_filename)}")
    
    if not os.path.exists(model_filename):
        # Lista arquivos disponíveis para debug
        if os.path.exists(MODELS_DIR):
            available_models = os.listdir(MODELS_DIR)
            logger.info(f"Modelos disponíveis: {available_models}")
        
        raise ModelLoadError(
            f"Arquivo de modelo não encontrado: {model_filename}",
            context={'product_name': product_name, 'normalized_name': normalized_name}
        )
    
    try:
        with open(model_filename, 'rb') as f:
            model = pickle.load(f)
        log_model_load(product_name, success=True, cache_hit=False)
        return model
    except Exception as e:
        raise ModelLoadError(
            f"Erro ao carregar modelo para {product_name}",
            context={
                'product_name': product_name,
                'model_file': model_filename,
                'file_exists': os.path.exists(model_filename)
            },
            original_exception=e
        )
    else:
        logging.warning(f"Arquivo de modelo não encontrado: {model_filename}")
        return None

def make_prediction(model, future_dates_df):
    forecast = model.predict(future_dates_df)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

DATA_COLLECTOR_SCRIPT = 'data_collector.py'


def update_data():
    try:
        result = subprocess.run([sys.executable, DATA_COLLECTOR_SCRIPT], check=False, capture_output=True, text=True)
        if result.returncode != 0:
            logging.error('Data collector failed: %s', result.stderr)
            return False
        logging.info('Data collector output: %s', result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logging.exception(f"Erro ao executar o script de coleta de dados: {e}")
        return False

# === ROTAS PRINCIPAIS ===

@app.route('/', methods=['GET'])
def welcome():
    """Página de boas-vindas da API."""
    return jsonify({
        'service': 'Sistema AI da Padaria',
        'version': '1.0.0',
        'status': 'online',
        'message': '🍞 API de Inteligência Artificial para Predição de Demanda',
        'documentation': 'http://localhost:5002',
        'endpoints': {
            'health': '/api/ai/health',
            'predict': '/api/ai/predict',
            'insights': '/api/ai/generate-insight',
            'products': '/api/ai/products',
            'monitoring': '/api/monitoring/health'
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api', methods=['GET'])
def api_info():
    """Informações da API."""
    return jsonify({
        'api_name': 'Sistema AI da Padaria',
        'version': '1.0.0',
        'description': 'API para predição de demanda usando IA',
        'documentation': 'http://localhost:5002',
        'health_check': '/api/ai/health',
        'available_routes': [
            'GET /',
            'GET /api',
            'POST /api/ai/predict',
            'GET /api/ai/products',
            'GET /api/ai/health',
            'POST /api/ai/generate-insight'
        ]
    })

@app.route('/favicon.ico')
def favicon():
    """Favicon simples para evitar erro 404."""
    return '', 204


@app.route('/api/ai/update-data', methods=['POST'])
@performance_monitor('/api/ai/update-data')
@handle_api_errors()
@with_database_retry
def trigger_update_data():
    """Atualiza dados com tratamento robusto de erros."""
    with CriticalOperation("update_data"):
        success = update_data()
        if success:
            return jsonify({'success': True, 'message': 'Atualização de dados concluída com sucesso.'}), 200
        else:
            raise DatabaseError("Falha na atualização de dados do banco")


@app.route('/api/ai/predict', methods=['POST'])
@limiter.limit("15 per minute")  # Limite de 15 previsões individuais por minuto
def _validate_prediction_request(data):
    """Valida os dados da requisição de predição."""
    product_name = data.get('product_name')
    days_ahead = data.get('days_ahead', 1)
    
    if days_ahead < 1 or days_ahead > 365:
        raise ValidationError(
            "days_ahead deve estar entre 1 e 365",
            context={'received_days': days_ahead}
        )
    
    return product_name, days_ahead

def _check_prediction_cache(product_name, days_ahead):
    """Verifica cache para predição."""
    cached_result = ModelCache.get_prediction(
        product_name, 
        days_ahead,
        temperatura_media=25,  
        promocao=0
    )
    
    if cached_result:
        logging.info(f"Cache HIT para predição: {product_name} ({days_ahead} dias)")
        return cached_result
    
    logging.info(f"Cache MISS para predição: {product_name} ({days_ahead} dias)")
    return None

@performance_monitor('/api/ai/predict')
@handle_api_errors()
@validate_request_data(required_fields=['product_name'])
def predict_demand():
    """Faz predição com tratamento robusto de erros e fallback."""
    data = request.get_json()
    product_name, days_ahead = _validate_prediction_request(data)
    
    # Verifica cache primeiro
    cached_prediction = _check_prediction_cache(product_name, days_ahead)
    if cached_prediction:
        return jsonify({
            'product_name': product_name,
            'predictions': cached_prediction,
            'cached': True
        })
    
    # Cache miss - processa predição
    model = load_model(product_name)
    if model is None:
        return jsonify({'error': f'Modelo para {product_name} não encontrado'}), 404
    
    try:    
        today = datetime.now()
        future_dates = []
        for i in range(1, days_ahead + 1):
            future_dates.append(today + timedelta(days=i))
        
        future_df = pd.DataFrame({'ds': future_dates})
        
        future_df["temperatura_media"] = 25 + 5 * (future_df.index % 7) # Exemplo de variação semanal
        future_df["promocao"] = (future_df.index % 10 == 0).astype(int) # Exemplo de promoção a cada 10 dias
        
        forecast = make_prediction(model, future_df)
        
        predictions = []
        for _, row in forecast.iterrows():
            # Tratamento seguro para valores NaN/infinitos
            predicted_demand = row['yhat']
            lower_bound = row['yhat_lower'] 
            upper_bound = row['yhat_upper']
            
            # Substitui NaN/inf por 0
            if pd.isna(predicted_demand) or not np.isfinite(predicted_demand):
                predicted_demand = 0
            if pd.isna(lower_bound) or not np.isfinite(lower_bound):
                lower_bound = 0
            if pd.isna(upper_bound) or not np.isfinite(upper_bound):
                upper_bound = 0
            
            predictions.append({
                'date': row['ds'].strftime('%Y-%m-%d'),
                'predicted_demand': round(float(predicted_demand)),
                'lower_bound': round(float(lower_bound)),
                'upper_bound': round(float(upper_bound))
            })

        ModelCache.set_prediction(
            product_name, 
            days_ahead, 
            predictions,
            temperatura_media=25,
            promocao=0
        )
        
        return jsonify({
            'product_name': product_name,
            'predictions': predictions,
            'cached': False
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def _get_available_products():
    """Obtém lista de produtos com modelos treinados."""
    all_products = []
    if os.path.isdir(MODELS_DIR):
        for filename in os.listdir(MODELS_DIR):
            if filename.startswith("prophet_model_") and filename.endswith(".pkl"):
                normalized_name = filename.replace("prophet_model_", "").replace(".pkl", "")
                display_name = reverse_normalize_for_display(normalized_name)
                all_products.append(display_name)
                logger.info(f"Produto encontrado: {display_name}")
    else:
        logger.info('Models directory %s does not exist.', MODELS_DIR)
    return all_products

def _create_future_dataframe(days_ahead):
    """Cria DataFrame com datas futuras e regressores."""
    today = datetime.now()
    future_dates = [today + timedelta(days=i) for i in range(1, days_ahead + 1)]
    
    future_df = pd.DataFrame({'ds': future_dates})
    # Adiciona regressores que foram usados no treinamento
    future_df["temperatura_media"] = 25 + 5 * (future_df.index % 7)
    future_df["promocao"] = (future_df.index % 10 == 0).astype(int)
    
    return future_df

def _process_single_product_prediction(product, future_df):
    """Processa previsão para um único produto."""
    try:
        logger.info(f"Processando produto: {product}")
        model = load_model(product)
        if not model:
            return None
            
        logger.info(f"Modelo carregado para: {product}")
        forecast = make_prediction(model, future_df)
        logger.info(f"Forecast gerado para {product}: {forecast.shape}")
        
        predictions = []
        for idx, row in forecast.iterrows():
            # Tratamento seguro para valores NaN/infinitos
            predicted_demand = _safe_numeric_value(row['yhat'])
            lower_bound = _safe_numeric_value(row['yhat_lower'])
            upper_bound = _safe_numeric_value(row['yhat_upper'])
            
            predictions.append({
                'date': row['ds'].strftime('%Y-%m-%d'),
                'predicted_demand': predicted_demand,
                'confidence_interval': {
                    'lower': lower_bound,
                    'upper': upper_bound
                }
            })
        
        return predictions
    except Exception as e:
        logger.error(f"Erro ao processar {product}: {e}")
        return None

def _safe_numeric_value(value):
    """Converte valor para número seguro (trata NaN/inf)."""
    if pd.isna(value) or not np.isfinite(value):
        return 0
    return float(value)

@app.route('/api/ai/predict-all', methods=['GET'])
@limiter.limit("10 per minute")  # Limite de 10 previsões por minuto
@performance_monitor('/api/ai/predict-all')
def predict_all_products():
    try:
        logger.info("=== INÍCIO DEBUG predict_all_products ===")
        
        if not update_data():
            logger.error("Falha na atualização de dados")
            return jsonify({'error': 'Falha ao atualizar os dados antes da previsão.'}), 500

        days_ahead = request.args.get('days_ahead', 1, type=int)
        logger.info(f"Days ahead: {days_ahead}")
        
        all_products = _get_available_products()
        
        if not all_products:
            logger.info('No trained models found in %s', MODELS_DIR)
            return jsonify({'predictions': {}, 'total_products': 0, 'message': 'No trained models available.'}), 200
        
        logger.info(f"Total produtos: {len(all_products)}")
        
        future_df = _create_future_dataframe(days_ahead)
        logger.info(f"Future dates criado: {future_df.shape}")
        
        all_predictions = {}
        for product in all_products:
            predictions = _process_single_product_prediction(product, future_df)
            if predictions:
                all_predictions[product] = predictions
        
        logger.info(f"Total predictions geradas: {len(all_predictions)}")
        
        result = {
            'predictions': all_predictions,
            'total_products': len(all_products)
        }
        
        logging.info(f"Resultado final: {result}")
        logging.info("=== JSON serialization test ===")
        
        # Teste de serialização
        import json
        try:
            json.dumps(result)  # Test JSON serialization
            logging.info("JSON serialization OK")
        except Exception as e:
            logging.error(f"JSON serialization FAILED: {str(e)}")
            import traceback
            logging.error(f"JSON traceback: {traceback.format_exc()}")
            return jsonify({'error': f'JSON serialization error: {str(e)}'}), 500
        
        logging.info("=== FIM DEBUG predict_all_products ===")
        return jsonify(result)
    
    except Exception as e:
        logging.error(f"ERRO GERAL predict_all_products: {str(e)}")
        import traceback
        logging.error(f"TRACEBACK GERAL: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/products', methods=['GET'])
def get_available_products():
    try:
        cached_products = ModelCache.get_products_list()
        if cached_products:
            logging.info("Cache HIT para lista de produtos")
            return jsonify({
                'products': cached_products,
                'total': len(cached_products),
                'cached': True
            })
        
        logging.info("Cache MISS para lista de produtos")
        
        products = []
        for filename in os.listdir(MODELS_DIR):
            if filename.startswith("prophet_model_") and filename.endswith(".pkl"):
                normalized_name = filename.replace("prophet_model_", "").replace(".pkl", "")
                display_name = reverse_normalize_for_display(normalized_name)
                products.append({
                    'name': display_name,
                    'normalized_name': normalized_name,
                    'model_file': filename
                })
        
        ModelCache.set_products_list(products)
        
        return jsonify({
            'products': products,
            'total': len(products),
            'cached': False
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/retrain', methods=['POST'])
@limiter.limit("2 per hour")  # Limite de 2 retreinamentos por hora (operação pesada)
def retrain_models():
    try:
        new_data = request.get_json()
        if not new_data or not isinstance(new_data, list):
            return jsonify({'error': 'Dados inválidos. Esperado uma lista de objetos JSON.'}), 400

        new_data_df = pd.DataFrame(new_data)
        if not all(col in new_data_df.columns for col in ['ds', 'item_name', 'y']):
            return jsonify({'error': 'Dados incompletos. Esperado \'ds\', \'item_name\' e \'y\'.'}), 400

            temp_dir = tempfile.gettempdir()
            temp_new_data_path = os.path.join(temp_dir, 'new_sales_data.csv')
            new_data_df.to_csv(temp_new_data_path, index=False)

            subprocess.Popen([sys.executable, RETRAINER_SCRIPT, DATA_FILE, MODELS_DIR, temp_new_data_path])

        return jsonify({'message': 'Retreinamento iniciado em segundo plano.'}), 202

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/health', methods=['GET'])
def health_check_endpoint():
    base_health = {
        'status': 'healthy',
        'service': 'AI Prediction Service',
        'timestamp': datetime.now().isoformat()
    }
    
    cache_health = health_check()
    base_health['cache'] = cache_health
    
    return jsonify(base_health)

@app.route('/api/ai/rate-limits', methods=['GET'])
def rate_limit_status():
    """Retorna informações sobre rate limits"""
    try:
        return jsonify({
            "rate_limits": {
                "predict_all": "10 per minute",
                "predict": "15 per minute", 
                "retrain": "2 per hour",
                "generate_insight": "20 per hour",
                "default": "200 per day, 50 per hour"
            },
            "headers_info": {
                "X-RateLimit-Limit": "Rate limit configured for endpoint",
                "X-RateLimit-Remaining": "Requests remaining in current window",
                "X-RateLimit-Reset": "Unix timestamp when rate limit resets"
            },
            "status": "active",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/security/stats', methods=['GET'])
def security_stats():
    """Retorna estatísticas de segurança e potenciais ameaças"""
    try:
        stats = security_monitor.get_security_stats()
        return jsonify({
            "security_monitoring": stats,
            "rate_limiting": {
                "status": "active",
                "blocked_ips": list(security_monitor.blocked_ips)
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/cache/info', methods=['GET'])
def cache_info():
    try:
        info = get_cache_info()
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/cache/clear', methods=['POST'])
def clear_cache():
    try:
        data = request.get_json() or {}
        target = data.get('target', 'all')  
        
        if target == 'all':
            cleared = ModelCache.invalidate_all()
            message = f"Cache completo limpo: {cleared} chaves removidas"
        elif target == 'models':
            from redis_cache import cache
            cleared = cache.clear_pattern("ai_module:*model*")
            message = f"Cache de modelos limpo: {cleared} chaves removidas"
        elif target == 'predictions':
            from redis_cache import cache
            cleared = cache.clear_pattern("ai_module:*prediction*")
            message = f"Cache de predições limpo: {cleared} chaves removidas"
        else:
            ModelCache.invalidate_model(target)
            message = f"Cache do produto '{target}' limpo"
        
        return jsonify({
            'message': message,
            'target': target,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/cache/warm-up', methods=['POST'])
def cache_warm_up():
    try:
        warm_up_cache()
        return jsonify({
            'message': 'Cache warm-up iniciado',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500





@app.route("/api/ai/generate-insight", methods=["POST"])
@limiter.limit("20 per hour")  # Limite de 20 insights por hora (usa API externa)
def generate_insight():
    try:
        data = request.get_json()
        product = data.get("produto")
        prediction = data.get("previsao")

        if not product or prediction is None:
            return jsonify({"error": "produto e previsao são obrigatórios"}), 400
        prompt = (
            f"Você é um assistente de gestão de padarias. A previsão de demanda para o produto '{product}' "
            f"amanhã é de {prediction} unidades. Gere: (1) um insight curto em 1-2 frases; (2) uma ação recomendada curta; "
            f"(3) uma confidência de 0 a 1 explicando o quão confiante você está nesta recomendação. Seja direto e prático."
        )

        # Try Gemini first
        if _GEMINI_AVAILABLE and gemini_generate_insights is not None:
            try:
                logging.info('Chamando Gemini para gerar insight')
                ok, text, provider = gemini_generate_insights(prompt)
                if ok:
                    # Try to parse structured output if Gemini returned JSON
                    try:
                        parsed = json.loads(text)
                        return jsonify({'insight': parsed.get('insight'), 'action': parsed.get('action'), 'confidence': parsed.get('confidence', 0.0), 'provider': provider})
                    except Exception:
                        return jsonify({'insight': text, 'action': None, 'confidence': None, 'provider': provider})
                else:
                    logging.warning(f'Gemini não retornou resposta útil: {text}')
            except Exception as e:
                logging.exception(f'Erro ao chamar Gemini: {e}')

        # Fallback to OpenAI with retries
        openai_attempts = int(os.getenv('OPENAI_RETRIES', 2))
        for attempt in range(1, openai_attempts + 2):
            try:
                logging.info(f'Chamando OpenAI (attempt {attempt})')
                response = openai.ChatCompletion.create(
                    model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
                    messages=[
                        {"role": "system", "content": "Você é um assistente de gestão de padarias. Seja prático e direto."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.6,
                )
                # New API may return different structure; defensive parsing
                if hasattr(response.choices[0], 'message'):
                    text = response.choices[0].message.content.strip()
                else:
                    text = getattr(response.choices[0], 'text', '').strip()

                # Try parse JSON in response
                try:
                    parsed = json.loads(text)
                    return jsonify({'insight': parsed.get('insight'), 'action': parsed.get('action'), 'confidence': parsed.get('confidence', 0.0), 'provider': 'openai'})
                except Exception:
                    # Heuristic extraction: split into lines, first line = insight, second = action
                    lines = [l.strip() for l in text.split('\n') if l.strip()]
                    insight_text = lines[0] if lines else text
                    action_text = lines[1] if len(lines) > 1 else None
                    # Confidence heuristic: look for percentage or numeric in text
                    confidence = None
                    import re
                    m = re.search(r"(\d{1,3})%", text)
                    if m:
                        confidence = float(m.group(1)) / 100.0

                    return jsonify({'insight': insight_text, 'action': action_text, 'confidence': confidence, 'provider': 'openai'})

            except Exception as e:
                logging.exception(f'Erro OpenAI attempt {attempt}: {e}')
                time.sleep(attempt * 1.0)

        return jsonify({'error': 'Falha ao gerar insight com LLMs'}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Inicialização do cache quando o serviço inicia
def initialize_cache():
    """Inicializa o cache quando o serviço é iniciado."""
    logger.info("🚀 Inicializando serviço AI com monitoramento...")
    logger.info("⚠️ Modo sem Redis - cache desabilitado para esta execução")
    # Cache Redis temporariamente desabilitado

# === ROTAS DE MONITORAMENTO ===

@app.route('/api/monitoring/health', methods=['GET'])
@performance_monitor('/api/monitoring/health')
def get_health_status():
    """Endpoint para health checks completos."""
    try:
        health_data = health_checker.run_all_checks()
        status_code = 200 if health_data['overall_status'] == 'healthy' else 503
        return jsonify(health_data), status_code
    except Exception as e:
        logger.error("Erro ao executar health checks", error=str(e))
        return jsonify({
            'overall_status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/monitoring/metrics', methods=['GET'])
@performance_monitor('/api/monitoring/metrics')
def get_performance_metrics():
    """Endpoint para métricas de performance."""
    try:
        metrics_data = metrics.get_metrics()
        return jsonify(metrics_data), 200
    except Exception as e:
        logger.error("Erro ao obter métricas", error=str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/api/monitoring/dashboard', methods=['GET'])
@performance_monitor('/api/monitoring/dashboard')
def get_monitoring_dashboard():
    """Endpoint para dados completos do dashboard."""
    try:
        dashboard_data = get_monitoring_data()
        return jsonify(dashboard_data), 200
    except Exception as e:
        logger.error("Erro ao obter dados do dashboard", error=str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/api/monitoring/logs', methods=['GET'])
def get_recent_logs():
    """Endpoint para logs recentes (últimas 100 linhas)."""
    try:
        log_file = 'ai_service.log'
        if not os.path.exists(log_file):
            return jsonify({'logs': [], 'message': 'Log file not found'}), 200
        
        # Lê últimas linhas do arquivo de log
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Pega últimas 100 linhas
        recent_logs = []
        for line in lines[-100:]:
            try:
                log_entry = json.loads(line.strip())
                recent_logs.append(log_entry)
            except json.JSONDecodeError:
                # Se não for JSON válido, trata como log texto simples
                recent_logs.append({
                    'timestamp': datetime.now().isoformat(),
                    'level': 'INFO',
                    'message': line.strip(),
                    'raw': True
                })
        
        return jsonify({
            'logs': recent_logs,
            'count': len(recent_logs),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health/robust', methods=['GET'])
@handle_api_errors
def robust_health_check():
    """Endpoint para health check robusto."""
    try:
        # Executa health check robusto
        health_result = integrate_robust_health_checks()
        
        if health_result:
            return jsonify({
                'status': 'success',
                'overall_status': health_result.overall_status.value,
                'timestamp': health_result.timestamp.isoformat(),
                'components': [
                    {
                        'name': comp.name,
                        'type': comp.type.value,
                        'status': comp.status.value,
                        'response_time': round(comp.response_time, 3),
                        'uptime_percentage': round(comp.uptime_percentage, 2),
                        'metrics': [
                            {
                                'name': metric.name,
                                'value': metric.value,
                                'unit': metric.unit,
                                'status': metric.status.value,
                                'message': metric.message
                            }
                            for metric in comp.metrics
                        ],
                        'error_message': comp.error_message
                    }
                    for comp in health_result.components
                ],
                'system_metrics': [
                    {
                        'name': metric.name,
                        'value': metric.value,
                        'unit': metric.unit,
                        'status': metric.status.value
                    }
                    for metric in health_result.system_metrics
                ],
                'summary': {
                    'total_components': health_result.total_components,
                    'healthy_components': health_result.healthy_components,
                    'warning_components': health_result.warning_components,
                    'critical_components': health_result.critical_components
                },
                'alerts': health_result.alerts
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Falha ao executar health check robusto'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erro no health check robusto: {str(e)}'
        }), 500


def setup_ssl_context():
    """Configura o contexto SSL para HTTPS."""
    pass


# Inicializa o cache na importação do módulo
initialize_cache()


# Inicializa o cache na importação do módulo
initialize_cache()


def get_ssl_context():
    """Configura o contexto SSL para HTTPS."""
    import ssl
    import os
    
    # Caminhos dos certificados SSL
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cert_dir = os.path.join(base_dir, 'ssl_certificates')
    cert_file = os.path.join(cert_dir, 'server.crt')
    key_file = os.path.join(cert_dir, 'server.key')
    
    # Verificar se os certificados existem
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print(f"❌ Certificados SSL não encontrados em {cert_dir}")
        print(f"   Esperado: {cert_file} e {key_file}")
        return None
    
    try:
        # Criar contexto SSL com protocolo seguro
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.minimum_version = ssl.TLSVersion.TLSv1_2  # Usar TLS 1.2 ou superior
        context.load_cert_chain(cert_file, key_file)
        print(f"✅ Certificados SSL carregados de {cert_dir}")
        return context
    except Exception as e:
        print(f"❌ Erro ao carregar certificados SSL: {e}")
        return None

if __name__ == '__main__':
    import os
    
    # Configuração de porta
    use_https = os.getenv('USE_HTTPS', 'true').lower() == 'true'
    port = int(os.getenv('AI_SERVICE_PORT', '5443' if use_https else '5001'))
    
    if use_https:
        ssl_context = get_ssl_context()
        if ssl_context:
            print("🔒 Iniciando AI Service com HTTPS na porta", port)
            app.run(host='0.0.0.0', port=port, debug=True, ssl_context=ssl_context)
        else:
            print("⚠️ Falha ao configurar HTTPS, iniciando com HTTP na porta 5001")
            app.run(host='0.0.0.0', port=5001, debug=True)
    else:
        print(f"🌐 Iniciando AI Service com HTTP na porta {port}")
        app.run(host='0.0.0.0', port=port, debug=True)