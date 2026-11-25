import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Activity,
  Bell,
  CalendarDays,
  Shield,
  Database,
} from "lucide-react";
import "../styles/sidebar.css";

function Sidebar() {
  const menuItems = [
    {
      name: "Dashboard",
      path: "/",
      icon: <LayoutDashboard size={20} />,
    },
    {
      name: "Monitoring",
      path: "/monitoring",
      icon: <Activity size={20} />,
    },
    {
      name: "Events",
      path: "/events",
      icon: <CalendarDays size={20} />,
    },
    {
      name: "Alerts",
      path: "/alerts",
      icon: <Bell size={20} />,
    },
    {
      name: "Baselines",
      path: "/baselines",
      icon: <Database size={20} />,
    },
    {
      name: "Protection",
      path: "/protection",
      icon: <Shield size={20} />,
    },
  ];

  return (
    <aside className="sidebar">
      <div className="logo">
        <div className="logo-icon">🛡️</div>

        <div className="logo-text">
          <h2>FlowGuard</h2>
          <p>Workflow Protection</p>
        </div>
      </div>

      <nav className="sidebar-menu">
        {menuItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              isActive ? "menu-item active" : "menu-item"
            }
          >
            {item.icon}
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;