"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { getAvgPriceByFuel } from "@/lib/api"
import { formatCurrency } from "@/lib/format"
import { Fuel, TrendingUp } from "lucide-react"
import type { AvgPriceByFuel } from "@/types/fuel"

export function KpiCards() {
  const [data, setData] = useState<AvgPriceByFuel[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchData() {
      try {
        const result = await getAvgPriceByFuel()
        setData(result)
      } catch (err) {
        setError("Erro ao carregar dados")
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="grid gap-4 md:grid-cols-3">
        {[1, 2, 3].map((i) => (
          <Card key={i} className="bg-card/50 border-border/50">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <div className="h-4 w-24 bg-muted animate-pulse rounded" />
              <Fuel className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="h-8 w-32 bg-muted animate-pulse rounded mb-2" />
              <div className="h-3 w-20 bg-muted animate-pulse rounded" />
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (error) {
    return <div className="p-4 bg-destructive/10 text-destructive rounded-lg border border-destructive/20">{error}</div>
  }

  if (data.length === 0) {
    return (
      <div className="p-8 text-center bg-muted/30 rounded-lg border border-border/50">
        <Fuel className="h-12 w-12 text-muted-foreground mx-auto mb-3" />
        <p className="text-muted-foreground font-medium">Sem dados disponíveis</p>
        <p className="text-sm text-muted-foreground mt-1">Nenhum registro de preço foi encontrado</p>
      </div>
    )
  }

  const getFuelColor = (fuelType: string) => {
    if (fuelType.includes("Gasolina")) return "text-amber-500"
    if (fuelType.includes("Etanol")) return "text-green-500"
    if (fuelType.includes("Diesel")) return "text-blue-500"
    return "text-muted-foreground"
  }

  return (
    <div className="grid gap-4 md:grid-cols-3">
      {data.map((item) => (
        <Card key={item.fuel_type} className="bg-card border-border/50 hover:border-primary/50 transition-colors">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">{item.fuel_type}</CardTitle>
            <Fuel className={`h-4 w-4 ${getFuelColor(item.fuel_type)}`} />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground">{formatCurrency(item.avg_price)}</div>
            <p className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
              <TrendingUp className="h-3 w-3" />
              {item.total_records} registros
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
