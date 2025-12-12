"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { getCollections } from "@/lib/api"
import { formatCurrency, formatVolume, formatDate } from "@/lib/format"
import { ChevronLeft, ChevronRight, Filter } from "lucide-react"
import type { CollectionsResponse } from "@/types/fuel"

export function CollectionsTable() {
  const [data, setData] = useState<CollectionsResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [page, setPage] = useState(1)
  const [fuelType, setFuelType] = useState<string>("all")
  const [vehicleType, setVehicleType] = useState<string>("all")
  const [city, setCity] = useState<string>("")
  const [cityInput, setCityInput] = useState<string>("")

  useEffect(() => {
    const timer = setTimeout(() => {
      setCity(cityInput)
    }, 500)
    return () => clearTimeout(timer)
  }, [cityInput])

  useEffect(() => {
    async function fetchData() {
      setLoading(true)
      try {
        const result = await getCollections({
          page,
          page_size: 10,
          fuel_type: fuelType !== "all" ? fuelType : undefined,
          vehicle_type: vehicleType !== "all" ? vehicleType : undefined,
          city: city || undefined,
        })
        setData(result)
      } catch (err) {
        setError("Erro ao carregar coletas")
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [page, fuelType, vehicleType, city])

  const totalPages = data ? Math.ceil(data.total / data.page_size) : 0

  return (
    <Card className="bg-card border-border/50">
      <CardHeader>
        <CardTitle className="text-lg font-semibold text-foreground flex items-center gap-2">
          <Filter className="h-5 w-5" />
          Registro de Abastecimentos
        </CardTitle>
        <div className="grid gap-4 md:grid-cols-4 mt-4">
          <Select
            value={fuelType}
            onValueChange={(value) => {
              setFuelType(value)
              setPage(1)
            }}
          >
            <SelectTrigger>
              <SelectValue placeholder="Tipo de Combustível" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos</SelectItem>
              <SelectItem value="Gasolina">Gasolina</SelectItem>
              <SelectItem value="Etanol">Etanol</SelectItem>
              <SelectItem value="Diesel S10">Diesel S10</SelectItem>
            </SelectContent>
          </Select>

          <Select
            value={vehicleType}
            onValueChange={(value) => {
              setVehicleType(value)
              setPage(1)
            }}
          >
            <SelectTrigger>
              <SelectValue placeholder="Tipo de Veículo" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos</SelectItem>
              <SelectItem value="Carro">Carro</SelectItem>
              <SelectItem value="Moto">Moto</SelectItem>
              <SelectItem value="Caminhão Leve">Caminhão Leve</SelectItem>
              <SelectItem value="Carreta">Carreta</SelectItem>
              <SelectItem value="Ônibus">Ônibus</SelectItem>
            </SelectContent>
          </Select>

          <Input
            placeholder="Filtrar por cidade..."
            value={cityInput}
            onChange={(e) => {
              setCityInput(e.target.value)
              setPage(1)
            }}
            className="md:col-span-2"
          />
        </div>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
          </div>
        ) : error ? (
          <div className="p-4 bg-destructive/10 text-destructive rounded-lg border border-destructive/20">{error}</div>
        ) : !data || data.data.length === 0 ? (
          <div className="p-12 text-center bg-muted/30 rounded-lg border border-border/50">
            <div className="text-6xl mb-4">🔍</div>
            <p className="text-muted-foreground font-medium text-lg">Sem dados disponíveis</p>
            <p className="text-sm text-muted-foreground mt-2">Nenhum abastecimento foi encontrado com os filtros aplicados</p>
          </div>
        ) : (
          <>
            <div className="rounded-lg border border-border overflow-hidden">
              <Table>
                <TableHeader>
                  <TableRow className="bg-muted/50">
                    <TableHead>Data/Hora</TableHead>
                    <TableHead>Posto</TableHead>
                    <TableHead>Cidade/UF</TableHead>
                    <TableHead>Combustível</TableHead>
                    <TableHead className="text-right">Preço</TableHead>
                    <TableHead className="text-right">Volume</TableHead>
                    <TableHead>Veículo</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {data?.data.map((item) => (
                    <TableRow key={item.id} className="hover:bg-muted/50">
                      <TableCell className="text-sm">{formatDate(item.collection_date)}</TableCell>
                      <TableCell className="font-medium">{item.store_name}</TableCell>
                      <TableCell className="text-sm">
                        {item.city}/{item.state}
                      </TableCell>
                      <TableCell>
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary">
                          {item.fuel_type}
                        </span>
                      </TableCell>
                      <TableCell className="text-right font-mono text-sm">{formatCurrency(item.sale_price)}</TableCell>
                      <TableCell className="text-right font-mono text-sm">{formatVolume(item.volume_sold)}</TableCell>
                      <TableCell className="text-sm">{item.vehicle_type}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>

            <div className="flex items-center justify-between mt-4">
              <p className="text-sm text-muted-foreground">
                Mostrando {data?.data.length || 0} de {data?.total || 0} registros
              </p>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1}
                >
                  <ChevronLeft className="h-4 w-4" />
                  Anterior
                </Button>
                <span className="text-sm text-muted-foreground">
                  Página {page} de {totalPages}
                </span>
                <Button variant="outline" size="sm" onClick={() => setPage((p) => p + 1)} disabled={page >= totalPages}>
                  Próxima
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  )
}
