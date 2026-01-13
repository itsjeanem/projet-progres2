export default function StatsPage() {
  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Statistiques</h2>

      <ul className="list-disc pl-6">
        <li>Agents actifs : 2</li>
        <li>Alertes détectées : 2</li>
        <li>Dernière alerte : SYN Flood</li>
      </ul>
    </div>
  );
}
