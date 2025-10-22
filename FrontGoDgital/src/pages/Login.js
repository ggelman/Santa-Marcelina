import { useMemo, useState } from "react"
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
  const [otp, setOtp] = useState("")
  const [erro, setErro] = useState("")
  const [carregando, setCarregando] = useState(false)
  const [mfaStep, setMfaStep] = useState("password")
  const [mfaSecret, setMfaSecret] = useState("")
  const [mfaUrl, setMfaUrl] = useState("")

  const { login } = useAuth()
  const navigate = useNavigate()

  const qrCodeUrl = useMemo(() => {
    if (!mfaUrl) return ""
    return `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(mfaUrl)}`
  }, [mfaUrl])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErro("")
    setCarregando(true)

    try {
      const resultado = await login(email, senha, mfaStep !== "password" ? otp : undefined)

      if (resultado.success) {
        setOtp("")
        setMfaStep("password")
        navigate("/")
        return
      }

      if (resultado.mfaSetupRequired) {
        setMfaStep("setup")
        setMfaSecret(resultado.secret || "")
        setMfaUrl(resultado.otpauthUrl || "")
        setOtp("")
        setErro("Finalize a configuração do autenticador e informe o código gerado.")
        return
      }

      if (resultado.mfaRequired) {
        setMfaStep("challenge")
        setOtp("")
        setErro("Informe o código de autenticação para continuar.")
        return
      }

      if (resultado.error) {
        setErro(resultado.error)
        if (resultado.error.toLowerCase().includes("mfa")) {
          setMfaStep("challenge")
        }
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

          {mfaStep !== "password" && (
            <Input
              type="text"
              placeholder="Código do autenticador"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              inputMode="numeric"
              pattern="[0-9]*"
              maxLength={6}
              required
            />
          )}

          <Button type="submit" disabled={carregando} style={{ backgroundColor: "#B8860B" }}>
            {carregando ? "Validando..." : mfaStep === "password" ? "Entrar" : "Confirmar"}
          </Button>
        </Form>

        {erro && <ErrorMessage>{erro}</ErrorMessage>}

        {mfaStep === "setup" && (
          <div style={{ marginTop: "20px" }}>
            <h4 style={{ color: "#B8860B", marginBottom: "10px" }}>Ative o Autenticador</h4>
            <p style={{ fontSize: "14px", color: "#555", marginBottom: "10px" }}>
              Escaneie o QR Code abaixo no aplicativo de autenticação ou insira o código manualmente.
            </p>
            {qrCodeUrl && (
              <img
                src={qrCodeUrl}
                alt="QR Code MFA"
                style={{ margin: "10px auto", display: "block", border: "1px solid #eee", borderRadius: "8px", padding: "8px", background: "white" }}
              />
            )}
            <p style={{ fontFamily: "monospace", fontSize: "16px", letterSpacing: "2px", color: "#333" }}>{mfaSecret}</p>
            <p style={{ fontSize: "13px", color: "#777" }}>Após cadastrar, informe o código de 6 dígitos no campo acima.</p>
          </div>
        )}

        <CredentialsInfo>
          <h4>🔐 Credenciais para Teste</h4>
          <div>
            <strong>Admin:</strong> <span>admin@padaria.com</span> / <span>admin123</span>
            <br />
            <small style={{ color: "#777" }}>Será solicitado um código MFA após o login.</small>
          </div>
        </CredentialsInfo>
      </LoginCard>
    </LoginContainer>
  )
}
