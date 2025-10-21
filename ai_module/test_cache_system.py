#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes para validar o sistema de cache Redis.
Verifica performance, funcionalidade e fallback.
"""

import time
import sys
import os
import statistics
from datetime import datetime
from typing import List, Dict

# Adiciona o diretório atual ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_redis_connection():
    """Testa conexão básica com Redis."""
    print("🧪 Testando conexão com Redis...")
    
    try:
        from redis_cache import cache, health_check
        
        health = health_check()
        if health['redis_available']:
            print("  ✅ Redis conectado e funcionando")
            if 'stats' in health:
                stats = health['stats']
                print(f"  📊 Clientes conectados: {stats.get('connected_clients', 'N/A')}")
                print(f"  💾 Memória usada: {stats.get('used_memory_human', 'N/A')}")
                print(f"  🎯 Taxa de hit: {stats.get('hit_rate', 0):.1f}%")
            return True
        else:
            print(f"  ⚠️ Redis não disponível: {health.get('error', 'Motivo desconhecido')}")
            return False
            
    except Exception as e:
        print(f"  ❌ Erro ao testar Redis: {e}")
        return False

def test_model_cache_performance():
    """Testa performance do cache de modelos."""
    print("\n🧪 Testando performance do cache de modelos...")
    
    try:
        from ai_service import load_model
        from product_name_utils import get_all_display_product_names
        
        products = get_all_display_product_names()[:3]  # Testa apenas 3 produtos
        
        # Primeira execução (cache miss)
        print("  📊 Primeira execução (cache miss):")
        miss_times = []
        for product in products:
            start = time.time()
            model = load_model(product)
            duration = time.time() - start
            miss_times.append(duration)
            status = "✅" if model is not None else "❌"
            print(f"    {status} {product}: {duration:.3f}s")
        
        # Segunda execução (cache hit)
        print("  📊 Segunda execução (cache hit):")
        hit_times = []
        for product in products:
            start = time.time()
            model = load_model(product)
            duration = time.time() - start
            hit_times.append(duration)
            status = "✅" if model is not None else "❌"
            print(f"    {status} {product}: {duration:.3f}s")
        
        # Análise de performance
        if miss_times and hit_times:
            avg_miss = statistics.mean(miss_times)
            avg_hit = statistics.mean(hit_times)
            speedup = avg_miss / avg_hit if avg_hit > 0 else 0
            
            print(f"  📈 Tempo médio (miss): {avg_miss:.3f}s")
            print(f"  ⚡ Tempo médio (hit): {avg_hit:.3f}s")
            print(f"  🚀 Aceleração: {speedup:.1f}x")
            
            return speedup > 2  # Cache deve ser pelo menos 2x mais rápido
        
        return False
        
    except Exception as e:
        print(f"  ❌ Erro no teste de performance: {e}")
        return False

def test_prediction_cache():
    """Testa cache de predições."""
    print("\n🧪 Testando cache de predições...")
    
    try:
        from redis_cache import ModelCache
        import json
        
        # Dados de teste
        test_product = "Bolo de Chocolate"
        test_days = 3
        test_prediction = [
            {'date': '2025-10-02', 'predicted_demand': 10, 'lower_bound': 8, 'upper_bound': 12},
            {'date': '2025-10-03', 'predicted_demand': 12, 'lower_bound': 10, 'upper_bound': 14},
            {'date': '2025-10-04', 'predicted_demand': 11, 'lower_bound': 9, 'upper_bound': 13}
        ]
        
        # Teste de escrita
        success = ModelCache.set_prediction(test_product, test_days, test_prediction)
        print(f"  📝 Escrita no cache: {'✅' if success else '❌'}")
        
        # Teste de leitura
        cached_result = ModelCache.get_prediction(test_product, test_days)
        read_success = cached_result == test_prediction
        print(f"  📖 Leitura do cache: {'✅' if read_success else '❌'}")
        
        # Teste de invalidação
        ModelCache.invalidate_model(test_product)
        invalidated_result = ModelCache.get_prediction(test_product, test_days)
        invalidation_success = invalidated_result is None
        print(f"  🗑️ Invalidação: {'✅' if invalidation_success else '❌'}")
        
        return success and read_success and invalidation_success
        
    except Exception as e:
        print(f"  ❌ Erro no teste de predições: {e}")
        return False

def test_cache_ttl():
    """Testa expiração do cache (TTL)."""
    print("\n🧪 Testando TTL do cache...")
    
    try:
        from redis_cache import cache
        
        # Teste com TTL curto
        test_key = "ai_module:test_ttl"
        test_value = {"test": "ttl_value", "timestamp": datetime.now().isoformat()}
        
        # Define TTL de 2 segundos
        cache.set(test_key, test_value, ttl=2)
        
        # Verifica se está no cache
        immediate_result = cache.get(test_key)
        immediate_success = immediate_result == test_value
        print(f"  📝 Valor imediato: {'✅' if immediate_success else '❌'}")
        
        # Espera expirar
        print("  ⏳ Aguardando expiração (3s)...")
        time.sleep(3)
        
        # Verifica se expirou
        expired_result = cache.get(test_key)
        expiration_success = expired_result is None
        print(f"  ⏰ Expiração: {'✅' if expiration_success else '❌'}")
        
        return immediate_success and expiration_success
        
    except Exception as e:
        print(f"  ❌ Erro no teste de TTL: {e}")
        return False

def test_cache_fallback():
    """Testa fallback quando Redis não está disponível."""
    print("\n🧪 Testando fallback sem Redis...")
    
    try:
        from redis_cache import RedisCache
        
        # Simula Redis indisponível
        mock_cache = RedisCache()
        mock_cache.enabled = False
        mock_cache.redis_client = None
        
        # Testa operações básicas
        set_result = mock_cache.set("test_key", "test_value")
        get_result = mock_cache.get("test_key")
        delete_result = mock_cache.delete("test_key")
        
        fallback_success = (
            set_result is False and  # Set deve retornar False
            get_result is None and   # Get deve retornar None
            delete_result is False   # Delete deve retornar False
        )
        
        print(f"  🔄 Fallback funcionando: {'✅' if fallback_success else '❌'}")
        
        return fallback_success
        
    except Exception as e:
        print(f"  ❌ Erro no teste de fallback: {e}")
        return False

def test_cache_statistics():
    """Testa estatísticas do cache."""
    print("\n🧪 Testando estatísticas do cache...")
    
    try:
        from redis_cache import get_cache_info
        
        stats = get_cache_info()
        
        required_fields = ['enabled']
        if stats.get('enabled'):
            required_fields.extend(['connected_clients', 'used_memory_human', 'hit_rate'])
        
        stats_success = all(field in stats for field in required_fields)
        print(f"  📊 Estatísticas disponíveis: {'✅' if stats_success else '❌'}")
        
        if stats_success and stats.get('enabled'):
            print(f"    - Status: {'Habilitado' if stats['enabled'] else 'Desabilitado'}")
            print(f"    - Taxa de hit: {stats.get('hit_rate', 0):.1f}%")
            print(f"    - Chaves AI: {stats.get('ai_module_keys', 0)}")
        
        return stats_success
        
    except Exception as e:
        print(f"  ❌ Erro no teste de estatísticas: {e}")
        return False

def benchmark_cache_performance():
    """Benchmark completo de performance."""
    print("\n🏁 Benchmark de performance do cache...")
    
    try:
        from ai_service import load_model
        from product_name_utils import get_all_display_product_names
        
        products = get_all_display_product_names()[:5]  # 5 produtos para benchmark
        iterations = 3
        
        print(f"  🎯 Testando {len(products)} produtos, {iterations} iterações cada")
        
        total_times = {'miss': [], 'hit': []}
        
        for i in range(iterations):
            print(f"    Iteração {i+1}/{iterations}")
            
            # Limpa cache para garantir miss
            from redis_cache import ModelCache
            ModelCache.invalidate_all()
            
            # Cache miss
            miss_start = time.time()
            for product in products:
                load_model(product)
            miss_time = time.time() - miss_start
            total_times['miss'].append(miss_time)
            
            # Cache hit
            hit_start = time.time()
            for product in products:
                load_model(product)
            hit_time = time.time() - hit_start
            total_times['hit'].append(hit_time)
        
        avg_miss = statistics.mean(total_times['miss'])
        avg_hit = statistics.mean(total_times['hit'])
        speedup = avg_miss / avg_hit if avg_hit > 0 else 0
        
        print("  📊 Resultados do benchmark:")
        print(f"    - Tempo médio sem cache: {avg_miss:.3f}s")
        print(f"    - Tempo médio com cache: {avg_hit:.3f}s")
        print(f"    - Aceleração total: {speedup:.1f}x")
        print(f"    - Economia de tempo: {((avg_miss - avg_hit) / avg_miss * 100):.1f}%")
        
        return speedup > 5  # Cache deve dar pelo menos 5x de speedup no total
        
    except Exception as e:
        print(f"  ❌ Erro no benchmark: {e}")
        return False

def main():
    """Executa todos os testes de cache."""
    print("🔍 Iniciando testes do sistema de cache Redis...")
    print("=" * 60)
    
    tests = [
        ("Conexão Redis", test_redis_connection),
        ("Performance de Modelos", test_model_cache_performance),
        ("Cache de Predições", test_prediction_cache),
        ("TTL (Expiração)", test_cache_ttl),
        ("Fallback sem Redis", test_cache_fallback),
        ("Estatísticas", test_cache_statistics),
        ("Benchmark Completo", benchmark_cache_performance),
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        try:
            result = test_func()
            if result:
                passed_tests += 1
                print(f"✅ {test_name}: PASSOU")
            else:
                print(f"❌ {test_name}: FALHOU")
        except Exception as e:
            print(f"💥 {test_name}: ERRO - {e}")
    
    print("\n" + "=" * 60)
    print("📊 RESUMO FINAL DOS TESTES DE CACHE")
    print(f"✅ Testes que passaram: {passed_tests}/{total_tests}")
    print(f"❌ Testes que falharam: {total_tests - passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("\n🎉 TODOS OS TESTES DE CACHE PASSARAM!")
        print("O sistema de cache Redis está funcionando perfeitamente.")
    elif passed_tests >= total_tests * 0.7:  # 70% de sucesso
        print(f"\n⚠️ MAIORIA DOS TESTES PASSARAM ({passed_tests}/{total_tests})")
        print("O cache está funcional, mas algumas funcionalidades podem precisar de ajustes.")
    else:
        print(f"\n❌ MUITOS TESTES FALHARAM ({total_tests - passed_tests}/{total_tests})")
        print("O sistema de cache pode precisar de correções significativas.")
    
    return passed_tests >= total_tests * 0.7

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)