import React, { useEffect, useState } from "react";
import { API_BASE_URL } from "./constants";

function HomePage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/homepage/`)
      .then((res) => res.json())
      .then((data) => setData(data))
      .catch((err) => console.error("Failed to fetch homepage data:", err));
  }, []);

  if (!data) return <p>Loading homepage...</p>;

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>{data.message}</h1>

      <section>
        <h2>Categories</h2>
        <ul style={{ display: "flex", gap: "1rem", listStyle: "none" }}>
          {data.categories.map((cat) => (
            <li key={cat.id}>
              <span>{cat.icon}</span> {cat.name}
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Featured Ads</h2>
        <div style={{ display: "flex", gap: "1rem" }}>
          {data.featured_ads.map((ad) => (
            <div key={ad.id} style={{ border: "1px solid #ccc", padding: "1rem" }}>
              {ad.image && <img src={ad.image} alt={ad.title} style={{ width: "150px" }} />}
              <h3>{ad.title}</h3>
              <p>{ad.city}</p>
              <p>${ad.price}</p>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2>Site Stats</h2>
        <p>Total Ads: {data.stats.total_ads}</p>
        <p>Active Ads: {data.stats.active_ads}</p>
        <p>Total Users: {data.stats.total_users}</p>
      </section>

      <section>
        <h2>Join Us</h2>
        <a href={data.auth.login_url}>Login</a> | <a href={data.auth.signup_url}>Sign Up</a>
      </section>
    </div>
  );
}

export default HomePage;
