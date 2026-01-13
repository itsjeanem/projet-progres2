import Link from "next/link";

export default function Navbar() {
  return (
    <nav style={{ padding: "1rem", borderBottom: "1px solid #ddd" }}>
      <h2>NetGuard Pro</h2>

      <ul style={{ display: "flex", gap: "1rem", listStyle: "none" }}>
        <li><Link href="/">Accueil</Link></li>
        <li><Link href="/agents">Agents</Link></li>
        <li><Link href="/alerts">Alertes</Link></li>
        <li><Link href="/stats">Statistiques</Link></li>
      </ul>
    </nav>
  );
}
