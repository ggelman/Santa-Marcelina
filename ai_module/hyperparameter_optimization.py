import numpy as np
from sklearn.model_selection import ParameterGrid
from prophet import Prophet
from model_evaluation import evaluate_model

def optimize_hyperparameters(df, param_grid, horizon='30 days', parallel='processes'):
    """
    Otimiza os hiperparâmetros do modelo Prophet usando grid search.
    
    Args:
        df: DataFrame com os dados de treino (deve ter colunas 'ds' e 'y')
        param_grid: Dicionário com os parâmetros a serem otimizados
        horizon: String com o horizonte de previsão para validação cruzada
        parallel: String 'processes' ou 'threads' para paralelização
    
    Returns:
        Dict com os melhores parâmetros encontrados
    """
    best_rmse = float('inf')
    best_params = None
    
    # Gera todas as combinações de parâmetros
    param_combinations = ParameterGrid(param_grid)
    
    for params in param_combinations:
        try:
            print(f"Testando parâmetros: {params}")
            
            # Treina o modelo com os parâmetros atuais
            model = Prophet(**params)
            model.fit(df)
            
            # Avalia o modelo
            metrics = evaluate_model(model, df, horizon=horizon, parallel=parallel)
            
            if metrics and metrics['rmse'] < best_rmse:
                best_rmse = metrics['rmse']
                best_params = params
                print(f"Novo melhor RMSE: {best_rmse:.2f}")
                
        except Exception as e:
            print(f"Erro ao testar parâmetros {params}: {e}")
            continue
    
    return best_params