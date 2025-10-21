import { useState } from "react"
import { useNavigate } from "react-router-dom"
import styled from "styled-components"
import { useAuth } from "../context/AuthContext"
import { Button } from "../components/Button"
import { Input } from "../components/Input"
import { Card } from "../components/Card"

const LoginContainer = styled.div`
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #FDFBF7 0%, #F5F1E8 100%);
  padding: 20px;
`

const LoginCard = styled(Card)`
  width: 100%;
  max-width: 400px;
  padding: 40px;
  text-align: center;
`

const Logo = styled.div`
  margin-bottom: 30px;
  
  img {
    width: 100px;
    height: 100px;
    margin-bottom: 20px;
    object-fit: contain;
  }
  
  h1 {
    color: #B8860B;
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 8px;
  }
  
  p {
    color: #666;
    font-size: 14px;
    font-style: italic;
  }
`

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
`

const ErrorMessage = styled.div`
  color: #dc3545;
  font-size: 14px;
  margin-top: 10px;
  padding: 10px;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
`

const CredentialsInfo = styled.div`
  margin-top: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #B8860B;
  
  h4 {
    color: #B8860B;
    margin-bottom: 15px;
    font-size: 16px;
  }
  
  div {
    margin-bottom: 10px;
    font-size: 14px;
    
    strong {
      color: #333;
    }
    
    span {
      color: #666;
      font-family: monospace;
    }
  }
`

export const Login = () => {
  const [email, setEmail] = useState("")
  const [senha, setSenha] = useState("")
  const [erro, setErro] = useState("")
  const [carregando, setCarregando] = useState(false)

  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErro("")
    setCarregando(true)

    try {
      const sucesso = await login(email, senha)
      if (sucesso) {
        navigate("/")
      } else {
        setErro("Email ou senha inválidos")
      }
    } catch (error) {
      setErro("Erro ao fazer login. Tente novamente.")
    } finally {
      setCarregando(false)
    }
  }

  return (
    <LoginContainer>
      <LoginCard>
        <Logo>
          <img a alt="Image"lt="Image"
            src="/images/logo-santa-marcelina.png"
            alt="Logo Padaria Santa Marcelina"
            onError={(e) => {
              e.target.style.display = "none"
              e.target.nextSibling.style.display = "flex"
            }}
          />
          <div
            style={{
              width: "100px",
              height: "100px",
              backgroundColor: "#B8860B",
              borderRadius: "50%",
              margin: "0 auto 20px",
              display: "none",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "40px",
              color: "white",
            }}
          >
            🥖
          </div>
          <h1>Padaria Santa Marcelina</h1>
          <p>Sistema de Gestão - Desde 1978</p>
        </Logo>

        <Form onSubmit={handleSubmit}>
          <Input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />

          <Input
            type="password"
            placeholder="Senha"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            required
          />

          <Button type="submit" disabled={carregando} style={{ backgroundColor: "#B8860B" }}>
            {carregando ? "Entrando..." : "Entrar"}
          </Button>
        </Form>

        {erro && <ErrorMessage>{erro}</ErrorMessage>}

        <CredentialsInfo>
          <h4>🔐 Credenciais para Teste</h4>
          <div>
            <strong>Admin:</strong> <span>admin@padaria.com</span> / <span>admin123</span>
          </div>
        </CredentialsInfo>
      </LoginCard>
    </LoginContainer>
  )
}
