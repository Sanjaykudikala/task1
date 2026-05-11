import React, { useState } from "react";
import { Input, Button, Spin, Card, Row, Col, message } from "antd";
import axios from "axios";

const { TextArea } = Input;

const App = () => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [products, setProducts] = useState([]);

  const handleSearch = async () => {
    if (!query.trim()) {
      message.warning("Please enter a query");
      return;
    }
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8001/recommend", {
        query: query.trim(),
      });
      if (response.data.error) {
        message.error(response.data.error);
        setProducts([]);
      } else {
        setProducts(response.data);
      }
    } catch (err) {
      console.error(err);
      message.error("Failed to fetch recommendations");
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: 800, margin: "0 auto" }}>
      <h1 style={{ textAlign: "center" }}>AI Product Recommender</h1>
      <TextArea
        rows={2}
        placeholder="e.g., gaming phone under $500"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <Button
        type="primary"
        block
        style={{ marginTop: "1rem" }}
        onClick={handleSearch}
        disabled={loading}
      >
        Search
      </Button>
      {loading && (
        <div style={{ textAlign: "center", marginTop: "1rem" }}>
          <Spin tip="Loading..." />
        </div>
      )}
      <Row gutter={[16, 16]} style={{ marginTop: "2rem" }}>
        {products.map((item, idx) => (
          <Col xs={24} sm={12} md={8} key={idx}>
            <Card
              hoverable
              title={item.name}
              extra={<a href={item.link} target="_blank" rel="noopener noreferrer">Buy</a>}
            >
              <p><strong>Price:</strong> {item.price}</p>
              <p>{item.description}</p>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default App;
