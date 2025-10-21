#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir problemas de encoding nos arquivos de modelos.
Remove duplicatas com encoding incorreto e normaliza nomes de produtos.
"""

import os
import re
import shutil
import json
from pathlib import Path
import unicodedata

def normalize_product_name(name):
    """
    Normaliza nomes de produtos para evitar problemas de encoding.
    Remove acentos e caracteres especiais de forma consistente.
    """
    # Remove acentos usando unicodedata
    normalized = unicodedata.normalize('NFD', name)
    ascii_name = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    
    # Substitui espaços por underscore e remove caracteres especiais
    clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', ascii_name)
    
    # Remove underscores duplicados
    clean_name = re.sub(r'_+', '_', clean_name)
    
    # Remove underscores no início e fim
    clean_name = clean_name.strip('_')
    
    return clean_name

def get_product_name_mapping():
    """
    Cria um mapeamento dos nomes de produtos problemáticos para nomes corretos.
    """
    mapping = {
        # Nomes com encoding incorreto -> Nomes corretos
        'P├úo_de_A├º├║car': 'Pao_de_Acucar',
        'P├úo_Franc├¬s': 'Pao_Frances', 
        'P├úo_Integral': 'Pao_Integral',
        'Caf├®_Expresso': 'Cafe_Expresso',
        
        # Nomes com acentos corretos -> Nomes normalizados
        'Pão_de_Açúcar': 'Pao_de_Acucar',
        'Pão_Francês': 'Pao_Frances',
        'Pão_Integral': 'Pao_Integral', 
        'Café_Expresso': 'Cafe_Expresso',
        
        # Outros produtos
        'Bolo_de_Chocolate': 'Bolo_de_Chocolate',
        'Brigadeiro_Gourmet': 'Brigadeiro_Gourmet',
        'Cappuccino': 'Cappuccino',
        'Croissant': 'Croissant',
        'Suco_Natural': 'Suco_Natural',
        'Torta_de_Morango': 'Torta_de_Morango'
    }
    
    return mapping

def clean_duplicate_models():
    """
    Remove arquivos de modelos duplicados com encoding incorreto.
    """
    models_dir = Path('trained_models')
    if not models_dir.exists():
        print("Diretório trained_models não encontrado.")
        return
    
    # Obtém mapeamento de nomes de produtos
    get_product_name_mapping()
    
    # Arquivos problemáticos a serem removidos
    problematic_files = [
        'prophet_model_P├úo_de_A├º├║car.pkl',
        'prophet_model_P├úo_Franc├¬s.pkl', 
        'prophet_model_P├úo_Integral.pkl',
        'prophet_model_Caf├®_Expresso.pkl',
        'prophet_params_P├úo_de_A├º├║car.json',
        'prophet_params_P├úo_Franc├¬s.json',
        'prophet_params_P├úo_Integral.json', 
        'prophet_params_Caf├®_Expresso.json'
    ]
    
    removed_files = []
    for filename in problematic_files:
        file_path = models_dir / filename
        if file_path.exists():
            try:
                file_path.unlink()  # Remove o arquivo
                removed_files.append(filename)
                print(f"✅ Removido arquivo problemático: {filename}")
            except Exception as e:
                print(f"❌ Erro ao remover {filename}: {e}")
    
    print(f"\n📊 Total de arquivos removidos: {len(removed_files)}")
    return removed_files

def rename_models_to_normalized_names():
    """
    Renomeia arquivos de modelos para usar nomes normalizados.
    """
    models_dir = Path('trained_models')
    if not models_dir.exists():
        print("Diretório trained_models não encontrado.")
        return
    
    # Obter mapeamento de nomes
    mapping = get_product_name_mapping()
    renamed_files = []
    
    # Listar todos os arquivos .pkl e .json
    all_files = list(models_dir.glob('prophet_model_*.pkl')) + list(models_dir.glob('prophet_params_*.json'))
    
    for file_path in all_files:
        filename = file_path.name
        
        # Extrair nome do produto do arquivo
        if filename.startswith('prophet_model_'):
            product_part = filename.replace('prophet_model_', '').replace('.pkl', '')
            prefix = 'prophet_model_'
            suffix = '.pkl'
        elif filename.startswith('prophet_params_'):
            product_part = filename.replace('prophet_params_', '').replace('.json', '')
            prefix = 'prophet_params_'
            suffix = '.json'
        else:
            continue
        
        # Verificar se precisa renomear
        if product_part in mapping and mapping[product_part] != product_part:
            new_name = prefix + mapping[product_part] + suffix
            new_path = models_dir / new_name
            
            try:
                file_path.rename(new_path)
                renamed_files.append((filename, new_name))
                print(f"✅ Renomeado: {filename} -> {new_name}")
            except Exception as e:
                print(f"❌ Erro ao renomear {filename}: {e}")
    
    print(f"\n📊 Total de arquivos renomeados: {len(renamed_files)}")
    return renamed_files

def create_product_name_utils():
    """
    Cria um arquivo de utilitários para normalização de nomes de produtos.
    """
    utils_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitários para normalização de nomes de produtos.
Evita problemas de encoding em todo o sistema.
"""

import re
import unicodedata

def normalize_product_name(name):
    """
    Normaliza nomes de produtos para evitar problemas de encoding.
    
    Args:
        name (str): Nome do produto original
        
    Returns:
        str: Nome normalizado sem acentos e caracteres especiais
    """
    if not name or not isinstance(name, str):
        return ""
    
    # Remove acentos usando unicodedata
    normalized = unicodedata.normalize('NFD', name)
    ascii_name = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    
    # Substitui espaços por underscore e remove caracteres especiais
    clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', ascii_name)
    
    # Remove underscores duplicados
    clean_name = re.sub(r'_+', '_', clean_name)
    
    # Remove underscores no início e fim
    clean_name = clean_name.strip('_')
    
    return clean_name

def get_normalized_filename(product_name, file_type='model'):
    """
    Gera nome de arquivo normalizado para um produto.
    
    Args:
        product_name (str): Nome do produto
        file_type (str): Tipo do arquivo ('model' ou 'params')
        
    Returns:
        str: Nome do arquivo normalizado
    """
    normalized_name = normalize_product_name(product_name)
    
    if file_type == 'model':
        return f"prophet_model_{normalized_name}.pkl"
    elif file_type == 'params':
        return f"prophet_params_{normalized_name}.json"
    else:
        return f"{normalized_name}.{file_type}"

def reverse_normalize_for_display(normalized_name):
    """
    Converte nome normalizado de volta para exibição amigável.
    
    Args:
        normalized_name (str): Nome normalizado
        
    Returns:
        str: Nome para exibição
    """
    # Mapeamento reverso para nomes conhecidos
    display_mapping = {
        'Pao_de_Acucar': 'Pão de Açúcar',
        'Pao_Frances': 'Pão Francês', 
        'Pao_Integral': 'Pão Integral',
        'Cafe_Expresso': 'Café Expresso',
        'Bolo_de_Chocolate': 'Bolo de Chocolate',
        'Brigadeiro_Gourmet': 'Brigadeiro Gourmet',
        'Suco_Natural': 'Suco Natural',
        'Torta_de_Morango': 'Torta de Morango'
    }
    
    if normalized_name in display_mapping:
        return display_mapping[normalized_name]
    
    # Fallback: substitui underscores por espaços
    return normalized_name.replace('_', ' ')

# Mapeamento de produtos conhecidos
KNOWN_PRODUCTS = {
    'Pão de Açúcar': 'Pao_de_Acucar',
    'Pão Francês': 'Pao_Frances',
    'Pão Integral': 'Pao_Integral', 
    'Café Expresso': 'Cafe_Expresso',
    'Bolo de Chocolate': 'Bolo_de_Chocolate',
    'Brigadeiro Gourmet': 'Brigadeiro_Gourmet',
    'Cappuccino': 'Cappuccino',
    'Croissant': 'Croissant',
    'Suco Natural': 'Suco_Natural',
    'Torta de Morango': 'Torta_de_Morango'
}

def get_all_normalized_product_names():
    """Retorna lista de todos os nomes de produtos normalizados."""
    return list(KNOWN_PRODUCTS.values())

def get_all_display_product_names():
    """Retorna lista de todos os nomes de produtos para exibição."""
    return list(KNOWN_PRODUCTS.keys())
'''
    
    with open('product_name_utils.py', 'w', encoding='utf-8') as f:
        f.write(utils_content)
    
    print("✅ Criado arquivo product_name_utils.py")

def main():
    """Função principal que executa todas as correções."""
    print("🔧 Iniciando correção de problemas de encoding...")
    print("=" * 60)
    
    # 1. Limpar arquivos duplicados problemáticos
    print("\n1️⃣ Removendo arquivos duplicados com encoding incorreto...")
    removed = clean_duplicate_models()
    
    # 2. Renomear arquivos para nomes normalizados
    print("\n2️⃣ Renomeando arquivos para nomes normalizados...")
    renamed = rename_models_to_normalized_names()
    
    # 3. Criar utilitários para normalização
    print("\n3️⃣ Criando utilitários de normalização...")
    create_product_name_utils()
    
    print("\n" + "=" * 60)
    print("✅ Correção de encoding concluída!")
    print("📊 Resumo:")
    print(f"   - Arquivos removidos: {len(removed) if removed else 0}")
    print(f"   - Arquivos renomeados: {len(renamed) if renamed else 0}")
    print("   - Utilitários criados: 1")

if __name__ == "__main__":
    main()