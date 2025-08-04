# Inteo v3.0 Home Assistant Integration

Custom Home Assistant integration for Inteo v3.0 devices.

**[🇧🇷 Versão em português](README.md)**

## 📋 Description

This integration allows you to control devices connected to the **Somfy InteO V3 Hub** through Home Assistant using OAuth2 authentication.

**⚠️ Important:** This integration works exclusively with:
- **Somfy InteO V3 Hub** (hardware)
- **My Inteo 3.0 App** (required for initial device configuration)
- **RTS protocol devices** (Radio Technology Somfy)

Devices (blinds, curtains, etc.) must be configured first in the **My Inteo 3.0 App** before using this integration.

## 🚀 Installation

### Method 1: HACS (Recommended)
1. Install [HACS](https://hacs.xyz/)
2. Go to **HACS → Integrations → Add**
3. Click the 3 dots in the top right corner
4. Add this repository: `Somfy-Brasil/inteo_v3_ha`
5. Search for "My InteO 3.0" in integrations
6. Click **Download**
7. **Restart Home Assistant**
8. **Configure the integration** (see "Configuration" section below)

### Method 2: Manual
1. Download this repository
2. Copy the `custom_components/inteo_v3` folder to `/config/custom_components/`
3. Restart Home Assistant
4. Go to **Settings → Devices & Services → Add Integration**
5. Search for "My InteO 3.0" and configure

## ⚙️ Configuration

### Prerequisites
1. **Somfy InteO V3 Hub** installed and working
2. **My Inteo 3.0 App** installed and devices configured
3. **Home Assistant 2025.1+** (for PKCE support)

### Integration Setup
**After installing via HACS or manually:**

1. **Go to Settings → Devices & Services**
2. **Click "Add Integration"**
3. **Search for "My InteO 3.0"**
4. **Click on the integration** to start configuration
5. **Authenticate** with your Inteo account via OAuth2
6. **Devices will be discovered** automatically

### 🔧 OAuth2 Authentication Flow
1. **Click "Configure"** on the integration
2. **You'll be redirected** to the Inteo website
3. **Login** with your credentials
4. **Authorize** access to Home Assistant
5. **Return to HA** - configuration will be completed automatically

## 🔧 Features

- ✅ **Secure OAuth2 PKCE authentication** (Home Assistant 2025.1+)
- ✅ **Automatic device discovery**
- ✅ **Blind/curtain control**
- ✅ **Multiple device support**

## 📱 Supported Devices

- Motorized curtains
- Blinds
- Other devices compatible with Somfy InteO V3 Hub

**🔧 Protocol:** All devices use the **RTS protocol** (Radio Technology Somfy).

**📱 Prerequisite:** All devices must be configured first in the **My Inteo 3.0 App**.

## 🛠️ Development

### Project Structure
```
custom_components/inteo_v3/
├── __init__.py          # Main setup and OAuth2 PKCE
├── config_flow.py       # Configuration flow
├── manifest.json        # Integration metadata
├── strings.json         # Translations (PT-BR)
├── .translations/       # Translations (EN)
├── const.py            # Constants
└── cover.py            # Cover entity
```

### Requirements
- Home Assistant 2025.1+ (for PKCE support)
- Python 3.9+

### ⚠️ Important
This integration uses **OAuth2 PKCE** which is only available in Home Assistant 2025.1+. If you're using an earlier version, consider updating or using an alternative version of the integration.

## 📄 License

This project is under MIT License. See the [LICENSE](LICENSE) file for more details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/Somfy-Brasil/inteo_v3_ha/issues)

## 📝 Changelog

### v0.1.0
- ✅ Initial implementation
- ✅ OAuth2 PKCE authentication
- ✅ Cover entity support 