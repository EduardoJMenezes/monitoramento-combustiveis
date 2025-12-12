// API URL - usa variável de ambiente ou localhost como fallback
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
const USE_MOCK_DATA = false // Set to false to use real API

import { getMockCollections, getMockAvgPrices, getMockVolumes, getMockDriverReport } from "./mock-data"

export async function getCollections(params: {
  page?: number
  page_size?: number
  fuel_type?: string
  city?: string
  vehicle_type?: string
}) {
  if (USE_MOCK_DATA) {
    // Simulate network delay
    await new Promise((resolve) => setTimeout(resolve, 300))
    return getMockCollections(params)
  }

  const queryParams = new URLSearchParams()

  if (params.page) queryParams.append("page", params.page.toString())
  if (params.page_size) queryParams.append("page_size", params.page_size.toString())
  if (params.fuel_type) queryParams.append("fuel_type", params.fuel_type)
  if (params.city) queryParams.append("city", params.city)
  if (params.vehicle_type) queryParams.append("vehicle_type", params.vehicle_type)

  const response = await fetch(`${API_BASE_URL}/collections?${queryParams.toString()}`)
  if (!response.ok) throw new Error("Erro ao buscar coletas")
  return response.json()
}

export async function getAvgPriceByFuel() {
  if (USE_MOCK_DATA) {
    await new Promise((resolve) => setTimeout(resolve, 200))
    return getMockAvgPrices()
  }

  const response = await fetch(`${API_BASE_URL}/kpis/avg-price-by-fuel`)
  if (!response.ok) throw new Error("Erro ao buscar preços médios")
  return response.json()
}

export async function getVolumeByVehicle() {
  if (USE_MOCK_DATA) {
    await new Promise((resolve) => setTimeout(resolve, 200))
    return getMockVolumes()
  }

  const response = await fetch(`${API_BASE_URL}/kpis/volume-by-vehicle`)
  if (!response.ok) throw new Error("Erro ao buscar volumes")
  return response.json()
}

export async function getDriverReport(search: string) {
  if (USE_MOCK_DATA) {
    await new Promise((resolve) => setTimeout(resolve, 400))
    const report = getMockDriverReport(search)
    if (!report) {
      throw new Error("NOT_FOUND")
    }
    return report
  }

  const response = await fetch(`${API_BASE_URL}/reports/drivers?search=${encodeURIComponent(search)}`)
  if (response.status === 404) {
    throw new Error("NOT_FOUND")
  }
  if (!response.ok) throw new Error("Erro ao buscar relatório do motorista")
  return response.json()
}
