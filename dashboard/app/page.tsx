// app/page.tsx
// Dashboard principal NetGuard Pro
// Inspiré des interfaces SOC (Wazuh / Zabbix)
// Next.js (App Router) + Tailwind CSS
// Toutes les données sont statiques pour l’instant (API plus tard)

export default function HomePage() {
  return (
    <main className="min-h-screen bg-zinc-50 p-6 space-y-8">

      {/* ============================= */}
      {/* Titre principal */}
      {/* ============================= */}
      <h1 className="text-2xl font-semibold text-zinc-800">
        Tableau de bord
      </h1>

      {/* ============================= */}
      {/* LIGNE 1 — Cartes KPI */}
      {/* ============================= */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">

        {/* Agents actifs */}
        <div className="bg-white border border-zinc-200 rounded-lg p-5">
          <p className="text-sm text-zinc-500">Agents actifs</p>
          <p className="mt-2 text-3xl font-semibold text-blue-600">12</p>
        </div>

        {/* Alertes détectées */}
        <div className="bg-white border border-zinc-200 rounded-lg p-5">
          <p className="text-sm text-zinc-500">Alertes détectées</p>
          <p className="mt-2 text-3xl font-semibold text-orange-500">38</p>
        </div>

        {/* Trafic réseau */}
        <div className="bg-white border border-zinc-200 rounded-lg p-5">
          <p className="text-sm text-zinc-500">Paquets analysés</p>
          <p className="mt-2 text-3xl font-semibold text-violet-600">1.2M</p>
        </div>

        {/* État du réseau */}
        <div className="bg-white border border-zinc-200 rounded-lg p-5">
          <p className="text-sm text-zinc-500">État du réseau</p>
          <p className="mt-2 text-xl font-semibold text-green-600">Stable</p>
        </div>

      </section>

      {/* ============================= */}
      {/* LIGNE 2 — Analyse visuelle */}
      {/* ============================= */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* 1/3 — Répartition des agents (Pie simulé) */}
        <div className="bg-white border border-zinc-200 rounded-lg p-5">
          <h2 className="text-sm font-medium text-zinc-700 mb-4">
            Agents par statut
          </h2>

          {/* Simulation visuelle type Wazuh */}
          <ul className="space-y-3">
            <li className="flex justify-between text-sm">
              <span className="text-green-600">● Actifs</span>
              <span>8</span>
            </li>
            <li className="flex justify-between text-sm">
              <span className="text-yellow-500">● Inactifs</span>
              <span>3</span>
            </li>
            <li className="flex justify-between text-sm">
              <span className="text-red-500">● Déconnectés</span>
              <span>1</span>
            </li>
          </ul>
        </div>

        {/* 2/3 — Alertes par gravité */}
        <div className="bg-white border border-zinc-200 rounded-lg p-5 lg:col-span-2">
          <h2 className="text-sm font-medium text-zinc-700 mb-4">
            Alertes par niveau de gravité
          </h2>

          <div className="space-y-4">

            {/* Élevé */}
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-red-600">Élevé</span>
                <span>12</span>
              </div>
              <div className="h-2 bg-zinc-200 rounded">
                <div className="h-2 bg-red-600 rounded w-[60%]" />
              </div>
            </div>

            {/* Moyen */}
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-orange-500">Moyen</span>
                <span>18</span>
              </div>
              <div className="h-2 bg-zinc-200 rounded">
                <div className="h-2 bg-orange-500 rounded w-[80%]" />
              </div>
            </div>

            {/* Faible */}
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-green-600">Faible</span>
                <span>8</span>
              </div>
              <div className="h-2 bg-zinc-200 rounded">
                <div className="h-2 bg-green-600 rounded w-[40%]" />
              </div>
            </div>

          </div>
        </div>

      </section>

      {/* ============================= */}
      {/* LIGNE 3 — Tables principales */}
      {/* ============================= */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        {/* Derniers agents */}
        <div className="bg-white border border-zinc-200 rounded-lg p-5">
          <h2 className="text-sm font-medium text-zinc-700 mb-4">
            Derniers agents connectés
          </h2>

          <table className="w-full text-sm">
            <thead className="text-zinc-500 border-b">
              <tr>
                <th className="text-left py-2">Agent</th>
                <th className="text-left py-2">Réseau</th>
                <th className="text-left py-2">Statut</th>
              </tr>
            </thead>
            <tbody>
              {[
                ["Agent-01", "Réseau A", "Actif"],
                ["Agent-02", "Réseau B", "Actif"],
                ["Agent-03", "Réseau C", "Inactif"],
                ["Agent-04", "Réseau A", "Actif"],
                ["Agent-05", "Réseau B", "Déconnecté"],
              ].map(([agent, reseau, statut]) => (
                <tr key={agent} className="border-b last:border-none">
                  <td className="py-2">{agent}</td>
                  <td>{reseau}</td>
                  <td>{statut}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Dernières alertes */}
        <div className="bg-white border border-zinc-200 rounded-lg p-5">
          <h2 className="text-sm font-medium text-zinc-700 mb-4">
            Dernières alertes
          </h2>

          <table className="w-full text-sm">
            <thead className="text-zinc-500 border-b">
              <tr>
                <th className="text-left py-2">Type</th>
                <th className="text-left py-2">Gravité</th>
                <th className="text-left py-2">Agent</th>
              </tr>
            </thead>
            <tbody>
              {[
                ["Port Scan", "Élevé", "Agent-02"],
                ["SYN Flood", "Élevé", "Agent-01"],
                ["ICMP Flood", "Moyen", "Agent-04"],
                ["Scan réseau", "Faible", "Agent-03"],
                ["Connexion suspecte", "Moyen", "Agent-05"],
              ].map(([type, niveau, agent], i) => (
                <tr key={i} className="border-b last:border-none">
                  <td className="py-2">{type}</td>
                  <td>{niveau}</td>
                  <td>{agent}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

      </section>

    </main>
  );
}
