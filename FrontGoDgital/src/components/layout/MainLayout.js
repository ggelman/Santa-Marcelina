import styled from "styled-components"
import { useAuth } from "../../context/AuthContext"
import { usePermissions } from "../../hooks/usePermissions"
import { useNavigate, useLocation } from "react-router-dom"
import { useSecurityAlerts } from "../security/SecurityAlertsProvider"
import { QuickAccessPortal } from "./QuickAccessPortal"
import PropTypes from "prop-types"

const LayoutContainer = styled.div`
  display: flex;
  min-height: 100vh;
`

const Sidebar = styled.aside`
  width: 280px;
  min-width: 280px;
  background-color: ${(props) => props.theme.colors.white};
  box-shadow: 2px 0 4px rgba(0,0,0,0.05);
  padding: 20px 0;
`

const Logo = styled.div`
  padding: 0 20px 30px;
  text-align: center;
  border-bottom: 1px solid ${(props) => props.theme.colors.border};
  margin-bottom: 30px;
  
  img {
    width: 80px;
    height: 80px;
    margin-bottom: 15px;
    object-fit: contain;
  }
  
  h3 {
    color: #B8860B;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 5px;
  }
  
  p {
    color: ${(props) => props.theme.colors.textPrimary};
    font-size: 12px;
    margin-top: 5px;
    font-style: italic;
  }
`

const NavMenu = styled.nav`
  padding: 0 20px;
`

const NavItem = styled.div`
  margin-bottom: 8px;
  
  a {
    display: block;
    padding: 12px 16px;
    color: ${(props) => props.theme.colors.textPrimary};
    text-decoration: none;
    border-radius: 8px;
    transition: all 0.2s ease;
    font-weight: 500;
    
    &:hover, &.active {
      background-color: #B8860B;
      color: white;
    }
  }
`

const MainContent = styled.main`
  flex: 1;
  display: flex;
  flex-direction: column;
`

const Header = styled.header`
  background-color: ${(props) => props.theme.colors.white};
  padding: 16px 24px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
`

const UserInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
  
  span {
    font-weight: 600;
    color: ${(props) => props.theme.colors.textPrimary};
  }
`

const UserProfile = styled.span`
  background-color: #B8860B;
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
`

const LogoutButton = styled.button`
  background: none;
  color: ${(props) => props.theme.colors.danger};
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 6px;
  transition: background-color 0.2s ease;
  
  &:hover {
    background-color: rgba(220, 53, 69, 0.1);
  }
`

const ContentArea = styled.div`
  flex: 1;
  padding: 24px;
  overflow-y: auto;
`

export const MainLayout = ({ children }) => {
  const { user, logout } = useAuth()
  const { canAccess, userProfile } = usePermissions()
  const { alerts } = useSecurityAlerts()
  const navigate = useNavigate()
  const location = useLocation()

  // Contar alertas não lidos
  const unreadAlertsCount = alerts.filter(alert => !alert.read).length

  const handleLogout = () => {
    logout()
    navigate("/login")
  }

  const allMenuItems = [
    { path: "/", label: "Dashboard", icon: "🏠", permission: null },
    { path: "/financeiro", label: "Dashboard Financeiro", icon: "💰", permission: "relatorios" },
    { path: "/auditoria", label: "Dashboard Auditoria", icon: "🔍", permission: "auditoria" },
    { path: "/vendas/nova", label: "Nova Venda", icon: "🛒", permission: "vendas" },
    { path: "/vendas/historico", label: "Histórico de Vendas", icon: "📋", permission: "vendas" },
    { path: "/produtos/novo", label: "Cadastrar Produto", icon: "📦", permission: "produtos" },
    { path: "/produtos/categorias", label: "Categorias", icon: "🏷️", permission: "produtos" },
    { path: "/clientes/novo", label: "Cadastrar Cliente", icon: "👥", permission: "clientes" },
    { path: "/clientes", label: "Gestão de Clientes", icon: "⭐", permission: "clientes" },
    { path: "/estoque", label: "Gestão de Estoque", icon: "📊", permission: "estoque" },
    { path: "/usuarios", label: "Usuários", icon: "👤", permission: "usuarios" },
    { path: "/backup", label: "Sistema de Backup", icon: "💾", permission: "backup" },
    { path: "/relatorios", label: "Relatórios", icon: "📈", permission: "relatorios" },
    {
      path: "/security",
      label: "Monitor de Segurança",
      icon: "🔒",
      permission: "administrador",
      badge: unreadAlertsCount > 0 ? unreadAlertsCount : 0
    },
    { path: "/ia/previsao", label: "Previsão IA", icon: "🤖", permission: "administrador" },
    { path: "/ia/chat", label: "Chat com IA", icon: "💬", permission: "administrador" },
  ]

  const menuItems = allMenuItems.filter((item) => {
    if (!item.permission) return true
    
    // Para itens específicos de admin, verificar se é administrador
    if (item.permission === "administrador") {
      return userProfile === "administrador"
    }
    
    // Para dashboard de auditoria - apenas admin e gerente
    if (item.permission === "auditoria") {
      return userProfile === "administrador" || userProfile === "gerente"
    }
    
    // Para outros itens, usar canAccess normal
    return canAccess(item.path)
  })

  const getProfileDisplayName = (profile) => {
    switch (profile) {
      case "administrador":
        return "Admin"
      case "gerente":
        return "Gerente"
      case "funcionario":
        return "Funcionário"
      default:
        return "Usuário"
    }
  }

  return (
    <LayoutContainer>
      <Sidebar>
        <Logo>
          <img 
            src="/images/logo-santa-marcelina.png"
            alt="Logo Padaria Santa Marcelina"
            onError={(e) => {
              e.target.style.display = "none"
              e.target.nextSibling.style.display = "flex"
            }}
          />
          <div
            style={{
              width: "80px",
              height: "80px",
              backgroundColor: "#B8860B",
              borderRadius: "50%",
              margin: "0 auto 15px",
              display: "none",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "32px",
              color: "white",
            }}
          >
            🥖
          </div>
          <h3>Padaria Santa Marcelina</h3>
          <p>Desde 1978</p>
        </Logo>

        <NavMenu>
          {menuItems.map((item) => (
            <NavItem key={item.path}>
              <a
                href={item.path}
                className={location.pathname === item.path ? "active" : ""}
                onClick={(e) => {
                  e.preventDefault()
                  navigate(item.path)
                }}
                style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
              >
                <div>
                  {item.icon} {item.label}
                </div>
                {item.badge > 0 && (
                  <span style={{
                    backgroundColor: "#dc3545",
                    color: "white",
                    borderRadius: "12px",
                    padding: "2px 8px",
                    fontSize: "12px",
                    fontWeight: "500",
                    display: "inline-block",
                    lineHeight: "1",
                  }}>
                    {item.badge}
                  </span>
                )}
              </a>
            </NavItem>
          ))}
        </NavMenu>
      </Sidebar>

      <MainContent>
        <Header>
          <h1 style={{ color: "#3D2C21", fontSize: "20px" }}>Sistema de Gestão</h1>
          <UserInfo>
            <UserProfile>{getProfileDisplayName(userProfile)}</UserProfile>
            <span>Olá, {user?.nome}</span>
            <LogoutButton onClick={handleLogout}>Sair</LogoutButton>
          </UserInfo>
        </Header>

        <ContentArea>{children}</ContentArea>
        
        {/* Botão de acesso rápido ao portal do cliente */}
        <QuickAccessPortal />
      </MainContent>
    </LayoutContainer>
  )
}

MainLayout.propTypes = {
  children: PropTypes.node,
}