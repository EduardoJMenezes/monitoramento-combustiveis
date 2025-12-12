export interface FuelCollection {
  id: number
  store_id: number
  store_name: string
  city: string
  state: string
  collection_date: string
  fuel_type: string
  sale_price: number
  volume_sold: number
  driver_name: string
  driver_cpf: string
  driver_cpf_masked: string
  vehicle_plate: string
  vehicle_type: string
}

export interface CollectionsResponse {
  total: number
  page: number
  page_size: number
  data: FuelCollection[]
}

export interface AvgPriceByFuel {
  fuel_type: string
  avg_price: number
  total_records: number
}

export interface VolumeByVehicle {
  vehicle_type: string
  total_volume: number
  total_records: number
}

export interface DriverReport {
  driver_name: string
  driver_cpf_masked: string
  total_refuels: number
  total_spent: number
  total_volume: number
  favorite_fuel: string
  refuels: FuelCollection[]
}
