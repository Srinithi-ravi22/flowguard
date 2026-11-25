import { Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";

import Dashboard from "./pages/Dashboard";
import Monitoring from "./pages/Monitoring";
import Alerts from "./pages/Alerts";
import Events from "./pages/Events";
import Baselines from "./pages/Baselines";
import Protection from "./pages/Protection";
import ExecutionDetails from "./pages/ExecutionDetails";
import NotFound from "./pages/NotFound";

function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/monitoring" element={<Monitoring />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/events" element={<Events />} />
        <Route path="/baselines" element={<Baselines />} />
        <Route path="/protection" element={<Protection />} />
        <Route
          path="/execution/:id"
          element={<ExecutionDetails />}
        />
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default App;