export function Table({ data }) {
  return (
    <table className="min-w-full border">
      <thead>
        <tr>
          <th>IP</th><th>Ports</th><th>City</th><th>Country</th><th>ریسک</th>
        </tr>
      </thead>
      <tbody>
        {data.map((m, i) =>
          <tr key={i}>
            <td>{m.ip}</td>
            <td>{m.open_ports}</td>
            <td>{m.city}</td>
            <td>{m.country}</td>
            <td>{m.risk}</td>
          </tr>
        )}
      </tbody>
    </table>
  );
}