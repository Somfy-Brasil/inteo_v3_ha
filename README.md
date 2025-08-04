# Inteo v3.0 Home Assistant Integration

Integração customizada do Home Assistant para dispositivos Inteo v3.0.

**[🇺🇸 English version](README.en.md)**

## 📋 Descrição

Esta integração permite controlar dispositivos conectados ao **Hub Somfy InteO V3** através do Home Assistant usando autenticação OAuth2.

**⚠️ Importante:** Esta integração funciona exclusivamente com:
- **Hub Somfy InteO V3** (hardware)
- **App My Inteo 3.0** (necessário para configuração inicial dos dispositivos)
- **Dispositivos com protocolo RTS** (Radio Technology Somfy)

Os dispositivos (persianas, cortinas, etc.) devem ser configurados primeiro no app **My Inteo 3.0** antes de usar esta integração.

## 🚀 Instalação

### Método 1: HACS (Recomendado)
1. Instale o [HACS](https://hacs.xyz/)
2. Vá em **HACS → Integrações → Adicionar**
3. Clique nos 3 pontos no canto superior direito
4. Adicione este repositório: `Somfy-Brasil/inteo_v3_ha`
5. Procure por "My InteO 3.0" nas integrações
6. Clique em **Download**
7. **Reinicie o Home Assistant**
8. **Configure a integração** (veja seção "Configuração" abaixo)

### Método 2: Manual
1. Baixe este repositório
2. Copie a pasta `custom_components/inteo_v3` para `/config/custom_components/`
3. Reinicie o Home Assistant
4. Vá em **Configurações → Integrações → Adicionar Integração**
5. Procure por "My InteO 3.0" e configure

## ⚙️ Configuração

### Pré-requisitos
1. **Hub Somfy InteO V3** instalado e funcionando
2. **App My Inteo 3.0** instalado e dispositivos configurados
3. **Home Assistant 2025.1+** (para suporte PKCE)

### Configuração da Integração
**Após instalar via HACS ou manualmente:**

1. **Vá em Configurações → Dispositivos e Serviços**
2. **Clique em "Adicionar Integração"**
3. **Procure por "My InteO 3.0"**
4. **Clique na integração** para iniciar a configuração
5. **Autentique-se** com sua conta Inteo via OAuth2
6. **Dispositivos serão descobertos** automaticamente

### 🔧 Fluxo de Autenticação OAuth2
1. **Clique em "Configurar"** na integração
2. **Será redirecionado** para o site do Inteo
3. **Faça login** com suas credenciais
4. **Autorize** o acesso ao Home Assistant
5. **Retorne ao HA** - a configuração será finalizada automaticamente

## 🔧 Funcionalidades

- ✅ **Autenticação OAuth2 PKCE** segura (Home Assistant 2025.1+)
- ✅ **Descoberta automática** de dispositivos
- ✅ **Controle de cortinas/persianas**
- ✅ **Suporte a múltiplos dispositivos**

## 📱 Dispositivos Suportados

- Cortinas motorizadas
- Persianas
- Outros dispositivos compatíveis com o Hub Somfy InteO V3

**🔧 Protocolo:** Todos os dispositivos utilizam o **protocolo RTS** (Radio Technology Somfy).

**📱 Pré-requisito:** Todos os dispositivos devem ser configurados primeiro no app **My Inteo 3.0**.

## 🛠️ Desenvolvimento

### Estrutura do Projeto
```
custom_components/inteo_v3/
├── __init__.py          # Setup principal e OAuth2 PKCE
├── config_flow.py       # Fluxo de configuração
├── manifest.json        # Metadados da integração
├── strings.json         # Traduções (PT-BR)
├── .translations/       # Traduções (EN)
├── const.py            # Constantes
└── cover.py            # Entidade cover
```

### Requisitos
- Home Assistant 2025.1+ (para suporte PKCE)
- Python 3.9+

### ⚠️ Importante
Esta integração usa **OAuth2 PKCE** que só está disponível no Home Assistant 2025.1+. Se você estiver usando uma versão anterior, considere atualizar sua instalação do Home Assistant.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🆘 Suporte

- **Issues**: [GitHub Issues](https://github.com/Somfy-Brasil/inteo_v3_ha/issues)

## 📝 Changelog

### v0.1.0
- ✅ Implementação inicial
- ✅ OAuth2 authentication
- ✅ Cover entity support 