"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { getDriverReport } from "@/lib/api"
import { formatCurrency, formatVolume, formatDate, validateCPF } from "@/lib/format"
import { Search, User, ChevronDown, AlertCircle } from "lucide-react"
import type { DriverReport } from "@/types/fuel"

export function DriverSearch() {
  const [search, setSearch] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [report, setReport] = useState<DriverReport | null>(null)
  const [showDialog, setShowDialog] = useState(false)

  async function handleSearch() {
    if (!search.trim()) {
      setError("Digite um CPF ou nome para buscar")
      return
    }

    // Validate CPF if it looks like a CPF
    const cleanSearch = search.replace(/\D/g, "")
    if (cleanSearch.length > 0 && cleanSearch.length <= 11) {
      if (cleanSearch.length === 11 && !validateCPF(cleanSearch)) {
        setError("CPF inválido. Digite 11 dígitos numéricos.")
        return
      }
    }

    setLoading(true)
    setError(null)

    try {
      const result = await getDriverReport(search)
      setReport(result)
      setShowDialog(true)
    } catch (err: any) {
      if (err.message === "NOT_FOUND") {
        setError("Motorista não encontrado. Verifique o CPF ou nome.")
      } else {
        setError("Erro ao buscar relatório do motorista")
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Card className="bg-card border-border/50">
        <CardHeader>
          <CardTitle className="text-lg font-semibold text-foreground flex items-center gap-2">
            <User className="h-5 w-5" />
            Buscar Motorista
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-2">
            <Input
              placeholder="Digite CPF (11 dígitos) ou nome do motorista..."
              value={search}
              onChange={(e) => {
                setSearch(e.target.value)
                setError(null)
              }}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              className="flex-1"
            />
            <Button onClick={handleSearch} disabled={loading}>
              {loading ? (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
              ) : (
                <Search className="h-4 w-4" />
              )}
            </Button>
          </div>
          {error && (
            <div className="mt-3 p-3 bg-destructive/10 text-destructive rounded-lg border border-destructive/20 flex items-start gap-2 text-sm">
              <AlertCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}
        </CardContent>
      </Card>

      <Dialog open={showDialog} onOpenChange={setShowDialog}>
        <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-xl font-semibold">Relatório do Motorista</DialogTitle>
          </DialogHeader>

          {report && (
            <div className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div className="p-4 rounded-lg bg-muted/50 border border-border">
                  <p className="text-sm text-muted-foreground mb-1">Nome</p>
                  <p className="font-semibold text-lg">{report.driver_name}</p>
                </div>
                <div className="p-4 rounded-lg bg-muted/50 border border-border">
                  <p className="text-sm text-muted-foreground mb-1">CPF</p>
                  <p className="font-semibold text-lg">{report.driver_cpf_masked}</p>
                </div>
              </div>

              <div className="grid gap-4 md:grid-cols-4">
                <div className="p-4 rounded-lg bg-primary/10 border border-primary/20">
                  <p className="text-sm text-muted-foreground mb-1">Total de Abastecimentos</p>
                  <p className="text-2xl font-bold text-primary">{report.total_refuels}</p>
                </div>
                <div className="p-4 rounded-lg bg-green-500/10 border border-green-500/20">
                  <p className="text-sm text-muted-foreground mb-1">Total Gasto</p>
                  <p className="text-2xl font-bold text-green-600">{formatCurrency(report.total_spent)}</p>
                </div>
                <div className="p-4 rounded-lg bg-blue-500/10 border border-blue-500/20">
                  <p className="text-sm text-muted-foreground mb-1">Volume Total</p>
                  <p className="text-2xl font-bold text-blue-600">{formatVolume(report.total_volume)}</p>
                </div>
                <div className="p-4 rounded-lg bg-amber-500/10 border border-amber-500/20">
                  <p className="text-sm text-muted-foreground mb-1">Combustível Favorito</p>
                  <p className="text-2xl font-bold text-amber-600">{report.favorite_fuel}</p>
                </div>
              </div>

              <Collapsible>
                <CollapsibleTrigger asChild>
                  <Button variant="outline" className="w-full bg-transparent">
                    <ChevronDown className="h-4 w-4 mr-2" />
                    Ver Histórico de Abastecimentos ({report.refuels.length})
                  </Button>
                </CollapsibleTrigger>
                <CollapsibleContent className="mt-4">
                  <div className="rounded-lg border border-border overflow-hidden">
                    <Table>
                      <TableHeader>
                        <TableRow className="bg-muted/50">
                          <TableHead>Data/Hora</TableHead>
                          <TableHead>Posto</TableHead>
                          <TableHead>Cidade/UF</TableHead>
                          <TableHead>Combustível</TableHead>
                          <TableHead className="text-right">Valor</TableHead>
                          <TableHead className="text-right">Volume</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {report.refuels.map((refuel) => (
                          <TableRow key={refuel.id}>
                            <TableCell className="text-sm">{formatDate(refuel.collection_date)}</TableCell>
                            <TableCell className="font-medium">{refuel.store_name}</TableCell>
                            <TableCell className="text-sm">
                              {refuel.city}/{refuel.state}
                            </TableCell>
                            <TableCell>
                              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary">
                                {refuel.fuel_type}
                              </span>
                            </TableCell>
                            <TableCell className="text-right font-mono text-sm">
                              {formatCurrency(refuel.sale_price * refuel.volume_sold)}
                            </TableCell>
                            <TableCell className="text-right font-mono text-sm">
                              {formatVolume(refuel.volume_sold)}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </CollapsibleContent>
              </Collapsible>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </>
  )
}

// Add missing Table import
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
