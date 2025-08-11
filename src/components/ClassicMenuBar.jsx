import React, { useState } from "react";
import "./classic-menu-bar.css";

const menuData = [
  {
    label: "File",
    items: [
      { label: "Dashboard", action: () => window.location = "/dashboard" },
      { label: "Map View", action: () => window.location = "/map" },
      { label: "Export Data", action: () => window.location = "/export" },
      { label: "Exit", action: () => window.close() }
    ]
  },
  {
    label: "Scan",
    items: [
      { label: "New Scan", action: () => window.location = "/scan" },
      { label: "Stop Scan", action: () => alert("Scan stopped!") }
    ]
  },
  {
    label: "Devices",
    items: [
      { label: "Device List", action: () => window.location = "/devices" },
      { label: "Statistics", action: () => window.location = "/stats" }
    ]
  },
  {
    label: "Rules",
    items: [
      { label: "Rule Manager", action: () => window.location = "/rules" },
      { label: "AI/ML Engine", action: () => window.location = "/ai" }
    ]
  },
  {
    label: "Report",
    items: [
      { label: "Download Report", action: () => window.location = "/report" },
      { label: "View Graphs", action: () => window.location = "/charts" }
    ]
  },
  {
    label: "Settings",
    items: [
      { label: "User Management", action: () => window.location = "/users" },
      { label: "API Keys", action: () => window.location = "/apikeys" },
      { label: "Alerts/Notifications", action: () => window.location = "/notifications" }
    ]
  },
  {
    label: "Help",
    items: [
      { label: "About", action: () => alert("Kashif Miner System v1.0") }
    ]
  }
];

export default function ClassicMenuBar() {
  const [openMenu, setOpenMenu] = useState(null);

  const handleMenuEnter = idx => setOpenMenu(idx);
  const handleMenuLeave = () => setOpenMenu(null);

  return (
    <div className="classic-menu-bar" onMouseLeave={handleMenuLeave}>
      {menuData.map((menu, idx) => (
        <div
          className={`menu-bar-item${openMenu === idx ? " open" : ""}`}
          key={menu.label}
          onMouseEnter={() => handleMenuEnter(idx)}
          tabIndex={0}
        >
          <div className="menu-bar-title">{menu.label}</div>
          {openMenu === idx && (
            <div className="dropdown">
              {menu.items.map(item => (
                <div
                  className="dropdown-item"
                  key={item.label}
                  onClick={item.action}
                  tabIndex={0}
                >
                  {item.label}
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
