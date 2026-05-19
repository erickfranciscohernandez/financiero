#!/usr/bin/env python3
"""
Fetch live economic data - FASE 4
Indicadores macro, commodities, y mercados en tiempo real
"""
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Configuración de APIs
CONFIG = {
    'alpha_vantage_key': 'demo',  # Cambiar a tu API key desde alphavantage.co
    'fred_key': 'demo',            # Cambiar a tu API key desde stlouisfed.org
    'use_mock': True               # Usar datos mock si las APIs fallan
}

class LiveDataFetcher:
    """Obtiene datos económicos en vivo"""

    def __init__(self):
        self.alpha_url = "https://www.alphavantage.co/query"
        self.fred_url = "https://api.stlouisfed.org/fred/series/observations"
        self.cache_file = 'live_data_cache.json'
        self.cache = self._load_cache()

    def _load_cache(self):
        """Cargar datos cacheados"""
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def _save_cache(self):
        """Guardar cache"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  Error guardando cache: {e}")

    def get_usd_clp(self) -> Optional[Dict]:
        """USD/CLP tipo de cambio (Alpha Vantage)"""
        try:
            print("📊 Buscando USD/CLP...")

            params = {
                'function': 'CURRENCY_EXCHANGE_RATE',
                'from_currency': 'USD',
                'to_currency': 'CLP',
                'apikey': CONFIG['alpha_vantage_key']
            }

            response = requests.get(self.alpha_url, params=params, timeout=5)
            data = response.json()

            if 'Realtime Currency Exchange Rate' in data:
                rate = data['Realtime Currency Exchange Rate']
                result = {
                    'tipo': 'USD/CLP',
                    'precio': float(rate['5. Exchange Rate']),
                    'fecha': datetime.now().isoformat(),
                    'cambio': float(rate['8. Bid Price']) - float(rate['9. Ask Price'])
                }
                self.cache['usd_clp'] = result
                self._save_cache()
                return result
        except Exception as e:
            print(f"⚠️  Error USD/CLP: {e}")

        # Fallback a datos mock
        return self._get_mock_usd_clp()

    def get_inflation_rate(self) -> Optional[Dict]:
        """Tasa de inflación (FRED)"""
        try:
            print("📈 Buscando tasa de inflación...")

            # CPIAUCSL = Consumer Price Index
            params = {
                'series_id': 'CPIAUCSL',
                'api_key': CONFIG['fred_key'],
                'limit': 12,
                'sort_order': 'desc',
                'units': 'pch'  # Cambio porcentual
            }

            response = requests.get(self.fred_url, params=params, timeout=5)
            data = response.json()

            if 'observations' in data and len(data['observations']) > 0:
                obs = data['observations'][0]
                result = {
                    'tipo': 'Inflación Anual (CPI)',
                    'porcentaje': float(obs['value']) if obs['value'] != '.' else 0,
                    'fecha': obs['date'],
                    'fuente': 'Federal Reserve FRED'
                }
                self.cache['inflacion'] = result
                self._save_cache()
                return result
        except Exception as e:
            print(f"⚠️  Error inflación: {e}")

        return self._get_mock_inflation()

    def get_fed_rate(self) -> Optional[Dict]:
        """Tasa de fondos federales"""
        try:
            print("🏦 Buscando tasa Fed...")

            # FEDFUNDS = Federal Funds Effective Rate
            params = {
                'series_id': 'FEDFUNDS',
                'api_key': CONFIG['fred_key'],
                'limit': 1,
                'sort_order': 'desc'
            }

            response = requests.get(self.fred_url, params=params, timeout=5)
            data = response.json()

            if 'observations' in data and len(data['observations']) > 0:
                obs = data['observations'][0]
                result = {
                    'tipo': 'Tasa de fondos Fed',
                    'porcentaje': float(obs['value']) if obs['value'] != '.' else 0,
                    'fecha': obs['date'],
                    'fuente': 'Federal Reserve'
                }
                self.cache['fed_rate'] = result
                self._save_cache()
                return result
        except Exception as e:
            print(f"⚠️  Error Fed rate: {e}")

        return self._get_mock_fed_rate()

    def get_copper_price(self) -> Optional[Dict]:
        """Precio del cobre (Alpha Vantage)"""
        try:
            print("🔴 Buscando precio del cobre...")

            params = {
                'function': 'CURRENCY_EXCHANGE_RATE',
                'from_currency': 'HG',  # Copper futures
                'to_currency': 'USD',
                'apikey': CONFIG['alpha_vantage_key']
            }

            response = requests.get(self.alpha_url, params=params, timeout=5)
            data = response.json()

            if 'Realtime Currency Exchange Rate' in data:
                rate = data['Realtime Currency Exchange Rate']
                result = {
                    'tipo': 'Cobre (USD/lb)',
                    'precio': float(rate['5. Exchange Rate']),
                    'fecha': datetime.now().isoformat()
                }
                self.cache['copper'] = result
                self._save_cache()
                return result
        except Exception as e:
            print(f"⚠️  Error cobre: {e}")

        return self._get_mock_copper()

    def get_sp500(self) -> Optional[Dict]:
        """Índice S&P 500"""
        try:
            print("📊 Buscando S&P 500...")

            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': '^GSPC',
                'apikey': CONFIG['alpha_vantage_key']
            }

            response = requests.get(self.alpha_url, params=params, timeout=5)
            data = response.json()

            if 'Global Quote' in data and '05. price' in data['Global Quote']:
                quote = data['Global Quote']
                result = {
                    'tipo': 'S&P 500',
                    'precio': float(quote['05. price']),
                    'cambio': float(quote['09. change']) if quote['09. change'] != 'N/A' else 0,
                    'fecha': datetime.now().isoformat()
                }
                self.cache['sp500'] = result
                self._save_cache()
                return result
        except Exception as e:
            print(f"⚠️  Error S&P 500: {e}")

        return self._get_mock_sp500()

    # Mock data para fallback
    def _get_mock_usd_clp(self) -> Dict:
        """Mock USD/CLP"""
        precio_base = 825
        variacion = precio_base * 0.02
        return {
            'tipo': 'USD/CLP (simulado)',
            'precio': precio_base + (variacion if datetime.now().day % 2 else -variacion),
            'fecha': datetime.now().isoformat(),
            'cambio': variacion,
            'mock': True
        }

    def _get_mock_inflation(self) -> Dict:
        """Mock inflación"""
        return {
            'tipo': 'Inflación Anual (simulada)',
            'porcentaje': 3.2,
            'fecha': (datetime.now() - timedelta(days=1)).isoformat(),
            'fuente': 'Simulado',
            'mock': True
        }

    def _get_mock_fed_rate(self) -> Dict:
        """Mock Fed rate"""
        return {
            'tipo': 'Tasa de fondos Fed (simulada)',
            'porcentaje': 4.50,
            'fecha': (datetime.now() - timedelta(days=1)).isoformat(),
            'fuente': 'Simulado',
            'mock': True
        }

    def _get_mock_copper(self) -> Dict:
        """Mock cobre"""
        return {
            'tipo': 'Cobre (simulado USD/lb)',
            'precio': 4.12,
            'fecha': datetime.now().isoformat(),
            'mock': True
        }

    def _get_mock_sp500(self) -> Dict:
        """Mock S&P 500"""
        return {
            'tipo': 'S&P 500 (simulado)',
            'precio': 5243.88,
            'cambio': 12.5,
            'fecha': datetime.now().isoformat(),
            'mock': True
        }

    def get_all_indicators(self) -> Dict:
        """Obtener todos los indicadores"""
        print("\n📊 FETCH LIVE DATA - FASE 4\n")

        indicators = {
            'fecha': datetime.now().isoformat(),
            'version': 'v4',
            'datos': {
                'usd_clp': self.get_usd_clp(),
                'inflacion': self.get_inflation_rate(),
                'fed_rate': self.get_fed_rate(),
                'cobre': self.get_copper_price(),
                'sp500': self.get_sp500()
            }
        }

        # Guardar en JSON
        with open('live_indicators.json', 'w', encoding='utf-8') as f:
            json.dump(indicators, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Indicadores guardados: live_indicators.json\n")
        return indicators


def generate_chart_data(indicators: Dict) -> Dict:
    """Generar datos para gráficos Chart.js"""

    data = {
        'usd_clp': {
            'label': 'USD/CLP',
            'value': indicators['datos']['usd_clp']['precio'],
            'status': 'up' if indicators['datos']['usd_clp']['cambio'] > 0 else 'down'
        },
        'inflacion': {
            'label': 'Inflación Anual (%)',
            'value': indicators['datos']['inflacion']['porcentaje'],
            'status': 'critical' if indicators['datos']['inflacion']['porcentaje'] > 4 else 'normal'
        },
        'fed_rate': {
            'label': 'Tasa Fed (%)',
            'value': indicators['datos']['fed_rate']['porcentaje'],
            'status': 'normal'
        },
        'cobre': {
            'label': 'Cobre (USD/lb)',
            'value': indicators['datos']['cobre']['precio'],
            'status': 'normal'
        },
        'sp500': {
            'label': 'S&P 500',
            'value': indicators['datos']['sp500']['precio'],
            'cambio': indicators['datos']['sp500']['cambio'],
            'status': 'up' if indicators['datos']['sp500']['cambio'] > 0 else 'down'
        }
    }

    return data


def main():
    fetcher = LiveDataFetcher()
    indicators = fetcher.get_all_indicators()

    # Mostrar resultados
    print("="*60)
    print("📊 INDICADORES MACRO EN VIVO")
    print("="*60)

    for key, value in indicators['datos'].items():
        if value:
            print(f"\n{value['tipo']}:")
            if 'precio' in value:
                print(f"  💰 Precio: {value['precio']}")
            if 'porcentaje' in value:
                print(f"  📈 Valor: {value['porcentaje']}%")
            if 'cambio' in value:
                print(f"  📊 Cambio: {value['cambio']}")
            if 'mock' in value:
                print(f"  ⚠️  (Datos simulados)")

    print("\n✅ Datos guardados en live_indicators.json")
    print("="*60)


if __name__ == '__main__':
    main()
