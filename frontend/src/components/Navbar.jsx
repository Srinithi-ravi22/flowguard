import { Search, Bell, UserCircle } from "lucide-react";
import "../styles/navbar.css";

function Navbar() {
  const today = new Date();

  return (
    <header className="navbar">
      <div className="navbar-left">
        <h2>FlowGuard Dashboard</h2>
        <p>
          {today.toLocaleDateString()} | {today.toLocaleTimeString()}
        </p>
      </div>

      <div className="navbar-right">
        <div className="search-box">
          <Search size={18} />
          <input type="text" placeholder="Search..." />
        </div>

        <Bell size={22} className="nav-icon" />

        <div className="profile">
          <UserCircle size={34} />
          <span>Admin</span>
        </div>
      </div>
    </header>
  );
}

export default Navbar;