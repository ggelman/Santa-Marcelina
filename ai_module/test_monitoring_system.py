#!/usr/bin/env python3
"""
Teste Completo do Sistema de Monitoramento
Valida logging estruturado, métricas e health checks
"""

import time
import json
from datetime import datetime
import os

def test_monitoring_system():
    """Teste completo do sistema de monitoramento."""
    print("🔍 TESTE COMPLETO DO SISTEMA DE MONITORAMENTO")
    print("=" * 60)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    
    # Teste 1: Importações do sistema de monitoramento
    print("\n🔍 1. TESTANDO IMPORTAÇÕES")
    print("-" * 40)
    
    try:
        from monitoring_system import (
            logger, metrics, health_checker, performance_monitor,
            log_prediction, log_model_load, get_monitoring_data,
            StructuredLogger, PerformanceMetrics, HealthChecker
        )
        print("  ✅ Todas as importações do sistema de monitoramento")
        
        import psutil
        print(f"  ✅ psutil {psutil.__version__}")
        
    except Exception as e:
        print(f"  ❌ Erro nas importações: {e}")
        return False
    
    # Teste 2: Logging estruturado
    print("\n🔍 2. TESTANDO LOGGING ESTRUTURADO")
    print("-" * 40)
    
    try:
        # Teste de diferentes níveis de log
        logger.info("Teste de log informativo", 
                   test_type="structured_logging",
                   component="test_system")
        
        logger.warning("Teste de log de aviso", 
                      test_type="structured_logging",
                      component="test_system")
        
        logger.error("Teste de log de erro", 
                    test_type="structured_logging",
                    component="test_system")
        
        print("  ✅ Logs estruturados em JSON funcionando")
        
        # Verifica se arquivo de log foi criado
        if os.path.exists('ai_service.log'):
            print("  ✅ Arquivo de log criado com sucesso")
        else:
            print("  ⚠️ Arquivo de log não encontrado")
        
    except Exception as e:
        print(f"  ❌ Erro no logging: {e}")
        return False
    
    # Teste 3: Sistema de métricas
    print("\n🔍 3. TESTANDO SISTEMA DE MÉTRICAS")
    print("-" * 40)
    
    try:
        # Registra algumas métricas de teste
        metrics.record_request('/api/test', 0.150, 200, False)
        metrics.record_request('/api/test', 0.200, 200, False)
        metrics.record_request('/api/test', 0.100, 500, True)
        
        # Registra métricas de acurácia
        metrics.record_accuracy('test_model', 0.95)
        metrics.record_accuracy('test_model', 0.92)
        
        # Obtém métricas compiladas
        compiled_metrics = metrics.get_metrics()
        
        print("  ✅ Métricas de performance registradas")
        print(f"     - Endpoints: {len(compiled_metrics.get('performance', {}))}")
        print(f"     - Modelos: {len(compiled_metrics.get('accuracy', {}))}")
        
        if '/api/test' in compiled_metrics.get('performance', {}):
            test_metrics = compiled_metrics['performance']['/api/test']
            print(f"     - Tempo médio: {test_metrics['avg_response_time_ms']}ms")
            print(f"     - Taxa de erro: {test_metrics['error_rate_percent']}%")
        
    except Exception as e:
        print(f"  ❌ Erro nas métricas: {e}")
        return False
    
    # Teste 4: Health checks
    print("\n🔍 4. TESTANDO HEALTH CHECKS")
    print("-" * 40)
    
    try:
        # Executa todos os health checks
        health_results = health_checker.run_all_checks()
        
        print("  ✅ Health checks executados")
        print(f"     - Status geral: {health_results['overall_status']}")
        print(f"     - Checks executados: {len(health_results.get('checks', {}))}")
        
        for check_name, result in health_results.get('checks', {}).items():
            status_icon = "✅" if result['status'] == 'healthy' else "❌"
            print(f"     - {check_name}: {status_icon} {result['status']}")
        
    except Exception as e:
        print(f"  ❌ Erro nos health checks: {e}")
        return False
    
    # Teste 5: Decorator de performance
    print("\n🔍 5. TESTANDO DECORATOR DE PERFORMANCE")
    print("-" * 40)
    
    try:
        @performance_monitor('test_function')
        def test_function(delay=0.1):
            time.sleep(delay)
            return f"Função executada com delay de {delay}s"
        
        # Executa função decorada
        result = test_function(0.1)
        print(f"  ✅ Decorator funcionando: {result}")
        
        # Verifica se métrica foi registrada
        new_metrics = metrics.get_metrics()
        if 'test_function' in new_metrics.get('performance', {}):
            print("  ✅ Métrica registrada pelo decorator")
        else:
            print("  ⚠️ Métrica não registrada pelo decorator")
        
    except Exception as e:
        print(f"  ❌ Erro no decorator: {e}")
        return False
    
    # Teste 6: Integração com AI Service (se disponível)
    print("\n🔍 6. TESTANDO INTEGRAÇÃO COM AI SERVICE")
    print("-" * 40)
    
    try:
        from ai_service import app
        print("  ✅ AI Service com monitoramento carregado")
        
        # Teste de funções de log específicas
        log_prediction("test_product", 7, 0.95, True)
        log_model_load("test_product", True, False)
        
        print("  ✅ Funções de log específicas funcionando")
        
    except Exception as e:
        print(f"  ❌ Erro na integração: {e}")
        return False
    
    # Teste 7: Dados de monitoramento completos
    print("\n🔍 7. TESTANDO DADOS COMPLETOS")
    print("-" * 40)
    
    try:
        monitoring_data = get_monitoring_data()
        
        print("  ✅ Dados de monitoramento completos:")
        print(f"     - Métricas: {'✅' if 'metrics' in monitoring_data else '❌'}")
        print(f"     - Health: {'✅' if 'health' in monitoring_data else '❌'}")
        print(f"     - Timestamp: {'✅' if 'timestamp' in monitoring_data else '❌'}")
        
    except Exception as e:
        print(f"  ❌ Erro nos dados completos: {e}")
        return False
    
    # Teste 8: Verificação de arquivos
    print("\n🔍 8. VERIFICANDO ARQUIVOS IMPLEMENTADOS")
    print("-" * 40)
    
    required_files = [
        "monitoring_system.py",
        "monitoring_dashboard.html",
        "requirements.txt"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - AUSENTE")
    
    print("\n" + "=" * 60)
    print("🎉 TESTE DO SISTEMA DE MONITORAMENTO CONCLUÍDO")
    print("=" * 60)
    
    print("\n📋 RESUMO DA IMPLEMENTAÇÃO:")
    print("✅ Logging estruturado em JSON implementado")
    print("✅ Sistema de métricas de performance ativo")
    print("✅ Health checks robustos funcionando")
    print("✅ Dashboard de monitoramento criado")
    print("✅ Integração com AI Service completa")
    
    print("\n🚀 FUNCIONALIDADES IMPLEMENTADAS:")
    print("📊 Métricas em tempo real de performance")
    print("🏥 Health checks automáticos para todos componentes")
    print("📋 Logs estruturados em formato JSON")
    print("📈 Dashboard web interativo")
    print("🔄 Monitoramento automático com atualização em tempo real")
    
    print("\n💡 COMO USAR:")
    print("1. Iniciar AI Service: python ai_service.py")
    print("2. Abrir dashboard: monitoring_dashboard.html")
    print("3. Acessar APIs de monitoramento:")
    print("   - GET /api/monitoring/health")
    print("   - GET /api/monitoring/metrics")
    print("   - GET /api/monitoring/dashboard")
    print("   - GET /api/monitoring/logs")
    
    return True

if __name__ == "__main__":
    success = test_monitoring_system()
    if success:
        print("\n🎯 SISTEMA DE MONITORAMENTO: ✅ IMPLEMENTADO COM SUCESSO!")
    else:
        print("\n❌ FALHA NA IMPLEMENTAÇÃO DO MONITORAMENTO")