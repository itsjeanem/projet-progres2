"use client";

import { useState } from "react";

// Page Agents - NetGuard Pro
export default function AgentsPage() {
  const [search, setSearch] = useState("");

  const agents = [
    {
      id: "003",
      name: "wazuh-premises-production-civ",
      ip: "192.168.3.21",
      groups: "linux-agents +1",
      os: "Ubuntu 24.04.3 LTS",
      node: "manager-master-0",
      version: "v4.12.0",
    },
    {
      id: "004",
      name: "asterix-premises-production-sen",
      ip: "10.10.50.13",
      groups: "linux-agents",
      os: "Ubuntu 22.04.5 LTS",
      node: "manager-master-0",
      version: "v4.14.1",
    },
    {
      id: "008",
      name: "bastion-premises-production-sen",
      ip: "10.10.60.13",
      groups: "windows-agents",
      os: "Microsoft Windows 11 Pro",
      node: "manager-master-0",
      version: "v4.14.1",
    },
  ];

  const filteredAgents = agents.filter((agent) =>
    Object.values(agent)
      .join(" ")
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <main className="min-h-screen bg-zinc-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* En-tête */}
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <h1 className="text-2xl font-semibold text-zinc-800">
            Agents <span className="text-zinc-500">({filteredAgents.length})</span>
          </h1>

          <div className="flex gap-6 text-sm">
            <a className="text-blue-600 hover:text-blue-800 cursor-pointer">
              Refresh
            </a>
            <a className="text-blue-600 hover:text-blue-800 cursor-pointer">
              Export formatted
            </a>
          </div>
        </div>

        {/* Recherche */}
        <div className="bg-white border border-zinc-200 rounded-lg p-4 shadow-sm">
          <input
            type="text"
            placeholder="Search agents..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="
              w-full md:w-80
              border border-zinc-300 rounded-md
              px-3 py-2 text-sm
              focus:outline-none
              focus:ring-2 focus:ring-blue-500
              focus:border-blue-500
            "
          />
        </div>

        {/* Table */}
        <div className="bg-white border border-zinc-200 rounded-lg shadow-sm overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-zinc-50 text-zinc-600 text-xs uppercase tracking-wide">
              <tr>
                <th className="px-4 py-3 text-left">ID</th>
                <th className="px-4 py-3 text-left">Name</th>
                <th className="px-4 py-3 text-left">IP address</th>
                <th className="px-4 py-3 text-left">Group(s)</th>
                <th className="px-4 py-3 text-left">Operating system</th>
                <th className="px-4 py-3 text-left">Cluster node</th>
                <th className="px-4 py-3 text-left">Version</th>
                <th className="px-4 py-3 text-left">Status</th>
                <th className="px-4 py-3 text-left">Actions</th>
              </tr>
            </thead>

            <tbody>
              {filteredAgents.map((agent) => (
                <tr
                  key={agent.id}
                  className="border-t hover:bg-blue-50/40 transition"
                >
                  <td className="px-4 py-3 font-mono text-xs">
                    {agent.id}
                  </td>
                  <td className="px-4 py-3 font-medium text-zinc-800">
                    {agent.name}
                  </td>
                  <td className="px-4 py-3">{agent.ip}</td>
                  <td className="px-4 py-3">{agent.groups}</td>
                  <td className="px-4 py-3">{agent.os}</td>
                  <td className="px-4 py-3">{agent.node}</td>
                  <td className="px-4 py-3">{agent.version}</td>
                  <td className="px-4 py-3">
                    <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700">
                      Active
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className="text-blue-600 hover:underline cursor-pointer">
                      View
                    </span>
                  </td>
                </tr>
              ))}

              {filteredAgents.length === 0 && (
                <tr>
                  <td
                    colSpan={9}
                    className="px-4 py-6 text-center text-zinc-500"
                  >
                    Aucun agent trouvé
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Footer */}
        <div className="flex justify-between items-center text-sm text-zinc-500">
          <span>Rows per page: 10</span>
          <span>Page 1</span>
        </div>

      </div>
    </main>
  );
}
