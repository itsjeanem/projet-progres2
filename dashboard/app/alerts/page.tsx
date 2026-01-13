const alerts = [
  {
    id: 1,
    type: "Port Scan",
    severity: "Élevée",
    date: "2026-01-10",
  },
  {
    id: 2,
    type: "SYN Flood",
    severity: "Critique",
    date: "2026-01-11",
  },
];

export default function AlertsPage() {
  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Alertes de sécurité</h2>

      <table className="w-full border">
        <thead>
          <tr className="bg-gray-200">
            <th className="border p-2">ID</th>
            <th className="border p-2">Type</th>
            <th className="border p-2">Gravité</th>
            <th className="border p-2">Date</th>
          </tr>
        </thead>
        <tbody>
          {alerts.map((alert) => (
            <tr key={alert.id}>
              <td className="border p-2">{alert.id}</td>
              <td className="border p-2">{alert.type}</td>
              <td className="border p-2">{alert.severity}</td>
              <td className="border p-2">{alert.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
