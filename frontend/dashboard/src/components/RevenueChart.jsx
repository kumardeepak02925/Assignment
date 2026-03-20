import { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

export default function RevenueChart({ data = [] }) {

  const [startMonth, setStartMonth] = useState("");
  const [endMonth, setEndMonth] = useState("");

  const filteredData = data.filter((item) => {

    const month = item.order_year_month;

    if (startMonth && month < startMonth) return false;

    if (endMonth && month > endMonth) return false;

    return true;
  });

  const resetFilters = () => {
    setStartMonth("");
    setEndMonth("");
  };

  return (
    <div className="card">

      <h3>Revenue Trend</h3>

      <div style={{ display: "flex", gap: "10px", marginBottom: "15px", alignItems:"end" }}>

        <div>
          <label>Start Month</label>
          <br />
          <input
            type="month"
            value={startMonth}
            onChange={(e) => setStartMonth(e.target.value)}
          />
        </div>

        <div>
          <label>End Month</label>
          <br />
          <input
            type="month"
            value={endMonth}
            onChange={(e) => setEndMonth(e.target.value)}
          />
        </div>

        <button onClick={resetFilters} style={{height:"32px"}}>
          Reset
        </button>

      </div>


      <ResponsiveContainer width="100%" height={300}>

        <LineChart data={filteredData}>

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="order_year_month" />

          <YAxis />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="total_revenue"
            stroke="#007bff"
            strokeWidth={3}
          />

        </LineChart>

      </ResponsiveContainer>

    </div>
  );
}