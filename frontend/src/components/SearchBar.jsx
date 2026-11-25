import { Search } from "lucide-react";
import "../styles/search.css";

function SearchBar({ value, onChange, placeholder = "Search..." }) {
  return (
    <div className="search-container">
      <Search size={18} className="search-icon" />

      <input
        type="text"
        className="search-input"
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}

export default SearchBar;