#!/usr/bin/env python3
"""
Script de Ingestão de Dados Simulados para V-Lab Fuel Monitor
Gera dados fictícios realistas e envia para a API via POST /ingest
"""

import requests
from faker import Faker
from random import choice, uniform, randint
from datetime import datetime, timedelta
import time

# Configurações
API_URL = "http://localhost:8000/ingest"
NUM_RECORDS = 100  # Número de registros a serem gerados

# Dados realistas para simulação
FUEL_TYPES = ["Gasolina", "Etanol", "Diesel S10"]
VEHICLE_TYPES = ["Carro", "Moto", "Caminhão Leve", "Carreta", "Ônibus"]

# Preços médios por tipo de combustível (R$ por litro)
FUEL_PRICES = {
    "Gasolina": (5.50, 6.50),
    "Etanol": (3.80, 4.80),
    "Diesel S10": (5.80, 6.80)
}

# Volumes típicos por tipo de veículo (litros)
VEHICLE_VOLUMES = {
    "Carro": (30, 60),
    "Moto": (10, 20),
    "Caminhão Leve": (80, 150),
    "Carreta": (300, 600),
    "Ônibus": (200, 400)
}

# Lista de postos fictícios
STATIONS = [
    {"store_id": "12345678000190", "store_name": "Posto Estrela", "city": "São Paulo", "state": "SP"},
    {"store_id": "98765432000111", "store_name": "Auto Posto BR", "city": "Rio de Janeiro", "state": "RJ"},
    {"store_id": "11223344000155", "store_name": "Posto Horizonte", "city": "Belo Horizonte", "state": "MG"},
    {"store_id": "55667788000199", "store_name": "Combustível Rápido", "city": "Curitiba", "state": "PR"},
    {"store_id": "99887766000122", "store_name": "Posto Atlântico", "city": "Salvador", "state": "BA"},
    {"store_id": "33445566000177", "store_name": "Auto Center", "city": "Brasília", "state": "DF"},
    {"store_id": "77889900000133", "store_name": "Posto Sul", "city": "Porto Alegre", "state": "RS"},
    {"store_id": "22334455000188", "store_name": "Combustível Norte", "city": "Manaus", "state": "AM"},
]

def generate_cpf():
    """Gera um CPF fictício (apenas números)"""
    return ''.join([str(randint(0, 9)) for _ in range(11)])

def generate_plate():
    """Gera uma placa de veículo fictícia"""
    fake = Faker('pt_BR')
    letters = ''.join([choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(3)])
    numbers = ''.join([str(randint(0, 9)) for _ in range(4)])
    return f"{letters}{numbers}"

def generate_fuel_collection():
    """Gera um registro de coleta de combustível fictício"""
    fake = Faker('pt_BR')
    
    # Seleciona dados aleatórios
    station = choice(STATIONS)
    fuel_type = choice(FUEL_TYPES)
    vehicle_type = choice(VEHICLE_TYPES)
    
    # Gera preço e volume baseado nos tipos selecionados
    price_range = FUEL_PRICES[fuel_type]
    sale_price = round(uniform(price_range[0], price_range[1]), 2)
    
    volume_range = VEHICLE_VOLUMES[vehicle_type]
    volume_sold = round(uniform(volume_range[0], volume_range[1]), 2)
    
    # Gera dados do motorista e veículo
    driver_name = fake.name()
    driver_cpf = generate_cpf()
    vehicle_plate = generate_plate()
    
    # Monta o payload
    data = {
        "store_id": station["store_id"],
        "store_name": station["store_name"],
        "city": station["city"],
        "state": station["state"],
        "fuel_type": fuel_type,
        "sale_price": sale_price,
        "volume_sold": volume_sold,
        "driver_name": driver_name,
        "driver_cpf": driver_cpf,
        "vehicle_plate": vehicle_plate,
        "vehicle_type": vehicle_type
    }
    
    return data

def main():
    """Função principal que executa a ingestão"""
    print(f"🚀 Iniciando ingestão de {NUM_RECORDS} registros...")
    print(f"📡 Endpoint: {API_URL}\n")
    
    success_count = 0
    error_count = 0
    
    for i in range(NUM_RECORDS):
        try:
            # Gera os dados
            data = generate_fuel_collection()
            
            # Envia para a API
            response = requests.post(API_URL, json=data, timeout=5)
            
            if response.status_code == 201:
                success_count += 1
                print(f"✅ [{i+1}/{NUM_RECORDS}] Registro inserido: {data['driver_name']} | {data['fuel_type']} | {data['city']}")
            else:
                error_count += 1
                print(f"❌ [{i+1}/{NUM_RECORDS}] Erro {response.status_code}: {response.text[:100]}")
        
        except requests.exceptions.RequestException as e:
            error_count += 1
            print(f"❌ [{i+1}/{NUM_RECORDS}] Erro de conexão: {str(e)[:100]}")
        
        # Pequeno delay para não sobrecarregar a API
        time.sleep(0.1)
    
    # Resumo final
    print(f"\n{'='*60}")
    print(f"📊 RESUMO DA INGESTÃO")
    print(f"{'='*60}")
    print(f"✅ Sucessos: {success_count}")
    print(f"❌ Erros: {error_count}")
    print(f"📈 Total: {NUM_RECORDS}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
