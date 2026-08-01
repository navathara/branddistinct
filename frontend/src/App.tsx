import { Route, Routes } from "react-router-dom";
import { Layout } from "@/components/Layout";
import { Home } from "@/pages/Home";
import { Discover } from "@/pages/Discover";
import { Evaluate } from "@/pages/Evaluate";
import { NotFound } from "@/pages/NotFound";

/**
 * Route table.
 *
 * "/discover" renders the Brand Discovery page. "/evaluate" renders the
 * Evaluation page, which also mounts the Results Dashboard after a
 * successful evaluation. There is no separate results route — anything
 * else falls through to NotFound.
 */
function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="discover" element={<Discover />} />
        <Route path="evaluate" element={<Evaluate />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default App;
