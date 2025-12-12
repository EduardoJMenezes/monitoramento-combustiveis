import { KpiCards } from "@/components/kpi-cards"
import { VolumeChart } from "@/components/volume-chart"
import { CollectionsTable } from "@/components/collections-table"
import { DriverSearch } from "@/components/driver-search"
import { Fuel } from "lucide-react"

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-card border-b border-border/50 sticky top-0 z-50 backdrop-blur-sm bg-card/95">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="bg-primary/10 p-2 rounded-lg">
              <Fuel className="h-6 w-6 text-primary" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-foreground">V-Lab Fuel Monitor</h1>
              <p className="text-sm text-muted-foreground">Ministério dos Transportes</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="space-y-8">
          {/* Page Title */}
          <div>
            <h2 className="text-3xl font-bold text-foreground mb-2">Dashboard de Combustíveis</h2>
            <p className="text-muted-foreground">Monitoramento em tempo real de preços e consumo de combustíveis</p>
          </div>

          {/* KPI Cards */}
          <section>
            <h3 className="text-lg font-semibold text-foreground mb-4">Indicadores de Preço</h3>
            <KpiCards />
          </section>

          {/* Chart and Driver Search */}
          <div className="grid gap-6 lg:grid-cols-2">
            <VolumeChart />
            <DriverSearch />
          </div>

          {/* Collections Table */}
          <section>
            <CollectionsTable />
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border/50 bg-card mt-12">
        <div className="container mx-auto px-4 py-6">
          <p className="text-center text-sm text-muted-foreground">
            © 2025 Ministério dos Transportes - Sistema de Monitoramento de Combustíveis
          </p>
        </div>
      </footer>
    </div>
  )
}
