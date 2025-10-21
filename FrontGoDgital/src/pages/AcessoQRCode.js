import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import styled from 'styled-components';
import { FiSquare, FiUsers, FiShoppingBag, FiCreditCard, FiShield, FiArrowRight } from 'react-icons/fi';

// Estilos Principais
const AcessoContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
`;

const AcessoCard = styled.div`
  background: white;
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  max-width: 480px;
  width: 100%;
  padding: 40px;
  text-align: center;
`;

const LogoPadaria = styled.div`
  margin-bottom: 30px;
  
  h1 {
    color: #2c3e50;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    margin-bottom: 8px;
  }
  
  p {
    color: #7f8c8d;
    font-size: 1rem;
    margin: 0;
  }
`;

const BemVindo = styled.div`
  margin-bottom: 40px;
  
  h2 {
    color: #2c3e50;
    font-size: 1.8rem;
    margin-bottom: 12px;
  }
  
  p {
    color: #7f8c8d;
    font-size: 1.1rem;
    line-height: 1.6;
  }
`;

const QRIcon = styled.div`
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
  
  svg {
    color: white;
    font-size: 40px;
  }
`;

const OpcoesMenu = styled.div`
  display: grid;
  gap: 16px;
  margin-bottom: 32px;
`;

const OpcaoItem = styled.button`
  background: #f8f9fa;
  border: 2px solid #e9ecef;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  
  &:hover {
    border-color: #667eea;
    background: #f0f4ff;
    transform: translateY(-2px);
  }
  
  .icon {
    background: #667eea;
    color: white;
    border-radius: 50%;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
  }
  
  .content {
    flex: 1;
    margin: 0 16px;
    
    h3 {
      color: #2c3e50;
      font-size: 1.1rem;
      font-weight: 600;
      margin: 0 0 4px 0;
    }
    
    p {
      color: #7f8c8d;
      font-size: 0.9rem;
      margin: 0;
    }
  }
  
  .arrow {
    color: #667eea;
    font-size: 20px;
  }
`;

const MesaInfo = styled.div`
  background: #e3f2fd;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 24px;
  
  .mesa-numero {
    color: #1976d2;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 4px;
  }
  
  .mesa-descricao {
    color: #1976d2;
    font-size: 0.9rem;
  }
`;

const DisclaimerLGPD = styled.div`
  background: #f8f9fa;
  border-left: 4px solid #667eea;
  border-radius: 8px;
  padding: 16px;
  margin-top: 24px;
  text-align: left;
  
  .titulo {
    color: #2c3e50;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .texto {
    color: #7f8c8d;
    font-size: 0.8rem;
    line-height: 1.5;
  }
`;

const AcessoQRCode = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [mesaInfo, setMesaInfo] = useState(null);

  useEffect(() => {
    // Captura parâmetros do QR Code
    const mesa = searchParams.get('mesa');
    const area = searchParams.get('area');
    const codigo = searchParams.get('codigo');

    if (mesa) {
      setMesaInfo({
        numero: mesa,
        area: area || 'Salão Principal',
        codigo: codigo
      });
    }
  }, [searchParams]);

  const opcoesCliente = [
    {
      icon: FiUsers,
      titulo: 'Fazer Pedido',
      descricao: 'Cadastre-se e faça seu pedido',
      acao: () => navigate('/cliente/cadastro' + (mesaInfo ? `?mesa=${mesaInfo.numero}&area=${mesaInfo.area}` : '')),
      destaque: true
    },
    {
      icon: FiShoppingBag,
      titulo: 'Ver Cardápio',
      descricao: 'Explore nossos produtos',
      acao: () => navigate('/cliente/cardapio')
    },
    {
      icon: FiShield,
      titulo: 'Seus Direitos LGPD',
      descricao: 'Gerencie seus dados pessoais',
      acao: () => navigate('/cliente/direitos-lgpd')
    }
  ];

  return (
    <AcessoContainer>
      <AcessoCard>
        <LogoPadaria>
          <h1>🥖 Santa Marcelina</h1>
          <p>Panificadora & Confeitaria</p>
        </LogoPadaria>

        <QRIcon>
          <FiSquare />
        </QRIcon>

        <BemVindo>
          <h2>Bem-vindo!</h2>
          <p>
            Acesse nosso sistema digital para fazer pedidos, 
            visualizar o cardápio e gerenciar seus dados.
          </p>
        </BemVindo>

        {mesaInfo && (
          <MesaInfo>
            <div className="mesa-numero">Mesa {mesaInfo.numero}</div>
            <div className="mesa-descricao">{mesaInfo.area}</div>
          </MesaInfo>
        )}

        <OpcoesMenu>
          {opcoesCliente.map((opcao, index) => (
            <OpcaoItem key={index} onClick={opcao.acao}>
              <div className="icon">
                <opcao.icon />
              </div>
              <div className="content">
                <h3>{opcao.titulo}</h3>
                <p>{opcao.descricao}</p>
              </div>
              <div className="arrow">
                <FiArrowRight />
              </div>
            </OpcaoItem>
          ))}
        </OpcoesMenu>

        <DisclaimerLGPD>
          <div className="titulo">
            <FiShield size={16} />
            Proteção de Dados (LGPD)
          </div>
          <div className="texto">
            Seus dados pessoais são protegidos conforme a Lei Geral de Proteção 
            de Dados. Você pode gerenciar suas informações e consentimentos 
            a qualquer momento através do portal de direitos.
          </div>
        </DisclaimerLGPD>
      </AcessoCard>
    </AcessoContainer>
  );
};

export default AcessoQRCode;