import { useEffect, useRef, useState } from "react";
import * as maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

export default function App() {
  const contenedor_mapa = useRef(null);
  const mapa = useRef(null);
  const [puntos, setPuntos] = useState([]);

  useEffect(() => {
    if (mapa.current) return; // evita crear el mapa dos veces

    mapa.current = new maplibregl.Map({
      container: contenedor_mapa.current,
      style: "https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
      center: [-70.65, -33.45], // [lon, lat] — Santiago
      zoom: 11,
    });

    mapa.current.on("click", (e) => {
      const { lat, lng } = e.lngLat;
      new maplibregl.Marker().setLngLat([lng, lat]).addTo(mapa.current);
      setPuntos((prev) => [...prev, { lat, lon: lng }]);
    });
  }, []);

  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
        padding: 16,             // espacio entre todo y los bordes de la ventana
        gap: 16,                 // espacio entre las columnas
        boxSizing: "border-box", // para que el padding no haga crecer la página
        background: "#f3f4f6",
      }}
    >
      {/* Sidebar izquierdo */}
      <aside style={estiloPanel}>
        <h2>Capas</h2>
        <p>Aquí irán las capas y opciones del escaneo.</p>
      </aside>

      {/* Mapa */}
      <div
        ref={contenedor_mapa}
        style={{ flex: 1, borderRadius: 12, overflow: "hidden" }}
      />

      {/* Sidebar derecho */}
      <aside style={estiloPanel}>
        <h2>GISSCAN</h2>
        <p>Haz clic en el mapa para agregar puntos.</p>
        <ol>
          {puntos.map((p, i) => (
            <li key={i}>{p.lat.toFixed(5)}, {p.lon.toFixed(5)}</li>
          ))}
        </ol>
      </aside>
    </div>
  );
}

const estiloPanel = {
  width: 260,
  padding: 16,
  overflowY: "auto",
  background: "white",
  borderRadius: 12,
  boxSizing: "border-box",
};