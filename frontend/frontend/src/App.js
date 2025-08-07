import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('/api/homepage/')
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []);

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h1>Vyzio Ads Homepage</h1>
      {data ? (
        <>
          <p><strong>Message:</strong> {data.message}</p>
          <p><strong>Status:</strong> {data.status}</p>
        </>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;
