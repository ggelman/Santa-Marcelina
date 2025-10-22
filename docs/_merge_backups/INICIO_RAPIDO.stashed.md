# ÔÜí IN├ìCIO R├üPIDO - 5 Minutos

> Como rodar o sistema completo em **5 minutos**

---

## ­ƒÜÇ EXECU├ç├âO AUTOM├üTICA

### 1´©ÅÔâú **Abrir Terminal**
```batch
cd C:\projects\FIAP\Fase7\Santa-Marcelina
```

### 2´©ÅÔâú **Executar Script**
```batch
.\start_all_services_correto.bat
```

### 3´©ÅÔâú **Aguardar Inicializa├º├úo**
- ÔÅ│ AI Service (30s)
- ÔÅ│ Backend (60s) 
- ÔÅ│ Frontend (30s)

### 4´©ÅÔâú **Acessar Sistema**
- ­ƒîÉ **URL:** http://localhost:3000
- ­ƒæñ **Login:** admin@padaria.com
- ­ƒöæ **Senha:** admin123

---

## Ô£à VERIFICA├ç├âO R├üPIDA

### ­ƒöì **Portas Ativas**
```batch
netstat -an | findstr ":3000 :8443 :5443"
```

**Resultado esperado:**
```
:3000  Ô£à Frontend
:8443  Ô£à Backend HTTPS  
:5443  Ô£à AI Service
```

### ­ƒº¬ **Teste Funcional**
1. **Login** ÔåÆ Dashboard carrega
2. **Menu lateral** ÔåÆ Todas op├º├Áes vis├¡veis
3. **Monitor de Seguran├ºa** ÔåÆ Status verde
4. **Nova Venda** ÔåÆ Formul├írio funciona

---

## ÔØî PROBLEMAS COMUNS

| Erro | Solu├º├úo |
|------|---------|
| `Erro: Diret├│rio n├úo encontrado` | Verifique se est├í na pasta correta: `C:\projects\FIAP\` |
| `Porta j├í em uso` | Execute: `stop_all_services.bat` |
| `Status Desconhecido` | Aguarde 2 minutos ou aceite certificado SSL |
| `Login falha` | Verifique se backend est├í rodando (porta 8443) |

---

## ­ƒøæ PARAR SISTEMA

```batch
.\stop_all_services.bat
```

ou **Ctrl+C** em cada terminal

---

## ­ƒôÜ PR├ôXIMOS PASSOS

- ­ƒôû **README.md** ÔåÆ Vis├úo geral completa
- ­ƒº¬ **CHECKLIST_TESTE.md** ÔåÆ Valida├º├úo completa
- ­ƒöº **SOLUCAO_PROBLEMAS.md** ÔåÆ Problemas espec├¡ficos

---

**ÔÅ▒´©Å Tempo total: ~5 minutos | ­ƒÄ» Taxa de sucesso: 95%**
