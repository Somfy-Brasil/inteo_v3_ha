# Inteo v3.0 Home Assistant Integration

Integração customizada do Home Assistant para dispositivos Inteo v3.0.

## 📋 Descrição

Esta integração permite controlar dispositivos conectados ao **Hub Somfy InteO V3** através do Home Assistant usando autenticação OAuth2.

**⚠️ Importante:** Esta integração funciona exclusivamente com:
- **Hub Somfy InteO V3** (hardware)
- **App My Inteo 3.0** (necessário para configuração inicial dos dispositivos)

Os dispositivos (persianas, cortinas, etc.) devem ser configurados primeiro no app **My Inteo 3.0** antes de usar esta integração.

## 🚀 Instalação

### Método 1: HACS (Recomendado)
1. Instale o [HACS](https://hacs.xyz/)
2. Vá em **HACS → Integrações → Adicionar**
3. Clique nos 3 pontos no canto superior direito
4. Adicione este repositório: `Somfy-Brasil/inteo_v3_ha`
5. Procure por "My InteO 3.0" nas integrações
6. Clique em **Download**
7. Reinicie o Home Assistant

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
1. **Adicione a integração** via interface do Home Assistant
2. **Autentique-se** com sua conta Inteo via OAuth2
3. **Dispositivos serão descobertos** automaticamente

## 🔧 Funcionalidades

- ✅ **Autenticação OAuth2 PKCE** segura (Home Assistant 2025.1+)
- ✅ **Descoberta automática** de dispositivos
- ✅ **Controle de cortinas/persianas**
- ✅ **Renovação automática** de tokens
- ✅ **Suporte a múltiplos dispositivos**

## 📱 Dispositivos Suportados

- Cortinas motorizadas
- Persianas
- Outros dispositivos compatíveis com o Hub Somfy InteO V3

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
Esta integração usa **OAuth2 PKCE** que só está disponível no Home Assistant 2025.1+. Se você estiver usando uma versão anterior, considere atualizar ou usar uma versão alternativa da integração.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🆘 Suporte

- **Issues**: [GitHub Issues](https://github.com/Somfy-Brasil/inteo_v3_ha/issues)

## 📝 Changelog

### v0.1.0
- ✅ Implementação inicial
- ✅ OAuth2 authentication
- ✅ Cover entity support
- ✅ Automatic token renewal 