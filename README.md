# Inteo v3.0 Home Assistant Integration

Integração customizada do Home Assistant para dispositivos Inteo v3.0.

## 📋 Descrição

Esta integração permite controlar dispositivos Inteo (cortinas, persianas, etc.) através do Home Assistant usando autenticação OAuth2.

## 🚀 Instalação

### Método 1: HACS (Recomendado)
1. Instale o [HACS](https://hacs.xyz/)
2. Adicione este repositório como integração customizada
3. Procure por "Inteo" nas integrações
4. Instale e reinicie o Home Assistant

### Método 2: Manual
1. Baixe este repositório
2. Copie a pasta `custom_components/inteo` para `/config/custom_components/`
3. Reinicie o Home Assistant
4. Vá em **Configurações → Integrações → Adicionar Integração**
5. Procure por "Inteo" e configure

## ⚙️ Configuração

1. **Adicione a integração** via interface do Home Assistant
2. **Autentique-se** com sua conta Inteo via OAuth2
3. **Dispositivos serão descobertos** automaticamente

## 🔧 Funcionalidades

- ✅ **Autenticação OAuth2** segura
- ✅ **Descoberta automática** de dispositivos
- ✅ **Controle de cortinas/persianas**
- ✅ **Renovação automática** de tokens
- ✅ **Suporte a múltiplos dispositivos**

## 📱 Dispositivos Suportados

- Cortinas motorizadas
- Persianas
- Outros dispositivos Inteo v3.0

## 🛠️ Desenvolvimento

### Estrutura do Projeto
```
custom_components/inteo/
├── __init__.py          # Setup principal e OAuth2
├── config_flow.py       # Fluxo de configuração
├── manifest.json        # Metadados da integração
├── strings.json         # Traduções (PT-BR)
├── .translations/       # Traduções (EN)
├── const.py            # Constantes
└── cover.py            # Entidade cover
```

### Requisitos
- Home Assistant 2023.8+
- Python 3.9+

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🆘 Suporte

- **Issues**: [GitHub Issues](https://github.com/Somfy-Brasil/inteo_v3_ha/issues)
- **Documentação**: [Wiki](https://github.com/Somfy-Brasil/inteo_v3_ha/wiki)

## 📝 Changelog

### v0.1.0
- ✅ Implementação inicial
- ✅ OAuth2 authentication
- ✅ Cover entity support
- ✅ Automatic token renewal 