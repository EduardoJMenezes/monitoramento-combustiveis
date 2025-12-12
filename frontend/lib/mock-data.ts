import type { FuelCollection, CollectionsResponse, AvgPriceByFuel, VolumeByVehicle, DriverReport } from "@/types/fuel"

const MOCK_COLLECTIONS: FuelCollection[] = [
  {
    id: 1,
    store_id: 101,
    store_name: "Posto Ipiranga Centro",
    city: "São Paulo",
    state: "SP",
    collection_date: "2024-03-15T08:30:00",
    fuel_type: "Gasolina",
    sale_price: 5.89,
    volume_sold: 45.5,
    driver_name: "João Silva",
    driver_cpf: "123.456.789-00",
    driver_cpf_masked: "123.456.XXX-XX",
    vehicle_plate: "ABC-1234",
    vehicle_type: "Carro",
  },
  {
    id: 2,
    store_id: 102,
    store_name: "Shell Avenida Paulista",
    city: "São Paulo",
    state: "SP",
    collection_date: "2024-03-15T09:15:00",
    fuel_type: "Diesel S10",
    sale_price: 6.15,
    volume_sold: 120.0,
    driver_name: "Maria Santos",
    driver_cpf: "987.654.321-00",
    driver_cpf_masked: "987.654.XXX-XX",
    vehicle_plate: "DEF-5678",
    vehicle_type: "Caminhão Leve",
  },
  {
    id: 3,
    store_id: 103,
    store_name: "BR Petrobras Rodovia",
    city: "Rio de Janeiro",
    state: "RJ",
    collection_date: "2024-03-15T10:00:00",
    fuel_type: "Diesel S10",
    sale_price: 6.25,
    volume_sold: 380.5,
    driver_name: "Carlos Oliveira",
    driver_cpf: "456.789.123-00",
    driver_cpf_masked: "456.789.XXX-XX",
    vehicle_plate: "GHI-9012",
    vehicle_type: "Carreta",
  },
  {
    id: 4,
    store_id: 104,
    store_name: "Ale Combustíveis",
    city: "Belo Horizonte",
    state: "MG",
    collection_date: "2024-03-15T11:20:00",
    fuel_type: "Etanol",
    sale_price: 3.99,
    volume_sold: 38.2,
    driver_name: "João Silva",
    driver_cpf: "123.456.789-00",
    driver_cpf_masked: "123.456.XXX-XX",
    vehicle_plate: "ABC-1234",
    vehicle_type: "Carro",
  },
  {
    id: 5,
    store_id: 105,
    store_name: "Posto do Carmo",
    city: "Curitiba",
    state: "PR",
    collection_date: "2024-03-15T12:45:00",
    fuel_type: "Gasolina",
    sale_price: 5.75,
    volume_sold: 52.0,
    driver_name: "Ana Paula Costa",
    driver_cpf: "321.654.987-00",
    driver_cpf_masked: "321.654.XXX-XX",
    vehicle_plate: "JKL-3456",
    vehicle_type: "Carro",
  },
  {
    id: 6,
    store_id: 106,
    store_name: "Texaco Express",
    city: "Porto Alegre",
    state: "RS",
    collection_date: "2024-03-15T14:10:00",
    fuel_type: "Diesel S10",
    sale_price: 6.1,
    volume_sold: 450.0,
    driver_name: "Roberto Lima",
    driver_cpf: "789.123.456-00",
    driver_cpf_masked: "789.123.XXX-XX",
    vehicle_plate: "MNO-7890",
    vehicle_type: "Carreta",
  },
  {
    id: 7,
    store_id: 107,
    store_name: "Raízen Posto",
    city: "Brasília",
    state: "DF",
    collection_date: "2024-03-14T08:00:00",
    fuel_type: "Diesel S10",
    sale_price: 6.2,
    volume_sold: 280.0,
    driver_name: "Fernando Alves",
    driver_cpf: "159.753.486-00",
    driver_cpf_masked: "159.753.XXX-XX",
    vehicle_plate: "PQR-1357",
    vehicle_type: "Ônibus",
  },
  {
    id: 8,
    store_id: 108,
    store_name: "Ipiranga Rede",
    city: "Salvador",
    state: "BA",
    collection_date: "2024-03-14T09:30:00",
    fuel_type: "Etanol",
    sale_price: 4.05,
    volume_sold: 41.5,
    driver_name: "Juliana Ferreira",
    driver_cpf: "753.159.846-00",
    driver_cpf_masked: "753.159.XXX-XX",
    vehicle_plate: "STU-2468",
    vehicle_type: "Carro",
  },
  {
    id: 9,
    store_id: 109,
    store_name: "Shell Select",
    city: "Recife",
    state: "PE",
    collection_date: "2024-03-14T10:45:00",
    fuel_type: "Gasolina",
    sale_price: 5.95,
    volume_sold: 48.0,
    driver_name: "Pedro Henrique",
    driver_cpf: "852.963.741-00",
    driver_cpf_masked: "852.963.XXX-XX",
    vehicle_plate: "VWX-3691",
    vehicle_type: "Carro",
  },
  {
    id: 10,
    store_id: 110,
    store_name: "BR Posto Cidade",
    city: "Fortaleza",
    state: "CE",
    collection_date: "2024-03-14T12:00:00",
    fuel_type: "Diesel S10",
    sale_price: 6.18,
    volume_sold: 95.0,
    driver_name: "Maria Santos",
    driver_cpf: "987.654.321-00",
    driver_cpf_masked: "987.654.XXX-XX",
    vehicle_plate: "DEF-5678",
    vehicle_type: "Caminhão Leve",
  },
  {
    id: 11,
    store_id: 111,
    store_name: "Ale Combustíveis Premium",
    city: "Manaus",
    state: "AM",
    collection_date: "2024-03-14T13:15:00",
    fuel_type: "Gasolina",
    sale_price: 6.1,
    volume_sold: 50.5,
    driver_name: "Lucas Andrade",
    driver_cpf: "147.258.369-00",
    driver_cpf_masked: "147.258.XXX-XX",
    vehicle_plate: "YZA-4802",
    vehicle_type: "Moto",
  },
  {
    id: 12,
    store_id: 112,
    store_name: "Posto São Jorge",
    city: "Belém",
    state: "PA",
    collection_date: "2024-03-14T14:30:00",
    fuel_type: "Etanol",
    sale_price: 3.89,
    volume_sold: 39.0,
    driver_name: "Carla Souza",
    driver_cpf: "369.258.147-00",
    driver_cpf_masked: "369.258.XXX-XX",
    vehicle_plate: "BCD-5913",
    vehicle_type: "Carro",
  },
  {
    id: 13,
    store_id: 113,
    store_name: "Texaco Highway",
    city: "Goiânia",
    state: "GO",
    collection_date: "2024-03-13T08:20:00",
    fuel_type: "Diesel S10",
    sale_price: 6.12,
    volume_sold: 410.0,
    driver_name: "Roberto Lima",
    driver_cpf: "789.123.456-00",
    driver_cpf_masked: "789.123.XXX-XX",
    vehicle_plate: "MNO-7890",
    vehicle_type: "Carreta",
  },
  {
    id: 14,
    store_id: 114,
    store_name: "Raízen Express",
    city: "Campinas",
    state: "SP",
    collection_date: "2024-03-13T09:40:00",
    fuel_type: "Gasolina",
    sale_price: 5.82,
    volume_sold: 47.5,
    driver_name: "João Silva",
    driver_cpf: "123.456.789-00",
    driver_cpf_masked: "123.456.XXX-XX",
    vehicle_plate: "ABC-1234",
    vehicle_type: "Carro",
  },
  {
    id: 15,
    store_id: 115,
    store_name: "Ipiranga Auto",
    city: "São Paulo",
    state: "SP",
    collection_date: "2024-03-13T11:00:00",
    fuel_type: "Diesel S10",
    sale_price: 6.22,
    volume_sold: 310.0,
    driver_name: "Fernando Alves",
    driver_cpf: "159.753.486-00",
    driver_cpf_masked: "159.753.XXX-XX",
    vehicle_plate: "PQR-1357",
    vehicle_type: "Ônibus",
  },
]

const MOCK_AVG_PRICES: AvgPriceByFuel[] = [
  { fuel_type: "Gasolina", avg_price: 5.89, total_records: 342 },
  { fuel_type: "Etanol", avg_price: 3.98, total_records: 218 },
  { fuel_type: "Diesel S10", avg_price: 6.17, total_records: 456 },
]

const MOCK_VOLUMES: VolumeByVehicle[] = [
  { vehicle_type: "Carreta", total_volume: 12540.5, total_records: 45 },
  { vehicle_type: "Ônibus", total_volume: 8320.0, total_records: 32 },
  { vehicle_type: "Caminhão Leve", total_volume: 6150.0, total_records: 58 },
  { vehicle_type: "Carro", total_volume: 4280.5, total_records: 195 },
  { vehicle_type: "Moto", total_volume: 890.2, total_records: 76 },
]

export function getMockCollections(params: {
  page?: number
  page_size?: number
  fuel_type?: string
  city?: string
  vehicle_type?: string
}): CollectionsResponse {
  let filtered = [...MOCK_COLLECTIONS]

  // Apply filters
  if (params.fuel_type) {
    filtered = filtered.filter((c) => c.fuel_type === params.fuel_type)
  }
  if (params.city) {
    filtered = filtered.filter((c) => c.city.toLowerCase().includes(params.city!.toLowerCase()))
  }
  if (params.vehicle_type) {
    filtered = filtered.filter((c) => c.vehicle_type === params.vehicle_type)
  }

  // Pagination
  const page = params.page || 1
  const page_size = params.page_size || 10
  const start = (page - 1) * page_size
  const end = start + page_size

  return {
    total: filtered.length,
    page,
    page_size,
    data: filtered.slice(start, end),
  }
}

export function getMockAvgPrices(): AvgPriceByFuel[] {
  return MOCK_AVG_PRICES
}

export function getMockVolumes(): VolumeByVehicle[] {
  return MOCK_VOLUMES
}

export function getMockDriverReport(search: string): DriverReport | null {
  // Search by CPF or name
  const searchLower = search.toLowerCase().replace(/[.-]/g, "")

  // Find all refuels for this driver
  const refuels = MOCK_COLLECTIONS.filter((c) => {
    const cpfMatch = c.driver_cpf.replace(/[.-]/g, "").includes(searchLower)
    const nameMatch = c.driver_name.toLowerCase().includes(searchLower)
    return cpfMatch || nameMatch
  })

  if (refuels.length === 0) return null

  // Calculate metrics
  const total_spent = refuels.reduce((sum, r) => sum + r.sale_price * r.volume_sold, 0)
  const total_volume = refuels.reduce((sum, r) => sum + r.volume_sold, 0)

  // Find favorite fuel (most frequent)
  const fuelCounts = refuels.reduce(
    (acc, r) => {
      acc[r.fuel_type] = (acc[r.fuel_type] || 0) + 1
      return acc
    },
    {} as Record<string, number>,
  )
  const favorite_fuel = Object.entries(fuelCounts).sort((a, b) => b[1] - a[1])[0][0]

  return {
    driver_name: refuels[0].driver_name,
    driver_cpf_masked: refuels[0].driver_cpf_masked,
    total_refuels: refuels.length,
    total_spent,
    total_volume,
    favorite_fuel,
    refuels,
  }
}
