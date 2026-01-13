const agents = [
  { id: 1, name: "Agent A", status: "Actif", network: "Réseau A" },
  { id: 2, name: "Agent B", status: "Actif", network: "Réseau B" },
  { id: 3, name: "Agent C", status: "Inactif", network: "Réseau C" },
];

export default function AgentsPage() {
  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Agents actifs</h2>

      <table className="w-full border">
        <thead>
          <tr className="bg-gray-200">
            <th className="border p-2">ID</th>
            <th className="border p-2">Nom</th>
            <th className="border p-2">Statut</th>
            <th className="border p-2">Réseau</th>
          </tr>
        </thead>
        <tbody>
          {agents.map((agent) => (
            <tr key={agent.id}>
              <td className="border p-2">{agent.id}</td>
              <td className="border p-2">{agent.name}</td>
              <td className="border p-2">{agent.status}</td>
              <td className="border p-2">{agent.network}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
